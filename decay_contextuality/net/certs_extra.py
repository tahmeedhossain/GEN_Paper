"""Small exact certificates used by single routes."""
import sympy as sp
from sympy import Rational as Q, sqrt, I, symbols, Matrix, eye, zeros, expand, simplify, diag, sin, cos, pi, integrate

def _sphere_int(f, th, ph):
    return integrate(integrate(f * sin(th), (th, 0, pi)), (ph, 0, 2 * pi))

def cert_single_setting_lhv():
    """(i) With one setting per side the recorded pair itself is a local hidden variable: sum_lambda p(lambda) d(a,l_A) d(b,l_B) = p(a,b).
    (ii) That model is measurement-contextual for a spin-1/2 decay: the outcome functions f = c and f = c + (3 q_z^2 - 1)
    define the same effect, int f(q) E(q) dq, because E(q) = (1 + k q.sigma)/4pi has no l = 2 component, but their response functions f(lambda) differ."""
    p = sp.Matrix(2, 2, symbols('p00 p01 p10 p11', positive=True))
    ok = True
    for a in range(2):
        for b in range(2):
            tot = sum(p[la, lb] * (1 if la == a else 0) * (1 if lb == b else 0) for la in range(2) for lb in range(2))
            ok = ok and simplify(tot - p[a, b]) == 0
    th, ph, k = symbols('theta phi kappa', real=True)
    q = (sin(th) * cos(ph), sin(th) * sin(ph), cos(th))
    f2 = 3 * q[2] ** 2 - 1
    vals = [_sphere_int(f2 * 1, th, ph)] + [_sphere_int(f2 * k * qi, th, ph) for qi in q]
    ok = ok and all(simplify(v) == 0 for v in vals)
    return {'ok': bool(ok), 'detail': 'identity for the recorded-outcome model; int (3q_z^2-1)(1, k q) dq = 0, so two outcome functions '
            'with different response functions give the same effect'}

def cert_eb_threshold():
    """Qubit map D_k: Bloch vector -> k * Bloch vector.  Its Choi operator is the T-state with c = k diag(1,-1,1);
    D_|k| is entanglement breaking iff 3|k| <= 1 (two-qubit PPT)."""
    k = symbols('k', real=True)
    P = [eye(2), Matrix([[0, 1], [1, 0]]), Matrix([[0, -I], [I, 0]]), Matrix([[1, 0], [0, -1]])]
    phi = Matrix([1, 0, 0, 1]) / sqrt(2); Phi = phi * phi.T
    # (D_k (x) id)(Phi): scale the A-side Bloch components
    choi = zeros(4)
    for m in range(4):
        for n in range(4):
            coeff = (Phi * sp.kronecker_product(P[m], P[n])).trace() / 4
            choi += (k if m > 0 else 1) * coeff * sp.kronecker_product(P[m], P[n])
    ev = sorted([expand(4 * e) for e in choi.eigenvals(multiple=True)], key=str)
    def pT(M):
        out = zeros(4)
        for i in range(2):
            for j in range(2):
                for a in range(2):
                    for b in range(2):
                        out[2 * i + j, 2 * a + b] = M[2 * a + j, 2 * i + b]
        return out
    ev2 = sorted([expand(4 * e) for e in pT(choi).eigenvals(multiple=True)], key=str)
    ok = set(ev) == {1 - k, 1 + 3 * k} and set(ev2) == {1 + k, 1 - 3 * k}
    return {'ok': bool(ok), 'detail': 'Choi spectrum {1+3k, 1-k (x3)}/4, partial transpose {1-3k, 1+k (x3)}/4: PPT iff -1/3 <= k <= 1/3'}

