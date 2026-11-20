"""Exact certificates for the spin-1 results (single particle region R, pair region R2) and the
general-spin quadrature bound.  SymPy / exact arithmetic."""
import itertools
import sympy as sp
from sympy import Rational as Q, sqrt, I, symbols, Matrix, eye, zeros, expand, simplify, diag

def _S():
    eps = lambda i, j, k: sp.LeviCivita(i, j, k)
    return [Matrix(3, 3, lambda j, k: -I * eps(i, j, k)) for i in range(3)]
def _Qop(i, k, S): return (S[i] * S[k] + S[k] * S[i]) / 2 - Q(2, 3) * (1 if i == k else 0) * eye(3)

def X_of_pA(p, A, tr=1):
    S = _S(); X = Q(1, 3) * tr * eye(3)
    for i in range(3):
        X += Q(1, 2) * p[i] * S[i]
        for k in range(3):
            X += A[i, k] * _Qop(i, k, S)
    return X

def cert_spin1_algebra():
    S = _S()
    ok = simplify(S[0] * S[1] - S[1] * S[0] - I * S[2]) == zeros(3)
    # Tr(Q_ij Q_kl)
    for i, k, a, b in itertools.product(range(3), repeat=4):
        lhs = (_Qop(i, k, S) * _Qop(a, b, S)).trace()
        rhs = Q(1, 2) * (int(i == a) * int(k == b) + int(i == b) * int(k == a)) - Q(1, 3) * int(i == k) * int(a == b)
        ok = ok and simplify(lhs - rhs) == 0
    # kernel: w+ P+ + w0 P0 + w- P-  =  1/3 + (eta1/2) q.S + (eta2/6)(3 (q.S)^2 - 2)   on |q| = 1
    qx, qy, qz, wp, w0, wm = symbols('q_x q_y q_z w_p w_0 w_m', real=True)
    qS = qx * S[0] + qy * S[1] + qz * S[2]
    _c = qx ** 2 + qy ** 2 + qz ** 2 - 1
    def red(e): return expand(sp.rem(expand(e), _c, qz))          # remainder modulo |q|^2 = 1
    def on_sphere(M): return M.applyfunc(red)
    ok = ok and on_sphere(qS ** 3 - qS) == zeros(3)                 # eigenvalues 1,0,-1
    Pp = (qS * qS + qS) / 2; Pm = (qS * qS - qS) / 2; P0 = eye(3) - qS * qS
    eta1 = wp - wm; eta2 = 1 - 3 * w0
    lhs = wp * Pp + w0 * P0 + wm * Pm
    rhs = Q(1, 3) * eye(3) + eta1 / 2 * qS + eta2 / 6 * (3 * qS * qS - 2 * eye(3))
    ok = ok and on_sphere((lhs - rhs).subs(wm, 1 - wp - w0)) == zeros(3)
    # w-symbol of sigma = 1/3 + p.S/2 + A.Q :  1/3 + (eta1/2) p.q + (eta2/2) q^T A q
    p = symbols('p1:4', real=True); a11, a22, a12, a13, a23 = symbols('a11 a22 a12 a13 a23', real=True)
    A = Matrix([[a11, a12, a13], [a12, a22, a23], [a13, a23, -a11 - a22]])
    sig = X_of_pA(p, A)
    e1, e2 = symbols('eta1 eta2', real=True)
    ker = Q(1, 3) * eye(3) + e1 / 2 * qS + e2 / 6 * (3 * qS * qS - 2 * eye(3))
    qv = Matrix([qx, qy, qz])
    val = expand((sig * ker).trace())
    target = Q(1, 3) + e1 / 2 * (p[0] * qx + p[1] * qy + p[2] * qz) + e2 / 2 * (qv.T * A * qv)[0]
    ok = ok and red(val - target) == 0
    # pure state cos(al) e_x + i sin(al) e_y : p = (0,0,sin 2al), A = diag(1/3 - cos^2, 1/3 - sin^2, 1/3)
    al = symbols('alpha', real=True)
    psi = Matrix([sp.cos(al), I * sp.sin(al), 0]); G = psi * psi.H
    pG = [simplify((G * S[i]).trace()) for i in range(3)]
    AG = Matrix(3, 3, lambda i, k: simplify((G * _Qop(i, k, S)).trace()))
    ok = ok and simplify(pG[0]) == 0 and simplify(pG[1]) == 0 and simplify(pG[2] - sp.sin(2 * al)) == 0
    ok = ok and simplify(AG - diag(Q(1, 3) - sp.cos(al) ** 2, Q(1, 3) - sp.sin(al) ** 2, Q(1, 3))) == zeros(3)
    # twirl coefficients: <G^(1),s^(1)> = p.p'/2 ; <G^(2),s^(2)> = Tr(A A')  ->  m1 = p.p'/2, m2 = (3/5) Tr(AA')
    okc = simplify((S[0] * S[0]).trace() - 2) == 0 and simplify((S[0] * S[1]).trace()) == 0
    return {'ok': bool(ok and okc), 'detail': 'Tr(QQ) identity; kernel = 1/3 + (eta1/2) q.S + (eta2/6)(3(q.S)^2-2); symbol '
            '1/3 + (eta1/2) p.q + (eta2/2) q^T A q; pure-state (p,A); m1 = p.p\'/2, m2 = (3/5) Tr(AA\')'}

