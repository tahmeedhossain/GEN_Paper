"""
Paper A.  R. Ganardi, T. V. Kondra, N. H. Y. Ng, A. Streltsov,
"Second Law of Entanglement Manipulation with an Entanglement Battery",
Phys. Rev. Lett. 135, 010202 (2025); arXiv:2405.10599.

Encoded against the resource-theory network GEN_QRT_Level v1.2 (nodes sF-ent, sR-ent,
pF-ent, pX-ent, p-cat, F-STEIN, wQ-ent; edges MM11, MM12, P8, C18, W15; gap QG9).

Notation in the SMT certificates: every E-value is a real number (this is where the
paper's finiteness hypothesis enters); additivity and monotonicity appear as linear
relations between those numbers.
"""
from itertools import product

import sympy as sp
import z3

from kernel import CertResult, Claim, Edge, Node, Paper, smt_entails

R = z3.Real


# ----------------------------------------------------------------------------
# certificates
# ----------------------------------------------------------------------------

def cert_GB1():
    """Necessity in Theorem 1 (Eq. (14))."""
    Er, Es, Et, Et2, Ein, Eout = z3.Reals("E_rho E_sigma E_tau E_tau2 E_in E_out")
    prem = {
        "additivity on the input  E(ρ⊗τ) = E(ρ)+E(τ)": Ein == Er + Et,
        "additivity on the output E(σ⊗τ~) = E(σ)+E(τ~)": Eout == Es + Et2,
        "LOCC monotonicity  E(Λ[ρ⊗τ]) ≤ E(ρ⊗τ)": Eout <= Ein,
        "battery condition (10)  E(τ~) ≥ E(τ)": Et2 >= Et,
    }
    ok, info = smt_entails(prem, Es <= Er)
    return CertResult(ok, "SMT (linear real arithmetic): the four premises entail E(σ) ≤ E(ρ); "
                      f"each premise is needed ({len(info.get('needed', []))}/4 — dropping any one admits a counter-model)",
                      info)


def _swap_check(dA, dB, alice_only=False):
    """alice_only = True plants an error (Bob does not swap); used by controls.py."""
    n = dA * dB
    X = sp.Matrix(n, n, sp.symbols(f"x0:{n * n}"))
    Y = sp.Matrix(n, n, sp.symbols(f"y0:{n * n}"))
    N = n * n

    def idx(a, b, a2, b2):
        return ((a * dB + b) * dA + a2) * dB + b2

    W, WA, WB = sp.zeros(N, N), sp.zeros(N, N), sp.zeros(N, N)
    for a, b, a2, b2 in product(range(dA), range(dB), range(dA), range(dB)):
        W[idx(a2, b2, a, b), idx(a, b, a2, b2)] = 1          # |a b a' b'> -> |a' b' a b>
        WA[idx(a2, b, a, b2), idx(a, b, a2, b2)] = 1         # Alice swaps A <-> A'
        WB[idx(a, b2, a2, b), idx(a, b, a2, b2)] = 1         # Bob swaps B <-> B'
    if alice_only:
        W = WA.copy()
    lhs = W * sp.kronecker_product(X, Y) * W.T
    c = {
        "W (X⊗Y) W^T = Y⊗X for symbolic X, Y": (lhs - sp.kronecker_product(Y, X)).is_zero_matrix,
        "W = W_A W_B = W_B W_A": (W - WA * WB).is_zero_matrix and (WA * WB - WB * WA).is_zero_matrix,
    }
    # W_A is (SWAP on A,A') ⊗ 1 on (B,B') after reordering (A,B,A',B') -> (A,A',B,B')
    P = sp.zeros(N, N)
    for a, b, a2, b2 in product(range(dA), range(dB), range(dA), range(dB)):
        P[((a * dA + a2) * dB + b) * dB + b2, idx(a, b, a2, b2)] = 1
    SW_A = sp.zeros(dA * dA, dA * dA)
    for a, a2 in product(range(dA), repeat=2):
        SW_A[a2 * dA + a, a * dA + a2] = 1
    SW_B = sp.zeros(dB * dB, dB * dB)
    for b, b2 in product(range(dB), repeat=2):
        SW_B[b2 * dB + b, b * dB + b2] = 1
    c["W_A = SWAP_{AA'} ⊗ 1_{BB'} (local to Alice)"] = (P * WA * P.T - sp.kronecker_product(SW_A, sp.eye(dB * dB))).is_zero_matrix
    c["W_B = 1_{AA'} ⊗ SWAP_{BB'} (local to Bob)"] = (P * WB * P.T - sp.kronecker_product(sp.eye(dA * dA), SW_B)).is_zero_matrix
    return c


def cert_GB2():
    """Sufficiency in Theorem 1 (Eqs. (15)-(17)): the swap protocol."""
    res, ok = {}, True
    for dA, dB in ((2, 2), (2, 3)):
        c = _swap_check(dA, dB)
        res[f"dA={dA}, dB={dB}"] = c
        ok &= all(c.values())
    Er, Es, Et, Et2 = z3.Reals("E_rho E_sigma E_tau E_tau2")
    ok2, info = smt_entails({"battery starts in the target: E(τ) = E(σ)": Et == Es,
                             "battery ends in the source: E(τ~) = E(ρ)": Et2 == Er,
                             "hypothesis E(ρ) ≥ E(σ)": Er >= Es}, Et2 >= Et)
    return CertResult(ok and ok2, "exact: the product of Alice's swap A↔A' and Bob's swap B↔B' maps X^{AB}⊗Y^{A'B'} to "
                      "Y^{AB}⊗X^{A'B'} for symbolic X, Y; SMT: with τ = σ the battery condition is E(ρ) ≥ E(σ)",
                      {"swap": res, "battery": info,
                       "reading": "the protocol is a pair of local permutations; no property of E is used in this "
                                  "direction, and the battery's initial state is a copy of the target state"},
                      scope="instances: (dA,dB) = (2,2), (2,3) for the permutation identity (an index identity valid in every dimension)")