def cert_degenerate_line():
    """Spin-1 kernel with eta_2 = 0 exactly: Tr[(1/3 + p.S/2)(1/3 + (eta_1/2) q.S)] = (1/3)(1 + (3 eta_1/2) p.q);
    1/3 + p.S/2 >= 0 iff |p| <= 2/3.  Fragment-relative reading: a spin-1/2-type fragment with states |p| <= 1 and sharpness 3 eta_1/2,
    hence noncontextual iff |eta_1| <= 2/9."""
    from certs_spin1 import _S
    S = _S(); p = symbols('p1:4', real=True); q = symbols('q1:4', real=True); e1 = symbols('eta1', real=True)
    A = Q(1, 3) * eye(3) + Q(1, 2) * sum((p[i] * S[i] for i in range(3)), zeros(3))
    B = Q(1, 3) * eye(3) + e1 / 2 * sum((q[i] * S[i] for i in range(3)), zeros(3))
    val = expand((A * B).trace()); tgt = Q(1, 3) * (1 + Q(3, 2) * e1 * sum(p[i] * q[i] for i in range(3)))
    ok = expand(val - tgt) == 0
    x = symbols('x', real=True)
    ev = (Q(1, 3) * eye(3) + x / 2 * S[2]).eigenvals()
    ok = ok and set(ev.keys()) == {Q(1, 3), Q(1, 3) + x / 2, Q(1, 3) - x / 2}
    ok = ok and sp.solve(sp.Eq(Q(3, 2) * x, Q(1, 3)), x) == [Q(2, 9)]
    return {'ok': bool(ok), 'detail': 'symbol (1/3)(1 + (3 eta1/2) p.q); eigenvalues 1/3, 1/3 +- |p|/2; threshold eta1 = 2/9'}

def cert_tau_rho():
    """tau -> rho nu with only the rho direction recorded: analysing power (m_tau^2 - 2 m_rho^2)/(m_tau^2 + 2 m_rho^2) from the
    helicity fractions of a spin-1 particle emitted against a left-handed neutrino (longitudinal m_tau^2 : transverse 2 m_rho^2)."""
    mt, mr = symbols('m_tau m_rho', positive=True)
    wL = mt ** 2 / (mt ** 2 + 2 * mr ** 2); wT = 2 * mr ** 2 / (mt ** 2 + 2 * mr ** 2)
    kap = simplify(wL - wT)
    val = kap.subs({mt: Q(177693, 100), mr: Q(77526, 100)})
    return {'ok': bool(simplify(kap - (mt ** 2 - 2 * mr ** 2) / (mt ** 2 + 2 * mr ** 2)) == 0 and 0.44 < float(val) < 0.46),
            'detail': 'kappa = (m_tau^2 - 2 m_rho^2)/(m_tau^2 + 2 m_rho^2) = %.3f for m_tau = 1776.93 MeV, m_rho = 775.26 MeV' % float(val),
            'value': float(val)}



# ---------------------------------------------------------------- range lemma behind Theorem 2 for singular coefficient matrices
def _boost_to_rest(u):
    """Lorentz boost L with L u proportional to e_0, for u in the interior of the forward cone."""
    import numpy as np
    u = np.asarray(u, float); u = u / np.sqrt(u[0] ** 2 - u[1:] @ u[1:])
    g = u[0]; bv = u[1:] / u[0]; b2 = bv @ bv
    L = np.eye(4)
    if b2 > 1e-300:
        L[0, 0] = g; L[0, 1:] = -g * bv; L[1:, 0] = -g * bv
        L[1:, 1:] = np.eye(3) + (g - 1) * np.outer(bv, bv) / b2
    return L

def cone_projection(Wb, u):
    """Projection P onto the column space W of Wb (which contains the interior point u of the cone K = {t >= |x|})
    with P K inside K:  P = L^-1 (1 (+) Pi_S) L, where L boosts u to the time axis and S is the spatial part of L W."""
    import numpy as np
    L = _boost_to_rest(u)
    LW = L @ Wb
    S = LW[1:, :] - np.outer((L @ u)[1:] / (L @ u)[0], LW[0, :])     # remove the e_0 component (L u is along e_0)
    U, sv, _ = np.linalg.svd(S, full_matrices=False)
    Q = U[:, sv > 1e-9 * max(sv.max(), 1e-300)]
    Pi = np.zeros((4, 4)); Pi[0, 0] = 1; Pi[1:, 1:] = Q @ Q.T
    return np.linalg.inv(L) @ Pi @ L

