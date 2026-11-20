"""
Paper C.  ATLAS Collaboration,
"Observation of quantum entanglement with top quarks at the ATLAS detector",
Nature 633, 542-547 (2024); arXiv:2311.07288.

Encoded against two released networks at once:
  GEN_HEP v1.2 (Standard-Model graph): m_cc (charged-current gauge vertex), m_A (observable
      postulate / Born rule), s_W, lepton sectors;
  GEN_GPT_Level v2.6 / GEN_QRT_Level v1.2: s-sep / sF-ent, s-ent / sR-ent, w-entw / wD-ent.

Dirac algebra conventions in the certificates
  metric (+,-,-,-); Dirac representation; gamma5 = i g0 g1 g2 g3; P_L = (1 - gamma5)/2;
  spin projectors  u ubar = (pslash + m)(1 + gamma5 sslash)/2,
                   v vbar = (pslash - m)(1 + gamma5 sslash)/2,   s.p = 0, s^2 = -1.
"""
from itertools import product

import sympy as sp
import z3

from kernel import CertResult, Claim, Edge, Node, Paper, smt_entails

I = sp.I
s0 = sp.eye(2)
SIG = [sp.Matrix([[0, 1], [1, 0]]), sp.Matrix([[0, -I], [I, 0]]), sp.Matrix([[1, 0], [0, -1]])]
Z2 = sp.zeros(2)


def blk(a, b, c, d):
    return sp.Matrix(sp.BlockMatrix([[a, b], [c, d]]))


G = [blk(s0, Z2, Z2, -s0)] + [blk(Z2, s, -s, Z2) for s in SIG]
G5 = I * G[0] * G[1] * G[2] * G[3]
E4 = sp.eye(4)
PL, PR = (E4 - G5) / 2, (E4 + G5) / 2
METRIC = [1, -1, -1, -1]


def slash(p):
    return sum((METRIC[mu] * p[mu] * G[mu] for mu in range(4)), sp.zeros(4))


def dot(a, b):
    return sum(METRIC[mu] * a[mu] * b[mu] for mu in range(4))


def vec4(name):
    return sp.Matrix(sp.symbols(f"{name}0:4", real=True))


def zero(M):
    return all(sp.simplify(x) == 0 for x in M)


# ----------------------------------------------------------------------------
# certificates
# ----------------------------------------------------------------------------

def _rho(Bp, Bm, C):
    rho = sp.eye(4)
    for i in range(3):
        rho += Bp[i] * sp.kronecker_product(SIG[i], s0) + Bm[i] * sp.kronecker_product(s0, SIG[i])
        for j in range(3):
            rho += C[i, j] * sp.kronecker_product(SIG[i], SIG[j])
    return rho / 4


def cert_TQ1():
    """Pauli parametrisation of a two-qubit state."""
    Bp = sp.Matrix(sp.symbols("Bp0:3", real=True))
    Bm = sp.Matrix(sp.symbols("Bm0:3", real=True))
    C = sp.Matrix(3, 3, sp.symbols("C0:9", real=True))
    rho = _rho(Bp, Bm, C)
    c = {"tr ρ = 1": sp.simplify(rho.trace() - 1) == 0, "ρ = ρ†": zero(rho - rho.H)}
    c["tr[ρ σ_i⊗1] = B+_i, tr[ρ 1⊗σ_i] = B−_i"] = all(
        sp.simplify((rho * sp.kronecker_product(SIG[i], s0)).trace() - Bp[i]) == 0 and
        sp.simplify((rho * sp.kronecker_product(s0, SIG[i])).trace() - Bm[i]) == 0 for i in range(3))
    c["tr[ρ σ_i⊗σ_j] = C_ij"] = all(
        sp.simplify((rho * sp.kronecker_product(SIG[i], SIG[j])).trace() - C[i, j]) == 0
        for i in range(3) for j in range(3))
    # the 16 products of {1, σ_i} are a basis of the 4x4 matrices
    basis = [sp.kronecker_product(a, b) for a in [s0] + SIG for b in [s0] + SIG]
    c["{1,σ}⊗{1,σ} is a basis of M_4(C)"] = sp.Matrix([list(m) for m in basis]).rank() == 16
    ok = all(c.values())
    return CertResult(ok, "exact: the 15 real coefficients (B+, B−, C) are the Pauli expectation values and determine ρ"
                      if ok else "FAILED", {"checks": c})


def _traces(kind, quark_chirality="L"):
    """Spin-summed squared amplitude. quark_chirality = "R" plants an error (used by controls.py)."""
    pb, pn, pl, pt, s = (vec4(n) for n in ("pb", "pn", "pl", "pt", "s"))
    m, mb = sp.symbols("m mb", real=True)
    total = 0
    if kind == "top":            # t(pt, s) -> b(pb) l+(pl) nu(pn)
        U = (slash(pt) + m * E4) * (E4 + G5 * slash(s)) / 2
        Pq, Pq_bar = (PL, PR) if quark_chirality == "L" else (PR, PL)
        left = [(slash(pb) + mb * E4) * G[mu] * Pq * U * Pq_bar for mu in range(4)]
        lepL = [slash(pn) * G[mu] * PL * slash(pl) * PR for mu in range(4)]
    else:                        # tbar(pt, s) -> bbar(pb) l-(pl) nubar(pn)
        V = (slash(pt) - m * E4) * (E4 + G5 * slash(s)) / 2
        left = [V * G[mu] * PL * (slash(pb) - mb * E4) * PR for mu in range(4)]
        lepL = [slash(pl) * G[mu] * PL * slash(pn) * PR for mu in range(4)]
    for mu in range(4):
        for nu in range(4):
            H = (left[mu] * G[nu]).trace()
            L = (lepL[mu] * G[nu]).trace()
            total += METRIC[mu] * METRIC[nu] * H * L
    return sp.expand(total), (pb, pn, pl, pt, s, m, mb)