def cert_region_R_formulas():
    """Elementary steps of the support-function computation for R and the description of its boundary."""
    a, b, s, t, tau = symbols('a b s t tau', real=True)
    ok = True
    # 2x2 block [[t, -a s/2], [-a s/2, t/3 - b/5]] >= 0  <=>  t >= t_B := (3/2)[b/5 + sqrt(b^2/25 + a^2 s^2/3)]
    tB = Q(3, 2) * (b / 5 + sqrt(b ** 2 / 25 + a ** 2 * s ** 2 / 3))
    ok = ok and simplify(expand(tB * (tB / 3 - b / 5) - a ** 2 * s ** 2 / 4)) == 0
    # (2/3) t_B(s=1) = b/5 + sqrt(b^2/25 + a^2/3) = support function of the ellipse 3x^2 + 25(y-1/5)^2 <= 1
    hB = simplify(Q(2, 3) * tB.subs(s, 1) - (b / 5 + sqrt(b ** 2 / 25 + a ** 2 / 3)))
    ok = ok and hB == 0
    # extreme pairs (coherent g ; sigma with symbol (c + sqrt(tau) q_3)^2, c^2 = (2-tau)/3): m1 = sqrt(tau(2-tau)/3), m2 = tau/5
    c = sqrt((2 - tau) / 3)
    p_g = Matrix([0, 0, 1]); A_g = diag(Q(-1, 6), Q(-1, 6), Q(1, 3))
    p_s = Matrix([0, 0, 2 * c * sqrt(tau)]); A_s = tau * diag(Q(-1, 3), Q(-1, 3), Q(2, 3))
    m1 = Q(1, 2) * p_g.dot(p_s); m2 = Q(3, 5) * (A_g * A_s).trace()
    ok = ok and simplify(m1 ** 2 - tau * (2 - tau) / 3) == 0 and simplify(m2 - tau / 5) == 0
    ok = ok and simplify(3 * tau * (2 - tau) / 3 + 25 * (tau / 5 - Q(1, 5)) ** 2 - 1) == 0         # on the ellipse for every tau
    # symbol of sigma(tau): 2/3 + p.q + q^T A q = (c + sqrt(tau) q3)^2 on the sphere
    q3 = symbols('q3', real=True)
    sym = Q(2, 3) + 2 * c * sqrt(tau) * q3 + tau * (q3 ** 2 - Q(1, 3))
    ok = ok and simplify(expand(sym - (c + sqrt(tau) * q3) ** 2)) == 0
    # apex: g = linear polarisation along x (p=0, A=diag(-2/3,1/3,1/3)); sigma: p=0, A=diag(4/3,-2/3,-2/3), symbol 2 q1^2
    Ag = diag(Q(-2, 3), Q(1, 3), Q(1, 3)); As = diag(Q(4, 3), Q(-2, 3), Q(-2, 3))
    ok = ok and Q(3, 5) * (Ag * As).trace() == Q(-4, 5)
    q1, q2 = symbols('q1 q2', real=True)
    symA = Q(2, 3) + Q(4, 3) * q1 ** 2 - Q(2, 3) * q2 ** 2 - Q(2, 3) * (1 - q1 ** 2 - q2 ** 2)
    ok = ok and expand(symA - 2 * q1 ** 2) == 0
    # top of R: g = sigma = linear polarisation: m2 = (3/5)(2/3) = 2/5
    ok = ok and Q(3, 5) * (Ag * Ag).trace() == Q(2, 5)
    # tangent points from the apex (0,-4/5) to the ellipse: (+-2 sqrt2/5, 4/25), i.e. tau = 4/5
    xt, yt = 2 * sqrt(2) / 5, Q(4, 25)
    ok = ok and simplify(3 * xt ** 2 + 25 * (yt - Q(1, 5)) ** 2 - 1) == 0
    grad = Matrix([6 * xt, 50 * (yt - Q(1, 5))]); chord = Matrix([xt, yt + Q(4, 5)])
    ok = ok and simplify(grad.dot(chord)) == 0
    # width of R on the axis eta2 = 0 (limit eta2 -> 0): sqrt2/3 ; largest |eta1| in R: 1/sqrt3 at eta2 = 1/5
    ok = ok and simplify(xt * Q(4, 5) / (yt + Q(4, 5)) - sqrt(2) / 3) == 0
    # parity-symmetric kernels: eta2 = 1 - 3 w0 in [-4/5, 2/5]  <=>  w0 in [1/5, 3/5]  <=>  alpha = (1-3w0)/(1+w0) in [-1/2, 1/3]
    w0 = symbols('w0', positive=True)
    al = (1 - 3 * w0) / (1 + w0)
    ok = ok and al.subs(w0, Q(1, 5)) == Q(1, 3) and al.subs(w0, Q(3, 5)) == Q(-1, 2) and simplify(sp.diff(al, w0)) != 0
    # massive fermion pair through a vector current: w0 = 2x/(1+2x), x = m_f^2/M^2 ; w0 >= 1/5 <=> x >= 1/8
    x = symbols('x', positive=True)
    ok = ok and sp.solve(sp.Eq(2 * x / (1 + 2 * x), Q(1, 5)), x) == [Q(1, 8)]
    # exactly degenerate kernel eta2 = 0: effects 1 + (3 eta1/2) q.p on the unit ball of p  ->  |eta1| <= 2/9
    return {'ok': bool(ok), 'detail': 't_B root; ellipse 3x^2+25(y-1/5)^2=1 traced by tau in [1/2,2]; apex (0,-4/5); top (0,2/5); '
            'tangent points (+-2sqrt2/5, 4/25); alpha window [-1/2,1/3]; x >= 1/8'}