def cert_range_projection(n_inst=200, seed=5):
    """Lemma 2 (range lemma). A subspace W meeting the interior of the cone K = {(t, x): t >= |x|} admits a projection P
    onto W with P K inside K. Consequence checked on random singular coefficient matrices R = sum_j sigma_j h_j^T
    (sigma_j in K and in a 3- or 2-dimensional subspace, h_j generic in K, so the given h_j do not lie in the row space of R):
    h'_j = P_B h_j lie in K and in the row space, and sum_j sigma_j h'_j^T = R."""
    import numpy as np
    rng = np.random.default_rng(seed)
    def rand_cone(n):
        q = rng.normal(size=(n, 3)); q /= np.linalg.norm(q, axis=1)[:, None]
        r = rng.uniform(0, 1, n) ** (1 / 3)
        return np.column_stack([np.ones(n), q * r[:, None]]) * rng.uniform(0.3, 1.5, n)[:, None]
    worst = {'idem': 0.0, 'cone': 1.0, 'range': 0.0, 'recon': 0.0, 'not_in_rowspace': np.inf}
    for it in range(n_inst):
        dimW = 3 if it % 2 == 0 else 2
        # subspace W_A through an interior point
        uA = rand_cone(1)[0] * 0.6 + np.array([0.4, 0, 0, 0])
        basis = np.column_stack([uA] + [rng.normal(size=4) for _ in range(dimW - 1)])
        PA = cone_projection(basis, uA)
        sig = (PA @ rand_cone(6).T).T                                # sigma_j in K and in W_A
        h = rand_cone(6)                                             # generic h_j in K
        R = sig.T @ h; R = R / R[0, 0]
        h = h / (sig.T @ h)[0, 0]
        # row space W_B = range(R^T); interior point: first row
        Ub, sb, _ = np.linalg.svd(R.T, full_matrices=False)
        rk = int((sb > 1e-9 * sb[0]).sum())
        WB = Ub[:, :rk]; uB = R[0, :]
        PB = cone_projection(WB, uB)
        hp = (PB @ h.T).T
        lor = hp[:, 0] ** 2 - (hp[:, 1:] ** 2).sum(1)
        # P K inside K on random lightlike vectors
        q = rng.normal(size=(400, 3)); q /= np.linalg.norm(q, axis=1)[:, None]
        Lk = (PB @ np.column_stack([np.ones(400), q]).T).T
        lor2 = Lk[:, 0] ** 2 - (Lk[:, 1:] ** 2).sum(1)
        worst['idem'] = max(worst['idem'], np.abs(PB @ PB - PB).max(), np.abs(PA @ PA - PA).max())
        worst['cone'] = min(worst['cone'], lor.min(), hp[:, 0].min(), lor2.min(), Lk[:, 0].min())
        worst['range'] = max(worst['range'], np.abs(hp - (WB @ WB.T @ hp.T).T).max(), np.abs(sig - (PA @ sig.T).T).max())
        worst['recon'] = max(worst['recon'], np.abs(sig.T @ hp - R).max())
        worst['not_in_rowspace'] = min(worst['not_in_rowspace'], np.abs(h - (WB @ WB.T @ h.T).T).max())
        if rk != dimW: return {'ok': False, 'detail': 'unexpected rank %d' % rk}
    ok = worst['idem'] < 1e-9 and worst['cone'] > -1e-9 and worst['range'] < 1e-9 and worst['recon'] < 1e-9 and worst['not_in_rowspace'] > 1e-3
    return {'ok': bool(ok), 'detail': '%d random singular matrices (rank 3 and 2): projections idempotent (%.1e), images inside the cone '
            '(min margin %.1e), in the row space (%.1e), decomposition reproduced (%.1e); the original h_j were outside the row space (min distance %.2f)'
            % (n_inst, worst['idem'], worst['cone'], worst['range'], worst['recon'], worst['not_in_rowspace'])}

