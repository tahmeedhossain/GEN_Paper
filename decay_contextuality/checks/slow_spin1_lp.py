"""Brute-force LPs for the two spin-1 regions (no twirl reduction, no S-lemma).
   mode R : single particle, all states            N_eta = sum_k tau_k Tr(G_k .), G_k pure states
   mode R2: maximally entangled pair, two decays   same with G_k Husimi-nonnegative unit-trace operators
tau_k: Hermitian variables, Husimi function >= 0 on a grid of nq directions.
Finite G set -> inner approximation; finite direction grid -> slight outer relaxation.
Usage: python3 slow_spin1_lp.py R|R2 nq out.json  deg1 deg2 ..."""
import sys, json, time; sys.path.insert(0, 'lib')
import numpy as np, scipy.sparse as sp
from scipy.optimize import linprog
from spinlib import *
from regions import radial_R, radial_R2

mode, nq, outfile = sys.argv[1], int(sys.argv[2]), sys.argv[3]
degs = [float(x) for x in sys.argv[4:]]
rng = np.random.default_rng(7)
B = multipole_basis(1); basis = B[0] + B[1] + B[2]; lab = [0] + [1] * 3 + [2] * 5
def vec(X): return np.array([np.real(hs(b, X)) for b in basis])
U = np.array([[-1 / np.sqrt(2), 0, 1 / np.sqrt(2)], [-1j / np.sqrt(2), 0, -1j / np.sqrt(2)], [0, 1, 0]])
Gs = []
if mode == 'R':
    for q in fib_sphere(40):
        R = rot(1, q)
        for psi0 in (np.array([1, 0, 0]), np.array([0, 1, 0]),
                     np.array([np.cos(0.3), 0, np.sin(0.3)]), np.array([np.cos(0.6), 0, np.sin(0.6)])):
            psi = R @ psi0.astype(complex); Gs.append(np.outer(psi, psi.conj()))
    for _ in range(60):
        psi = rng.normal(size=3) + 1j * rng.normal(size=3); psi /= np.linalg.norm(psi)
        Gs.append(np.outer(psi, psi.conj()))
    radial = radial_R
else:
    def op_from_square(c, v):
        X = X_of_pA(2 * c * v, np.outer(v, v) - (v @ v) / 3 * np.eye(3))
        return U.conj().T @ X @ U
    for q in fib_sphere(24):
        for t in (0.5, 0.75, 1.0, 1.25, 1.58, 2.0):
            c = np.sqrt(max(0.0, (2 - t) / 3))
            Gs.append(op_from_square(c, np.sqrt(t) * q))
            if c > 1e-9: Gs.append(op_from_square(-c, np.sqrt(t) * q))
    radial = radial_R2
K = len(Gs); gv = np.array([vec(G) for G in Gs])
qs = fib_sphere(nq); coh = np.array([1, 0, 0], complex)
Pq = np.array([vec(np.outer(rot(1, q) @ coh, (rot(1, q) @ coh).conj())) for q in qs])
nvar = 9 * K + 1
blocks = sp.kron(sp.identity(K), sp.csr_matrix(-Pq))
A_ub = sp.hstack([blocks, sp.csr_matrix((blocks.shape[0], 1))]).tocsr(); b_ub = np.zeros(A_ub.shape[0])
cvec = np.zeros(nvar); cvec[-1] = -1
# equality rows that do not depend on the direction
rows, cols, vals = [], [], []
for a in range(9):
    for b in range(9):
        for k in range(K):
            rows.append(9 * a + b); cols.append(9 * k + a); vals.append(gv[k, b])
A_base = sp.csr_matrix((vals, (rows, cols)), shape=(81, nvar)).tolil()
res_all = {'mode': mode, 'K': K, 'nq': nq, 'rows': []}
for deg in degs:
    th = np.deg2rad(deg); A = A_base.copy(); bvec = np.zeros(81)
    for a in range(9):
        row = 9 * a + a
        if lab[a] == 0: bvec[row] = 1.0
        elif lab[a] == 1: A[row, nvar - 1] = -np.cos(th)
        else: A[row, nvar - 1] = -np.sin(th)
    t0 = time.time()
    res = linprog(cvec, A_ub=A_ub, b_ub=b_ub, A_eq=A.tocsr(), b_eq=bvec,
                  bounds=[(None, None)] * (9 * K) + [(0, None)], method='highs')
    t_lp = float(res.x[-1]) if res.status == 0 else None
    row = {'deg': deg, 'lp': t_lp, 'closed': float(radial(th)), 'seconds': round(time.time() - t0, 1), 'status': int(res.status)}
    res_all['rows'].append(row)
    print(row, flush=True)
    json.dump(res_all, open(outfile, 'w'), indent=1)

