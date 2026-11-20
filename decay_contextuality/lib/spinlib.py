"""Spin operators, multipole projections and spin-1 Cartesian parametrisation.

Conventions
-----------
Spin-j operators J_x, J_y, J_z in the basis |j,m>, m = j, j-1, ..., -j.
A one-direction polarimeter of a spin-j particle is the covariant POVM density
    E_w(q) = (d/4pi) R_q D_w R_q^dagger ,   D_w = diag(w_j, ..., w_{-j}),  sum w = 1,
with R_q any rotation taking z to q.
"""
import numpy as np
from functools import lru_cache
from scipy.linalg import expm


def spin_ops(j):
    d = int(round(2 * j + 1))
    m = np.array([j - k for k in range(d)], dtype=float)
    Jz = np.diag(m).astype(complex)
    Jp = np.zeros((d, d), dtype=complex)
    for k in range(1, d):
        mm = m[k]
        Jp[k - 1, k] = np.sqrt(j * (j + 1) - mm * (mm + 1))
    Jm = Jp.conj().T
    Jx = (Jp + Jm) / 2
    Jy = (Jp - Jm) / (2j)
    return Jx, Jy, Jz


def rot(j, q):
    """Rotation operator taking z to unit vector q (rotation about z x q)."""
    Jx, Jy, Jz = spin_ops(j)
    q = np.asarray(q, float)
    q = q / np.linalg.norm(q)
    th = np.arccos(np.clip(q[2], -1, 1))
    ph = np.arctan2(q[1], q[0])
    return expm(-1j * ph * Jz) @ expm(-1j * th * Jy)


def rot_axis_angle(j, axis, angle):
    Jx, Jy, Jz = spin_ops(j)
    a = np.asarray(axis, float)
    a = a / np.linalg.norm(a)
    return expm(-1j * angle * (a[0] * Jx + a[1] * Jy + a[2] * Jz))


def hs(A, B):
    return np.trace(A.conj().T @ B)


@lru_cache(maxsize=None)
def multipole_basis(j):
    """Orthonormal (Hilbert-Schmidt) Hermitian bases of the rank-l tensor-operator
    subspaces V_l, l = 0..2j, obtained from the Casimir superoperator
    C(X) = sum_i [J_i,[J_i,X]] with eigenvalue l(l+1)."""
    Jx, Jy, Jz = spin_ops(j)
    d = Jz.shape[0]
    # Hermitian orthonormal basis of all d x d matrices
    herm = []
    for a in range(d):
        E = np.zeros((d, d), complex); E[a, a] = 1; herm.append(E)
    for a in range(d):
        for b in range(a + 1, d):
            E = np.zeros((d, d), complex); E[a, b] = E[b, a] = 1 / np.sqrt(2); herm.append(E)
            E = np.zeros((d, d), complex); E[a, b] = -1j / np.sqrt(2); E[b, a] = 1j / np.sqrt(2); herm.append(E)
    n = len(herm)
    def cas(X):
        out = np.zeros_like(X)
        for J in (Jx, Jy, Jz):
            out += J @ (J @ X - X @ J) - (J @ X - X @ J) @ J
        return out
    C = np.zeros((n, n))
    for a in range(n):
        CX = cas(herm[a])
        for b in range(n):
            C[b, a] = np.real(hs(herm[b], CX))
    C = (C + C.T) / 2
    w, v = np.linalg.eigh(C)
    bases = {}
    for l in range(int(round(2 * j)) + 1):
        idx = [k for k in range(n) if abs(w[k] - l * (l + 1)) < 1e-8]
        assert len(idx) == 2 * l + 1, (l, len(idx))
        bases[l] = [sum(v[a, k] * herm[a] for a in range(n)) for k in idx]
    return bases


def proj_l(j, X, l):
    """Projection of X onto the rank-l subspace."""
    B = multipole_basis(j)[l]
    return sum(np.real(hs(b, X)) * b for b in B)


def kernel_D(j, w):
    return np.diag(np.asarray(w, float)).astype(complex)


def coherent_kernel(j):
    d = int(round(2 * j + 1))
    w = np.zeros(d); w[0] = 1.0
    return w


def eta_of_w(j, w):
    """Multipole ratios eta_l(w) = <T_l0, D_w>/<T_l0, D_coh>, l = 1..2j."""
    D = kernel_D(j, w); Dc = kernel_D(j, coherent_kernel(j))
    out = []
    for l in range(1, int(round(2 * j)) + 1):
        a = proj_l(j, D, l); c = proj_l(j, Dc, l)
        out.append(np.real(hs(c, a)) / np.real(hs(c, c)))
    return np.array(out)


def m_coeffs(j, G, sigma):
    """Twirl coefficients m_l(G,sigma) = d <G^(l), sigma^(l)>/(2l+1), l = 1..2j,
    for unit-trace G and sigma."""
    d = int(round(2 * j + 1))
    return np.array([d * np.real(hs(proj_l(j, G, l), proj_l(j, sigma, l))) / (2 * l + 1)
                     for l in range(1, int(round(2 * j)) + 1)])


# ---------------- spin-1 Cartesian parametrisation ----------------
def spin1_cart():
    """Spin-1 matrices in the Cartesian basis: (S_i)_{jk} = -i eps_{ijk}."""
    eps = np.zeros((3, 3, 3))
    eps[0, 1, 2] = eps[1, 2, 0] = eps[2, 0, 1] = 1
    eps[0, 2, 1] = eps[2, 1, 0] = eps[1, 0, 2] = -1
    return [-1j * eps[i] for i in range(3)]


def pA_of(X):
    """Vector p_i = Tr(X S_i) and traceless symmetric A_ij = Tr(X ({S_i,S_j}/2 - (2/3) delta_ij))
    for a 3x3 operator X given in the Cartesian basis."""
    S = spin1_cart()
    p = np.array([np.real(np.trace(X @ S[i])) for i in range(3)])
    A = np.zeros((3, 3))
    for i in range(3):
        for k in range(3):
            Q = (S[i] @ S[k] + S[k] @ S[i]) / 2 - (2 / 3) * (i == k) * np.eye(3)
            A[i, k] = np.real(np.trace(X @ Q))
    return p, A


def X_of_pA(p, A, tr=1.0):
    """Inverse map: X = tr/3 + (1/2) p.S + sum_ij A_ij Q_ij (Cartesian basis)."""
    S = spin1_cart()
    X = tr / 3 * np.eye(3, dtype=complex)
    for i in range(3):
        X = X + 0.5 * p[i] * S[i]
        for k in range(3):
            Q = (S[i] @ S[k] + S[k] @ S[i]) / 2 - (2 / 3) * (i == k) * np.eye(3)
            X = X + A[i, k] * Q
    return X


def pure_spin1(alpha):
    """Pure state cos(alpha) e_x + i sin(alpha) e_y in the Cartesian basis.
    alpha = 0: m=0 state along x; alpha = pi/4: m=+1 coherent state along z (up to phase)."""
    psi = np.array([np.cos(alpha), 1j * np.sin(alpha), 0])
    return np.outer(psi, psi.conj())


def fib_sphere(n):
    k = np.arange(n) + 0.5
    phi = np.arccos(1 - 2 * k / n)
    th = np.pi * (1 + 5 ** 0.5) * k
    return np.stack([np.cos(th) * np.sin(phi), np.sin(th) * np.sin(phi), np.cos(phi)], 1)