def _decay_cert(kind, quark_chirality="L"):
    W, (pb, pn, pl, pt, s, m, mb) = _traces(kind, quark_chirality)
    sign = -1 if kind == "top" else +1
    P = pt + sign * m * s                       # top: p_t - m s ; antitop: p_t + m s
    form = sp.expand(dot(pb, pn) * dot(P, pl))
    # fix the constant at one integer point, then demand a polynomial identity
    pt_vals = {}
    vals = iter([3, 1, -2, 5, 2, -1, 4, 1, 7, 2, 3, -5, 1, 6, -2, 3, 2, 1, -4, 5, 3, 2])
    for v in list(pb) + list(pn) + list(pl) + list(pt) + list(s) + [m, mb]:
        pt_vals[v] = next(vals)
    k = sp.nsimplify(W.subs(pt_vals) / form.subs(pt_vals))
    identity = sp.expand(W - k * form) == 0
    no_mb = sp.diff(W, mb) == 0
    # rest frame of the decaying quark
    E, sx, sy, sz, qx, qy, qz = sp.symbols("E s_x s_y s_z q_x q_y q_z", real=True)
    rest = dot(sp.Matrix([m, 0, 0, 0]) + sign * m * sp.Matrix([0, sx, sy, sz]), sp.Matrix([E, E * qx, E * qy, E * qz]))
    kappa = -sign
    rest_ok = sp.expand(rest - m * E * (1 + kappa * (sx * qx + sy * qy + sz * qz))) == 0
    return W, k, identity, no_mb, rest_ok, kappa


def cert_TQ2():
    """V-A charged current => lepton analysing power +1 in top decay."""
    conv = {
        "γ5 = iγ0γ1γ2γ3 is [[0,1],[1,0]] in the Dirac representation": zero(G5 - blk(Z2, s0, s0, Z2)),
        "{γμ, γν} = 2 g_μν": all(zero(G[a] * G[b] + G[b] * G[a] - 2 * (METRIC[a] if a == b else 0) * E4)
                                for a in range(4) for b in range(4)),
    }
    # anchor of the spin convention: top at rest, s = +z  ->  2m |up><up|
    m = sp.Symbol("m", positive=True)
    U = (slash(sp.Matrix([m, 0, 0, 0])) + m * E4) * (E4 + G5 * slash(sp.Matrix([0, 0, 0, 1]))) / 2
    conv["u ubar at rest with s = +z equals 2m·diag(1,0,0,0)"] = zero(U - 2 * m * sp.diag(1, 0, 0, 0))
    W, k, identity, no_mb, rest_ok, kappa = _decay_cert("top")
    ok = all(conv.values()) and identity and no_mb and rest_ok and kappa == 1
    return CertResult(ok, f"exact polynomial identity in all 20 momentum and spin components, m and m_b: "
                      f"Σ|M|² = {k}·(p_b·p_ν)·((p_t − m s)·p_ℓ), independent of m_b; in the top rest frame "
                      f"(p_t − m s)·p_ℓ = m E_ℓ (1 + ŝ·q̂): analysing power κ = +1" if ok else "FAILED",
                      {"conventions": conv, "constant": str(k), "polynomial identity": identity,
                       "independent of m_b": no_mb, "rest-frame form": rest_ok,
                       "reading": "p_b·p_ν = ((p_t − p_ℓ)² − m_b²)/2 depends on the lepton only through its energy, "
                                  "and the W propagator integrates to a function of E_ℓ; the spin enters only "
                                  "through the factor (1 + ŝ·q̂)"},
                      scope="general (tree level, massless lepton and neutrino; no on-shell condition is used)")


def cert_TQ3():
    """Antitop decay: analysing power -1."""
    m = sp.Symbol("m", positive=True)
    V = (slash(sp.Matrix([m, 0, 0, 0])) - m * E4) * (E4 + G5 * slash(sp.Matrix([0, 0, 0, 1]))) / 2
    anchor = zero(V + 2 * m * sp.diag(0, 0, 0, 1))
    W, k, identity, no_mb, rest_ok, kappa = _decay_cert("antitop")
    ok = anchor and identity and no_mb and rest_ok and kappa == -1
    return CertResult(ok, f"exact polynomial identity: Σ|M|² = {k}·(p_b̄·p_ν̄)·((p_t̄ + m s)·p_ℓ); in the antitop rest "
                      f"frame (p_t̄ + m s)·p_ℓ = m E_ℓ (1 − ŝ·q̂): analysing power κ = −1" if ok else "FAILED",
                      {"constant": str(k), "polynomial identity": identity, "independent of m_b": no_mb,
                       "rest-frame form": rest_ok,
                       "v vbar at rest with s = +z equals −2m·diag(0,0,0,1) (antiquark with spin +z)": anchor},
                      scope="general (tree level, massless lepton and neutrino)")