# ---------------------------------------------------------------- icosahedral finite models
def _icosa_group():
    phi = (1 + sqrt(5)) / 2
    g1 = diag(-1, -1, 1)
    g2 = Matrix([[0, 0, 1], [1, 0, 0], [0, 1, 0]])
    g3 = Q(1, 2) * Matrix([[1, -phi, 1 / phi], [phi, 1 / phi, -1], [1 / phi, 1, phi]])
    def canon(M): return M.applyfunc(lambda e: sp.nsimplify(sp.radsimp(expand(e))))
    gens = [canon(g) for g in (g1, g2, g3)]
    elems = [eye(3)]; keys = {tuple(eye(3))}
    frontier = [eye(3)]
    while frontier:
        new = []
        for M in frontier:
            for g in gens:
                Pm = canon(M * g); key = tuple(Pm)
                if key not in keys:
                    keys.add(key); elems.append(Pm); new.append(Pm)
        frontier = new
        if len(elems) > 60: break
    return elems

_GROUP = None
def _twirl(G, sig):
    """Superoperator T(X) = (3/|I|) sum_g (g sig g^T) Tr(g G g^T X) on 3x3 matrices (Cartesian basis), as a 9x9 matrix."""
    global _GROUP
    if _GROUP is None: _GROUP = _icosa_group()
    T = zeros(9, 9)
    for R in _GROUP:
        sg = R * sig * R.T; Gg = R * G * R.T
        T += Matrix(9, 1, list(sg)) * Matrix(1, 9, list(Gg.T))      # Tr(Gg X) = sum_ab Gg[b,a] X[a,b]
    return (Q(3, len(_GROUP)) * T).applyfunc(lambda e: sp.radsimp(expand(e)))

def _target(m1, m2):
    """Pi_0 + m1 Pi_1 + m2 Pi_2 with Pi_0 X = tr(X)/3, Pi_1 X = (X - X^T)/2, Pi_2 X = (X + X^T)/2 - tr(X)/3."""
    T = zeros(9, 9)
    for a in range(3):
        for b in range(3):
            X = zeros(3); X[a, b] = 1
            Y = Q(1, 3) * X.trace() * eye(3) + m1 * (X - X.T) / 2 + m2 * ((X + X.T) / 2 - Q(1, 3) * X.trace() * eye(3))
            T[:, 3 * a + b] = Matrix(9, 1, list(Y))
    return T

def _sq(tau, sign=1):
    """Unit-trace operator with Husimi-type symbol (c + sqrt(tau) q_3)^2, c = sign*sqrt((2-tau)/3)."""
    tau = sp.nsimplify(tau); c = sign * sqrt((2 - tau) / 3)
    return X_of_pA([0, 0, 2 * c * sqrt(tau)], tau * diag(Q(-1, 3), Q(-1, 3), Q(2, 3)))

