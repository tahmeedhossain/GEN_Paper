"""Exact (symbolic or exact-arithmetic) certificates.  Each function returns a dict
{'ok': bool, 'detail': str, ...}.  SymPy only; no floating point enters a pass/fail decision
unless stated in the detail string."""
import sympy as sp
from sympy import Rational as Q, sqrt, I, pi, symbols, Matrix, eye, zeros, simplify, expand, integrate, diag

# ---------------------------------------------------------------- Dirac algebra (explicit matrices)
def _gammas():
    s0 = eye(2); sx = Matrix([[0, 1], [1, 0]]); sy = Matrix([[0, -I], [I, 0]]); sz = Matrix([[1, 0], [0, -1]])
    def blk(a, b, c, d): return Matrix(sp.BlockMatrix([[a, b], [c, d]]))
    g0 = blk(s0, zeros(2), zeros(2), -s0)
    g = [g0] + [blk(zeros(2), s, -s, zeros(2)) for s in (sx, sy, sz)]
    g5 = I * g[0] * g[1] * g[2] * g[3]
    return g, g5
_ETA = diag(1, -1, -1, -1)
def _slash(p, g): return sum((_ETA[m, m] * p[m] * g[m] for m in range(4)), zeros(4))
def _dot(a, b): return sum(_ETA[m, m] * a[m] * b[m] for m in range(4))

def cert_va_trace():
    """Sum over final spins of |[ubar(p2) g^mu P_L u(p1,s)][ubar(p3) g_mu P_L v(p4)]|^2 for massless 2,3,4,
    with the spin density factor (pslash1+m)(1+g5 sslash)/2 of the parent, equals 8 ((p1 - m s).p4)(p2.p3)
    as a polynomial identity in arbitrary four-vectors (no on-shell condition is used)."""
    g, g5 = _gammas(); PL = (eye(4) - g5) / 2; PR = (eye(4) + g5) / 2
    p1 = symbols('p1_0:4', real=True); p2 = symbols('p2_0:4', real=True)
    p3 = symbols('p3_0:4', real=True); p4 = symbols('p4_0:4', real=True); s = symbols('s_0:4', real=True)
    m = symbols('m', positive=True)
    rho1 = (_slash(p1, g) + m * eye(4)) * (eye(4) + g5 * _slash(s, g)) / 2
    lhs = 0
    for mu in range(4):
        for nu in range(4):
            A = (_slash(p2, g) * g[mu] * PL * rho1 * PR * g[nu]).trace()
            B = (_slash(p3, g) * (_ETA[mu, mu] * g[mu]) * PL * _slash(p4, g) * PR * (_ETA[nu, nu] * g[nu])).trace()
            lhs += A * B
    a = [p1[k] - m * s[k] for k in range(4)]
    rhs = 8 * _dot(a, p4) * _dot(p2, p3)
    ok = expand(lhs - rhs) == 0
    return {'ok': bool(ok), 'detail': 'polynomial identity in 20 real symbols: sum |M|^2 = 8 ((p1-m s).p4)(p2.p3)'}

def cert_rank_one_effect():
    """In the parent rest frame (p1-m s).p4 = m E4 (1 + s.q4): the recorded direction of particle 4
    defines the rank-one covariant effect (1+q.sigma)/4pi, analysing power +1, for every value of the other variables."""
    m, E = symbols('m E', positive=True); sx, sy, sz, qx, qy, qz = symbols('s_x s_y s_z q_x q_y q_z', real=True)
    p1 = (m, 0, 0, 0); s = (0, sx, sy, sz); p4 = (E, E * qx, E * qy, E * qz)
    val = expand(_dot([p1[k] - m * s[k] for k in range(4)], p4))
    ok = simplify(val - m * E * (1 + sx * qx + sy * qy + sz * qz)) == 0
    # Tr[(1+s.sigma)/2 (1+q.sigma)] = 1 + s.q
    S = [Matrix([[0, 1], [1, 0]]), Matrix([[0, -I], [I, 0]]), Matrix([[1, 0], [0, -1]])]
    rho = (eye(2) + sx * S[0] + sy * S[1] + sz * S[2]) / 2
    Eff = eye(2) + qx * S[0] + qy * S[1] + qz * S[2]
    ok2 = simplify((rho * Eff).trace() - (1 + sx * qx + sy * qy + sz * qz)) == 0
    det = simplify(Eff.det().subs(qz ** 2, 1 - qx ** 2 - qy ** 2))
    return {'ok': bool(ok and ok2 and det == 0), 'detail': '(p1-ms).p4 = m E (1+s.q); effect 1+q.sigma has determinant 0 on |q|=1'}