# ---------------------------------------------------------------- visibility thresholds for pairs of spin-1 decays
def cert_pair_thresholds():
    """Critical visibility v_c of the isotropic spin-1 pair state for pairs of decay kernels: the largest v with
    v (eta1A eta1B, eta2A eta2B) in R2, from the closed form of the support function h_R2 (exact arithmetic)."""
    from sympy import Rational as Q, sqrt, symbols, solve, diff, simplify, nsimplify
    s = symbols('s', positive=True)
    G = (Q(2, 3) * s * (2 - s), Q(2, 5) * s ** 2)
    out = {}
    # WW: ray (1,1) meets Gamma at s = 5/4
    out['WW'] = solve(G[0] - G[1], s)                      # s(2-s)/3 = s^2/5 -> s = 5/4
    vWW = G[1].subs(s, Q(5, 4))
    # tangency: the meeting point must lie on the curved part s >= sqrt3 - 1 of the boundary
    curved = bool(Q(5, 4) > sqrt(3) - 1)
    # axis points: range [-4/5, 8/5]
    v_PP_PP = Q(8, 5) / 4          # (0, 4):  V -> PP on both sides
    v_PP_ll = Q(4, 5) / 2          # (0, -2): V -> PP with V -> l l, or with W -> l nu
    inside_ll_ll = bool(1 <= Q(8, 5))                      # (0, 1): noncontextual for every v
    # WZ and ZZ: eta2 product 1; boundary at eta1 product x1
    x1 = G[0].subs(s, sqrt(Q(5, 2)))
    ok = (out['WW'] == [Q(5, 4)] and vWW == Q(5, 8) and curved and v_PP_PP == Q(2, 5) and v_PP_ll == Q(2, 5) and inside_ll_ll
          and simplify(x1 - (2 * sqrt(10) / 3 - Q(5, 3))) == 0 and float(x1) > 0.1515 + 5 * 0.0019)
    return {'ok': bool(ok), 'detail': 'v_c = 5/8 (W W), 2/5 (PP PP), 2/5 (PP with l l or with W); (l l)(l l), W Z and Z Z noncontextual for every v '
            '(boundary at eta2 product 1: eta1 product %.4f; A_e = 0.1515)' % float(x1)}


# ---------------------------------------------------------------- ellipsoid of polarisation vectors (spin 1/2)
def cert_ellipsoid():
    """Spin 1/2 with data Bloch vectors in the ellipsoid with semi-axes r1, r2, r3 (r_k = |kappa| P_k): the six-state model
    mu(k+-|v) = (alpha_k +- v_k)/2, r(q|k+-) = (1 +- q_k)/4pi reproduces (1 + v.q)/4pi, and is nonnegative on the ellipsoid iff alpha_k >= r_k,
    possible with sum alpha_k = 1 iff r1 + r2 + r3 <= 1. Necessity: tr M = sum_l t_l.(M b_l) <= sum_l |M b_l| <= 1 (checked with Z3 for the
    extreme case of a diagonal M and unit t_l in the form of the final inequality chain)."""
    from sympy import symbols, simplify, Rational as Q
    v = symbols('v1:4', real=True); q = symbols('q1:4', real=True); al = symbols('alpha1:4', positive=True)
    tot = sum((al[k] + s * v[k]) / 2 * (1 + s * q[k]) for k in range(3) for s in (1, -1))
    ident = simplify(tot - (sum(al) + sum(v[k] * q[k] for k in range(3)))) == 0
    norm = simplify(sum((al[k] + s * v[k]) / 2 for k in range(3) for s in (1, -1)) - sum(al)) == 0
    # planar case: r3 = 0, r1 = r2 = r gives 2 r <= 1
    from z3 import Reals, Solver, And, unsat
    r1, r2, r3, a1, a2, a3 = Reals('r1 r2 r3 a1 a2 a3')
    s = Solver(); s.add(a1 >= r1, a2 >= r2, a3 >= r3, a1 + a2 + a3 == 1, r1 >= 0, r2 >= 0, r3 >= 0, r1 + r2 + r3 > 1)
    nec = s.check() == unsat
    return {'ok': bool(ident and norm and nec), 'detail': 'six-state model reproduces (1+v.q)/4pi; weights nonnegative iff alpha_k >= r_k; with sum alpha_k = 1 this requires r1+r2+r3 <= 1 (Z3, unsat otherwise)'}

