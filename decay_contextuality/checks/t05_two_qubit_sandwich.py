"""Two-sided numerical check of the two-qubit criterion.
outer LP: finite subsets of states and effects  -> feasible set too large (threshold from above)
inner LP: finite subsets of the two dual cones   -> feasible set too small (threshold from below)
Both must bracket the exact threshold and close as the grids are refined."""
import sys; sys.path.insert(0, 'lib')
import numpy as np
from scipy.optimize import linprog
from spinlib import fib_sphere
from simplex_lp import nc_lp

def outer_ok(a, b, c, N):
    U = fib_sphere(N)
    V = np.array([(a + c @ q) / (1 + b @ q) for q in U])
    return nc_lp(V, U, 1.0)

def support_states(a, b, c, n, Q):
    """h(n) = max_q n.(a + c q)/(1 + b.q) over the sphere (dense sampling + local refinement)."""
    vals = (Q @ (c.T @ n) + n @ a) / (1 + Q @ b)
    i = np.argmax(vals); q = Q[i].copy(); best = vals[i]
    # projected-gradient polish
    for _ in range(60):
        num = n @ (a + c @ q); den = 1 + b @ q
        grad = (c.T @ n) / den - num * b / den ** 2
        grad -= (grad @ q) * q
        for step in (0.3, 0.1, 0.03, 0.01, 0.003):
            q2 = q + step * grad; q2 /= np.linalg.norm(q2)
            v2 = n @ (a + c @ q2) / (1 + b @ q2)
            if v2 > best: best, q = v2, q2; break
    return best

def inner_ok(a, b, c, N):
    U = fib_sphere(N); Q = fib_sphere(4000)
    S = np.hstack([np.ones((N, 1)), U])                           # sigma_b = (1, u_b): exactly in the dual of the effect cone
    G = np.array([[support_states(a, b, c, -n, Q) * (1 + 1e-9), n[0], n[1], n[2]] for n in U])   # g(v) = h(-n) + n.v >= 0 on all states
    na, nb = len(G), len(S)
    A = np.einsum('bi,aj->ijab', S, G).reshape(16, na * nb)
    res = linprog(np.zeros(na * nb), A_eq=A, b_eq=np.eye(4).reshape(-1), bounds=(0, None), method='highs')
    return res.status == 0

def bisect(f, lo, hi, n=11):
    for _ in range(n):
        mid = (lo + hi) / 2
        if f(mid): lo = mid
        else: hi = mid
    return (lo + hi) / 2

rng = np.random.default_rng(11)
c0 = rng.normal(size=(3, 3)); c0 /= np.linalg.norm(c0, 'nuc'); z = np.zeros(3)
print('T-state, exact threshold t = 1')
for N in (40, 100, 250):
    t_out = bisect(lambda t: outer_ok(z, z, t * c0, N), 0.6, 1.6)
    t_in = bisect(lambda t: inner_ok(z, z, t * c0, N), 0.6, 1.6)
    print('  N=%4d   inner %.4f  <= 1 <=  outer %.4f' % (N, t_in, t_out), flush=True)

# a state with polarisations: partially depolarised pure state seen through kA=0.75, kB=1 (raw coefficients)
sx = np.array([[0, 1], [1, 0]], complex); sy = np.array([[0, -1j], [1j, 0]]); sz = np.diag([1, -1]).astype(complex)
P = [np.eye(2, dtype=complex), sx, sy, sz]
psi = np.array([np.cos(0.5), 0.2, 0.1j, np.sin(0.5)], complex); psi /= np.linalg.norm(psi)
rho1 = np.outer(psi, psi.conj())
R1 = np.array([[np.trace(rho1 @ np.kron(P[m], P[n])).real for n in range(4)] for m in range(4)])
R0 = np.zeros((4, 4)); R0[0, 0] = 1
kA, kB = 0.75, 1.0
def Rraw(v):
    R = v * R1 + (1 - v) * R0
    return np.diag([1, kA, kA, kA]) @ R @ np.diag([1, kB, kB, kB])
def ppt(v):
    R = Rraw(v); rho = sum(R[m, n] * np.kron(P[m], P[n]) for m in range(4) for n in range(4)) / 4
    pt = rho.reshape(2, 2, 2, 2).transpose(2, 1, 0, 3).reshape(4, 4)
    return min(np.linalg.eigvalsh(rho).min(), np.linalg.eigvalsh(pt).min()) >= 0
v_exact = bisect(ppt, 0, 1, 40)
print('state with polarisations (kA=0.75,kB=1): exact PPT threshold v = %.5f' % v_exact)
for N in (40, 100, 250):
    f_out = lambda v: outer_ok(Rraw(v)[1:, 0], Rraw(v)[0, 1:], Rraw(v)[1:, 1:], N)
    f_in = lambda v: inner_ok(Rraw(v)[1:, 0], Rraw(v)[0, 1:], Rraw(v)[1:, 1:], N)
    print('  N=%4d   inner %.4f  <= %.4f <=  outer %.4f' % (N, bisect(f_in, 0, 1), v_exact, bisect(f_out, 0, 1)), flush=True)

