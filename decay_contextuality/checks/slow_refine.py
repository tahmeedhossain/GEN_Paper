"""Refinement of the three LP directions whose deviation from the closed form exceeded 0.5%:
   R  at 90 deg  and R2 at 270 deg : optimum has an isolated zero of its Husimi function -> finer direction grid;
   R2 at 80 deg                    : boundary point lies between members of the operator family -> add tau = 1.8.
Writes out/lp_refine.json."""
import sys, json, time; sys.path.insert(0, 'lib')
import numpy as np, scipy.sparse as sp
from scipy.optimize import linprog
from spinlib import *
from regions import radial_R, radial_R2
B = multipole_basis(1); basis = B[0] + B[1] + B[2]; lab = [0] + [1] * 3 + [2] * 5
def vec(X): return np.array([np.real(hs(b, X)) for b in basis])
U = np.array([[-1 / np.sqrt(2), 0, 1 / np.sqrt(2)], [-1j / np.sqrt(2), 0, -1j / np.sqrt(2)], [0, 1, 0]])
def sq(c, v):
    X = X_of_pA(2 * c * v, np.outer(v, v) - (v @ v) / 3 * np.eye(3)); return U.conj().T @ X @ U
def solve(Gs, nq, deg):
    K = len(Gs); gv = np.array([vec(G) for G in Gs]); qs = fib_sphere(nq); coh = np.array([1, 0, 0], complex)
    Pq = np.array([vec(np.outer(rot(1, q) @ coh, (rot(1, q) @ coh).conj())) for q in qs]); nvar = 9 * K + 1
    A_ub = sp.hstack([sp.kron(sp.identity(K), sp.csr_matrix(-Pq)), sp.csr_matrix((K * nq, 1))]).tocsr()
    rows, cols, vals = [], [], []
    for a in range(9):
        for b in range(9):
            for k in range(K): rows.append(9 * a + b); cols.append(9 * k + a); vals.append(gv[k, b])
    A = sp.csr_matrix((vals, (rows, cols)), shape=(81, nvar)).tolil(); bvec = np.zeros(81); th = np.deg2rad(deg)
    for a in range(9):
        row = 9 * a + a
        if lab[a] == 0: bvec[row] = 1.0
        elif lab[a] == 1: A[row, nvar - 1] = -np.cos(th)
        else: A[row, nvar - 1] = -np.sin(th)
    c = np.zeros(nvar); c[-1] = -1
    res = linprog(c, A_ub=A_ub, b_ub=np.zeros(K * nq), A_eq=A.tocsr(), b_eq=bvec, bounds=[(None, None)] * (9 * K) + [(0, None)], method='highs')
    return float(res.x[-1]) if res.status == 0 else None
out = {'rows': []}
dirs = fib_sphere(30)
# R at 90 deg: linear-polarisation and coherent pure states, direction grid 900 -> 3600
Gs = []
for q in dirs:
    R = rot(1, q)
    for psi0 in (np.array([1, 0, 0]), np.array([0, 1, 0])):
        psi = R @ psi0.astype(complex); Gs.append(np.outer(psi, psi.conj()))
for nq in (900, 3600):
    t0 = time.time(); v = solve(Gs, nq, 90.0)
    out['rows'].append({'region': 'R', 'deg': 90.0, 'nq': nq, 'K': len(Gs), 'lp': v, 'closed': float(radial_R(np.pi / 2)), 'seconds': round(time.time() - t0)})
    print(out['rows'][-1], flush=True); json.dump(out, open('out/lp_refine.json', 'w'), indent=1)
# R2 at 270 deg: operators with symbol 2 (n.q)^2 (tau = 2) and coherent ones, direction grid 700 -> 2800
Gs = [sq(0.0, np.sqrt(2.0) * q) for q in dirs] + [sq(np.sqrt(0.5), np.sqrt(0.5) * q) for q in dirs]
for nq in (700, 2800):
    t0 = time.time(); v = solve(Gs, nq, 270.0)
    out['rows'].append({'region': 'R2', 'deg': 270.0, 'nq': nq, 'K': len(Gs), 'lp': v, 'closed': float(radial_R2(1.5 * np.pi)), 'seconds': round(time.time() - t0)})
    print(out['rows'][-1], flush=True); json.dump(out, open('out/lp_refine.json', 'w'), indent=1)
# R2 at 80 deg: add tau = 1.8 (the closed-form boundary point has s = 1.809)
for taus in ((1.58, 2.0), (1.58, 1.8, 2.0)):
    Gs = []
    for q in fib_sphere(24):
        for t in taus:
            c = np.sqrt(max(0.0, (2 - t) / 3)); Gs.append(sq(c, np.sqrt(t) * q))
            if c > 1e-9: Gs.append(sq(-c, np.sqrt(t) * q))
    t0 = time.time(); v = solve(Gs, 700, 80.0)
    out['rows'].append({'region': 'R2', 'deg': 80.0, 'nq': 700, 'K': len(Gs), 'taus': list(taus), 'lp': v, 'closed': float(radial_R2(np.deg2rad(80))), 'seconds': round(time.time() - t0)})
    print(out['rows'][-1], flush=True); json.dump(out, open('out/lp_refine.json', 'w'), indent=1)