def cert_finite_models():
    """Explicit finite noncontextual models (ontic states = icosahedral rotations of one pair), verified exactly:
    T_{G,sigma} = Pi_0 + m1 Pi_1 + m2 Pi_2 for the extreme points of R and of R2."""
    ex = Matrix([1, 0, 0]); lin = ex * ex.T                                  # linear polarisation along x
    psi = Matrix([1, I, 0]) / sqrt(2); coh = psi * psi.H                     # coherent state m=+1 along z
    Z = eye(3) - 2 * lin                                                     # symbol 2 q_1^2
    cases = [
        ('R top (0, 2/5)', lin, lin, 0, Q(2, 5)),
        ('R coherent (1/2, 1/10)', coh, _sq(Q(1, 2)), Q(1, 2), Q(1, 10)),
        ('R max vector (1/sqrt3, 1/5)', coh, _sq(1), 1 / sqrt(3), Q(1, 5)),
        ('R tangent (2sqrt2/5, 4/25)', coh, _sq(Q(4, 5)), 2 * sqrt(2) / 5, Q(4, 25)),
        ('R apex (0, -4/5)', lin, Z, 0, Q(-4, 5)),
        ('R2 top (0, 8/5)', Z, Z, 0, Q(8, 5)),
        ('R2 isotropic WW (5/8, 5/8)', _sq(Q(5, 4)), _sq(Q(5, 4)), Q(5, 8), Q(5, 8)),
        ('R2 tangent Gamma(sqrt3-1)', _sq(sqrt(3) - 1), _sq(sqrt(3) - 1),
         Q(2, 3) * (sqrt(3) - 1) * (3 - sqrt(3)), Q(2, 5) * (sqrt(3) - 1) ** 2),
    ]
    global _GROUP
    if _GROUP is None: _GROUP = _icosa_group()
    ok = len(_GROUP) == 60
    # coherent state equals the tau = 1/2 square:  coh = _sq(1/2)
    ok = ok and simplify(coh - _sq(Q(1, 2))) == zeros(3)
    out = []
    for name, G, sig, m1, m2 in cases:
        D = (_twirl(G, sig) - _target(m1, m2)).applyfunc(lambda e: simplify(e))
        good = D == zeros(9, 9)
        ok = ok and good; out.append('%s:%s' % (name, 'ok' if good else 'FAIL'))
    return {'ok': bool(ok), 'detail': '|I| = %d; ' % len(_GROUP) + '; '.join(out)}

def cert_region_R2_formulas():
    import z3
    ok = True
    # (2-tau)(2-tau') <= (2-s)^2 for s = sqrt(tau tau'), tau, tau' in [0,2]
    t1, t2, s = z3.Reals('t1 t2 s')
    sol = z3.Solver(); sol.add(t1 >= 0, t1 <= 2, t2 >= 0, t2 <= 2, s >= 0, s * s == t1 * t2, (2 - t1) * (2 - t2) > (2 - s) * (2 - s))
    ok = ok and sol.check() == z3.unsat
    a, b, sv = symbols('a b s', positive=True)
    # stationary point of phi(s) = (2a/3)s(2-s) + (2b/5)s^2 and its value
    phi = Q(2, 3) * a * sv * (2 - sv) + Q(2, 5) * b * sv ** 2
    s0 = sp.solve(sp.diff(phi, sv), sv)[0]
    ok = ok and simplify(s0 - (a / 3) / (a / 3 - b / 5)) == 0
    ok = ok and simplify(phi.subs(sv, s0) - (2 * a ** 2 / 9) / (a / 3 - b / 5)) == 0
    # Gamma(s) = ((2/3)s(2-s), (2/5)s^2): convex arc (constant sign of x'y''-y'x''), top (0,8/5), widest point (2/3,2/5)
    x = Q(2, 3) * sv * (2 - sv); y = Q(2, 5) * sv ** 2
    curv = simplify(sp.diff(x, sv) * sp.diff(y, sv, 2) - sp.diff(y, sv) * sp.diff(x, sv, 2))
    ok = ok and curv == Q(16, 15)
    ok = ok and x.subs(sv, 2) == 0 and y.subs(sv, 2) == Q(8, 5) and x.subs(sv, 1) == Q(2, 3) and y.subs(sv, 1) == Q(2, 5)
    # tangent from the apex (0,-4/5): s^2 + 2s - 2 = 0  ->  s = sqrt3 - 1
    tang = simplify(x * sp.diff(y, sv) - (y + Q(4, 5)) * sp.diff(x, sv))
    roots = sp.solve(tang, sv)
    ok = ok and any(simplify(r - (sqrt(3) - 1)) == 0 for r in roots)
    # the diagonal ray meets Gamma at s = 5/4: (5/8, 5/8); eta2 = 1 is met at s = sqrt(5/2): eta1 = (2/3)sqrt(5/2)(2-sqrt(5/2))
    ok = ok and x.subs(sv, Q(5, 4)) == Q(5, 8) and y.subs(sv, Q(5, 4)) == Q(5, 8)
    e1 = simplify(x.subs(sv, sqrt(Q(5, 2))))
    ok = ok and simplify(e1 - (Q(2, 3) * sqrt(10) - Q(5, 3))) == 0
    # axis eta1 = 0: (3/5) Tr(A A') with A = 2nn^T - 2/3, A' = 2mm^T - 2/3 equals (3/5)(4 (n.m)^2 - 4/3) in [-4/5, 8/5]
    mu = symbols('mu', real=True)
    n = Matrix([1, 0, 0]); mvec = Matrix([mu, sqrt(1 - mu ** 2), 0])
    A = 2 * n * n.T - Q(2, 3) * eye(3); Ap = 2 * mvec * mvec.T - Q(2, 3) * eye(3)
    val = simplify(Q(3, 5) * (A * Ap).trace())
    ok = ok and simplify(val - Q(3, 5) * (4 * mu ** 2 - Q(4, 3))) == 0
    return {'ok': bool(ok), 'detail': 'AM-GM step (Z3, unsat); stationary value 2a^2/(9(a/3-b/5)); Gamma convex (x\'y\'\'-y\'x\'\' = 16/15); '
            'tangent at s = sqrt3-1; diagonal point (5/8,5/8); eta2 = 1 at eta1 = %s; axis range [-4/5, 8/5]' % e1}

