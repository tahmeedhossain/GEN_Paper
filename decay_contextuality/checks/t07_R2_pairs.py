"""Maximally entangled spin-1 pair, one decay on each side: region R2.
(a) sample the generating family (pairs of normalised squares) and compare the numerical
    support function with the closed form;
(b) brute-force LP without the twirl reduction: N_eta = sum_k tau_k Tr(G_k .) with G_k a finite set of
    Husimi-nonnegative unit-trace operators and tau_k Husimi-nonnegative on a grid."""
import sys; sys.path.insert(0, 'lib')
import numpy as np, scipy.sparse as sp
from scipy.optimize import linprog
from spinlib import *
from regions import h_R2, radial_R2

rng = np.random.default_rng(5)
# (a) generating family: x = (2 c v, v v^T - |v|^2/3),  c^2 + |v|^2/3 = 2/3
n = 400000
tau = rng.uniform(0, 2, n); taup = rng.uniform(0, 2, n); mu = rng.uniform(-1, 1, n)
sg = rng.choice([-1, 1], n)
m1 = sg * (2 / 3) * np.sqrt(tau * (2 - tau) * taup * (2 - taup)) * mu
m2 = 0.6 * tau * taup * (mu ** 2 - 1 / 3)
# add the symmetric curve explicitly (measure-zero in the sample)
s = np.linspace(0, 2, 4001)
m1 = np.concatenate([m1, (2 / 3) * s * (2 - s), -(2 / 3) * s * (2 - s), [0.0]])
m2 = np.concatenate([m2, 0.4 * s * s, 0.4 * s * s, [-0.8]])
worst_over = 0; worst_gap = 0
for ph in np.linspace(0, 2 * np.pi, 361):
    a, b = np.cos(ph), np.sin(ph)
    num = (a * m1 + b * m2).max(); cl = h_R2(a, b)
    worst_over = max(worst_over, num - cl); worst_gap = max(worst_gap, cl - num)
print('(a) sampled support function vs closed form: max excess %.2e (must be <= 0 up to rounding), max deficit %.2e'
      % (worst_over, worst_gap))

# (b) LP
B = multipole_basis(1); basis = B[0] + B[1] + B[2]; lab = [0] + [1] * 3 + [2] * 5
def vec(X): return np.array([np.real(hs(b, X)) for b in basis])
U = np.array([[-1 / np.sqrt(2), 0, 1 / np.sqrt(2)], [-1j / np.sqrt(2), 0, -1j / np.sqrt(2)], [0, 1, 0]])
def op_from_square(c, v):
    """unit-trace operator (spherical basis) with Husimi function (3/2)... i.e. (p,A) = (2cv, vv^T-|v|^2/3)."""
    X = X_of_pA(2 * c * v, np.outer(v, v) - (v @ v) / 3 * np.eye(3))
    return U.conj().T @ X @ U
Gs = []
for q in fib_sphere(30):
    for t in (0.5, 0.75, 1.0, 1.3, 1.6, 2.0):
        c = np.sqrt((2 - t) / 3)
        Gs.append(op_from_square(c, np.sqrt(t) * q)); 
        if c > 1e-12: Gs.append(op_from_square(-c, np.sqrt(t) * q))
K = len(Gs); gv = np.array([vec(G) for G in Gs])
qs = fib_sphere(900); coh = np.array([1, 0, 0], complex)
Pq = np.array([vec(np.outer(rot(1, q) @ coh, (rot(1, q) @ coh).conj())) for q in qs])
# sanity: all G_k Husimi-nonnegative
print('    min Husimi value over the G set: %.2e' % (gv @ Pq.T).min())
nvar = 9 * K + 1
blocks = sp.kron(sp.identity(K), sp.csr_matrix(-Pq))
A_ub = sp.hstack([blocks, sp.csr_matrix((blocks.shape[0], 1))]).tocsr(); b_ub = np.zeros(A_ub.shape[0])
cvec = np.zeros(nvar); cvec[-1] = -1
def eq_matrix(th):
    A = sp.lil_matrix((81, nvar)); bvec = np.zeros(81)
    for a in range(9):
        for b in range(9):
            row = 9 * a + b
            for k in range(K): A[row, 9 * k + a] = gv[k, b]
            if a == b:
                if lab[a] == 0: bvec[row] = 1.0
                elif lab[a] == 1: A[row, nvar - 1] = -np.cos(th)
                else: A[row, nvar - 1] = -np.sin(th)
    return A.tocsr(), bvec
print('(b) LP with K=%d operators, %d directions' % (K, len(qs)))
out = []
for deg in (0, 45, 66.2, 90, 270, 315):
    th = np.deg2rad(deg)
    A_eq, b_eq = eq_matrix(th)
    res = linprog(cvec, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=[(None, None)] * (9 * K) + [(0, None)], method='highs')
    t_lp = res.x[-1] if res.status == 0 else np.nan
    out.append((deg, t_lp, radial_R2(th)))
    print('    theta=%6.1f  LP t=%.4f   closed-form radius=%.4f   ratio=%.4f' % (deg, t_lp, out[-1][2], t_lp / out[-1][2]), flush=True)
np.save('out/t07_R2_lp.npy', np.array(out))