def _two_body_tensor():
    """int q'^a q^b dLIPS_2(Q;q,q') = (V2/12)(Q^2 g^{ab} + 2 Q^a Q^b) for massless q,q':
    solve the two contractions for the coefficients."""
    A, B, V2, Q2 = symbols('A B V2 Q2', positive=True)
    sol = sp.solve([4 * A + B - Q(1, 2) * V2, A + B - Q(1, 4) * V2], [A, B], dict=True)[0]
    return sol[A] / V2, sol[B] / V2          # coefficients of Q^2 g and of QQ, in units of V2

def cert_leptonic_spectrum():
    """Three-body V-A decay with the direction and energy of fermion 3 recorded (e.g. the electron in
    mu- -> nu_mu e- nubar_e): spectrum x^2[(3-2x) - (2x-1) s.q]; energy-integrated analysing power -1/3."""
    cA, cB = _two_body_tensor()
    ok0 = (cA == Q(1, 12)) and (cB == Q(1, 6))
    m, x, c = symbols('m x c', real=True)
    E = m * x / 2
    # a = p1 - m s, k = p3 (recorded), Q = p1 - k ; contraction a_alpha k_beta I^{alpha beta}
    a_k = m * E * (1 + c); Q2 = m ** 2 - 2 * m * E
    a_Q = m ** 2 - m * E - m * E * c; k_Q = m * E
    contr = expand(cA * a_k * Q2 + cB * a_Q * k_Q)
    spec = sp.factor(contr * E)              # phase-space factor E dE dOmega
    target = x ** 2 * ((3 - 2 * x) + c * (1 - 2 * x))
    ratio = simplify(spec / target)
    ok1 = ratio.free_symbols <= {m}
    num = integrate(x ** 2 * (1 - 2 * x), (x, 0, 1)); den = integrate(x ** 2 * (3 - 2 * x), (x, 0, 1))
    kappa = num / den
    x0 = symbols('x0', positive=True)
    kx0 = simplify(integrate(x ** 2 * (2 * x - 1), (x, x0, 1)) / integrate(x ** 2 * (3 - 2 * x), (x, x0, 1)))
    amax = sp.limit((2 * x - 1) / (3 - 2 * x), x, 1)
    return {'ok': bool(ok0 and ok1 and kappa == Q(-1, 3) and amax == 1),
            'detail': 'tensor coefficients 1/12, 1/6; spectrum x^2[(3-2x)-(2x-1)cos]; integrated analysing power = %s; '
                      'endpoint analysing power = %s; with cut x>x0: |kappa|(x0) = %s' % (kappa, amax, sp.factor(kx0)),
            'kappa_cut': str(sp.factor(kx0))}

def cert_top_b_power():
    """t -> b W(-> l nu), narrow width, m_b = 0, b direction recorded: kappa_b = -(xi-2)/(xi+2), xi = m_t^2/m_W^2;
    |kappa_b| > 1/3  <=>  m_t > 2 m_W."""
    cA, cB = _two_body_tensor()
    m, mW, c = symbols('m m_W c', positive=True)
    Eb = (m ** 2 - mW ** 2) / (2 * m)
    b_a = m * Eb * (1 + c); Q2 = mW ** 2; b_Q = m * Eb; a_Q = m ** 2 - m * Eb * (1 + c)
    contr = expand(cA * b_a * Q2 + cB * b_Q * a_Q)
    const = contr.subs(c, 0); lin = sp.diff(contr, c)
    kb = simplify(lin / const)
    xi = symbols('xi', positive=True)
    ok = simplify(kb.subs(m, mW * sqrt(xi)) + (xi - 2) / (xi + 2)) == 0
    thr = sp.solve(sp.Eq((xi - 2) / (xi + 2), Q(1, 3)), xi)
    return {'ok': bool(ok and thr == [4]), 'detail': 'kappa_b = -(xi-2)/(xi+2); equals -1/3 at xi = %s, i.e. m_t = 2 m_W' % thr}