def cert_TQ4():
    """The decay as a measurement of the spin: effects (1 ± q·σ)/4π."""
    th, ph = sp.symbols("theta phi", real=True)
    chi = sp.Matrix([sp.cos(th / 2), sp.exp(I * ph) * sp.sin(th / 2)])
    shat = sp.Matrix([sp.sin(th) * sp.cos(ph), sp.sin(th) * sp.sin(ph), sp.cos(th)])
    q = sp.Matrix(sp.symbols("q_x q_y q_z", real=True))
    qs = sum((q[i] * SIG[i] for i in range(3)), sp.zeros(2))
    c = {}
    c["<χ|σ|χ> = ŝ"] = all(sp.simplify(sp.expand_complex((chi.H * SIG[i] * chi)[0]) - shat[i]) == 0 for i in range(3))
    c["<χ|(1 ± q·σ)|χ> = 1 ± ŝ·q̂"] = all(
        sp.simplify(sp.expand_complex((chi.H * (s0 + sg * qs) * chi)[0]) - (1 + sg * shat.dot(q))) == 0 for sg in (1, -1))
    # a Hermitian 2x2 operator is fixed by its expectation values on pure states
    x0, x1, x2, x3 = sp.symbols("x0:4", real=True)
    Xop = x0 * s0 + x1 * SIG[0] + x2 * SIG[1] + x3 * SIG[2]
    states = [sp.Matrix([1, 0]), sp.Matrix([0, 1]), sp.Matrix([1, 1]) / sp.sqrt(2), sp.Matrix([1, I]) / sp.sqrt(2)]
    eqs = [sp.simplify((v.H * Xop * v)[0]) for v in states]
    sol = sp.solve(eqs, [x0, x1, x2, x3], dict=True)
    c["zero expectation on |0>, |1>, |+>, |+i> forces X = 0"] = sol == [{x0: 0, x1: 0, x2: 0, x3: 0}]
    # normalisation of the POVM over the sphere
    a, b = sp.symbols("a b", real=True)
    qhat = [sp.sin(a) * sp.cos(b), sp.sin(a) * sp.sin(b), sp.cos(a)]
    Eop = (s0 + sum((qhat[i] * SIG[i] for i in range(3)), sp.zeros(2))) / (4 * sp.pi)
    integ = Eop.applyfunc(lambda x: sp.integrate(sp.integrate(x * sp.sin(a), (b, 0, 2 * sp.pi)), (a, 0, sp.pi)))
    c["∫dΩ (1 + q̂·σ)/4π = 1"] = zero(integ - s0)
    ok = all(c.values())
    return CertResult(ok, "exact: the unique Hermitian operators with expectation (1 ± ŝ·q̂)/4π on every pure spin "
                      "state are (1 ± q̂·σ)/4π; they integrate to the identity over the sphere" if ok else "FAILED",
                      {"checks": c})


def cert_TQ5():
    """Joint lepton distribution from the spin density matrix."""
    Bp = sp.Matrix(sp.symbols("Bp0:3", real=True))
    Bm = sp.Matrix(sp.symbols("Bm0:3", real=True))
    C = sp.Matrix(3, 3, sp.symbols("C0:9", real=True))
    qp = sp.Matrix(sp.symbols("qp0:3", real=True))
    qm = sp.Matrix(sp.symbols("qm0:3", real=True))
    rho = _rho(Bp, Bm, C)
    Ep = s0 + sum((qp[i] * SIG[i] for i in range(3)), sp.zeros(2))
    Em = s0 - sum((qm[i] * SIG[i] for i in range(3)), sp.zeros(2))
    lhs = sp.expand((rho * sp.kronecker_product(Ep, Em)).trace())
    rhs = sp.expand(1 + Bp.dot(qp) - Bm.dot(qm) - (qp.T * C * qm)[0])
    ok = sp.simplify(lhs - rhs) == 0
    return CertResult(ok, "exact: tr[ρ (1 + q̂+·σ)⊗(1 − q̂−·σ)] = 1 + B+·q̂+ − B−·q̂− − q̂+·C·q̂− "
                      "(divide by (4π)² for the density)" if ok else "FAILED", {"identity": ok})


def cert_TQ6():
    """cos φ distribution and the estimator D = -3 <cos φ>."""
    th, al, ph, be = sp.symbols("theta alpha varphi beta", real=True)
    qp = sp.Matrix([sp.sin(th) * sp.cos(al), sp.sin(th) * sp.sin(al), sp.cos(th)])
    e1 = sp.Matrix([sp.cos(th) * sp.cos(al), sp.cos(th) * sp.sin(al), -sp.sin(th)])
    e2 = sp.Matrix([-sp.sin(al), sp.cos(al), 0])
    qm = sp.cos(ph) * qp + sp.sin(ph) * (sp.cos(be) * e1 + sp.sin(be) * e2)
    frame = (sp.simplify(qp.dot(qp)) == 1 and sp.simplify(e1.dot(e1)) == 1 and sp.simplify(e2.dot(e2)) == 1
             and sp.simplify(qp.dot(e1)) == 0 and sp.simplify(qp.dot(e2)) == 0 and sp.simplify(e1.dot(e2)) == 0
             and sp.simplify(qm.dot(qm)) == 1 and sp.simplify(qp.dot(qm) - sp.cos(ph)) == 0)
    Bp = sp.Matrix(sp.symbols("Bp0:3", real=True))
    Bm = sp.Matrix(sp.symbols("Bm0:3", real=True))
    C = sp.Matrix(3, 3, sp.symbols("C0:9", real=True))
    f = sp.expand(1 + Bp.dot(qp) - Bm.dot(qm) - (qp.T * C * qm)[0])
    # average over q+ (uniform on the sphere) and over the azimuth β of q- around q+, at fixed φ
    g = sp.integrate(sp.expand(f), (be, 0, 2 * sp.pi)) / (2 * sp.pi)
    g = sp.integrate(sp.expand(g), (al, 0, 2 * sp.pi))
    g = sp.integrate(sp.expand(g * sp.sin(th)), (th, 0, sp.pi)) / (4 * sp.pi)
    trC = C[0, 0] + C[1, 1] + C[2, 2]
    avg_ok = sp.simplify(g - (1 - sp.cos(ph) * trC / 3)) == 0
    c, D = sp.symbols("c D", real=True)
    p = (1 - D * c) / 2
    norm = sp.integrate(p, (c, -1, 1)) == 1
    mean = sp.simplify(sp.integrate(c * p, (c, -1, 1)) + D / 3) == 0
    ok = frame and avg_ok and norm and mean
    return CertResult(ok, "exact integration: the density of cos φ is (1 − D cos φ)/2 with D = tr C/3 (B+ and B− "
                      "drop out), it is normalised, and <cos φ> = −D/3" if ok else "FAILED",
                      {"orthonormal frame and q̂+·q̂− = cos φ": frame, "angular average = 1 − (tr C/3) cos φ": avg_ok,
                       "normalisation": norm, "<cos φ> = −D/3": mean})


