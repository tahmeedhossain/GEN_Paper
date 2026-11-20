"""General spin j: vector analysing power bound  |kappa_1| <= xi_{2j}.
(1) xi_n from Gauss / Gauss-Radau nodes;
(2) independent LP: max |Tr(sigma J_z)| over unit-trace sigma with nonnegative Husimi function equals (j+1) xi_{2j};
(3) first-moment coefficient c = kappa_1/((j+1)d) for random kernels;
(4) tightness: the kernel with multipole ratios m_l(G_coh, sigma*) is a valid probability vector (so the bound is attained)."""
import sys; sys.path.insert(0, 'lib')
import numpy as np
from math import comb
from scipy.optimize import linprog
from scipy.special import roots_legendre, roots_jacobi
from spinlib import *

def xi(n):
    """sup of first-moment/mean over nonnegative polynomials of degree <= n on [-1,1] (Lebesgue weight)."""
    k = n // 2
    if n % 2 == 0:
        return roots_legendre(k + 1)[0].max()          # largest Gauss-Legendre node, k+1 nodes
    return roots_jacobi(k + 1, 0, 1)[0].max()          # largest free Gauss-Radau node (fixed node -1)

rows = []
for twoj in range(1, 9):
    j = twoj / 2; d = twoj + 1
    # (2) LP over axially symmetric sigma = diag(s_m): Q(x) = sum_m s_m C(2j,j+m) ((1+x)/2)^(j+m) ((1-x)/2)^(j-m) >= 0
    xs = np.cos(np.linspace(0, np.pi, 20001))
    ms = np.array([j - k for k in range(d)])
    Bq = np.array([[comb(twoj, int(round(j + m))) * ((1 + x) / 2) ** (j + m) * ((1 - x) / 2) ** (j - m) for m in ms] for x in xs])
    res = linprog(-ms, A_ub=-Bq, b_ub=np.zeros(len(xs)), A_eq=np.ones((1, d)), b_eq=[1.0], bounds=(None, None), method='highs')
    pmax = -res.fun; s_star = res.x
    # (4) tightness: kernel with eta_l = m_l(G_coh, sigma*)
    G = np.zeros((d, d), complex); G[0, 0] = 1
    sig = np.diag(s_star).astype(complex)
    m = m_coeffs(j, G, sig)
    Dc = kernel_D(j, coherent_kernel(j))
    D = proj_l(j, Dc, 0) + sum(m[l - 1] * proj_l(j, Dc, l) for l in range(1, twoj + 1))
    w = np.real(np.diag(D)); offdiag = np.abs(D - np.diag(np.diag(D))).max()
    kappa1 = sum(ms * w) / j
    rows.append((j, xi(twoj), pmax / (j + 1), m[0], w.min(), kappa1))
    print('j=%.1f  xi_2j=%.6f   LP max|p|/(j+1)=%.6f   m_1(G_coh,sigma*)=%.6f   min w=%+.4f  kappa_1(w)=%.6f  offdiag=%.1e'
          % (j, xi(twoj), pmax / (j + 1), m[0], w.min(), kappa1, offdiag))
# closed forms
print('closed forms: xi_1 = 1/3 = %.6f ; xi_2 = 1/sqrt3 = %.6f ; xi_3 = (1+sqrt6)/5 = %.6f ; xi_4 = sqrt(3/5) = %.6f'
      % (1 / 3, 1 / np.sqrt(3), (1 + np.sqrt(6)) / 5, np.sqrt(0.6)))
# (3) first-moment coefficient for random kernels
rng = np.random.default_rng(2)
for j in (0.5, 1.0, 1.5, 2.0):
    d = int(2 * j + 1); Jx, Jy, Jz = spin_ops(j)
    w = rng.dirichlet(np.ones(d)); D = kernel_D(j, w)
    kappa1 = np.real(np.trace(D @ Jz)) / j
    # M_z = (1/4pi) int R_q D R_q^+ q_z dq  via quadrature
    th, wts = np.polynomial.legendre.leggauss(40); M = np.zeros((d, d), complex)
    for x, wt in zip(th, wts):
        for ph in np.linspace(0, 2 * np.pi, 40, endpoint=False):
            q = np.array([np.sqrt(1 - x * x) * np.cos(ph), np.sqrt(1 - x * x) * np.sin(ph), x])
            R = rot(j, q); M += wt * (2 * np.pi / 40) * x * (R @ D @ R.conj().T)
    M /= 4 * np.pi
    c = kappa1 / ((j + 1) * d)
    print('j=%.1f  first-moment operator = c J_z with c = kappa_1/((j+1)d): max err %.2e' % (j, np.abs(M - c * Jz).max()))
np.save('out/t08_general_j.npy', np.array(rows))