def cert_GB4():
    """Additivity over copies, E(ρ^{⊗k}) = k E(ρ): induction step."""
    k, Ek, Ek1, Er = z3.Reals("k E_k E_k1 E_rho")
    ok, info = smt_entails({"induction hypothesis E(ρ^{⊗k}) = k E(ρ)": Ek == k * Er,
                            "additivity E(ρ^{⊗k}⊗ρ) = E(ρ^{⊗k}) + E(ρ)": Ek1 == Ek + Er}, Ek1 == (k + 1) * Er)
    return CertResult(ok, "SMT: induction step holds (base case k = 1 is trivial); the induction schema itself is "
                      "not a kernel rule", info, scope="general (induction step checked; schema assumed)")


def cert_GB5():
    """Zero-error upper bound, Eqs. (30)-(31)."""
    n, m, Er, Es, Et, Et2, Ein, Eout = z3.Reals("n m E_rho E_sigma E_tau E_tau2 E_in E_out")
    prem = {
        "n, m ≥ 1 and E(σ) > 0": z3.And(n >= 1, m >= 1, Es > 0),
        "additivity on the input  E(ρ^{⊗n}⊗τ) = nE(ρ)+E(τ)": Ein == n * Er + Et,
        "additivity on the output E(σ^{⊗m}⊗τ~) = mE(σ)+E(τ~)": Eout == m * Es + Et2,
        "LOCC monotonicity": Eout <= Ein,
        "battery condition": Et2 >= Et,
    }
    ok, info = smt_entails(prem, m / n <= Er / Es)
    return CertResult(ok, "SMT (nonlinear real arithmetic): m/n ≤ E(ρ)/E(σ); every premise needed", info)


def cert_GB6():
    """Achievability: relabelling protocol with battery σ^{⊗m} -> ρ^{⊗n}."""
    n, m, Er, Es, Et, Et2 = z3.Reals("n m E_rho E_sigma E_tau E_tau2")
    ok, info = smt_entails({"battery starts as σ^{⊗m}": Et == m * Es,
                            "battery ends as ρ^{⊗n}": Et2 == n * Er,
                            "rate condition m E(σ) ≤ n E(ρ)": m * Es <= n * Er}, Et2 >= Et)
    return CertResult(ok, "SMT: for every pair (n, m) with m E(σ) ≤ n E(ρ) the relabelling of the n source copies "
                      "and the m battery copies satisfies the battery condition; output is exactly σ^{⊗m} (zero error)",
                      dict(info, reading="the operation is the identity up to a relabelling of which subsystems are "
                                         "called system and battery"))


def cert_GB7():
    """Rates m/n approach any real x >= 0 from below (floor construction)."""
    n, m, x, delta = z3.Reals("n m x delta")
    ok, info = smt_entails({"n ≥ 1/δ, δ > 0": z3.And(delta > 0, n >= 1 / delta),
                            "m = floor(n x):  m ≤ n x < m + 1": z3.And(m <= n * x, n * x < m + 1)},
                           z3.And(m / n <= x, m / n > x - delta))
    return CertResult(ok, "SMT: with m = ⌊n x⌋ and n ≥ 1/δ one has x − δ < m/n ≤ x; existence of the floor is the "
                      "Archimedean property of the reals (library fact)", info)


def cert_GB9():
    """Theorem 2, converse at finite n: Eqs. (19)-(23), with a general continuity modulus."""
    n, m, Er, Es, Emu, Et, Et2, Ein, Eout, xg, f = z3.Reals("n m E_rho E_sigma E_mu E_tau E_tau2 E_in E_out x f")
    prem = {
        "domain: n, m ≥ 1, E(ρ) ≥ 0, f ≥ 0, x ≥ 0": z3.And(n >= 1, m >= 1, Er >= 0, f >= 0, xg >= 0),
        "additivity on the input (19)": Ein == n * Er + Et,
        "additivity on the product output μ⊗τ~ (19)": Eout == Emu + Et2,
        "LOCC monotonicity (19)": Eout <= Ein,
        "battery condition (11c)": Et2 >= Et,
        "continuity (21):  m E(σ) − E(μ) ≤ m x + f,  x = g(ε) log2 d": m * Es - Emu <= m * xg + f,
        "smallness (24):  x < E(σ)": xg < Es,
    }
    ok, info = smt_entails(prem, m / n <= (Er + f / n) / (Es - xg))
    # the paper's linear form is the special case x = K ε log2 d
    K, eps, L = z3.Reals("K eps L")
    ok_lin, _ = smt_entails(dict(prem, **{"linear modulus (13): x = K ε log2 d": xg == K * eps * L}),
                            m / n <= (Er + f / n) / (Es - eps * K * L), minimality=False)
    return CertResult(ok and ok_lin, "SMT: m/n ≤ (E(ρ) + f/n)/(E(σ) − x) for any modulus x = g(ε)·log2 d with x < E(σ); "
                      "Eq. (23) is the case g(ε) = Kε; every premise needed", dict(info, linear_case=ok_lin))


def cert_GB10():
    """Limit step: the bound of GB9 tends to E(ρ)/E(σ)."""
    a, s, x, f, n, eta = z3.Reals("a s x f n eta")
    prem = {
        "domain: a = E(ρ) ≥ 0, s = E(σ) > 0, x, f ≥ 0, n ≥ 1, η > 0": z3.And(a >= 0, s > 0, x >= 0, f >= 0, n >= 1, eta > 0),
        "x ≤ s/2": x <= s / 2,
        "f ≤ η s/4": f <= eta * s / 4,
        "a x ≤ η s²/4": a * x <= eta * s * s / 4,
    }
    ok, info = smt_entails(prem, (a + f / n) / (s - x) <= a / s + eta)
    return CertResult(ok, "SMT: for every η > 0, once x and f are below explicit thresholds the right-hand side of "
                      "(23) is at most E(ρ)/E(σ) + η; since g(ε), f(ε) → 0 this gives R ≤ E(ρ)/E(σ)", info)


def cert_GB3():
    """Theorem 1 as the conjunction of its two directions."""
    conv = z3.Bool("converts")
    Er, Es = z3.Reals("E_rho E_sigma")
    ok, info = smt_entails({"GB1: conversion ⇒ E(ρ) ≥ E(σ)": z3.Implies(conv, Er >= Es),
                            "GB2: E(ρ) ≥ E(σ) ⇒ conversion": z3.Implies(Er >= Es, conv)}, conv == (Er >= Es))
    return CertResult(ok, "SMT: the two implications give the equivalence", info)