# ---------------------------------------------------------------- spin 1/2
def cert_spin_half_model():
    """Four-state model for a ball of data Bloch vectors of radius 1/3 with all sharp effects:
    mu(j|v) = (1+3 t_j.v)/4, xi(q|j) = (1+q.t_j)/4pi, t_j tetrahedron vertices."""
    t = [Matrix([1, 1, 1]) / sqrt(3), Matrix([1, -1, -1]) / sqrt(3), Matrix([-1, 1, -1]) / sqrt(3), Matrix([-1, -1, 1]) / sqrt(3)]
    v = Matrix(symbols('v1:4', real=True)); q = Matrix(symbols('q1:4', real=True))
    tot = sum(Q(1, 4) * (1 + 3 * t[j].dot(v)) * (1 + q.dot(t[j])) for j in range(4))
    ok1 = simplify(tot - (1 + v.dot(q))) == 0
    ok2 = sum(t, zeros(3, 1)) == zeros(3, 1) and simplify(sum((tj * tj.T for tj in t), zeros(3)) - Q(4, 3) * eye(3)) == zeros(3)
    # positivity: min of 1 + 3 t.v on |v| = r is 1 - 3r ; min of 1 + q.t on |q| = 1 is 0
    return {'ok': bool(ok1 and ok2), 'detail': 'sum_j mu xi = (1+v.q)/4pi; mu >= 0 iff |v| <= 1/3; four ontic states'}

def cert_spin_half_necessity():
    """Necessity of |v| <= 1/3 (rho := |kappa| P): from id = sum_j sigma_j (x) g_j,
    3 = sum_j s_j.g_j <= sum_j |g_j| <= (1/rho) sum_j g_j0 = 1/rho.   Checked as an implication with Z3
    for the scalar chain; the vector inequalities are Cauchy-Schwarz."""
    import z3
    rho, S, Gsum, G0 = z3.Reals('rho S Gsum G0')
    solver = z3.Solver()
    # premises: S = 3 (trace of the 3x3 block), S <= Gsum (|s_j| <= 1 and Cauchy-Schwarz), Gsum <= G0/rho, G0 = 1, rho > 0
    solver.add(S == 3, S <= Gsum, Gsum * rho <= G0, G0 == 1, rho > 0)
    solver.add(z3.Not(rho <= z3.Q(1, 3)))
    unsat = solver.check() == z3.unsat
    # each premise needed
    need = []
    prem = [S == 3, S <= Gsum, Gsum * rho <= G0, G0 == 1]
    for i in range(len(prem)):
        s2 = z3.Solver(); s2.add(rho > 0, *[p for k, p in enumerate(prem) if k != i]); s2.add(z3.Not(rho <= z3.Q(1, 3)))
        need.append(s2.check() == z3.sat)
    return {'ok': bool(unsat and all(need)), 'detail': 'premises entail rho <= 1/3 (unsat); each premise needed: %s' % need}

# ---------------------------------------------------------------- two spin-1/2 particles
def _paulis():
    return [eye(2), Matrix([[0, 1], [1, 0]]), Matrix([[0, -I], [I, 0]]), Matrix([[1, 0], [0, -1]])]
def _kron(a, b): return sp.kronecker_product(a, b)

def cert_tstate():
    """T-states with diagonal raw correlation c = diag(c1,c2,c3):
    (i) eigenvalues of rho_raw and of its partial transpose;  both PSD  <=>  |c1|+|c2|+|c3| <= 1;
    (ii) explicit model: 1 + x y = (1/2)(1+x)(1+y) + (1/2)(1-x)(1-y)."""
    c1, c2, c3 = symbols('c1 c2 c3', real=True); P = _paulis()
    rho = (eye(4) + c1 * _kron(P[1], P[1]) + c2 * _kron(P[2], P[2]) + c3 * _kron(P[3], P[3])) / 4
    ev = sorted([sp.expand(4 * e) for e in rho.eigenvals(multiple=True)], key=str)
    target = sorted([1 - c1 - c2 - c3, 1 - c1 + c2 + c3, 1 + c1 - c2 + c3, 1 + c1 + c2 - c3], key=str)
    ok1 = ev == target
    pt = (eye(4) + c1 * _kron(P[1], P[1]) - c2 * _kron(P[2], P[2]) + c3 * _kron(P[3], P[3])) / 4   # transpose flips sigma_y
    ev2 = sorted([sp.expand(4 * e) for e in pt.eigenvals(multiple=True)], key=str)
    target2 = sorted([1 - c1 + c2 - c3, 1 - c1 - c2 + c3, 1 + c1 + c2 + c3, 1 + c1 - c2 - c3], key=str)
    ok2 = ev2 == target2
    # the eight linear forms 1 +- c1 +- c2 +- c3 are all >= 0 iff |c1|+|c2|+|c3| <= 1  (checked with Z3)
    import z3
    a, b, c = z3.Reals('a b c')
    forms = [1 + s1 * a + s2 * b + s3 * c for s1 in (1, -1) for s2 in (1, -1) for s3 in (1, -1)]
    absum = z3.If(a >= 0, a, -a) + z3.If(b >= 0, b, -b) + z3.If(c >= 0, c, -c)
    s = z3.Solver(); s.add(z3.Not(z3.And(*[f >= 0 for f in forms]) == (absum <= 1)))
    ok3 = s.check() == z3.unsat
    x, y = symbols('x y', real=True)
    ok4 = expand(Q(1, 2) * (1 + x) * (1 + y) + Q(1, 2) * (1 - x) * (1 - y) - (1 + x * y)) == 0
    return {'ok': bool(ok1 and ok2 and ok3 and ok4),
            'detail': 'spectra of rho_raw and its partial transpose are the eight forms (1+-c1+-c2+-c3)/4; all >= 0 iff |c1|+|c2|+|c3| <= 1; product-form identity for the explicit model'}

