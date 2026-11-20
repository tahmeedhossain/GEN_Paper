"""
Negative controls for the kernel.

A checker that never fails proves nothing. Each control below plants one error in a
statement that the kernel accepted in its correct form and requires the same check to
REJECT it. `run()` returns one record per control; `detected` must be True for all.
"""
import sympy as sp
import z3

import exact as ex
import paper_battery as PB
import paper_realqm as PR
import paper_top as PT
from exact import Alg
from kernel import smt_entails


def _c(name, planted, detected, detail=""):
    return {"control": name, "planted_error": planted, "detected": bool(detected), "detail": detail}


def run():
    out = []

    # --- SMT entailment -------------------------------------------------------------
    Er, Es, Et, Et2, Ein, Eout = z3.Reals("E_rho E_sigma E_tau E_tau2 E_in E_out")
    prem = {"add_in": Ein == Er + Et, "add_out": Eout == Es + Et2, "mono": Eout <= Ein, "battery": Et2 >= Et}
    ok, _ = smt_entails(prem, Es >= Er, minimality=False)
    out.append(_c("battery necessity, reversed conclusion", "claim E(σ) ≥ E(ρ) instead of E(σ) ≤ E(ρ)", not ok))
    ok, _ = smt_entails({k: v for k, v in prem.items() if k != "mono"}, Es <= Er, minimality=False)
    out.append(_c("battery necessity without monotonicity", "drop LOCC monotonicity", not ok))
    ok, _ = smt_entails({"add_in": Ein == Er + Et, "subadd_out": Eout <= Es + Et2, "mono": Eout <= Ein,
                         "battery": Et2 >= Et}, Es <= Er, minimality=False)
    out.append(_c("battery necessity with subadditivity only", "replace additivity on the output by E(σ⊗τ~) ≤ E(σ)+E(τ~)",
                  not ok, "a merely subadditive quantifier does not give Theorem 1"))

    # --- exact permutation identity ---------------------------------------------------
    c = PB._swap_check(2, 2, alice_only=True)
    out.append(_c("swap protocol with Alice's swap only", "Bob does not swap B and B'",
                  not c["W (X⊗Y) W^T = Y⊗X for symbolic X, Y"]))

    # --- block-matrix algebra -----------------------------------------------------------
    d = sp.Symbol("d", positive=True, integer=True)
    A1, A2, B1, B2 = (sp.MatrixSymbol(n, d, d) for n in ("A1", "A2", "B1", "B2"))
    Zd = sp.ZeroMatrix(d, d)
    T = lambda P, Q: PR.T_block(P, Q, sign=-1)          # [[P,-Q],[-Q,P]]: off-diagonal part squares to +1
    ok = PR.blocks_equal(T(A1, A2) * T(B1, B2), T(A1 * B1 - A2 * B2, A1 * B2 + A2 * B1), Zd)[0]
    out.append(_c("T with a 'J' that squares to +1", "T(A) = [[A1,-A2],[-A2,A1]]", not ok,
                  "multiplicativity fails without J² = −1"))

    # --- exact network computation ------------------------------------------------------
    tc = PR._tables()["c"]
    tr, _ = PR._real_table(product_flags=True)
    same = all(tr[f][k] == v for f in ("Pb", "APi", "PiC", "S") for k, v in tc[f].items())
    total = sum((tr["Pb"][b] for b in tr["Pb"]), Alg(0))
    out.append(_c("real model with product flag state", "flags of the two sources in ψ_even^(2)⊗ψ_even^(2) instead of ψ_even^(4)",
                  not same, f"Σ_b <Π_b> = {total} instead of 1: the product vector is not a state of the model"))
    T_b2, _ = PR._T_values(tc, fifth="b2", weighting="plain-sum-joint")
    out.append(_c("network functional with the printed prefactor", "(−1)^{b2} on (S_25 + S_26)", T_b2 != Alg(0, 6),
                  f"T = {T_b2}"))
    # Charlie measures real observables only (Y dropped from his settings): the value must change
    A_ops, C_ops, Pi = PR._settings()
    psi = ex.kronv(ex.bell("phi+"), ex.bell("phi+")).reshape([2] * 4)
    S33 = ex.expect(psi, [(A_ops[2], [0]), (Pi["00"], [1, 2]), (ex.re_part(C_ops[2]), [3])])
    out.append(_c("Charlie's C3 with its imaginary part removed", "C3 = Z/√2 instead of (Y+Z)/√2",
                  S33 != tc["S"][("00", 3, 3)], f"<A3 Π00 C3> = {S33} instead of {tc['S'][('00', 3, 3)]}"))

    # --- Dirac traces -----------------------------------------------------------------------
    W, k, identity, no_mb, rest_ok, kappa = PT._decay_cert("top", quark_chirality="R")
    out.append(_c("top decay with a right-handed quark current", "γ^μ P_R instead of γ^μ P_L at the t–b–W vertex",
                  not identity, "the squared amplitude is no longer proportional to (p_b·p_ν)((p_t − m s)·p_ℓ)"))

    # --- witness bound ------------------------------------------------------------------------
    a, b = sp.Matrix(sp.symbols("a0:3", real=True)), sp.Matrix(sp.symbols("b0:3", real=True))
    wrong = sp.expand(2 * (sp.Rational(1, 2) + a.dot(b)) - ((a + b).dot(a + b) + (1 - a.dot(a)) + (1 - b.dot(b)))) == 0
    out.append(_c("separability bound tr C ≥ −1/2", "claim a stronger bound than −1", not wrong,
                  "the sum-of-squares identity does not hold; |↑↓> attains −1"))
    sep = z3.Bool("separable")
    D = z3.Real("D")
    ok, _ = smt_entails({"sep ⇒ D ≥ −1/3": z3.Implies(sep, D >= -z3.Q(1, 3)), "measured": D < -z3.Q(3, 10)},
                        z3.Not(sep), minimality=False)
    out.append(_c("witness with a value above the bound", "conclude entanglement from D < −0.30", not ok))

    # --- kernel rule ---------------------------------------------------------------------------
    import kernel
    p = PR.build()
    for e in p.edges:
        if e.id == "RQ20":
            e.rule = dict(e.rule, premise="s-indep")       # a premise that the possibility edge also uses
    res = kernel.run_paper(p, verbose=False)
    st = [e for e in res["edges"] if e["id"] == "RQ20"][0]["status"]
    out.append(_c("scope separation with a shared premise", "name a premise that both edges use", st == "FAILED"))

    # --- decay-contextuality paper (generated work): the 16 planted errors of its own encoding ---------------
    import paper_decay
    dc = paper_decay.controls_module()
    for k in dc.CONTROLS:
        try:
            r = k()
        except Exception as err:                 # a crashing control counts as not detected
            r = {"rejected": False, "detail": f"control raised {type(err).__name__}: {err}"}
        out.append(_c(f"decay paper {k.__name__}", (k.__doc__ or "").strip(), r["rejected"], str(r["detail"])))
    return out


if __name__ == "__main__":
    recs = run()
    for r in recs:
        print(("detected " if r["detected"] else "MISSED   ") + r["control"] + " — " + r["detail"])
    print(f"{sum(r['detected'] for r in recs)}/{len(recs)} planted errors detected")
