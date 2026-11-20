"""Two-sided LP bracket for the two-qubit criterion; writes out/two_qubit_sandwich.json.
outer LP: finite subsets of states and effects  (threshold from above; infeasible => contextual)
inner LP: finite subsets of the two dual cones   (threshold from below; feasible  => noncontextual)"""
import sys, json; sys.path.insert(0, 'lib'); sys.path.insert(0, 'net')
import numpy as np
from scipy.optimize import linprog
from spinlib import fib_sphere
from simplex_lp import nc_lp

def outer_ok(a, b, c, N):
    U = fib_sphere(N); V = np.array([(a + c @ q) / (1 + b @ q) for q in U])
    return nc_lp(V, U, 1.0)
def support_states(a, b, c, n, Qg):
    vals = (Qg @ (c.T @ n) + n @ a) / (1 + Qg @ b)
    i = np.argmax(vals); q = Qg[i].copy(); best = vals[i]
    for _ in range(60):
        num = n @ (a + c @ q); den = 1 + b @ q
        grad = (c.T @ n) / den - num * b / den ** 2; grad -= (grad @ q) * q
        for step in (0.3, 0.1, 0.03, 0.01, 0.003):
            q2 = q + step * grad; q2 /= np.linalg.norm(q2); v2 = n @ (a + c @ q2) / (1 + b @ q2)
            if v2 > best: best, q = v2, q2; break
    return best
def inner_ok(a, b, c, N):
    U = fib_sphere(N); Qg = fib_sphere(4000)
    S = np.hstack([np.ones((N, 1)), U])
    G = np.array([[support_states(a, b, c, -n, Qg) * (1 + 1e-9), n[0], n[1], n[2]] for n in U])
    A = np.einsum('bi,aj->ijab', S, G).reshape(16, len(G) * len(S))
    res = linprog(np.zeros(A.shape[1]), A_eq=A, b_eq=np.eye(4).reshape(-1), bounds=(0, None), method='highs')
    return res.status == 0
def bisect(f, lo, hi, n=11):
    for _ in range(n):
        mid = (lo + hi) / 2
        if f(mid): lo = mid
        else: hi = mid
    return (lo + hi) / 2

out = {'rows': [], 'lambda': []}
rng = np.random.default_rng(11)
c0 = rng.normal(size=(3, 3)); c0 /= np.linalg.norm(c0, 'nuc'); z = np.zeros(3)
for N in (40, 100, 250):
    row = {'case': 'T-state', 'N': N, 'exact': 1.0,
           'inner': bisect(lambda t: inner_ok(z, z, t * c0, N), 0.6, 1.6), 'outer': bisect(lambda t: outer_ok(z, z, t * c0, N), 0.6, 1.6)}
    out['rows'].append(row); print(row, flush=True); json.dump(out, open('out/two_qubit_sandwich.json', 'w'), indent=1)
P = [np.eye(2, dtype=complex), np.array([[0, 1], [1, 0]], complex), np.array([[0, -1j], [1j, 0]]), np.diag([1, -1]).astype(complex)]
psi = np.array([np.cos(0.5), 0.2, 0.1j, np.sin(0.5)], complex); psi /= np.linalg.norm(psi); rho1 = np.outer(psi, psi.conj())
R1 = np.array([[np.trace(rho1 @ np.kron(P[m], P[n])).real for n in range(4)] for m in range(4)])
R0 = np.zeros((4, 4)); R0[0, 0] = 1; kA, kB = 0.75, 1.0
def Rraw(v): return np.diag([1, kA, kA, kA]) @ (v * R1 + (1 - v) * R0) @ np.diag([1, kB, kB, kB])
def ppt(v):
    R = Rraw(v); rho = sum(R[m, n] * np.kron(P[m], P[n]) for m in range(4) for n in range(4)) / 4
    pt = rho.reshape(2, 2, 2, 2).transpose(2, 1, 0, 3).reshape(4, 4)
    return min(np.linalg.eigvalsh(rho).min(), np.linalg.eigvalsh(pt).min()) >= 0
v_exact = bisect(ppt, 0, 1, 40)
for N in (40, 100, 250):
    fo = lambda v: outer_ok(Rraw(v)[1:, 0], Rraw(v)[0, 1:], Rraw(v)[1:, 1:], N)
    fi = lambda v: inner_ok(Rraw(v)[1:, 0], Rraw(v)[0, 1:], Rraw(v)[1:, 1:], N)
    row = {'case': 'polarised state, kA=0.75, kB=1', 'N': N, 'exact': v_exact, 'inner': bisect(fi, 0, 1), 'outer': bisect(fo, 0, 1)}
    out['rows'].append(row); print(row, flush=True); json.dump(out, open('out/two_qubit_sandwich.json', 'w'), indent=1)
# Lambda pairs at two production angles: direct verdicts
import certs_numeric as cn
al, dphi = cn.INPUTS['alpha_psi'][0], cn.INPUTS['DeltaPhi'][0]; a1, a2 = cn.INPUTS['alpha_minus'][0], cn.INPUTS['alpha_plus'][0]
for cth in (0.0, 0.40, 0.65):
    R = np.diag([1, a1, a1, a1]) @ cn.lambda_R(np.arccos(cth), al, dphi) @ np.diag([1, a2, a2, a2])
    o = bool(outer_ok(R[1:, 0], R[0, 1:], R[1:, 1:], 250)); i = bool(inner_ok(R[1:, 0], R[0, 1:], R[1:, 1:], 250))
    row = {'cos': cth, 'outer_feasible': o, 'inner_feasible': i}
    out['lambda'].append(row); print(row, flush=True); json.dump(out, open('out/two_qubit_sandwich.json', 'w'), indent=1)