def _sup_cert(with_error):
    """sup of the achievable rates equals x := E(ρ)/E(σ), by explicit instantiation of the quantifiers."""
    s_, x = z3.Reals("R x")
    if with_error:
        up = {"GB9+GB10 at η = (R − x)/2: every achievable rate is ≤ x + η, so R ≤ x + η":
              z3.Implies(s_ - x > 0, s_ <= x + (s_ - x) / 2)}
    else:
        up = {"GB5: every achievable rate is ≤ x, so R ≤ x": s_ <= x}
    low = {"GB6+GB7 at δ = x − R: some achievable rate exceeds x − δ, and R dominates it":
           z3.Implies(x - s_ > 0, s_ > x - (x - s_))}
    return smt_entails(dict(up, **low), s_ == x)


def cert_GB8():
    ok, info = _sup_cert(False)
    return CertResult(ok, "SMT: upper bound and approximation from below force R_ze = E(ρ)/E(σ) "
                      "(the quantifiers over δ are instantiated by hand, as shown in the premises)", info)


def cert_GB11():
    ok, info = _sup_cert(True)
    return CertResult(ok, "SMT: converse (for every η) and achievability (for every δ) force R = E(ρ)/E(σ) "
                      "(quantifiers instantiated by hand, as shown in the premises)", info)


def cert_GB21e():
    """The induced system channel of the swap protocol is the replacement channel X -> σ tr X."""
    dA = dB = 2
    n = dA * dB
    X = sp.Matrix(n, n, sp.symbols(f"x0:{n * n}"))
    Y = sp.Matrix(n, n, sp.symbols(f"y0:{n * n}"))
    out = sp.kronecker_product(Y, X)                      # state after the swap (GB2): Y on AB, X on A'B'
    red = sp.zeros(n, n)
    for i in range(n):
        for j in range(n):
            red[i, j] = sum(out[i * n + k, j * n + k] for k in range(n))
    replacement = (red - Y * X.trace()).applyfunc(sp.expand).is_zero_matrix
    Er2, Es, Et, Et2 = z3.Reals("E_rho2 E_sigma E_tau E_tau2")
    ok2, info = smt_entails({"same pair (swap, τ = σ): E(τ) = E(σ)": Et == Es,
                             "applied to another input ρ': E(τ~) = E(ρ')": Et2 == Er2,
                             "E(ρ') < E(σ), e.g. ρ' separable and σ entangled": Er2 < Es}, z3.Not(Et2 >= Et))
    return CertResult(replacement and ok2, "exact: tracing the battery out of the swapped state gives σ·tr X for "
                      "every input X, so the induced channel on the system is the replacement channel X ↦ σ, which "
                      "maps separable inputs to the entangled target; SMT: for an input with E(ρ') < E(σ) the same "
                      "pair (Λ, τ) violates the battery condition",
                      {"replacement channel": replacement, "smt": info,
                       "reading": "which pairs (Λ, τ) are admitted depends on the input state; the admitted "
                                  "transformations are not a class of non-entangling channels"},
                      scope="instances: dA = dB = 2 for the partial-trace identity (valid in every dimension)")


def cert_GB12():
    """Reversibility R(ρ→σ) R(σ→ρ) = 1."""
    Er, Es = z3.Reals("E_rho E_sigma")
    ok, info = smt_entails({"0 < E(ρ), E(σ) < ∞": z3.And(Er > 0, Es > 0)}, (Er / Es) * (Es / Er) == 1)
    return CertResult(ok, "SMT: (E(ρ)/E(σ))·(E(σ)/E(ρ)) = 1 for positive finite values", info)


def cert_GB14():
    """Geometric entanglement example, Eqs. (82)-(84)."""
    d = sp.Symbol("d", integer=True, positive=True)
    n = sp.Symbol("n", integer=True, positive=True)
    p0, p1 = sp.Rational(1, 2), 1 / (2 * (d - 1))                # Schmidt probabilities: p0 once, p1 (d-1) times
    c = {}
    c["probabilities sum to 1"] = sp.simplify(p0 + (d - 1) * p1 - 1) == 0
    # p0 - p1 = (d-2)/(2(d-1)) >= 0 for d >= 2, so the largest Schmidt probability is 1/2
    c["largest Schmidt probability is 1/2 for d ≥ 2:  p0 − p1 = (d−2)/(2(d−1))"] = sp.simplify(
        p0 - p1 - (d - 2) / (2 * (d - 1))) == 0
    S = -p0 * sp.log(p0, 2) - (d - 1) * p1 * sp.log(p1, 2)
    target = 1 + sp.Rational(1, 2) * sp.log(d - 1, 2)
    c["S(ψ^A) = 1 + (1/2) log2(d−1)  (Eq. (83))"] = sp.simplify(sp.expand_log(S - target, force=True)) == 0
    Eg_psi, Eg_phi = 1 - p0, 1 - sp.Rational(1, 2)
    c["E_g(ψ) = E_g(φ+) = 1/2"] = (Eg_psi == sp.Rational(1, 2)) and (Eg_phi == sp.Rational(1, 2))
    c["E_g(ψ^{⊗n}) = E_g(φ+^{⊗n}) = 1 − 2^{−n}  (Eq. (84))"] = sp.simplify((1 - p0 ** n) - (1 - 2 ** (-n))) == 0
    c["E_g is not additive: E_g(φ+⊗φ+) = 3/4 ≠ 2·E_g(φ+) = 1"] = (1 - sp.Rational(1, 4)) != 1
    c["S(ψ^A) → ∞ as d → ∞"] = sp.limit(target, d, sp.oo) == sp.oo
    ok = all(c.values())
    return CertResult(ok, "exact (symbolic d, n): Schmidt spectrum {1/2, 1/(2(d−1)) × (d−1)}; E_g equal to that of a "
                      "Bell state for every number of copies, entropy of entanglement unbounded in d; E_g violates Eq. (12)",
                      {"checks": c,
                       "library fact used": "for a pure bipartite state the maximal squared overlap with product "
                                            "states is the largest Schmidt probability (variational characterisation "
                                            "of the largest singular value); Schmidt spectra multiply under ⊗"})


