"""Two spin-1/2 particles: data-level criterion  NC  <=>  rho_raw and its partial transpose are PSD.
(1) T-states: closed form ||c||_1 <= 1 against the LP.
(2) Random states with polarisations: PPT of rho_raw against the LP along noise lines."""
import sys; sys.path.insert(0, 'lib')
import numpy as np
from spinlib import fib_sphere
from simplex_lp import nc_lp

rng = np.random.default_rng(3)
sx = np.array([[0, 1], [1, 0]], complex); sy = np.array([[0, -1j], [1j, 0]]); sz = np.diag([1, -1]).astype(complex)
P = [np.eye(2, dtype=complex), sx, sy, sz]

def bloch(rho):
    R = np.array([[np.trace(rho @ np.kron(P[m], P[n])).real for n in range(4)] for m in range(4)])
    return R                                   # R[0,0]=1, R[i,0]=a_i, R[0,j]=b_j, R[i,j]=C_ij

def rho_from_R(R):
    return sum(R[m, n] * np.kron(P[m], P[n]) for m in range(4) for n in range(4)) / 4

def raw_R(R, kA, kB):
    D = np.diag([1, kA, kA, kA]); E = np.diag([1, kB, kB, kB])
    return D @ R @ E

def ppt_both(Rraw):
    rho = rho_from_R(Rraw)
    pt = rho.reshape(2, 2, 2, 2).transpose(2, 1, 0, 3).reshape(4, 4)
    return min(np.linalg.eigvalsh(rho).min(), np.linalg.eigvalsh(pt).min())

UB = fib_sphere(150); UA = fib_sphere(150)

def lp_nc(Rraw):
    a = Rraw[1:, 0]; b = Rraw[0, 1:]; c = Rraw[1:, 1:]
    V = np.array([(a + c @ q) / (1 + b @ q) for q in UB])        # data Bloch vectors of the steered states
    return nc_lp(V, UA, 1.0)

# (1) T-states
print('T-states: threshold in t for c = t*c0 (LP bisection) vs 1/||c0||_1')
for trial in range(6):
    c0 = rng.normal(size=(3, 3)); c0 /= np.linalg.norm(c0, 'nuc')
    lo, hi = 0.5, 1.5
    for _ in range(12):
        mid = (lo + hi) / 2
        R = np.eye(4); R[1:, 1:] = mid * c0
        if lp_nc(R): lo = mid
        else: hi = mid
    print('  trial %d: LP threshold in [%.4f, %.4f]   exact 1.0000' % (trial, lo, hi))

# (2) general states: rho(v) = v*rho_1 + (1-v)*rho_0 with rho_1 entangled, rho_0 separable; analysing powers kA,kB
print('general two-qubit states: thresholds in v along noise lines')
def rand_pure_ent():
    psi = rng.normal(size=4) + 1j * rng.normal(size=4); psi /= np.linalg.norm(psi)
    return np.outer(psi, psi.conj())
def rand_prod_mix():
    out = 0
    for _ in range(3):
        a = rng.normal(size=2) + 1j * rng.normal(size=2); a /= np.linalg.norm(a)
        b = rng.normal(size=2) + 1j * rng.normal(size=2); b /= np.linalg.norm(b)
        out = out + np.kron(np.outer(a, a.conj()), np.outer(b, b.conj())) / 3
    return 0.5 * out + 0.5 * np.eye(4) / 4
rows = []
for trial in range(8):
    R1 = bloch(rand_pure_ent()); R0 = bloch(rand_prod_mix())
    kA = rng.choice([1.0, -1.0, 0.9, 0.75, -0.6]); kB = rng.choice([1.0, -1.0, 0.8, 0.75])
    f = lambda v: raw_R(v * R1 + (1 - v) * R0, kA, kB)
    # PPT threshold
    lo, hi = 0.0, 1.0
    if ppt_both(f(1.0)) >= 0:
        print('  trial %d: kA=%.2f kB=%.2f : raw operator PPT up to v=1 (no threshold)' % (trial, kA, kB)); continue
    for _ in range(40):
        mid = (lo + hi) / 2
        if ppt_both(f(mid)) >= 0: lo = mid
        else: hi = mid
    v_ppt = lo
    lo, hi = 0.0, 1.0
    for _ in range(12):
        mid = (lo + hi) / 2
        if lp_nc(f(mid)): lo = mid
        else: hi = mid
    rows.append((kA, kB, v_ppt, lo, hi, np.linalg.det(f(v_ppt))))
    print('  trial %d: kA=%+.2f kB=%+.2f : PPT threshold v=%.4f   LP threshold in [%.4f, %.4f]   det R_raw=%.3g'
          % (trial, kA, kB, v_ppt, lo, hi, rows[-1][-1]))
np.save('out/t04_two_qubit.npy', np.array(rows))