def cert_TQ7():
    """Separable states have tr C >= -1: sum-of-squares certificate and convexity."""
    a = sp.Matrix(sp.symbols("a0:3", real=True))
    b = sp.Matrix(sp.symbols("b0:3", real=True))
    ra = (s0 + sum((a[i] * SIG[i] for i in range(3)), sp.zeros(2))) / 2
    rb = (s0 + sum((b[i] * SIG[i] for i in range(3)), sp.zeros(2))) / 2
    prod_state = sp.kronecker_product(ra, rb)
    c = {}
    c["product state: C_ij = a_i b_j, so tr C = a·b"] = all(
        sp.simplify((prod_state * sp.kronecker_product(SIG[i], SIG[j])).trace() - a[i] * b[j]) == 0
        for i in range(3) for j in range(3))
    sos = (a + b).dot(a + b) + (1 - a.dot(a)) + (1 - b.dot(b))
    c["2(1 + a·b) = |a+b|² + (1−|a|²) + (1−|b|²)"] = sp.expand(2 * (1 + a.dot(b)) - sos) == 0
    p, t1, t2 = z3.Reals("p t1 t2")
    okc, info = smt_entails({"weights": z3.And(p >= 0, p <= 1), "t1 ≥ −1": t1 >= -1, "t2 ≥ −1": t2 >= -1},
                            p * t1 + (1 - p) * t2 >= -1)
    c["a mixture of two values ≥ −1 is ≥ −1 (induction step for finite mixtures)"] = okc
    # the bound is attained: the product state |up, down> has a = -b = z, tr C = -1
    updown = sp.kronecker_product(sp.Matrix([[1, 0], [0, 0]]), sp.Matrix([[0, 0], [0, 1]]))
    c["tight: the product state |↑↓> has tr C = −1"] = sum(
        (updown * sp.kronecker_product(SIG[i], SIG[i])).trace() for i in range(3)) == -1
    ok = all(c.values())
    return CertResult(ok, "exact: for Bloch vectors with |a|, |b| ≤ 1 the identity writes 2(1 + a·b) as a sum of "
                      "non-negative terms, so tr C = a·b ≥ −1 on product states; tr C is linear in ρ, so the bound "
                      "holds on the convex hull (separable states). Hence D ≥ −1/3" if ok else "FAILED",
                      {"checks": c, "smt": info},
                      scope="general (finite mixtures; limits of mixtures by continuity of the linear functional)")


def cert_TQ8():
    """Second route: the bound from the Peres-Horodecki criterion."""
    SW = sp.zeros(4, 4)
    for i, j in product(range(2), repeat=2):
        SW[j * 2 + i, i * 2 + j] = 1
    psim = sp.Matrix([0, 1, -1, 0]) / sp.sqrt(2)
    phip = sp.Matrix([1, 0, 0, 1]) / sp.sqrt(2)
    sumss = sum((sp.kronecker_product(s, s) for s in SIG), sp.zeros(4))

    def pt(M):       # partial transpose on the second qubit
        out = sp.zeros(4, 4)
        for i, j, k, l in product(range(2), repeat=4):
            out[i * 2 + l, k * 2 + j] = M[i * 2 + j, k * 2 + l]
        return out

    Bp = sp.Matrix(sp.symbols("Bp0:3", real=True))
    Bm = sp.Matrix(sp.symbols("Bm0:3", real=True))
    C = sp.Matrix(3, 3, sp.symbols("C0:9", real=True))
    rho = _rho(Bp, Bm, C)
    trC = C[0, 0] + C[1, 1] + C[2, 2]
    c = {
        "Σ_i σ_i⊗σ_i = 2·SWAP − 1 = 1 − 4|Ψ−><Ψ−|": zero(sumss - 2 * SW + sp.eye(4)) and zero(sumss - sp.eye(4) + 4 * psim * psim.T),
        "(|Φ+><Φ+|)^{T_B} = SWAP/2": zero(pt(phip * phip.T) - SW / 2),
        "<Φ+|ρ^{T_B}|Φ+> = (1 + tr C)/4": sp.simplify((phip.T * pt(rho) * phip)[0] - (1 + trC) / 4) == 0,
        "singlet fraction <Ψ−|ρ|Ψ−> = (1 − tr C)/4": sp.simplify((psim.T * rho * psim)[0] - (1 - trC) / 4) == 0,
    }
    # Peres: the partial transpose of a product state is a product state
    a = sp.Matrix(sp.symbols("a0:3", real=True))
    b = sp.Matrix(sp.symbols("b0:3", real=True))
    ra = (s0 + sum((a[i] * SIG[i] for i in range(3)), sp.zeros(2))) / 2
    rb = (s0 + sum((b[i] * SIG[i] for i in range(3)), sp.zeros(2))) / 2
    rbT = (s0 + b[0] * SIG[0] - b[1] * SIG[1] + b[2] * SIG[2]) / 2
    c["(ρ_a⊗ρ_b)^{T_B} = ρ_a⊗ρ_b' with b' = (b_x, −b_y, b_z), |b'| = |b|"] = zero(
        pt(sp.kronecker_product(ra, rb)) - sp.kronecker_product(ra, rbT))
    ok = all(c.values())
    return CertResult(ok, "exact: tr C + 1 < 0 is the statement <Φ+|ρ^{T_B}|Φ+> < 0, so ρ^{T_B} is not positive and ρ is "
                      "not separable (partial transposes of separable states are states). Equivalent form: "
                      "D < −1/3 iff the singlet fraction exceeds 1/2" if ok else "FAILED", {"checks": c})