def cert_raw_operator():
    """rho_raw = (D_kA (x) D_kB)(rho) on Bloch coefficients; for a negative analysing power the map is
    the universal NOT composed with a depolarising map, and  rho_raw = (sy (x) 1) [ (D_|kA| (x) D_|kB|) rho ]^{T_A} (sy (x) 1)
    when kA < 0 < kB.  Hence {rho_raw >= 0 and rho_raw^{T_A} >= 0}  <=>  (D_|kA| (x) D_|kB|) rho is PPT."""
    P = _paulis()
    R = sp.Matrix(4, 4, lambda m, n: symbols('r%d%d' % (m, n), real=True)); R[0, 0] = 1
    kA, kB = symbols('kA kB', positive=True)
    def rho_of(Rm): return sum((Rm[m, n] * _kron(P[m], P[n]) for m in range(4) for n in range(4)), zeros(4)) / 4
    def scale(Rm, a, b): return diag(1, a, a, a) * Rm * diag(1, b, b, b)
    raw = rho_of(scale(R, -kA, kB)); pos = rho_of(scale(R, kA, kB))
    def pT_A(M):
        out = zeros(4)
        for i in range(2):
            for j in range(2):
                for k in range(2):
                    for l in range(2):
                        out[2 * i + j, 2 * k + l] = M[2 * k + j, 2 * i + l]
        return out
    sy1 = _kron(P[2], P[0])
    ok = simplify(raw - sy1 * pT_A(pos) * sy1) == zeros(4)
    return {'ok': bool(ok), 'detail': 'sign flip of one analysing power = partial transpose up to a local unitary'}

def cert_trace_witness():
    """<Phi+| X^{T_B} |Phi+> = (1 + tr c)/4 and <Psi-| X |Psi-> = (1 - tr c)/4 for X = rho_raw:
    both PSD conditions give |tr c| <= 1, i.e. |D_raw| <= 1/3 with D_raw = -tr(c)/3."""
    P = _paulis()
    R = sp.Matrix(4, 4, lambda m, n: symbols('r%d%d' % (m, n), real=True)); R[0, 0] = 1
    X = sum((R[m, n] * _kron(P[m], P[n]) for m in range(4) for n in range(4)), zeros(4)) / 4
    def pT_B(M):
        out = zeros(4)
        for i in range(2):
            for j in range(2):
                for k in range(2):
                    for l in range(2):
                        out[2 * i + j, 2 * k + l] = M[2 * i + l, 2 * k + j]
        return out
    phi = Matrix([1, 0, 0, 1]) / sqrt(2); psi = Matrix([0, 1, -1, 0]) / sqrt(2)
    trc = R[1, 1] + R[2, 2] + R[3, 3]
    v1 = simplify((phi.T * pT_B(X) * phi)[0] - (1 + trc) / 4)
    v2 = simplify((psi.T * X * psi)[0] - (1 - trc) / 4)
    return {'ok': bool(v1 == 0 and v2 == 0), 'detail': 'PSD of rho_raw and of its partial transpose imply -1 <= tr c <= 1'}