def cert_gauss_nodes():
    """xi_n: largest Gauss-Legendre node (n even) or largest free Gauss-Radau node (n odd); extremal polynomials attain it."""
    x = symbols('x', real=True)
    ok = True; vals = {}
    # n = 1 (j = 1/2): Radau nodes -1, 1/3 ; extremal F = 1 + x
    F = 1 + x; r = sp.integrate(x * F, (x, -1, 1)) / sp.integrate(F, (x, -1, 1)); ok = ok and r == Q(1, 3); vals[1] = r
    # n = 2 (j = 1): zeros of P_2 ; extremal F = (x + 1/sqrt3)^2
    z = max(sp.solve(sp.legendre(2, x), x)); F = (x + z) ** 2
    r = simplify(sp.integrate(x * F, (x, -1, 1)) / sp.integrate(F, (x, -1, 1))); ok = ok and simplify(r - 1 / sqrt(3)) == 0; vals[2] = r
    # n = 3 (j = 3/2): free Radau nodes = zeros of P_2^{(0,1)} ~ 5x^2 - 2x - 1 ; extremal F = (1+x)(x - x_small)^2
    zs = sp.solve(sp.jacobi(2, 0, 1, x), x); zs = sorted(zs, key=lambda e: float(e))
    ok = ok and simplify(zs[1] - (1 + sqrt(6)) / 5) == 0
    F = (1 + x) * (x - zs[0]) ** 2
    r = simplify(sp.integrate(x * F, (x, -1, 1)) / sp.integrate(F, (x, -1, 1))); ok = ok and simplify(r - zs[1]) == 0; vals[3] = zs[1]
    # n = 4 (j = 2): zeros of P_3: 0, +-sqrt(3/5) ; extremal F = x^2 (x + sqrt(3/5))^2
    z = sqrt(Q(3, 5)); F = x ** 2 * (x + z) ** 2
    r = simplify(sp.integrate(x * F, (x, -1, 1)) / sp.integrate(F, (x, -1, 1))); ok = ok and simplify(r - z) == 0; vals[4] = z
    # j = 1 attaining kernel: eta = (1/sqrt3, 1/5): w0 = 4/15, w+- = 11/30 +- 1/(2 sqrt3) > 0
    w0 = (1 - Q(1, 5)) / 3; wp = (1 - w0) / 2 + 1 / (2 * sqrt(3)); wm = (1 - w0) / 2 - 1 / (2 * sqrt(3))
    ok = ok and w0 == Q(4, 15) and float(wm) > 0 and simplify(wp + wm + w0 - 1) == 0
    return {'ok': bool(ok), 'detail': 'xi_1 = 1/3, xi_2 = 1/sqrt3, xi_3 = (1+sqrt6)/5, xi_4 = sqrt(3/5); extremal polynomials attain them; '
            'j=1 kernel w = (%.4f, %.4f, %.4f)' % (float(wp), float(w0), float(wm))}