def cert_TQ9():
    """Invariance under a common rotation of both spins; validity for phase-space averages."""
    u = sp.Matrix(2, 2, sp.symbols("u0:4"))
    SW = sp.zeros(4, 4)
    for i, j in product(range(2), repeat=2):
        SW[j * 2 + i, i * 2 + j] = 1
    UU = sp.kronecker_product(u, u)
    c = {"SWAP (U⊗U) = (U⊗U) SWAP for every 2×2 matrix U": (SW * UU - UU * SW).applyfunc(sp.expand).is_zero_matrix}
    # tr C is a function of tr[ρ SWAP]; a common rotation leaves it unchanged; averages are mixtures
    p, t1, t2 = z3.Reals("p t1 t2")
    okc, info = smt_entails({"weights": z3.And(p > 0, p < 1), "ensemble average below the bound": p * t1 + (1 - p) * t2 < -1},
                            z3.Or(t1 < -1, t2 < -1))
    c["if a mixture has tr C < −1 then some component has tr C < −1"] = okc
    ok = all(c.values())
    return CertResult(ok, "exact + SMT: tr C = 2 tr[ρ SWAP] − 1 is unchanged when both spins are referred to rotated "
                      "common axes, and an average below −1 forces a component below −1" if ok else "FAILED",
                      {"checks": c, "smt": info,
                       "reading": "the measured D refers to an ensemble over production kinematics with event-dependent "
                                  "axes; D < −1/3 certifies entangled spin states on a set of kinematic points of "
                                  "positive weight, not a property of one fixed two-qubit state"},
                      scope="general (two-component mixtures; finite mixtures by induction)")


def cert_TQ10():
    """Range of D and the singlet value."""
    sumss = sum((sp.kronecker_product(s, s) for s in SIG), sp.zeros(4))
    ev = sumss.eigenvals()
    psim = sp.Matrix([0, 1, -1, 0]) / sp.sqrt(2)
    c = {"eigenvalues of Σσ_i⊗σ_i are 1 (×3) and −3 (×1)": ev == {1: 3, -3: 1},
         "singlet: tr C = −3, D = −1": (psim.T * sumss * psim)[0] == -3}
    ok = all(c.values())
    return CertResult(ok, "exact: −3 ≤ tr C ≤ 1, i.e. −1 ≤ D ≤ 1/3 for every state; the value D = −1 is attained only "
                      "by the singlet (the eigenvalue −3 is non-degenerate)" if ok else "FAILED", {"checks": c})


def cert_TQ11():
    """D < -1/3 => entangled (contraposition of TQ7)."""
    sep = z3.Bool("separable")
    D = z3.Real("D")
    ok, info = smt_entails({"TQ7: separable ⇒ D ≥ −1/3": z3.Implies(sep, D >= -z3.Q(1, 3)),
                            "measured: D < −1/3": D < -z3.Q(1, 3)}, z3.Not(sep))
    return CertResult(ok, "SMT: contraposition", info)


NUM = {"D_obs": sp.Rational(-537, 1000), "stat": sp.Rational(2, 1000), "syst": sp.Rational(19, 1000),
       "lim_pythia": sp.Rational(-322, 1000), "lim_pythia_unc": sp.Rational(9, 1000),
       "lim_herwig": sp.Rational(-27, 100),
       "D_exp": sp.Rational(-470, 1000), "exp_stat": sp.Rational(2, 1000), "exp_syst": sp.Rational(17, 1000)}


def cert_TQ15():
    """Arithmetic behind 'more than five standard deviations'."""
    n = NUM
    z1 = (n["lim_pythia"] - n["D_obs"]) / sp.sqrt(n["stat"] ** 2 + n["syst"] ** 2 + n["lim_pythia_unc"] ** 2)
    z2 = (n["lim_herwig"] - n["D_obs"]) / sp.sqrt(n["stat"] ** 2 + n["syst"] ** 2)
    # how large the total uncertainty would have to be for the separation to fall to 5 sigma
    need = (n["lim_pythia"] - n["D_obs"]) / 5
    ok = bool(z1 > 5) and bool(z2 > 5)
    return CertResult(ok, f"exact arithmetic on the quoted numbers: distance to the folded bound −0.322 is 0.215 = "
                      f"{float(z1):.1f}σ (uncertainties added in quadrature, bound uncertainty 0.009 included); to the "
                      f"alternative bound −0.27 it is 0.267 = {float(z2):.1f}σ; the separation stays above 5σ unless "
                      f"the total uncertainty exceeds {float(need):.3f}",
                      {"z_pythia": float(z1), "z_herwig": float(z2), "uncertainty_needed_for_5_sigma": float(need),
                       "assumptions": "Gaussian errors, statistical and systematic parts independent; the paper's own "
                                      "significance procedure is not reproduced"})


def cert_TQ16():
    """Observed versus expected D in the signal region."""
    n = NUM
    diff = n["D_obs"] - n["D_exp"]
    sig_ind = sp.sqrt(n["stat"] ** 2 + n["syst"] ** 2 + n["exp_stat"] ** 2 + n["exp_syst"] ** 2)
    z = abs(diff) / sig_ind
    ok = diff == sp.Rational(-67, 1000)
    return CertResult(ok, f"exact arithmetic: observed − expected = {float(diff):+.3f}; this is {float(z):.1f}σ if the "
                      f"two uncertainties are treated as independent (their correlation is not given in the text used)",
                      {"difference": float(diff), "z_if_independent": float(z)},
                      scope="general (arithmetic only; not a statistical statement of the paper)")


# ----------------------------------------------------------------------------
# the paper as a network delta
# ----------------------------------------------------------------------------