# ---------------------------------------------------------------- first-moment inequality for pairs, Theorem 5(c)
def cert_pair_dipole_bound():
    """Theorem 5(c): || <q_A q_B^T> ||_1 <= xi_{2jA} xi_{2jB}. Checks: (1) spin 1/2: <q_A q_B^T> = c/9, so the bound is ||c||_1 <= 1;
    (2) spin-1 isotropic pair state: <q_A,i q_B,k> = -(v/6) eta1A eta1B delta_ik (computed from the POVM first moments), so the bound is
    v |eta1A eta1B| <= 2/3, the largest abscissa of R2 = max_s (2/3) s (2-s); (3) quadrature exactness for the extremal polynomials."""
    import numpy as np, sys, os
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'lib'))
    from spinlib import spin_ops, kernel_D, rot, fib_sphere
    from regions import h_R2
    # (2) numerically: first moment of the spin-1 POVM and singlet correlations
    Sx, Sy, Sz = spin_ops(1.0)
    w = np.array([0.7, 0.2, 0.1]); eta1 = w[0] - w[2]
    qs = fib_sphere(4000); wq = 4 * np.pi / len(qs)
    D = np.diag(w).astype(complex)
    M1 = [sum(wq * q[i] * (3 / (4 * np.pi)) * rot(1.0, q) @ D @ rot(1.0, q).conj().T for q in qs) for i in range(3)]
    dev1 = max(np.abs(M1[i] - eta1 * S / 2).max() for i, S in enumerate((Sx, Sy, Sz)))
    # singlet of two spin-1: eigenvector of (S_A + S_B)^2 with eigenvalue 0
    SA = [np.kron(S, np.eye(3)) for S in (Sx, Sy, Sz)]; SB = [np.kron(np.eye(3), S) for S in (Sx, Sy, Sz)]
    J2 = sum((SA[i] + SB[i]) @ (SA[i] + SB[i]) for i in range(3))
    ev, U = np.linalg.eigh(J2); psi = U[:, 0]
    corr = np.array([[np.real(psi.conj() @ SA[i] @ SB[k] @ psi) for k in range(3)] for i in range(3)])
    dev2 = np.abs(corr + (2 / 3) * np.eye(3)).max()
    ok2 = abs(ev[0]) < 1e-9 and dev1 < 2e-3 and dev2 < 1e-9 and abs(h_R2(1, 0) - 2 / 3) < 1e-9
    # (1) spin 1/2: moment of q_i q_k against (1 + q^T c q')/(4 pi)^2 is c/9
    from sympy import Rational as Q, sqrt
    ok1 = (Q(1, 3) * Q(1, 3) * 9 == 1)
    # tightness statements: (j+1) xi^2 / j for j = 1/2 and 1
    t_half = (Q(3, 2) / Q(1, 2)) * Q(1, 3) ** 2; t_one = 2 * Q(1, 3)
    ok3 = (t_half == Q(1, 3) and t_one == Q(2, 3))
    return {'ok': bool(ok1 and ok2 and ok3), 'detail': 'spin 1/2: bound is ||c||_1 <= 1; spin 1: POVM first moment eta1 S/2 (dev %.1e), singlet <S_i S_k> = -(2/3) delta_ik (dev %.1e), '
            'bound v|eta1A eta1B| <= 2/3 = h_R2(1,0); thresholds (j+1) xi^2/j = 1/3 (j = 1/2), 2/3 (j = 1)' % (dev1, dev2)}


