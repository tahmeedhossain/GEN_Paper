"""Negative controls: each plants one error in an accepted statement; the corresponding check must reject it.
A control returns {'rejected': bool, 'detail': str}."""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(os.path.dirname(HERE), 'lib'))
import numpy as np, sympy as sp
from sympy import Rational as Q, sqrt, symbols, Matrix, eye, zeros, expand, simplify, diag
import certs_exact as ce, certs_spin1 as cs, certs_numeric as cn
from regions import h_R, h_R2

def k01():
    """spin-1/2 threshold 1/2 instead of 1/3: the tetrahedral weights (1+3 t.v)/4 must stay nonnegative at |v| = 1/2."""
    t = np.array([1, 1, 1]) / np.sqrt(3); v = -0.5 * t
    return {'rejected': bool((1 + 3 * t @ v) / 4 < 0), 'detail': 'weight %.3f < 0 at |v| = 1/2' % ((1 + 3 * t @ v) / 4)}
def k02():
    """direction-only leptonic analysing power 1/2 instead of 1/3."""
    x = symbols('x'); val = sp.integrate(x ** 2 * (2 * x - 1), (x, 0, 1)) / sp.integrate(x ** 2 * (3 - 2 * x), (x, 0, 1))
    return {'rejected': bool(val != Q(1, 2)), 'detail': 'integral gives %s' % val}
def k03():
    """Dirac trace with (p1 + m s) instead of (p1 - m s)."""
    g, g5 = ce._gammas(); PL = (eye(4) - g5) / 2; PR = (eye(4) + g5) / 2
    import random; random.seed(3)
    rv = lambda: [Q(random.randint(-9, 9), random.randint(1, 5)) for _ in range(4)]
    p1, p2, p3, p4, s = rv(), rv(), rv(), rv(), rv(); m = Q(7, 3)
    rho1 = (ce._slash(p1, g) + m * eye(4)) * (eye(4) + g5 * ce._slash(s, g)) / 2
    lhs = 0
    for mu in range(4):
        for nu in range(4):
            lhs += (ce._slash(p2, g) * g[mu] * PL * rho1 * PR * g[nu]).trace() * \
                   (ce._slash(p3, g) * (ce._ETA[mu, mu] * g[mu]) * PL * ce._slash(p4, g) * PR * (ce._ETA[nu, nu] * g[nu])).trace()
    wrong = 8 * ce._dot([p1[k] + m * s[k] for k in range(4)], p4) * ce._dot(p2, p3)
    return {'rejected': bool(sp.nsimplify(sp.expand(lhs - wrong)) != 0), 'detail': 'identity fails with the wrong sign of the spin vector'}
def k04():
    """T-state criterion with the Frobenius norm instead of the trace norm: c = diag(1/2,1/2,1/2) would be accepted."""
    c = np.diag([0.5, 0.5, 0.5]); P = cn._P
    rho = (np.eye(4) + sum(c[i, i] * np.kron(P[i + 1], P[i + 1]) for i in range(3))) / 4
    mn = min(np.linalg.eigvalsh(rho).min(), np.linalg.eigvalsh(cn._pt(rho)).min())
    return {'rejected': bool(np.linalg.norm(c) <= 1 and mn < 0), 'detail': 'Frobenius norm %.3f <= 1 but raw-PPT margin %.3f < 0' % (np.linalg.norm(c), mn)}
def k05():
    """ellipse centred at (0, 1/4) instead of (0, 1/5)."""
    tau = Q(1); m1sq = tau * (2 - tau) / 3; m2 = tau / 5
    return {'rejected': bool(3 * m1sq + 25 * (m2 - Q(1, 4)) ** 2 != 1), 'detail': 'extreme pair tau = 1 is not on the shifted ellipse'}
def k06():
    """apex of R at (0, -1) instead of (0, -4/5): support value in direction (0,-1) from the dual cone."""
    Ag = np.diag([-2 / 3, 1 / 3, 1 / 3]); As = np.diag([4 / 3, -2 / 3, -2 / 3])
    val = 0.6 * np.trace(Ag @ As)
    return {'rejected': bool(abs(h_R(0, -1) - 1.0) > 1e-9 and abs(val + 0.8) < 1e-12), 'detail': 'support value is 4/5, extreme pair gives %.3f' % val}
def k07():
    """twirl coefficient m2 = (1/2) Tr(AA') instead of (3/5) Tr(AA'): the finite model at the top of R must fail."""
    ex = Matrix([1, 0, 0]); lin = ex * ex.T
    Ag = diag(Q(-2, 3), Q(1, 3), Q(1, 3)); wrong_m2 = Q(1, 2) * (Ag * Ag).trace()
    D = (cs._twirl(lin, lin) - cs._target(0, wrong_m2)).applyfunc(simplify)
    return {'rejected': bool(D != zeros(9, 9)), 'detail': 'icosahedral twirl differs from Pi_0 + %s Pi_2' % wrong_m2}
def k08():
    """top of R2 at 2 instead of 8/5, which would make two ideal W decays on a singlet noncontextual."""
    return {'rejected': bool(h_R2(1, 1) < 2 and abs(h_R2(0, 1) - 1.6) < 1e-12), 'detail': 'h(1,1) = %.3f < 2 = (1,1).(1,1)' % h_R2(1, 1)}