def build() -> Paper:
    H = "GEN_HEP v1.2"
    Q = "GEN_QRT_Level v1.2"
    P_ = "GEN_GPT_Level v2.6"
    nodes = [
        Node("s_t", "S", "sector", "Top quark t (Standard-Model graph, outside its released scope)",
             "Massive spin-½ sector; decays before hadronisation, so its spin is passed to the decay products.",
             "out-of-scope", f"{H}: third generation not in the released graph"),
        Node("s_b", "S", "sector", "Bottom quark b (Standard-Model graph, outside its released scope)",
             "Massive spin-½ sector; enters only through the charged current t̄_L γ^μ b_L.", "out-of-scope"),
        Node("s_W", "S", "sector", "W± (Standard-Model graph)", "Massive spin-1 mediator sector.", "existing", f"{H}:s_W"),
        Node("s_lep", "S", "sector", "Charged leptons and neutrinos e, μ, ν_e, ν_μ (Standard-Model graph)",
             "Lepton doublets; treated as massless in the decay.", "existing", f"{H}:s_e, s_mu, s_nue, s_num"),
        Node("s-ttspin", "S", "hilbert", "Spin state ρ(k) of the t t̄ pair (two-qubit state)",
             "ρ = ¼[1 + Σ B+_i σ_i⊗1 + Σ B−_i 1⊗σ_i + Σ C_ij σ_i⊗σ_j] at fixed production kinematics k.", "new"),
        Node("s-ttavg", "S", "cluster", "Phase-space ensemble of t t̄ spin states (mass window)",
             "{ρ(k), dμ(k)} for 340 < m_tt̄ < 380 GeV, spins referred to event-dependent axes common to t and t̄.", "new"),
        Node("s-sep", "S", "free", "Separable states (nonclassicality / resource-theory networks)",
             "Convex mixtures of product states.", "existing", f"{P_}:s-sep; {Q}:sF-ent"),
        Node("s-ent", "S", "resource", "Entangled states (nonclassicality / resource-theory networks)",
             "States outside the separable set.", "existing", f"{P_}:s-ent; {Q}:sR-ent"),
        Node("d-singlet", "S", "dist", "Spin singlet |Ψ−> (resource-theory network: Bell state)",
             "(|↑↓> − |↓↑>)/√2; locally equivalent to |Φ+>.", "existing", f"{Q}:d-bell"),
        Node("m_cc", "M", "fund", "Charged-current gauge vertex (g/√2) W+_μ J^μ_CC (Standard-Model graph)",
             "J^μ_CC = Σ ψ̄_L γ^μ ψ'_L; here extended by the term t̄_L γ^μ b_L alongside ν̄_L γ^μ ℓ_L.",
             "existing", f"{H}:m_cc"),
        Node("m_A", "M", "frame", "Observable postulate and Born rule (Standard-Model graph)",
             "Outcome probabilities are tr(ρE) for effects E; amplitudes are linear in the state.", "existing", f"{H}:m_A"),
        Node("m-qcd", "M", "fund", "QCD production of t t̄ (strong sector, outside the released scope)",
             "gg, q q̄ → t t̄; near threshold the gg channel produces a spin-singlet pair.", "out-of-scope"),
        Node("m-mc", "M", "frame", "Monte Carlo model used for folding and calibration",
             "Event generators, parton shower and detector simulation relating parton-level to particle-level quantities.", "new"),
        Node("o-lepdir", "O", "direct", "Charged-lepton direction in the parent rest frame",
             "dΓ/dΩ for t → b ℓ+ ν and t̄ → b̄ ℓ− ν̄ with polarised parent.", "new"),
        Node("o-joint", "O", "direct", "Joint lepton distribution (1/σ) dσ/dΩ+ dΩ−",
             "Density of the two charged-lepton directions q̂+, q̂−, each in its parent's rest frame.", "new"),
        Node("o-cosphi", "O", "direct", "cos φ distribution",
             "φ = angle between q̂+ and q̂−; (1/σ) dσ/dcos φ.", "new"),
        Node("w-D", "O", "witness", "Entanglement marker D (entanglement witness)",
             "D = tr C/3 = −3<cos φ>; threshold: separable states have D ≥ −1/3.", "new", f"{P_}:w-entw; {Q}:wD-ent"),
        Node("e-ttent", "O", "effect", "Spin entanglement of top-quark pairs",
             "The spin state of the pair is not separable (on a set of kinematic points of positive weight).", "new"),
        Node("o-limit", "O", "direct", "Folded separability bound at particle level",
             "Image of D = −1/3 in the fiducial particle-level phase space: −0.322 ± 0.009 (Powheg+Pythia), −0.27 (Powheg+Herwig).", "new"),
        Node("o-Dobs", "O", "direct", "Measured D at particle level",
             "D = −0.537 ± 0.002 (stat.) ± 0.019 (syst.) for 340 < m_tt̄ < 380 GeV; expected −0.470 ± 0.002 ± 0.017.", "new"),
    ]

    E = Edge
    edges = [
        E("TQ1", ["m_A"], "s-ttspin", "defines",
          "Every two-qubit state is fixed by the 15 Pauli expectation values B+, B−, C.", "Main, first displayed equation (spin density matrix)",
          "exact", cert_TQ1, method="explicit Pauli basis"),
        E("TQ2", ["m_cc", "s_t", "s_b", "s_W", "s_lep"], "o-lepdir", "predicts",
          "For t(p_t, s) → b ℓ+ ν through the V−A current: Σ|M|² ∝ (p_b·p_ν)((p_t − m s)·p_ℓ), so "
          "dΓ/dΩ ∝ 1 + ŝ·q̂+ in the top rest frame.", "Main, decay paragraph: the leptons carry the spin information; no derivation and no reference in the paper", "exact", cert_TQ2,
          method="Dirac traces with explicit 4×4 matrices, fully symbolic",
          note="Library facts used and not regenerated: the Feynman rules that turn the vertex into a tree amplitude, "
               "and the spin sums Σ u ū = p̸ + m, Σ v v̄ = p̸ − m. The W propagator is a spin-independent factor and is "
               "left out. Radiative corrections are not included."),
        E("TQ3", ["m_cc", "s_t", "s_b", "s_W", "s_lep"], "o-lepdir", "predicts",
          "For t̄ → b̄ ℓ− ν̄: Σ|M|² ∝ (p_b̄·p_ν̄)((p_t̄ + m s)·p_ℓ), so dΓ/dΩ ∝ 1 − ŝ·q̂−.", "same", "exact", cert_TQ3,
          method="Dirac traces, fully symbolic"),
        E("TQ4", ["o-lepdir", "m_A"], "o-joint", "defines",
          "The decays act on the spins as measurements with effects (1 + q̂+·σ)/4π and (1 − q̂−·σ)/4π.",
          "not stated in the paper; step of the regeneration of the lepton distribution", "exact", cert_TQ4, uses=["TQ2", "TQ3"],
          method="uniqueness of a Hermitian operator given its pure-state expectations; integration over the sphere"),
        E("TQ5", ["s-ttspin", "m_cc", "m_A"], "o-joint", "predicts",
          "(1/σ) dσ/dΩ+dΩ− = [1 + B+·q̂+ − B−·q̂− − q̂+·C·q̂−]/(4π)².", "Main, second displayed equation; cited to Ref. [27]", "exact",
          cert_TQ5, uses=["TQ1", "TQ4"], method="symbolic trace",
          note="Uses that the two decays act on different tensor factors, so their effects multiply."),
        E("TQ6", ["o-joint"], "o-cosphi", "predicts",
          "(1/σ) dσ/dcos φ = ½(1 − D cos φ) with D = tr C/3, and <cos φ> = −D/3.", "Main: D = −3<cos φ>; Methods A.3: linear form; not derived in the paper", "exact",
          cert_TQ6, uses=["TQ5"], method="symbolic integration over both spheres"),
        E("TQ6b", ["o-cosphi"], "w-D", "defines",
          "D = −3<cos φ>.", "Main, third displayed equation", "definition", uses=["TQ6"]),
        E("TQ7", ["s-sep"], "w-D", "bounds",
          "Separable states satisfy tr C ≥ −1, i.e. D ≥ −1/3.", "Main: tr[C] + 1 < 0 as sufficient condition, Ref. [18]", "exact", cert_TQ7,
          method="sum-of-squares identity + convexity"),
        E("TQ8", ["s-sep"], "w-D", "bounds",
          "tr C + 1 < 0 iff <Φ+|ρ^{T_B}|Φ+> < 0, which contradicts positivity of the partial transpose.",
          "Main: the criterion is attributed to Peres and Horodecki, Refs. [35, 36]", "exact", cert_TQ8, method="operator identities"),
        E("TQ9", ["s-ttavg"], "w-D", "bounds",
          "The bound holds for the phase-space average with event-dependent common spin axes, and a violation "
          "implies entanglement of ρ(k) on a set of positive weight.", "Main, threshold paragraph: statement on averaging over the top-quark directions, Ref. [18]; no proof in the paper",
          "exact", cert_TQ9, uses=["TQ7"], method="commutation of SWAP with U⊗U; SMT"),
        E("TQ10", ["d-singlet"], "w-D", "predicts",
          "−1 ≤ D ≤ 1/3 for every state; D = −1 for the spin singlet.", "not stated in the paper", "exact", cert_TQ10,
          method="eigenvalues"),
        E("TQ11", ["w-D", "s-ttspin"], "e-ttent", "witness",
          "D < −1/3 implies that the state is entangled.", "Main: criterion D < −1/3, Refs. [35, 36]", "logic", cert_TQ11,
          uses=["TQ7", "TQ8"], method="SMT: contraposition"),
        E("TQ12", ["m-qcd"], "s-ttspin", "predicts",
          "Near threshold about 80% of t t̄ production comes from a spin-singlet state.", "Main, threshold paragraph; Refs. [28–30]", "import",
          note="Strong-sector dynamics; outside the released graph and not re-derived."),
        E("TQ13", ["m-mc", "w-D"], "o-limit", "calibrates",
          "The parton-level bound D = −1/3 corresponds to −0.322 ± 0.009 (Powheg+Pythia) or −0.27 (Powheg+Herwig) at "
          "particle level.", "1.2 Analysis procedure (second calibration curve); values in 1.3 Results", "import",
          note="Obtained by reweighting simulated events; depends on the shower model (the two generators differ)."),
        E("TQ14", ["m-mc"], "o-Dobs", "calibrates",
          "D = −0.537 ± 0.002 ± 0.019 observed; −0.470 ± 0.002 ± 0.017 expected.", "abstract (observed value); 1.3 Results", "import",
          note="Data, detector calibration and systematic uncertainties; not checkable here."),
        E("TQ15", ["o-Dobs", "o-limit", "w-D"], "e-ttent", "witness",
          "The observed D lies more than five standard deviations below the folded separability bound.", "abstract; 1.4 Discussion",
          "exact", cert_TQ15, uses=["TQ13", "TQ14"], method="rational arithmetic on the quoted numbers"),
        E("TQ16", ["o-Dobs", "m-mc"], "o-Dobs", "flags",
          "Observed − expected = −0.067 in the signal region.", "1.3 Results gives both values; the difference is not stated in the paper", "exact", cert_TQ16, uses=["TQ14"],
          method="rational arithmetic"),
        E("TQ17", ["m_cc", "m_A", "w-D"], "e-ttent", "scope",
          "The witness presupposes the quantum description of the decay (TQ2–TQ4); it is not a Bell test.",
          "the paper does not describe the measurement as a Bell test", "definition"),
    ]

    claims = [
        Claim("C-C1", "D = tr C/3 is measured as −3<cos φ> from the charged-lepton directions.", "Main",
              ["TQ6b"]),
        Claim("C-C2", "D < −1/3 is a sufficient condition for entanglement.", "Main", ["TQ11"]),
        Claim("C-C3", "The criterion applies to the measured phase-space average.", "Main, threshold paragraph (Ref. [18])", ["TQ9"]),
        Claim("C-C4", "The observed D = −0.537 ± 0.002 ± 0.019 is more than five standard deviations from a "
              "scenario without entanglement.", "abstract", ["TQ15"], kind="empirical"),
        Claim("C-C5", "Entanglement is observed in top-quark pairs.", "abstract",
              ["TQ6b", "TQ11", "TQ9", "TQ15"], kind="empirical"),
    ]

    delta = [
        {"op": "EXTEND", "node": "m_cc", "note": "J_CC gains the term t̄_L γ^μ b_L; by Rule 4 (route composition) this is "
         "one more route t(1) ∧ b(1) ∧ W(1) into the same vertex"},
        {"op": "ADD", "node": "s_t, s_b", "layer": "S.sector",
         "why": "Rule 8 (sector refinement); the released graph omits the third generation and the strong sector"},
        {"op": "PREDICT", "edge": "m_cc ∧ m_A → o-lepdir, o-joint, o-cosphi",
         "why": "model → observable edges of status 'pred'; TQ2–TQ6 regenerate them from the vertex"},
        {"op": "GLUE", "node": "w-D", "with": "w-entw (GEN_GPT_Level), wD-ent (GEN_QRT_Level)",
         "why": "D is an entanglement witness in the sense of those nodes: linear in ρ, bounded on the separable set (TQ7)"},
        {"op": "GLUE", "node": "e-ttent", "with": "s-ent / sR-ent",
         "why": "first shared concept between the particle-physics branch and the two quantum-information branches "
                "that is an observable on one side and a state property on the other"},
        {"op": "CALIBRATE", "edge": "m-mc → o-limit, o-Dobs", "why": "Rule 9: these edges carry the fitted and simulated "
         "inputs; the conclusion depends on them and they are imports for the kernel"},
        {"op": "FLAG", "node": "o-Dobs", "note": "observed more negative than expected (TQ16); the paper states that "
         "bound-state effects near threshold are not in the generators. A pseudoscalar excess at the t t̄ threshold was "
         "later reported by CMS (Rep. Prog. Phys. 88, 087801 (2025))"},
        {"op": "FIBRE", "note": "over the fixed model node (m_cc ∧ m_A) the observables o-cosphi in bins of m_tt̄ form "
         "one effect with one witness: an instance of the contraction lemma of the grand network (effect networks "
         "are fibres of the historical graph over a model node)"},
    ]

    findings = [
        {"level": "structure", "title": "What the witness certifies",
         "text": "TQ9: a violation certifies entangled spin states on a set of production kinematics of positive "
                 "weight, with spins referred to event-dependent axes; it is a statement about an ensemble. TQ17: the "
                 "inference uses the decay vertex and the Born rule as premises, so it is a witness, not a Bell test."},
        {"level": "structure", "title": "Two routes to the same bound",
         "text": "TQ7 (sum of squares on product states + convexity) and TQ8 (partial transpose) give the same "
                 "threshold; D < −1/3 is the statement that the singlet fraction exceeds 1/2."},
        {"level": "arithmetic", "title": "Quoted numbers",
         "text": "TQ15: 10.2σ from the Powheg+Pythia bound and 14.0σ from the Powheg+Herwig bound under simple "
                 "quadrature, consistent with 'more than five'. TQ16: the observed value is 0.067 below the expected "
                 "one (2.6σ if the uncertainties were independent)."},
        {"level": "premise", "title": "Imported edges",
         "text": "The folding of the bound to particle level (TQ13), the measured value with its systematics (TQ14) and "
                 "the production dynamics (TQ12) are outside what the kernel can regenerate. TQ2–TQ3 are tree level "
                 "with unit analysing power; radiative corrections to it are not included."},
        {"level": "note", "title": "Versions",
         "text": "The first arXiv version quotes D = −0.547 ± 0.002 ± 0.021; the published value is −0.537 ± 0.002 ± 0.019."},
    ]

    return Paper(
        key="top",
        citation="ATLAS Collaboration, Observation of quantum entanglement with top quarks at the ATLAS detector, "
                 "Nature 633, 542–547 (2024)",
        ids={"doi": "10.1038/s41586-024-07824-z", "arxiv": "2311.07288"},
        branch="Particle-physics branch (GEN_HEP v1.2) glued to the quantum-information branches",
        summary="Measures the angle between the two charged leptons from t t̄ decays near threshold, converts its mean "
                "into the spin-correlation marker D = tr C/3, and reports D below the bound that separable spin states obey.",
        nodes=nodes, edges=edges, claims=claims, delta=delta, findings=findings, year=2024,
        phases=[["predict", "the vertex and the Born rule give the lepton distributions and the expected D"],
                ["observe", "D is measured in the threshold window"],
                ["calibrate", "the separability bound and the measurement are folded through simulation"],
                ["deficit", "the observed D lies below the expected one"]],
        sources=[
            {"title": "ATLAS, Nature 633, 542 (2024)", "url": "https://doi.org/10.1038/s41586-024-07824-z"},
            {"title": "arXiv:2311.07288", "url": "https://arxiv.org/abs/2311.07288"},
            {"title": "CMS, Rep. Prog. Phys. 88, 087801 (2025), arXiv:2503.22382", "url": "https://arxiv.org/abs/2503.22382v2"},
        ],
    )