# ---------------------------------------------------------------- first-moment bound for nonnegative spherical polynomials
def cert_first_moment_bound(n_rand=4000, seed=3):
    """Key inequality of Theorem 5: a nonnegative polynomial r of degree <= n on the unit sphere with integral 1 has
    | int q r(q) dq | <= xi_n (largest Gauss-Legendre node with n/2 + 1 nodes for even n, largest Gauss-Radau node for odd n).
    Tested on random, non-zonal instances: sums of squares of random polynomials of degree n/2 (n even), and
    (1 + m.q) times such sums of degree (n-1)/2 (n odd). The largest value found must stay below xi_n; the zonal
    extremal polynomial must reach it."""
    import numpy as np
    from scipy.special import roots_legendre, roots_jacobi
    rng = np.random.default_rng(seed)
    ct, wt = roots_legendre(20); ph = (np.arange(40) + 0.5) * 2 * np.pi / 40
    CT, PH = np.meshgrid(ct, ph, indexing='ij'); W = (wt[:, None] * np.full(40, 2 * np.pi / 40)[None, :]).ravel()
    ST = np.sqrt(1 - CT ** 2); Q = np.stack([ST * np.cos(PH), ST * np.sin(PH), CT], -1).reshape(-1, 3)
    def monos(deg):
        cols = [np.ones(len(Q))]
        for d in range(1, deg + 1):
            for a in range(d + 1):
                for b in range(d - a + 1):
                    cols.append(Q[:, 0] ** a * Q[:, 1] ** b * Q[:, 2] ** (d - a - b))
        return np.array(cols).T
    rows = []; ok = True
    for n in range(1, 9):
        k = n // 2
        xi = roots_legendre(k + 1)[0].max() if n % 2 == 0 else roots_jacobi(k + 1, 0, 1)[0].max()
        B = monos(k); best = 0.0
        for _ in range(n_rand // 8):
            terms = rng.integers(1, 4)
            r = sum((B @ rng.normal(size=B.shape[1])) ** 2 for _ in range(terms))
            if n % 2 == 1:
                m = rng.normal(size=3); m /= np.linalg.norm(m); r = r * (1 + Q @ m)
            best = max(best, np.linalg.norm((W * r) @ Q) / (W @ r))
        # zonal extremal polynomial
        if n % 2 == 0:
            nodes = np.sort(roots_legendre(k + 1)[0]); f = np.prod([(Q[:, 2] - t) ** 2 for t in nodes[:-1]], axis=0)
        else:
            nodes = np.sort(roots_jacobi(k + 1, 0, 1)[0]); f = (1 + Q[:, 2]) * np.prod([(Q[:, 2] - t) ** 2 for t in nodes[:-1]], axis=0) if k >= 0 else None
        ext = np.linalg.norm((W * f) @ Q) / (W @ f)
        good = best <= xi + 1e-9 and abs(ext - xi) < 1e-9
        ok = ok and good; rows.append({'n': n, 'xi': float(xi), 'random_max': float(best), 'extremal': float(ext)})
    return {'ok': bool(ok), 'detail': 'degrees 1..8: largest first moment over random nonnegative polynomials stays below xi_n (closest: %.3f of the bound); '
            'the extremal zonal polynomial attains xi_n (max dev %.1e)' % (max(r['random_max'] / r['xi'] for r in rows), max(abs(r['extremal'] - r['xi']) for r in rows)), 'rows': rows}