def k09():
    """isotropic W-pair threshold 1/2 instead of 5/8: (1/2,1/2) must be strictly inside R2 and (5/8,5/8) on its boundary."""
    inside = all(np.cos(p) * 0.5 + np.sin(p) * 0.5 < h_R2(np.cos(p), np.sin(p)) - 1e-6 for p in np.linspace(0, 2 * np.pi, 721))
    onb = min(h_R2(np.cos(p), np.sin(p)) - (np.cos(p) + np.sin(p)) * 0.625 for p in np.linspace(0, 2 * np.pi, 7201))
    return {'rejected': bool(inside and abs(onb) < 1e-5), 'detail': '(1/2,1/2) is interior; boundary slack at (5/8,5/8) = %.1e' % onb}
def k10():
    """largest noncontextual vector analysing power for spin 1 claimed to be 0.6 instead of 1/sqrt3."""
    from scipy.optimize import linprog
    xs = np.cos(np.linspace(0, np.pi, 20001)); ms = np.array([1.0, 0.0, -1.0])
    Bq = np.array([[((1 + x) / 2) ** 2, 2 * ((1 + x) / 2) * ((1 - x) / 2), ((1 - x) / 2) ** 2] for x in xs])
    res = linprog(-ms, A_ub=-Bq, b_ub=np.zeros(len(xs)), A_eq=np.ones((1, 3)), b_eq=[1.0], bounds=(None, None), method='highs')
    return {'rejected': bool(abs(-res.fun / 2 - 0.6) > 1e-3), 'detail': 'LP value %.5f' % (-res.fun / 2)}
def k11():
    """b-quark polarimeter nonclassical iff m_t > 3 m_W (instead of 2 m_W)."""
    xi = symbols('xi', positive=True); thr = sp.solve(sp.Eq((xi - 2) / (xi + 2), Q(1, 3)), xi)
    return {'rejected': bool(thr != [9]), 'detail': 'threshold xi = %s, not 9' % thr}
def k12():
    """hyperon-pair state with the wrong sign of C_yy: must not be a density matrix."""
    al, dphi = cn.INPUTS['alpha_psi'][0], cn.INPUTS['DeltaPhi'][0]
    R = cn.lambda_R(np.pi / 2 - 0.3, al, dphi); R[2, 2] = -R[2, 2]
    mn = np.linalg.eigvalsh(cn._rho_from_R(R)).min()
    return {'rejected': bool(mn < -1e-6), 'detail': 'min eigenvalue %.3f' % mn}
def k13():
    """|D| <= 1/2 claimed as the noncontextuality bound: the witness values (1 +- tr c)/4 vanish at |tr c| = 1, i.e. |D| = 1/3."""
    return {'rejected': bool(abs((1 - 3 * 0.5) / 4) > 1e-9 and abs((1 - 3 * (1 / 3)) / 4) < 1e-12), 'detail': 'witness is zero at |D| = 1/3, negative at 1/2'}
def k14():
    """recorded-outcome model declared noncontextual: needs int (3 q_z^2 - 1) E(q) dq != 0, which is false."""
    r = __import__('certs_extra').cert_single_setting_lhv()
    return {'rejected': bool(r['ok']), 'detail': 'the l = 2 outcome function integrates to the zero effect'}
def k15():
    """range lemma with the Euclidean orthogonal projector instead of the boosted one: for a subspace that does not
    contain the time axis the Euclidean projection throws lightlike vectors out of the cone."""
    cx = __import__('certs_extra')
    W = np.column_stack([[1, 0, 0, 0.8], [0, 1, 0, 0], [0, 0, 1, 0]]).astype(float)
    Qm, _ = np.linalg.qr(W); PE = Qm @ Qm.T
    PB = cx.cone_projection(W, np.array([1, 0, 0, 0.8]))
    rng = np.random.default_rng(1); q = rng.normal(size=(4000, 3)); q /= np.linalg.norm(q, axis=1)[:, None]
    X = np.column_stack([np.ones(4000), q])
    lorE = ((PE @ X.T).T[:, 0]) ** 2 - (((PE @ X.T).T[:, 1:]) ** 2).sum(1)
    lorB = ((PB @ X.T).T[:, 0]) ** 2 - (((PB @ X.T).T[:, 1:]) ** 2).sum(1)
    return {'rejected': bool(lorE.min() < -1e-3 and lorB.min() > -1e-10), 'detail': 'Euclidean projector: min Lorentz norm %.3f < 0; boosted projector: %.1e' % (lorE.min(), lorB.min())}
def k16():
    """two decays into pseudoscalar pairs on a singlet: threshold visibility 1/2 instead of 2/5; the point (0, 2) must lie outside R2."""
    return {'rejected': bool(h_R2(0, 1) < 2 - 1e-9 and abs(h_R2(0, 1) - 4 * 0.4) < 1e-12), 'detail': 'h(0,1) = %.3f < 2; boundary at 4 v = 8/5' % h_R2(0, 1)}
CONTROLS = [k01, k02, k03, k04, k05, k06, k07, k08, k09, k10, k11, k12, k13, k14, k15, k16]

