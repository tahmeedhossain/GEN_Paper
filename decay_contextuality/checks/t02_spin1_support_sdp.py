"""Support function of the spin-1 single-particle region R computed by SDP
(maximise over pure states g and over the dual cone via the S-lemma), compared
with the closed form."""
import sys; sys.path.insert(0, 'lib')
import numpy as np, cvxpy as cp
from spinlib import *
from regions import h_R

def hQ(z1, Z2):
    """max <(p,A),(z1,Z2)> over (p,A) with 2/3 + p.q + q^T A q >= 0 on the sphere (S-lemma SDP)."""
    p = cp.Variable(3); A = cp.Variable((3, 3), symmetric=True); lam = cp.Variable()
    M = cp.bmat([[cp.reshape(2 / 3 - lam, (1, 1), order='C'), cp.reshape(p / 2, (1, 3), order='C')],
                 [cp.reshape(p / 2, (3, 1), order='C'), A + lam * np.eye(3)]])
    prob = cp.Problem(cp.Maximize(z1 @ p + cp.trace(Z2 @ A)), [M >> 0, cp.trace(A) == 0])
    prob.solve(solver=cp.CLARABEL)
    return prob.value

alphas = np.linspace(0, np.pi / 4, 46)
worst = 0
rows = []
for ph in np.linspace(0, 2 * np.pi, 49)[:-1]:
    a, b = np.cos(ph), np.sin(ph)
    best = -np.inf
    for al in alphas:
        u = np.array([np.cos(al), 0, 0]); v = np.array([0, np.sin(al), 0])
        pg = 2 * np.cross(u, v); Ag = np.eye(3) / 3 - np.outer(u, u) - np.outer(v, v)
        val = hQ(a / 2 * pg, 3 * b / 5 * Ag)
        best = max(best, val)
    rows.append((ph, best, h_R(a, b)))
    worst = max(worst, abs(best - h_R(a, b)))
for r in rows[::4]:
    print('phi=%.3f  SDP=%.6f  closed=%.6f' % r)
print('max |SDP - closed form| over 48 directions:', worst)

