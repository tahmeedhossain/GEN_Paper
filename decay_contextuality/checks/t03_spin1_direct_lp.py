"""Independent brute-force check of the spin-1 single-particle region R.

No twirl reduction and no S-lemma: for a ray t(cos th, sin th) in the (eta1, eta2) plane we
maximise t subject to
     Pi_0 + t (cos th Pi_1 + sin th Pi_2) = sum_k tau_k Tr(G_k . ),
with G_k a fixed finite set of pure spin-1 states and tau_k Hermitian variables whose
coherent-state (Husimi) function is nonnegative on a fine grid of directions.
(Inner approximation from the finite G set; slight outer relaxation from the q grid.)"""
import sys; sys.path.insert(0, 'lib')
import numpy as np, scipy.sparse as sp
from scipy.optimize import linprog
from spinlib import *
from regions import radial_R

rng = np.random.default_rng(7)
j = 1; d = 3
B = multipole_basis(1)
basis = B[0] + B[1] + B[2]                       # orthonormal Hermitian basis, 9 elements
lab = [0] + [1] * 3 + [2] * 5
def vec(X): return np.array([np.real(hs(b, X)) for b in basis])

# pure states G_k: random + coherent states + m=0 states along many directions + intermediate family
Gs = []
dirs = fib_sphere(40)
for q in dirs:
    R = rot(1, q)
    for psi0 in (np.array([1, 0, 0]), np.array([0, 1, 0]),
                 np.array([np.cos(0.3), 0, np.sin(0.3)]), np.array([np.cos(0.6), 0, np.sin(0.6)])):
        psi = R @ psi0.astype(complex); Gs.append(np.outer(psi, psi.conj()))
for _ in range(60):
    psi = rng.normal(size=3) + 1j * rng.normal(size=3); psi /= np.linalg.norm(psi)
    Gs.append(np.outer(psi, psi.conj()))
K = len(Gs)
gv = np.array([vec(G) for G in Gs])              # K x 9

qs = fib_sphere(900)
coh = np.array([1, 0, 0], complex)
Pq = []
for q in qs:
    psi = rot(1, q) @ coh
    Pq.append(vec(np.outer(psi, psi.conj())))
Pq = np.array(Pq)                                 # Nq x 9 : <q|tau|q> = Pq . vec(tau)

# variables: tau_k (9 each), then t.  Equality: sum_k vec(tau_k)_a gv[k,b] = delta_ab * coef(l_a)
nvar = 9 * K + 1
rows, cols, vals, rhs = [], [], [], []
r = 0
def eq_matrix(th):
    A = sp.lil_matrix((81, nvar)); bvec = np.zeros(81)
    for a in range(9):
        for b in range(9):
            row = 9 * a + b
            for k in range(K):
                A[row, 9 * k + a] = gv[k, b]
            if a == b:
                if lab[a] == 0: bvec[row] = 1.0
                elif lab[a] == 1: A[row, nvar - 1] = -np.cos(th)
                else: A[row, nvar - 1] = -np.sin(th)
    return A.tocsr(), bvec
# inequality: -Pq . tau_k <= 0
blocks = sp.kron(sp.identity(K), sp.csr_matrix(-Pq))
A_ub = sp.hstack([blocks, sp.csr_matrix((blocks.shape[0], 1))]).tocsr()
b_ub = np.zeros(A_ub.shape[0])
c = np.zeros(nvar); c[-1] = -1.0
bounds = [(None, None)] * (9 * K) + [(0, None)]
print('K pure states', K, ' q grid', len(qs), ' LP size', A_ub.shape)
out = []
for th in np.deg2rad([0, 20, 45, 70, 90, 135, 180, 225, 250, 270, 300, 340]):
    A_eq, b_eq = eq_matrix(th)
    res = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs')
    t_lp = res.x[-1] if res.status == 0 else np.nan
    out.append((np.rad2deg(th), t_lp, radial_R(th)))
    print('theta=%6.1f  LP t=%.4f   closed-form radius=%.4f   ratio=%.4f' % (out[-1] + (t_lp / out[-1][2],)), flush=True)
np.save('out/t03_lp_vs_closed.npy', np.array(out))

