import sys; sys.path.insert(0, 'lib')
import numpy as np
from spinlib import *
rng = np.random.default_rng(1)
S = spin1_cart()
# commutation relations in the Cartesian basis
assert np.allclose(S[0] @ S[1] - S[1] @ S[0], 1j * S[2])
# Tr(Q_ij Q_kl) = (1/2)(d_ik d_jl + d_il d_jk) - (1/3) d_ij d_kl
def Q(i, k): return (S[i] @ S[k] + S[k] @ S[i]) / 2 - (2 / 3) * (i == k) * np.eye(3)
err = 0
for i in range(3):
    for k in range(3):
        for a in range(3):
            for b in range(3):
                lhs = np.trace(Q(i, k) @ Q(a, b)).real
                rhs = 0.5 * ((i == a) * (k == b) + (i == b) * (k == a)) - (1 / 3) * (i == k) * (a == b)
                err = max(err, abs(lhs - rhs))
print('Tr(QQ) identity max err', err)
# decomposition round trip
X = rng.normal(size=(3, 3)) + 1j * rng.normal(size=(3, 3)); X = X + X.conj().T; X = X / np.trace(X).real
p, A = pA_of(X)
print('round trip err', np.abs(X_of_pA(p, A) - X).max(), ' trA', np.trace(A))
# pure-state formulas p = 2 u x v, A = 1/3 - (uu^T+vv^T)
for al in [0, 0.3, np.pi / 4]:
    G = pure_spin1(al); p, A = pA_of(G)
    u = np.array([np.cos(al), 0, 0]); v = np.array([0, np.sin(al), 0])
    print(al, np.allclose(p, 2 * np.cross(u, v)), np.allclose(A, np.eye(3) / 3 - np.outer(u, u) - np.outer(v, v)))
# w-symbol: Tr(sigma R_q D_w R_q^+) = 1/3 + (eta1/2) p.q + (eta2/2) q^T A q   (spherical basis objects)
j = 1
Jx, Jy, Jz = spin_ops(1)
# unitary from spherical basis |m> (m=1,0,-1) to Cartesian: |1> = -(x+iy)/sqrt2, |0> = z, |-1> = (x-iy)/sqrt2
U = np.array([[-1 / np.sqrt(2), 0, 1 / np.sqrt(2)], [-1j / np.sqrt(2), 0, -1j / np.sqrt(2)], [0, 1, 0]])
for a, b in zip((Jx, Jy, Jz), S):
    assert np.allclose(U @ a @ U.conj().T, b)
maxerr = 0
for trial in range(20):
    w = rng.dirichlet([1, 1, 1]); eta = eta_of_w(1, w)
    assert np.allclose(eta, [w[0] - w[2], 1 - 3 * w[1]])
    X = rng.normal(size=(3, 3)) + 1j * rng.normal(size=(3, 3)); X = X + X.conj().T; X = X / np.trace(X).real
    p, A = pA_of(U @ X @ U.conj().T)
    q = rng.normal(size=3); q /= np.linalg.norm(q)
    R = rot(1, q)
    lhs = np.trace(X @ R @ kernel_D(1, w) @ R.conj().T).real
    rhs = 1 / 3 + eta[0] / 2 * p @ q + eta[1] / 2 * q @ A @ q
    maxerr = max(maxerr, abs(lhs - rhs))
print('w-symbol formula max err', maxerr)
# twirl coefficients: m1 = (1/2) pG.ps ; m2 = (3/5) Tr(AG As)
maxerr = 0
for trial in range(20):
    psi = rng.normal(size=3) + 1j * rng.normal(size=3); psi /= np.linalg.norm(psi)
    G = np.outer(psi, psi.conj())
    X = rng.normal(size=(3, 3)) + 1j * rng.normal(size=(3, 3)); X = X + X.conj().T; X = X / np.trace(X).real
    m = m_coeffs(1, G, X)
    pG, AG = pA_of(U @ G @ U.conj().T); ps, As = pA_of(U @ X @ U.conj().T)
    maxerr = max(maxerr, abs(m[0] - 0.5 * pG @ ps), abs(m[1] - 0.6 * np.trace(AG @ As)))
print('m_l formulas max err', maxerr)
# Haar twirl of X -> sigma Tr(G X) equals sum_l m_l/(d) ... check against numerical Haar average
def haar_twirl_map(G, sig, n=4000):
    d = 3; T = np.zeros((d * d, d * d), complex)
    for _ in range(n):
        ax = rng.normal(size=3); ang = None
        # Haar on SO(3): random unit quaternion
        qv = rng.normal(size=4); qv /= np.linalg.norm(qv)
        ang = 2 * np.arccos(qv[0]); ax = qv[1:] / (np.linalg.norm(qv[1:]) + 1e-300)
        Ug = rot_axis_angle(1, ax, ang)
        Gg = Ug @ G @ Ug.conj().T; sg = Ug @ sig @ Ug.conj().T
        T += np.outer(sg.reshape(-1), Gg.conj().reshape(-1))
    return 3 * T / n
psi = rng.normal(size=3) + 1j * rng.normal(size=3); psi /= np.linalg.norm(psi)
G = np.outer(psi, psi.conj())
X = rng.normal(size=(3, 3)) + 1j * rng.normal(size=(3, 3)); X = X + X.conj().T; X = X / np.trace(X).real
T = haar_twirl_map(G, X, 20000)
m = m_coeffs(1, G, X)
for l in (1, 2):
    b = multipole_basis(1)[l][0]
    val = np.real(hs(b, (T @ b.reshape(-1)).reshape(3, 3)))
    print('l', l, 'twirled eigenvalue (MC)', round(val, 3), ' predicted m_l', round(m[l - 1], 3))