def cert_GB16():
    """Logarithmic negativity on a Bell state and on a two-qubit pure state."""
    eps = sp.Symbol("epsilon", positive=True)
    a, b = sp.sqrt(1 - eps), sp.sqrt(eps)
    psi = sp.Matrix([a, 0, 0, b])
    rho = psi * psi.T

    def pt(M):       # partial transpose on the first qubit
        out = sp.zeros(4, 4)
        for i, j, k, l in product(range(2), repeat=4):
            out[k * 2 + j, i * 2 + l] = M[i * 2 + j, k * 2 + l]
        return out

    ev = pt(rho).eigenvals()
    # for 0 < eps < 1 the eigenvalues are 1-eps, eps, +sqrt(eps(1-eps)), -sqrt(eps(1-eps))
    want = {1 - eps: 1, eps: 1, sp.sqrt(eps) * sp.sqrt(1 - eps): 1, -sp.sqrt(eps) * sp.sqrt(1 - eps): 1}
    got = {sp.simplify(k): v for k, v in ev.items()}
    spectrum_ok = all(any(sp.simplify(k - w) == 0 for k in got) for w in want) and sum(ev.values()) == 4
    tn = 1 + 2 * sp.sqrt(eps * (1 - eps))
    bell = tn.subs(eps, sp.Rational(1, 2))
    ok = spectrum_ok and bell == 2
    return CertResult(ok, "exact: the partial transpose of √(1−ε)|00>+√ε|11> has eigenvalues 1−ε, ε, ±√(ε(1−ε)); "
                      "trace norm 1 + 2√(ε(1−ε)), equal to 2 for the Bell state, so E_N(φ+) = 1 and E_N > 0 for all 0 < ε < 1",
                      {"spectrum": {str(k): v for k, v in ev.items()}, "trace_norm": str(tn)})


def cert_GB17():
    """Distillation bound with error for logarithmic negativity, Eqs. (74)-(79)."""
    n, m, En, Emu, Et, Et2, ell = z3.Reals("n m E_N E_mu E_tau E_tau2 ell")
    prem = {
        "n ≥ 1": n >= 1,
        "additivity + monotonicity: E_N(μ) + E_N(τ~) ≤ n E_N(ρ) + E_N(τ)": Emu + Et2 <= n * En + Et,
        "battery condition": Et2 >= Et,
        "Eq. (77): E_N(μ) ≥ m + log2(1−ε) =: m + ℓ": Emu >= m + ell,
    }
    ok, info = smt_entails(prem, m / n <= En - ell / n)
    return CertResult(ok, "SMT: m/n ≤ E_N(ρ) − (1/n)·log2(1−ε)  (Eq. (79))", info)


def cert_GB18():
    """Theorem 3: the same derivation with the free energy F."""
    Fr_, Fs, Ft, Ft2, Fin, Fout = z3.Reals("F_rho F_sigma F_tau F_tau2 F_in F_out")
    ok1, i1 = smt_entails({"additivity of F on non-interacting systems (input)": Fin == Fr_ + Ft,
                           "additivity (output)": Fout == Fs + Ft2,
                           "monotonicity of F under thermal operations": Fout <= Fin,
                           "battery condition": Ft2 >= Ft}, Fs <= Fr_)
    ok2, i2 = smt_entails({"battery starts in the target": Ft == Fs, "battery ends in the source": Ft2 == Fr_,
                           "hypothesis F(ρ) ≥ F(σ)": Fr_ >= Fs}, Ft2 >= Ft)
    return CertResult(ok1 and ok2, "SMT: the two directions of Theorem 1 with F in place of E", {"only if": i1, "if": i2})


def cert_GB19():
    """Free set of the battery-assisted theory is the zero set of E."""
    E0, Es = z3.Reals("E_rho0 E_sigma")
    # Theorem 1: rho0 -> sigma  iff  E(sigma) <= E(rho0)
    ok1, i1 = smt_entails({"E ≥ 0": Es >= 0, "E(ρ0) = 0 for the separable start": E0 == 0,
                           "reachable (Theorem 1): E(σ) ≤ E(ρ0)": Es <= E0}, Es == 0)
    ok2, i2 = smt_entails({"E(ρ0) = 0": E0 == 0, "E(σ) = 0": Es == 0}, Es <= E0)
    return CertResult(ok1 and ok2, "SMT: σ is reachable from a separable state iff E(σ) = 0", {"⇒": i1, "⇐": i2})


def cert_GB20():
    """Two admissible quantifiers order a pair of states oppositely."""
    eps = sp.Symbol("epsilon", positive=True)
    h = -eps * sp.log(eps, 2) - (1 - eps) * sp.log(1 - eps, 2)
    lim = sp.limit(h, eps, 0, "+")
    eN = sp.log(1 + 2 * sp.sqrt(eps * (1 - eps)), 2)
    pos = all(sp.N(eN.subs(eps, sp.Rational(1, 10 ** k))) > 0 for k in range(1, 12))
    # Theorem 1 (GB3) as the conversion predicate:  x -> y allowed  iff  E(x) >= E(y)
    Nr, Ns, Qr, Qs = z3.Reals("EN_rhoPPT EN_sigma Esq_rhoPPT Esq_sigma")
    prem = {
        "E_N(ρ_PPT) = 0 (PPT state)": Nr == 0,
        "E_N(σ_ε) > 0 (GB16)": Ns > 0,
        "E_sq(ρ_PPT) > 0 (faithfulness, GB13b)": Qr > 0,
        "E_sq(σ_ε) = h(ε) with 0 ≤ h(ε) < E_sq(ρ_PPT) (ε small)": z3.And(Qs >= 0, Qs < Qr),
    }
    concl = z3.And(Ns >= Nr, z3.Not(Nr >= Ns),      # E_N battery: σ_ε → ρ_PPT allowed, ρ_PPT → σ_ε forbidden
                   Qr >= Qs, z3.Not(Qs >= Qr))      # E_sq battery: ρ_PPT → σ_ε allowed, σ_ε → ρ_PPT forbidden
    okL, info = smt_entails(prem, concl)
    ok = (lim == 0) and pos and okL
    return CertResult(ok, "exact + SMT: h(ε) → 0 as ε → 0+ and E_N(σ_ε) > 0; hence for small ε the E_N battery allows "
                      "σ_ε → ρ_PPT and forbids ρ_PPT → σ_ε, while the E_sq battery does the reverse",
                      {"limit of h": str(lim), "E_N(σ_ε) > 0 at ε = 10^-1..10^-11": pos, "smt": info},
                      scope="general (given the imported properties of E_sq and the existence of PPT entangled states)")


# ----------------------------------------------------------------------------
# the paper as a network delta
# ----------------------------------------------------------------------------

def build() -> Paper:
    G = "GEN_QRT_Level v1.2"
    nodes = [
        Node("sR-ent", "S", "resource", "Entangled states ρ, σ (entanglement theory)",
             "Bipartite density operators outside SEP; here the source ρ^{AB} and the target σ^{AB}.", "existing", f"{G}:sR-ent"),
        Node("sF-ent", "S", "free", "SEP, separable states (entanglement theory)",
             "Convex hull of product states.", "existing", f"{G}:sF-ent"),
        Node("s-bat", "S", "resource", "Battery states τ, τ~ (entanglement battery)",
             "Bipartite states of an auxiliary system A'B' (or C); τ before, τ~ after the protocol; not fixed in advance.", "new"),
        Node("s-geo", "S", "dist", "States |ψ_d> (geometric-entanglement example)",
             "|ψ_d> = |00>/√2 + Σ_{i=1}^{d−1}|ii>/√(2(d−1)).", "new"),
        Node("s-order", "S", "dist", "Pair (ρ_PPT, σ_ε) (order-reversal example)",
             "ρ_PPT: a PPT entangled state; σ_ε = √(1−ε)|00> + √ε|11> with small ε.", "new"),
        Node("pF-ent", "M", "process", "LOCC (entanglement theory)",
             "Local operations and classical communication with respect to the cut AA'|BB'.", "existing", f"{G}:pF-ent"),
        Node("ax-add", "M", "axiom", "Additivity of E (Eq. (12))",
             "E(ρ^{AB}⊗σ^{A'B'}) = E(ρ^{AB}) + E(σ^{A'B'}) for all states.", "new"),
        Node("ax-mono", "M", "axiom", "LOCC monotonicity of E",
             "E(Λ[ρ]) ≤ E(ρ) for every LOCC protocol Λ.", "new"),
        Node("ax-fin", "M", "axiom", "Finiteness of E",
             "E(ρ) is a real number for every state (no value +∞).", "new"),
        Node("ax-ac", "M", "axiom", "Asymptotic continuity of E (Eq. (13), generalised)",
             "|E(ρ) − E(σ)| ≤ g(‖ρ−σ‖₁)·log2 d + f(‖ρ−σ‖₁) with g, f → 0 at 0, f independent of d. "
             "Eq. (13) is the case g(x) = Kx.", "new"),
        Node("p-bat", "M", "process", "LOCC with an entanglement battery, relative to E",
             "ρ → σ iff there are τ, τ~ and an LOCC protocol Λ with Λ(ρ⊗τ) = σ⊗τ~ and E(τ~) ≥ E(τ) (Eqs. (9)–(10)); "
             "asymptotic version Eqs. (11a)–(11d).", "new"),
        Node("pX-ent", "M", "process", "No second law under non-entangling operations (entanglement theory)",
             "Under exactly non-entangling operations entanglement manipulation is asymptotically irreversible.",
             "existing", f"{G}:pX-ent", refs=["Lami, Regula, Nat. Phys. 19, 184 (2023)"]),
        Node("ax-chan", "M", "axiom", "Operations form a class of channels (premise of the no-go for non-entangling operations)",
             "The allowed operations are a set of channels on the system, fixed independently of the input state and "
             "containing no channel that maps a separable state to an entangled one.", "split",
             f"{G}:pX-ent (part of its statement)"),
        Node("p-cat", "M", "process", "Catalysis (shared process node)",
             "Catalysts must be returned unchanged; a stricter condition than the battery condition.", "existing", f"{G}:p-cat"),
        Node("p-thbat", "M", "process", "Thermal operations with a free-energy battery",
             "(ρ,H_S) → (σ,H_S') iff a thermal operation maps ρ⊗τ to σ⊗τ~ with F(τ~) ≥ F(τ).", "new"),
        Node("wQ-E", "O", "witness", "Quantifier E (admissible class)",
             "A function on bipartite states satisfying ax-add, ax-mono, ax-fin (and ax-ac for Theorem 2).", "new"),
        Node("wQ-sq", "O", "witness", "Squashed entanglement E_sq",
             "E_sq(ρ^{AB}) = inf{ I(A;B|E)/2 : ρ^{ABE} an extension of ρ^{AB} } (Eq. (5)).", "new"),
        Node("wQ-neg", "O", "witness", "Logarithmic negativity E_N (entanglement theory)",
             "E_N(ρ) = log2 ‖ρ^{T_A}‖₁.", "existing", f"{G}:wQ-ent (negativity)"),
        Node("wQ-geo", "O", "witness", "Geometric entanglement E_g",
             "E_g(ψ) = 1 − max over product states of |<a,b|ψ>|².", "new"),
        Node("wQ-F", "O", "witness", "Free energy F (athermality)",
             "F(ρ,H) = k_B T (S(ρ‖γ) − log Z), 0 < T < ∞ (Eq. (7)).", "existing", f"{G}:wQ-ath"),
        Node("t-conv", "O", "task", "Single-copy conversion ρ → σ",
             "Existence of a battery-assisted protocol producing σ exactly from one copy of ρ.", "new"),
        Node("t-rate", "O", "task", "Asymptotic rate R(ρ → σ)",
             "Supremum of r such that for all ε, δ > 0 there are n, m with m/n > r − δ and a protocol satisfying "
             "(11a)–(11c); zero-error version with ε = 0.", "new"),
        Node("e-rev", "O", "effect", "Reversibility of entanglement manipulation",
             "R(ρ→σ)·R(σ→ρ) = 1 for all pairs of states with 0 < E < ∞.", "new"),
    ]

    E = Edge
    edges = [
        E("GB0", ["pF-ent", "wQ-E", "s-bat"], "p-bat", "defines",
          "Definition of battery-assisted LOCC: the operation class is defined through the quantifier E.",
          "Eqs. (9)–(11)", "definition",
          note="Signature M∧O∧S→M: an operation class defined through an observable-layer node. In the released "
               "resource-theory network v1.2 no operation class is defined this way; its one witness→process edge "
               "(W15) is a bound, not a definition."),
        E("GB1", ["p-bat", "ax-add", "ax-mono", "ax-fin"], "t-conv", "necessary",
          "If ρ → σ under battery-assisted LOCC then E(ρ) ≥ E(σ).", "Theorem 1 (only if), Eq. (14)", "logic", cert_GB1,
          uses=["GB0"], method="SMT entailment with premise-minimality test"),
        E("GB2", ["p-bat", "s-bat"], "t-conv", "enables",
          "If E(ρ) ≥ E(σ) then ρ → σ: take τ = σ and swap A↔A', B↔B'; then τ~ = ρ.", "Theorem 1 (if), Eqs. (15)–(17)",
          "exact", cert_GB2, uses=["GB0"], method="symbolic permutation identity + SMT"),
        E("GB3", ["p-bat", "wQ-E"], "t-conv", "equiv",
          "ρ → σ under battery-assisted LOCC iff E(ρ) ≥ E(σ).", "Theorem 1, Eq. (3)", "logic", cert_GB3,
          uses=["GB1", "GB2"], method="SMT: equivalence from the two implications"),
        E("GB4", ["ax-add"], "wQ-E", "implies",
          "E(ρ^{⊗k}) = k E(ρ).", "used in Eqs. (19), (22), (30)", "logic", cert_GB4, method="SMT, induction step"),
        E("GB5", ["p-bat", "ax-add", "ax-mono", "ax-fin"], "t-rate", "bounds",
          "Zero-error rates satisfy m/n ≤ E(ρ)/E(σ).", "Eqs. (30)–(31)", "logic", cert_GB5, uses=["GB0", "GB4"],
          method="SMT, nonlinear"),
        E("GB6", ["p-bat", "s-bat"], "t-rate", "enables",
          "Every pair (n, m) with m E(σ) ≤ n E(ρ) is achieved exactly by relabelling, with battery σ^{⊗m} → ρ^{⊗n}.",
          "Eqs. (26)–(27)", "logic", cert_GB6, uses=["GB0", "GB4"], method="SMT"),
        E("GB7", ["t-rate"], "t-rate", "implies",
          "Rational rates m/n approach E(ρ)/E(σ) from below.", "Eq. (27)", "logic", cert_GB7, method="SMT with a floor witness"),
        E("GB8", ["p-bat", "wQ-E"], "t-rate", "equiv",
          "R_ze(ρ → σ) = E(ρ)/E(σ) for additive, monotone, finite E with E(σ) > 0.", "Eq. (29)", "logic",
          cert_GB8, uses=["GB5", "GB6", "GB7"], method="SMT: supremum argument with instantiated quantifiers"),
        E("GB9", ["p-bat", "ax-add", "ax-mono", "ax-fin", "ax-ac"], "t-rate", "bounds",
          "With error ε: m/n ≤ (E(ρ) + f(ε)/n)/(E(σ) − g(ε) log2 d) whenever g(ε) log2 d < E(σ).",
          "Eqs. (19)–(24)", "logic", cert_GB9, uses=["GB0", "GB4"], method="SMT, nonlinear, general modulus"),
        E("GB10", ["ax-ac"], "t-rate", "implies",
          "The bound of GB9 converges to E(ρ)/E(σ) as ε → 0.", "Eq. (25) and the sentence after it", "logic", cert_GB10,
          method="SMT, explicit ε–η estimate"),
        E("GB11", ["p-bat", "wQ-E", "ax-ac"], "t-rate", "equiv",
          "R(ρ → σ) = E(ρ)/E(σ) for finite, additive, monotone, asymptotically continuous E.", "Theorem 2, Eqs. (4), (18)",
          "logic", cert_GB11, uses=["GB9", "GB10", "GB6", "GB7"],
          method="SMT: supremum argument with instantiated quantifiers",
          note="A zero-error protocol is in particular an ε-error protocol, so GB6 and GB7 give achievability."),
        E("GB12", ["t-rate", "wQ-E"], "e-rev", "implies",
          "R(ρ→σ)·R(σ→ρ) = 1.", "text after Theorem 2", "logic", cert_GB12, uses=["GB11"], method="SMT"),
        E("GB13a", ["wQ-sq"], "ax-add", "satisfies",
          "E_sq is additive on tensor products and does not increase under LOCC.", "Methods; ref. [27]", "import",
          refs=["Christandl, Winter, J. Math. Phys. 45, 829 (2004)"],
          note="Monotonicity is needed (GB1) and has no dedicated citation in the paper; it is proved in the same reference [from knowledge]."),
        E("GB13b", ["wQ-sq"], "sF-ent", "equiv",
          "E_sq(ρ) = 0 iff ρ is separable; E_sq is finite; E_sq of a pure state is the entropy of entanglement.",
          "Methods; ref. [31]", "import", refs=["Li, Winter, Commun. Math. Phys. 326, 63 (2014)",
                                               "Christandl, Winter, J. Math. Phys. 45, 829 (2004)"]),
        E("GB13c", ["wQ-sq"], "ax-ac", "satisfies",
          "|E_sq(ρ) − E_sq(σ)| ≤ 16√(2ε) log d + 4h(2√(2ε)) for trace distance ≤ ε.", "Methods; ref. [32]", "import",
          refs=["Alicki, Fannes, J. Phys. A 37, L55 (2004), arXiv:quant-ph/0312081",
                "Christandl, PhD thesis, arXiv:quant-ph/0604183, Corollary 4.16"],
          note="The modulus is proportional to √ε. This satisfies ax-ac in the generalised form used by GB9, not the "
               "linear form of Eq. (13) as printed."),
        E("GB14", ["s-geo", "wQ-geo"], "ax-add", "violates",
          "E_g(ψ_d^{⊗n}) = E_g(φ+^{⊗n}) = 1 − 2^{−n} while S(ψ_d^A) = 1 + ½ log2(d−1); E_g is not additive.",
          "Eqs. (82)–(84)", "exact", cert_GB14, method="symbolic Schmidt spectrum"),
        E("GB15", ["wQ-geo", "p-bat"], "t-rate", "trivialises",
          "With E = E_g the battery condition permits φ+^{⊗n} → ψ_d^{⊗n} for every d, hence unbounded singlet yield.",
          "text around Eq. (84)", "compose", uses=["GB14", "GB2", "GB15i"],
          method="GB14 (equal E_g for every n; entropy unbounded in d) and GB2 (swap protocol) give φ+^{⊗n} → ψ_d^{⊗n}; "
                 "GB15i then distils ψ_d^{⊗n} to singlets at rate S(ψ_d^A), which exceeds any bound for large d"),
        E("GB15i", ["pF-ent"], "t-rate", "enables",
          "Pure states are distilled to singlets by LOCC at rate S(ψ^A).", "Ref. [8], section on asymptotic transformations; used after Eq. (84)", "import",
          refs=["Bennett, Bernstein, Popescu, Schumacher, Phys. Rev. A 53, 2046 (1996)"]),
        E("GB16", ["wQ-neg", "s-order"], "wQ-neg", "defines",
          "‖(|φ+><φ+|)^{T_A}‖₁ = 2; for σ_ε the trace norm is 1 + 2√(ε(1−ε)).", "Eq. (36); used in Eq. (77)", "exact",
          cert_GB16, method="symbolic eigenvalues"),
        E("GB17", ["wQ-neg", "p-bat"], "t-rate", "bounds",
          "With error ε the singlet rate under the E_N battery obeys m/n ≤ E_N(ρ) − (1/n)log2(1−ε).", "Eqs. (74)–(79)",
          "logic", cert_GB17, uses=["GB16", "GB17i"], method="SMT"),
        E("GB17i", ["wQ-neg"], "ax-add", "satisfies",
          "E_N is additive and LOCC monotone; ‖X^{T_A}‖₁ ≤ d_A‖X‖₁ (Eq. (76)).", "Eqs. (36), (76)", "import",
          refs=["Vidal, Werner, Phys. Rev. A 65, 032314 (2002)", "Plenio, Phys. Rev. Lett. 95, 090503 (2005)"],
          note="[from knowledge; page data not re-verified]"),
        E("GB18", ["p-thbat", "wQ-F"], "t-conv", "equiv",
          "(ρ,H) → (σ,H') with thermal operations and a free-energy battery iff F(ρ,H) ≥ F(σ,H').", "Theorem 3", "logic",
          cert_GB18, uses=["GB18i"], method="SMT (same two entailments as Theorem 1)"),
        E("GB18i", ["wQ-F"], "ax-add", "satisfies",
          "F is additive over non-interacting systems, non-increasing under thermal operations, finite for 0 < T < ∞; "
          "swapping system and battery with their Hamiltonians is a thermal operation.", "proof of Theorem 3", "import",
          refs=["Brandão et al., PNAS 112, 3275 (2015)", "Horodecki, Oppenheim, Nat. Commun. 4, 2059 (2013)"],
          note="[from knowledge]"),
        E("GB19", ["p-bat", "wQ-E"], "sF-ent", "defines",
          "The states reachable from separable states are exactly those with E = 0.", "main text, paragraph comparing with Ref. [7]",
          "logic", cert_GB19, uses=["GB3"], method="SMT",
          note="For E_sq the zero set is SEP (GB13b). For E_N it is the set of PPT states, so the E_N battery allows "
               "bound entangled states to be made from separable ones."),
        E("GB20", ["wQ-sq", "wQ-neg", "s-order"], "t-conv", "distinct",
          "The pre-orders induced by E_sq and by E_N disagree on (ρ_PPT, σ_ε): each allows the conversion the other forbids.",
          "consequence of Theorem 1; main text: a different quantifier gives a different second law", "logic", cert_GB20,
          uses=["GB3", "GB13b", "GB16", "GB17i", "GB20i"], method="exact limit + SMT"),
        E("GB20i", ["sR-ent"], "s-order", "hosts",
          "PPT entangled states exist.", "—", "import", refs=["P. Horodecki, Phys. Lett. A 232, 333 (1997)"]),
        E("GB21i", ["pX-ent", "ax-chan"], "e-rev", "forbids",
          "Under non-entangling operations, a fixed class of channels, entanglement manipulation is irreversible.",
          "ref. [7]", "import", refs=["Lami, Regula, Nat. Phys. 19, 184 (2023)"]),
        E("GB21e", ["p-bat", "ax-chan"], "p-bat", "violates",
          "The pair (swap, τ = σ) induces the replacement channel X ↦ σ on the system and is admitted only for inputs "
          "with E(ρ) ≥ E(σ): battery-assisted LOCC is not a class of non-entangling channels.",
          "main text, paragraph comparing with Ref. [7]: the operation may depend on the initial and final states", "exact", cert_GB21e,
          uses=["GB2"], method="symbolic partial trace + SMT"),
        E("GB21", ["p-bat", "pX-ent"], "e-rev", "consistent",
          "GB12 (reversibility) does not contradict the irreversibility under non-entangling operations.",
          "discussion of ref. [7]", "logic", uses=["GB12", "GB21i", "GB21e"],
          rule={"type": "scope_separation", "nogo": "GB21i", "possibility": "GB12", "premise": "ax-chan",
                "evidence": "GB21e"},
          method="kernel rule: scope separation"),
        E("GB22", ["p-bat"], "p-cat", "distinct",
          "Battery-assisted LOCC is not catalysis: the battery may change state; only E(τ~) ≥ E(τ) is required.",
          "Eq. (37) and text", "definition"),
    ]

    claims = [
        Claim("A-C1", "Theorem 1: ρ can be converted into σ via LOCC with an entanglement battery iff E(ρ) ≥ E(σ), "
              "for additive, finite E.", "Theorem 1", ["GB3"]),
        Claim("A-C2", "Theorem 2: the asymptotic rate is R(ρ→σ) = E(ρ)/E(σ) for finite, additive, asymptotically "
              "continuous E.", "Theorem 2", ["GB11"]),
        Claim("A-C3", "Arbitrary mixed-state transformations are reversible: R(ρ→σ)R(σ→ρ) = 1.", "abstract", ["GB12"]),
        Claim("A-C4", "The theorems are not vacuous: squashed entanglement satisfies the hypotheses.", "Methods",
              ["GB13a", "GB13b", "GB13c"]),
        Claim("A-C5", "Without additivity the construction trivialises (geometric entanglement).", "Supplement, Eqs. (80)–(84)",
              ["GB15"]),
        Claim("A-C6", "Theorem 3: the same statement for thermal operations with a free-energy battery.", "Theorem 3", ["GB18"]),
        Claim("A-C7", "The result is compatible with the no-second-law theorem for non-entangling operations.",
              "discussion", ["GB21"]),
    ]

    delta = [
        {"op": "ADD", "node": "p-bat", "layer": "M.process",
         "why": "new operation class; closes the entanglement row of gap QG9 ('entanglement-battery second law, arXiv:2405.10599 [verify]')"},
        {"op": "ADD", "node": "wQ-sq", "layer": "O.witness (quantifier)",
         "why": "the quantifier that makes Theorems 1–2 non-vacuous; currently absent from wQ-ent"},
        {"op": "ROUTE", "edge": "pF-ent ∧ wQ-E ∧ s-bat → p-bat",
         "why": "AND route into a process node with a witness-layer leg: the first operation class in the "
                "resource-theory network that is defined through a quantifier"},
        {"op": "ADD", "edge": "p-bat —reversible→ sR-ent (rate E(ρ)/E(σ); via LOCC + battery relative to E)",
         "why": "Theorem 2; kernel-checked modulo the imported properties of E"},
        {"op": "SCOPE", "edge": "W15", "note": "'no single monotone can govern all transformations' holds for LOCC and "
         "for non-entangling operations; under p-bat(E) the single monotone E governs all transformations by construction"},
        {"op": "SCOPE", "edge": "C18", "note": "replace 'candidate route around pX-ent via entanglement batteries (QG9)' "
         "by the theorem, with the distinction battery ≠ catalyst (GB22)"},
        {"op": "CITE", "gap": "QG9", "note": "citation verified: Phys. Rev. Lett. 135, 010202 (2025), DOI 10.1103/kl56-p2vb"},
        {"op": "OPEN", "edge": "wQ-(E_r^∞) → ax-add", "note": "full additivity of the regularised relative entropy of "
         "entanglement is stated as unknown in the paper; if it held, p-bat(E_r^∞) would reproduce the rate of F-STEIN"},
    ]

    findings = [
        {"level": "premise", "title": "Form of asymptotic continuity",
         "text": "Eq. (13) is linear in the trace norm, K‖ρ−σ‖₁ log2 d + f. The bound available for squashed "
                 "entanglement from the cited route (Alicki–Fannes; Christandl's thesis, Cor. 4.16) is "
                 "16√(2ε) log d + 4h(2√(2ε)), which is not of that form. GB9–GB10 prove Theorem 2 for any modulus "
                 "g(ε) log2 d + f(ε) with g, f → 0, so the theorem holds for E_sq; the premise node ax-ac is stated in "
                 "that weaker form."},
        {"level": "premise", "title": "Monotonicity is a premise of Theorem 1",
         "text": "The statement lists 'additive and finite'; the SMT minimality test shows LOCC monotonicity is also "
                 "needed for the 'only if' direction (it is implied by 'entanglement measure' in the text). Eq. (21) "
                 "uses f(ε) for a distance < ε, which needs f nondecreasing (or its monotone envelope)."},
        {"level": "structure", "title": "What each direction uses",
         "text": "Achievability (GB2, GB6) is a relabelling of system and battery whose initial battery state is the "
                 "target; it uses no property of E. The converse (GB1, GB5, GB9) is three lines of additivity and "
                 "monotonicity. The operation class is defined through E (GB0), so each admissible E gives its own theory."},
        {"level": "derived", "title": "Free set and order reversal (elementary corollaries, not claimed as new)",
         "text": "GB19: the free states of the theory are the zero set of E — SEP for E_sq, all PPT states for E_N. "
                 "GB20: E_sq and E_N order the pair (PPT entangled state, weakly entangled pure state) oppositely."},
        {"level": "not encoded", "title": "Parts of the paper outside this encoding",
         "text": "Proposition 4 (continuity of E_r with a battery), the results for E_r and E_r^∞, the correlated-"
                 "battery variant of the Supplement and the multipartite extension were not encoded."},
    ]

    return Paper(
        key="battery",
        citation="R. Ganardi, T. V. Kondra, N. H. Y. Ng, A. Streltsov, Second Law of Entanglement Manipulation with an "
                 "Entanglement Battery, Phys. Rev. Lett. 135, 010202 (2025)",
        ids={"doi": "10.1103/kl56-p2vb", "arxiv": "2405.10599"},
        branch="Resource-theory branch (GEN_QRT_Level v1.2)",
        summary="Adds an auxiliary bipartite 'battery' whose entanglement, measured by a chosen quantifier E, may not "
                "decrease, and shows that LOCC assisted in this way converts ρ into σ iff E(ρ) ≥ E(σ), with asymptotic "
                "rate E(ρ)/E(σ); hence reversibility.",
        nodes=nodes, edges=edges, claims=claims, delta=delta, findings=findings, year=2025,
        phases=[["hypothesize", "a new operation class, LOCC with a battery, is proposed"],
                ["restructure", "the process layer gains a node that is defined through a quantifier"],
                ["predict", "conversion rates E(ρ)/E(σ) for every pair of states"]],
        sources=[
            {"title": "Ganardi et al., PRL 135, 010202 (2025)", "url": "https://journals.aps.org/prl/abstract/10.1103/kl56-p2vb"},
            {"title": "arXiv:2405.10599v2", "url": "https://arxiv.org/html/2405.10599v2"},
            {"title": "Alicki, Fannes, arXiv:quant-ph/0312081", "url": "https://arxiv.org/abs/quant-ph/0312081"},
            {"title": "Christandl, PhD thesis, arXiv:quant-ph/0604183", "url": "https://arxiv.org/pdf/quant-ph/0604183"},
        ],
    )
