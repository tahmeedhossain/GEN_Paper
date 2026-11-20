"""
Reading order of the four encoded papers (three published papers and one generated work).

For each paper: the units of the text in the order in which they are read, and for each unit
    nodes     : nodes whose first appearance is in this unit,
    announce  : routes stated in this unit while their support is located in a later unit,
    establish : routes whose support is located in this unit, with the kind of support the PAPER gives:
                  definition   a definition or construction
                  proof        a derivation written out in the paper
                  citation     a cited reference (literature fill)
                  measurement  a measured value with its analysis chain
                  simulation   a value obtained from simulated samples
                  certificate  supported by an executed program to which the text points, with no derivation at that
                               place (used for the generated decay paper, whose catalogue lists a certificate per route)
                  asserted     stated with at most a verbal reason; no derivation and no reference
                  implicit     used inside a derivation of the paper without being stated
    partial   : a unit that supplies part of the support of a route established later or earlier.

ADDED lists the routes (and nodes) of the encoding that have no counterpart in the text; they are shown
with the unit they refer to and are excluded from every count of the replay.

Sources of the order.  Section headings, equation numbers, theorem labels, cited reference numbers and the
position of each statement were taken from the arXiv texts
    battery : arXiv:2405.10599v2 (HTML),
    realqm  : arXiv:2503.17307 (PDF, equation numbers (1)-(124)),
    top     : arXiv:2311.07288v3 (PDF),
read through an automatic page reader on 2026-11-19.  Paragraph labels (A1.., C1.., T1.., M1..) are that
reader's segmentation and are approximate; headings and equation numbers are the anchors.  The assignment of
nodes and routes to units is made by hand from those anchors and from the `where` field of each route.

    decay   : the generated paper in decay_contextuality/paper (LaTeX source of 17 Nov 2026, rebuilt on 2026-11-20);
              section, equation, theorem and table numbers are resolved from the labels of the compiled text
              (paper_decay.LABELS, read from main.aux), so a location string such as "Sec. {sec:va}" prints as in
              the PDF.  The order was assigned on 2026-11-20 by reading that source.
"""

SUPPORTS = ("definition", "proof", "citation", "measurement", "simulation", "certificate", "asserted", "implicit")


def U(uid, block, label, loc, text, nodes=(), announce=(), establish=None, partial=None, encoded=True, pointers=()):
    return {"id": uid, "block": block, "label": label, "loc": loc, "text": text, "nodes": list(nodes),
            "announce": list(announce), "establish": dict(establish or {}), "partial": dict(partial or {}),
            "encoded": encoded, "pointers": list(pointers)}


# ---------------------------------------------------------------------------------------------------------------
BATTERY = {
    "key": "battery",
    "text_version": "arXiv:2405.10599v2",
    "units": [
        U("b0", "abstract", "Abstract", "abstract",
          "Names the battery and announces the results: mixed-state conversions become reversible under LOCC with a battery; "
          "the asymptotic rate is a ratio of entanglement; different quantifiers give different second laws.",
          nodes=["sR-ent", "pF-ent", "s-bat", "p-bat", "wQ-E", "t-conv", "t-rate", "e-rev"],
          announce=["GB11", "GB12", "GB20"]),
        U("b1", "main", "Introduction", "untitled opening, paragraphs A1–A6",
          "Second-law question; earlier work; the battery is introduced as a generalised catalyst; preview of the rate E(ρ)/E(σ).",
          nodes=["p-cat"], announce=["GB22", "GB11", "GB20"]),
        U("b2", "main", "Asymptotic transformations of entangled states and reversibility", "B1–B6",
          "Rates and reversibility are defined; pure-state rates are recalled from Ref. [8]; irreversibility under non-entangling "
          "operations is recalled from Ref. [7].",
          nodes=["pX-ent"], establish={"GB15i": "citation", "GB21i": "citation"}),
        U("b3", "main", "Reversible manipulations with a battery: the setting", "C1–C6, Eqs. (1)–(2)",
          "The transformation ρ⊗τ → σ⊗τ~ and the battery condition E(τ~) ≥ E(τ) define the operation class; the required "
          "properties of E are listed.",
          nodes=["ax-mono", "ax-add", "ax-ac", "ax-fin"], announce=["GB20"], establish={"GB0": "definition"}),
        U("b4", "main", "Theorem 1", "C7–C9, Eq. (3)",
          "Theorem 1 is stated with an outline of its proof (monotonicity for necessity, a swap with the battery for sufficiency).",
          announce=["GB3", "GB1", "GB2"], pointers=["Methods: proof of Theorem 1"]),
        U("b5", "main", "Theorem 2 and reversibility", "C10–C13, Eq. (4)",
          "Theorem 2 is stated with an outline; R(ρ→σ)·R(σ→ρ) = 1 is concluded from it.",
          announce=["GB11", "GB9", "GB6"], establish={"GB12": "proof"}, pointers=["Methods: proof of Theorem 2"]),
        U("b6", "main", "Quantifiers that qualify", "C14–C19, Eqs. (5)–(6)",
          "Squashed entanglement is named as a quantifier with the required properties; the regularised relative entropy and "
          "logarithmic negativity are discussed; multipartite extension.",
          nodes=["wQ-sq", "wQ-neg"], announce=["GB13a", "GB13b", "GB13c", "GB17"],
          pointers=["Methods: properties of squashed entanglement", "Methods: another example", "Methods: E_r^∞",
                    "Methods: logarithmic negativity"]),
        U("b7", "main", "Relation to Ref. [7]; correlations; geometric entanglement", "C20–C22",
          "The result is contrasted with the no-go of Ref. [7] (the operation may depend on the initial and final states); "
          "entanglement cannot be created from separable states; geometric entanglement does not constrain conversions.",
          nodes=["ax-chan", "sF-ent", "wQ-geo"], announce=["GB15"],
          establish={"GB19": "asserted", "GB21e": "asserted", "GB21": "asserted"},
          pointers=["Supplemental: correlations", "Supplemental: geometric entanglement"]),
        U("b8", "main", "Quantum thermodynamics", "D1–D10, Eqs. (7)–(8)",
          "Free energy and the free-energy battery; Theorem 3 is stated.",
          nodes=["wQ-F", "p-thbat"], announce=["GB18"]),
        U("b9", "main", "Conclusions", "E1–E4", "Summary and outlook; no new node or route."),
        U("b10", "methods", "Methods: LOCC with entanglement battery", "Eqs. (9)–(11)",
          "Formal definition of the exact, approximate and asymptotic tasks.", partial={"GB0": "formal restatement"}),
        U("b11", "methods", "Methods: proof of Theorem 1", "Eqs. (12)–(17)",
          "Additivity (12) and asymptotic continuity (13) are written out; necessity by Eq. (14); sufficiency by the swap, Eqs. (15)–(17).",
          establish={"GB1": "proof", "GB2": "proof", "GB3": "proof"}),
        U("b12", "methods", "Methods: proof of Theorem 2", "Eqs. (18)–(27)",
          "Upper bound on the rate, Eqs. (19)–(25); achievability by relabelling with a battery of copies, Eqs. (26)–(27).",
          establish={"GB4": "implicit", "GB9": "proof", "GB10": "proof", "GB6": "proof", "GB7": "proof", "GB11": "proof"}),
        U("b13", "methods", "Methods: proof of Theorem 3", "no numbered equation",
          "Both directions of Theorem 3; the properties of the free energy are stated without reference.",
          establish={"GB18i": "asserted", "GB18": "proof"}),
        U("b14", "methods", "Methods: zero-error conversion", "Eqs. (28)–(31)",
          "The zero-error rate equals E(ρ)/E(σ) without asymptotic continuity.",
          establish={"GB5": "proof", "GB8": "proof"}),
        U("b15", "methods", "Methods: measures that are additive and asymptotically continuous", "Eqs. (32)–(34)",
          "Properties of squashed entanglement, each with its reference: additivity [27], faithfulness [31], asymptotic continuity [32].",
          establish={"GB13a": "citation", "GB13b": "citation", "GB13c": "citation"}),
        U("b16", "methods", "Methods: other entanglement measures", "Eqs. (35)–(36)",
          "Relative entropy of entanglement; logarithmic negativity is defined and said to allow PPT states from separable states.",
          nodes=["s-order"], announce=["GB17i"], establish={"GB16": "definition", "GB20": "asserted"},
          pointers=["Supplemental: bounded rates for E_r and E_N"]),
        U("b17", "supplement", "Supplemental: connection to catalysis", "Eq. (37)",
          "Exact catalysis is defined; a battery only has to keep its entanglement.", establish={"GB22": "definition"}),
        U("b18", "supplement", "Supplemental: relative entropy of entanglement", "Eqs. (38)–(69), Proposition 4",
          "Not encoded: no route of the encoding refers to this section.", encoded=False),
        U("b19", "supplement", "Supplemental: logarithmic negativity", "Eqs. (71)–(79)",
          "The singlet rate under the E_N battery is bounded by E_N(ρ); additivity and monotonicity from Ref. [29], Eq. (76) from Ref. [62].",
          establish={"GB17i": "citation", "GB17": "proof"}),
        U("b20", "supplement", "Supplemental: geometric entanglement", "Eqs. (80)–(84)",
          "An explicit family of states shows that E_g is not additive; the theory with E_g is trivial.",
          nodes=["s-geo"], establish={"GB14": "proof", "GB15": "asserted"}),
        U("b21", "supplement", "Supplemental: correlations between main system and battery", "Eqs. (85)–(106)",
          "Not encoded: no route of the encoding refers to this section.", encoded=False),
        U("b22", "supplement", "Supplemental: self-dilution in thermodynamics", "Eqs. (107)–(111)",
          "Not encoded: no route of the encoding refers to this section.", encoded=False),
    ],
    "added": {
        "routes": {"GB20i": ("b16", "existence of PPT entangled states; not cited at this place in the paper")},
        "nodes": {},
    },
    "notes": [
        "s-order is an instance pair chosen by the encoding to exhibit GB20; the paper states the general claim (C5) and the PPT remark (Methods).",
        "GB0: Eqs. (1)–(2) define the exact single-copy class; Eqs. (9)–(11) restate it with error and rates.",
        "GB4 (E(ρ^{⊗k}) = kE(ρ)) is used in Eqs. (19), (22), (30) without being stated.",
    ],
}

# ---------------------------------------------------------------------------------------------------------------
REALQM = {
    "key": "realqm",
    "text_version": "arXiv:2503.17307 (equation numbers (1)–(124))",
    "units": [
        U("q0", "abstract", "Abstract", "paragraph T1",
          "Recalls the claim that real-number quantum mechanics can be falsified; announces a real-number formulation that "
          "reproduces all multipartite predictions, and the conclusion that complex numbers are a matter of convenience.",
          nodes=["m-quantum", "m-realqm", "m-realflag", "t-distinguish"], announce=["RQ17", "RQ19", "RQ21"]),
        U("q1", "main", "Introduction", "T2–T7",
          "Earlier real formulations; Renou et al. [12] and the experiments; a locality requirement is proposed in place of the "
          "tensor-product postulate; the construction is announced as a quotient space in one-to-one correspondence with complex QM.",
          nodes=["ax-tensorR", "e-net"], announce=["RQ17", "RQ19", "RQ9"]),
        U("q2", "main", "Postulates (P1)–(P4)", "T8",
          "(P1)–(P3) as in Ref. [12]; (P4): operators of A act trivially on B and conversely.",
          nodes=["ax-P4"], pointers=["Section E: formal (P4)"]),
        U("q3", "main", "Single system: the state map", "T9–T11, Eqs. (1)–(2)",
          "S maps a complex vector to a real vector with a flag; a global phase becomes a rotation of the flag.",
          nodes=["s-C", "f-real", "s-Rflag"], announce=["RQ2"]),
        U("q4", "main", "Single system: operators and expectation values", "T12–T13, Eqs. (3)–(6)",
          "T(Π), I_F and J_F; expectation values are preserved for single systems.",
          nodes=["ax-complex"], announce=["RQ1"],
          pointers=["Section A: projector form", "Section C: alternative derivation", "Section D: observables"]),
        U("q5", "main", "The naive tensor extension fails", "T14–T16",
          "Parameter count 8 against 16 and the phase ambiguity; an explicit two-qubit example; the inverse map is extended instead.",
          nodes=["s-indep"], announce=["RQ15"], pointers=["Section B: multipartite states"]),
        U("q6", "main", "Composite systems: quotient space and canonical representatives", "T17–T18, Eqs. (7)–(8)",
          "Flag classes and their canonical representatives; separability is defined.",
          nodes=["s-canon"], establish={"RQ4": "definition"}, pointers=["Section A: flag basis", "Section G: comparison with Ref. [8]"]),
        U("q7", "main", "Composite systems: predictions", "T19",
          "Eq. (6) is claimed for composite systems; the formulation of the experiment of Renou et al. is deferred.",
          nodes=["o-born"], announce=["RQ10", "RQ5", "RQ12"], pointers=["Section A", "Section H: Renou et al."]),
        U("q8", "main", "(P4) and reduced states", "T20",
          "(P4) holds through local flag operators; reduced density operators by partial trace.",
          announce=["RQ8", "RQ3"], pointers=["Section E", "Section F"]),
        U("q9", "main", "Summary", "T21",
          "Same predictions as complex QM; the tensor-product postulate is criticised; complex numbers are not necessary but useful.",
          establish={"RQ19": "asserted", "RQ20": "asserted", "RQ21": "asserted"}),
        U("q10", "supplement", "A. Uniqueness of the mapping", "Eqs. (9)–(39), Propositions 1–3",
          "Propositions 1 and 2 force the flag structure and the form of T; Proposition 3: S(ψ⊗φ) ≅ S(ψ) ⊗_F S(φ).",
          establish={"RQ5": "proof"}, partial={"RQ1": "Proposition 2"}),
        U("q11", "supplement", "B. State map: general case", "Eqs. (40)–(51), Remarks 4–5",
          "Even and odd flag vectors for N parties; Remark 5: they are not preserved by the tensor product.",
          establish={"RQ6": "proof", "RQ15": "proof"}, partial={"RQ5": "Eq. (51)", "RQ4": "projector, Eqs. (43)–(44)"}),
        U("q12", "supplement", "C. Alternative derivation of the map for operators", "Eqs. (52)–(61)",
          "I^(N), J^(N) and their product relations; composite operators.",
          establish={"RQ7": "proof", "RQ9": "proof"}),
        U("q13", "supplement", "D. Further properties of the construction", "Eqs. (62)–(70), Propositions 6–7",
          "Hermitian operators map to symmetric ones, unitaries to orthogonal ones; inner products and expectation values.",
          establish={"RQ1": "proof", "RQ18": "proof", "RQ2": "proof"}, partial={"RQ10": "Eq. (68)"}),
        U("q14", "supplement", "E. Formalisation of postulate (P4)", "Eqs. (71)–(82), Definitions 8–10, Proposition 11",
          "Independent preparation, local operation, formal (P4); Proposition 11: the construction satisfies it.",
          establish={"RQ8": "proof"}),
        U("q15", "supplement", "F. Density operators and reduced density operators", "Eqs. (83)–(94)",
          "The map for density operators; invariance of tr(ρA); partial traces of I^(N), J^(N).",
          establish={"RQ3": "proof", "RQ10": "proof"}, partial={"RQ7": "Eq. (91)"}),
        U("q16", "supplement", "G. Myrheim approach", "Eqs. (95)–(103)",
          "Not encoded: no route of the encoding refers to this section.", encoded=False),
        U("q17", "supplement", "H. Renou et al.: complex calculation", "Eqs. (104)–(112)",
          "The network functional; its value 6√2 in complex QM; the bound 7.6605 of Ref. [12] for real models with the tensor postulate.",
          nodes=["w-T"], establish={"RQ13": "definition", "RQ11": "proof", "RQ17": "citation"}),
        U("q18", "supplement", "H. Renou et al.: real-number calculation", "Eqs. (113)–(124)",
          "Real states and operators for the same network; the reduced state after Bob's outcome; the same probabilities and 6√2.",
          establish={"RQ14": "proof", "RQ12": "proof"}),
    ],
    "added": {
        "routes": {"RQ16": ("q5", "dimension count behind local tomography; a check of the encoding, not a statement of the paper")},
        "nodes": {"ax-loctom": "q5"},
    },
    "notes": [
        "Propositions 1 and 2 (uniqueness) are announced in the main text and are not encoded as a route.",
        "RQ7: the product relations are in Section C; the partial-trace identity of its statement is Eq. (91) of Section F.",
        "RQ17 is cited in general terms in T5; the network and the number 7.6605 appear in Section H.",
    ],
}

# ---------------------------------------------------------------------------------------------------------------
TOP = {
    "key": "top",
    "text_version": "arXiv:2311.07288v3",
    "units": [
        U("t0", "abstract", "Abstract", "abstract",
          "Entanglement of top–antitop pairs is reported from one observable D, measured from the angle between the charged "
          "leptons near threshold: D = −0.537 ± 0.002 ± 0.019, more than five standard deviations from no entanglement.",
          nodes=["s_t", "s_lep", "s-ent", "s-ttavg", "o-cosphi", "w-D", "o-Dobs", "e-ttent", "m-mc"],
          announce=["TQ11", "TQ14", "TQ15"]),
        U("t1", "main", "Main: colliders, the top quark as a qubit", "M1–M3",
          "Motivation; the top quark decays before its spin decorrelates; the five-standard-deviation result is restated.",
          announce=["TQ15"]),
        U("t2", "main", "Main: spin density matrix", "M4–M6, first displayed equation",
          "ρ of the pair in terms of B±, C; strong production gives no polarisation.",
          nodes=["s-ttspin", "m_A", "m-qcd"], establish={"TQ1": "definition"}),
        U("t3", "main", "Main: decay and lepton distribution", "M7–M8, second displayed equation",
          "The charged leptons carry the spin information (parity violation of the charged current); the normalised distribution "
          "in the two lepton directions, from Ref. [27].",
          nodes=["s_W", "s_b", "m_cc", "o-lepdir", "o-joint"],
          establish={"TQ2": "asserted", "TQ3": "asserted", "TQ5": "citation"}),
        U("t4", "main", "Main: threshold, singlet, trace witness", "M9",
          "About 80% of gluon-fusion production near threshold is a spin singlet [28–30]; after averaging over top directions "
          "tr[C] + 1 < 0 is sufficient for entanglement [18].",
          nodes=["d-singlet", "s-sep"], establish={"TQ12": "citation", "TQ7": "citation", "TQ9": "citation"}),
        U("t5", "main", "Main: the marker D", "M10, third displayed equation",
          "D = tr[C]/3 [18]; D = −3⟨cos φ⟩ is given as the way to measure it.",
          establish={"TQ6": "asserted", "TQ6b": "definition"}),
        U("t6", "main", "Main: the criterion D < −1/3", "M11–M12",
          "D < −1/3 demonstrates entanglement, from the Peres–Horodecki criterion [35, 36]; a restricted phase space is needed.",
          establish={"TQ8": "citation", "TQ11": "citation"}),
        U("t7", "main", "1.1 Detector and event samples", "section 1.1",
          "Detector, data set, simulated samples; detector, particle and parton levels.",
          pointers=["Methods A.1", "Methods A.2", "Methods A.6"]),
        U("t8", "main", "1.2 Analysis procedure", "P1–P10",
          "Selection, signal window 340–380 GeV, calibration curve from reweighted samples, uncertainties; a second curve folds "
          "the bound −1/3 to particle level.",
          nodes=["o-limit"], announce=["TQ13"], pointers=["Methods A.3", "Methods A.5"]),
        U("t9", "main", "1.3 Results", "R1–R3",
          "Observed −0.537 ± 0.002 ± 0.019 (expected −0.470 ± 0.002 ± 0.017); folded bound −0.322 ± 0.009 (Powheg+Pythia), −0.27 (Powheg+Herwig).",
          establish={"TQ14": "measurement", "TQ13": "simulation"}, pointers=["Methods A.5"]),
        U("t10", "main", "1.4 Discussion", "D1–D5",
          "Validation regions; effects absent from the generators; the result is well beyond five standard deviations from no entanglement.",
          establish={"TQ15": "measurement"}, pointers=["Methods A.6"]),
        U("t11", "methods", "Methods A.1–A.2", "objects, simulation",
          "Not encoded: no route of the encoding refers to these sections.", encoded=False),
        U("t12", "methods", "Methods A.3: reweighting the cos φ distribution", "two displayed equations",
          "The linear form of the cos φ distribution and the reweighting used for the calibration curve.",
          partial={"TQ6": "linear form of the distribution", "TQ13": "construction of the curve", "TQ14": "construction of the curve"}),
        U("t13", "methods", "Methods A.4–A.6", "backgrounds, uncertainties, parton shower",
          "Not encoded as routes: these sections supply the uncertainties of the measured values.", encoded=False,
          partial={"TQ13": "uncertainties", "TQ14": "uncertainties"}),
    ],
    "added": {
        "routes": {
            "TQ4": ("t3", "intermediate step of the regeneration of the lepton distribution; the paper cites the result"),
            "TQ10": ("t4", "range of D and its value for the singlet; not stated in the paper"),
            "TQ16": ("t9", "difference of the two values given in R1; the paper does not comment on it"),
            "TQ17": ("t6", "scope remark of the encoding; the paper does not mention Bell tests"),
        },
        "nodes": {},
    },
    "notes": [
        "TQ9: the location recorded on 2026-11-17 pointed to a phrase of M11 about the order of the calculation, whose meaning the "
        "text does not fix; the statement on averaging over the top-quark directions is in M9.",
        "TQ1 and TQ12 were recorded under 'Methods' on 2026-11-17; in arXiv v3 both are in section 1 (Main).",
        "TQ6: the relation ⟨cos φ⟩ = −D/3 is used in M10; the linear form of the distribution is in Methods A.3; neither is derived.",
    ],
}

# ---------------------------------------------------------------------------------------------------------------
# Generated work: T. Hossain with Claude (Anthropic), 17 November 2026, unpublished, not peer reviewed.
# Location strings carry label placeholders {label}; resolve_locations() replaces them by the numbers of the
# compiled text (paper_decay.LABELS).
DECAY = {
    "key": "decay",
    "text_version": "generated paper, decay_contextuality/paper (source of 2026-11-17, compiled 2026-11-20)",
    "units": [
        U("d0", "abstract", "Abstract", "abstract",
          "A decay is one fixed rotation-covariant measurement; single-setting data violate no Bell or steering inequality "
          "because the recorded directions are local hidden variables; the existence of a generalized-noncontextual model is "
          "decided exactly for spin 1/2 (P|κ| ≤ 1/3; ρ_raw and its partial transpose positive; ‖c‖₁ ≤ 1 and |D| ≤ 1/3), spin 1 "
          "(region R, pair region R₂, visibility 5/8) and spin j (ξ_2j, first-moment bound); muon and top decays, the ATLAS and "
          "CMS values of D and the BESIII ΛΛ̄ data; the results as routes of a concept graph.",
          nodes=["p-decay", "e-bell", "e-steer", "m-lhv1", "m-ncom", "u_mh", "p-half", "o-ang2", "w-rawppt", "s-tstate", "o-D",
                 "u_m1", "p-one", "w-region1", "s-iso1", "w-kappa", "e-ctx", "s-ttbar", "s-LLbar", "s-ent", "o_wu"],
          announce=["FW2", "FW3", "FW4", "H1", "H2", "H3", "H4", "H5", "H6", "V5", "V3", "P1", "P3", "G1", "G3", "G5",
                    "DV3", "DV4", "A2", "A4"]),
        U("d1", "main", "Introduction", "Sec. I: paragraphs 1–3, items (i)–(v), 'Relation to earlier work', 'The graph'",
          "Entanglement reported from decay angles; single-setting data admit a local model (the recorded momenta); a decay is a "
          "covariant POVM whose equivalent effects constrain a noncontextual model; noncontextuality is equivalent to simplex "
          "embeddability (Schmid et al.; Gitton and Woods; Selby et al.) and decidable by a linear programme (Selby et al.); the results (i)–(v) previewed with pointers; earlier work; "
          "the question read off as a missing connection between two released graphs.",
          nodes=["o-ang1", "m-quantum", "m-classical", "w-ncineq", "w-entw", "m_cc", "s-steer"],
          announce=["FW2", "FW3", "FW5", "H1", "H2", "DV9", "H3", "H4", "H9", "H8", "V5", "V3", "P1", "G2", "G1", "G3", "G5", "X2"],
          establish={"X1": "citation"},
          pointers=["Sec. {sec:models}: recorded-outcome model", "Theorems {thm:half}–{thm:spinj}, Proposition {prop:pairpoly}",
                    "Sec. {sec:apps}: data", "Sec. {sec:graph} and App. {app:catalogue}: encoding and checks"]),
        U("d2", "main", "The decay polarimeter", "Sec. {sec:polarimeter}, Eqs. ({eq:born})–({eq:symbol})",
          "Born rule for the recorded direction; rotation covariance gives the kernel form E_w(q) = (d/4π)U_q D_w U_q†, the decay "
          "polarimeter; multipole ratios, Husimi function and first moment, Eq. ({eq:firstmoment}), stated without derivation; "
          "spin-1/2 form; spin-1 kernel and symbol, Eqs. ({eq:spin1kernel})–({eq:symbol}), stated without derivation.",
          nodes=["s-spin", "m_A"], announce=["DV8", "DV7"], establish={"DV6": "proof", "X3": "definition"}),
        U("d3", "main", "Kernels from the charged-current vertex", "Sec. {sec:va}, Eqs. ({eq:amp})–({eq:kappanu})",
          "Squared V−A amplitude, Eq. ({eq:trace}); in the rest frame the antifermion direction has κ = 1 (one-line derivation); the "
          "muon-decay spectrum with its decay asymmetry (Michel; Kinoshita and Sirlin), κ = −1/3 and the threshold formula; κ_b and κ_ν for top decay; "
          "'checked symbolically ... (routes DV1–DV5 of Appendix {app:catalogue})'; comparison with the leading-order values of "
          "Ref. [Brandenburg, Si, Uwer].",
          nodes=["m_va", "m_mu"],
          establish={"DV1": "certificate", "DV2": "proof", "DV3": "certificate", "DV4": "certificate", "DV5": "certificate",
                     "A5": "citation", "DV12": "implicit"},
          pointers=["App. {app:va}: derivations", "App. {app:catalogue}: routes DV1–DV5"]),
        U("d4", "main", "Fragments and noncontextual models", "Sec. {sec:models}, Definitions 1–2, Lemma {lem:simplex}, Eq. ({eq:simplex}), Remark {rem:lhv}",
          "Fragments, ontological models, noncontextuality; fragment-relative and quantum-relative equivalence; Lemma {lem:simplex} "
          "(simplex embedding) with references, proof recalled in App. {app:lemma1}; Remark {rem:lhv}: the recorded-outcome model is "
          "constructed, hence no Bell violation (Brunner et al.) and no steering (Wiseman et al.), and the example f = 3q_z² − 1 shows that it is not "
          "measurement noncontextual; Definition 2 (classical polarimeter).",
          nodes=["ax-tomo"],
          establish={"FW1": "citation", "FW2": "proof", "FW3": "citation", "FW4": "citation", "FW5": "proof"},
          pointers=["App. {app:lemma1}: proof of Lemma {lem:simplex}"]),
        U("d5", "main", "Spin 1/2, one particle", "Sec. {sec:half} A, Theorem {thm:half}, Eq. ({eq:tetra})",
          "Theorem {thm:half} with proof: noncontextual iff P|κ| ≤ 1/3, tetrahedral four-state model; comparison with the "
          "entanglement-breaking threshold and with preparation noncontextuality; ellipsoidal state sets, |κ|(P₁+P₂+P₃) ≤ 1, by the same argument.",
          establish={"H1": "proof", "H2": "proof", "H13": "proof"}),
        U("d6", "main", "Spin 1/2, two particles: data and remote preparation", "Sec. {sec:pair}, Eqs. ({eq:pairdata})–({eq:rhoraw})",
          "Joint density of the two recorded directions and its raw coefficients (stated without derivation); the matrix R and "
          "ρ_raw = (D_κA ⊗ D_κB)[ρ]; the Bloch cone; the decay of B as a remote preparation of A; the fragments F_B→A and F_A→B.",
          announce=["DV9"], establish={"DV11": "definition"}),
        U("d7", "main", "Theorem 2", "Sec. {sec:pair}, Theorem {thm:pair}, Eqs. ({eq:localnc})–({eq:rangecond})",
          "Theorem {thm:pair} with proof: a model exists iff R = Σ z h^T with factors in the Bloch cone, iff ρ_raw and its partial "
          "transpose are positive (Peres; Horodecki et al.); the range condition, with Lemma {lem:range} of App. {app:range} for singular R.",
          nodes=["s-sep"], announce=["H12"], establish={"H3": "proof", "H4": "proof"},
          pointers=["App. {app:range}: Lemma {lem:range}"]),
        U("d8", "main", "Corollaries 1–4", "Sec. {sec:pair}, Corollaries {cor:tstate}–{cor:ent}, Eq. ({eq:svdmodel}), closing paragraph",
          "Unpolarised pairs (‖c‖₁ ≤ 1, seven-state model), opening angle (D defined, |D| ≤ 1/3), weak polarimeters, relation to "
          "entanglement (separable ⇒ noncontextual; equivalence for |κ_A| = |κ_B| = 1; Werner states), each with proof; the sign of "
          "κ, convexity, and the comparison with the entanglement test on the same data.",
          establish={"H5": "proof", "DV10": "definition", "H6": "proof", "H7": "proof", "H11": "proof", "H8": "proof",
                     "X2": "proof", "H9": "proof"},
          partial={"DV9": "sign flip of one analysing power: partial transposition followed by a local unitary (verbal reason)"}),
        U("d9", "main", "Covariant reduction", "Sec. {sec:one} A, Proposition {prop:cov}, Eqs. ({eq:ml})–({eq:m12})",
          "Operators with nonnegative Husimi function; the moments m_l(ψ, Z); Proposition {prop:cov} (classical iff the ratios lie in "
          "the convex hull of the points m(ψ, Z)), proof deferred to App. {app:cov}; the spin-1 parametrisation.",
          announce=["FW6"], pointers=["App. {app:cov}: proof of Proposition {prop:cov}"]),
        U("d10", "main", "One spin-1 particle", "Sec. {sec:one} B, Theorem {thm:one}, Eqs. ({eq:R})–({eq:hR}), Corollary {cor:parity}, Remark {rem:deg}",
          "Theorem {thm:one}: classical iff (η₁, η₂) ∈ R, with support function h_R (proof in App. {app:spin1}); boundary points and the "
          "operators that realise them; finite models announced; the triangle of kernels; Corollary {cor:parity} with proof; Remark "
          "{rem:deg}: at η₂ = 0 the criterion is |η₁| ≤ 2/9 (reading I), derived from Theorem {thm:half}.",
          announce=["V5", "V3", "V4"], establish={"V7": "proof"},
          partial={"A8": "Corollary {cor:parity} and its proof: the criterion for parity-symmetric kernels"},
          pointers=["App. {app:spin1}: proof of Theorem {thm:one}", "App. {app:finite}: finite models"]),
        U("d11", "main", "Spin-singlet pair of spin-1 particles", "Sec. {sec:one} C, Proposition {prop:pairpoly}, Theorem {thm:onepair}, Table {tab:pairs}, Corollary {cor:vis}",
          "Proposition {prop:pairpoly} with proof (local model with nonnegative polynomial response functions); the isotropic family "
          "ρ_v; Theorem {thm:onepair} (region R₂; proof in App. {app:spin1}); Table {tab:pairs} of critical visibilities with the "
          "kernels of W, Z and V decays; Corollary {cor:vis} with proof, A_ℓ from Ref. [PDG].",
          nodes=["m_nc"], announce=["P1"], establish={"A7": "citation", "P3": "proof", "P6": "proof"},
          partial={"G5": "Proposition {prop:pairpoly} and its proof"},
          pointers=["App. {app:spin1}: proof of Theorem {thm:onepair}"]),
        U("d12", "main", "Spin j", "Sec. {sec:one} D, Theorem {thm:spinj}, Eq. ({eq:dipole}), Table {tab:gj}",
          "ξ_2j as the largest node of a Gauss–Legendre or Gauss–Radau rule (Gautschi); Theorem {thm:spinj}: (a) bound with proof, (b) "
          "supremum (proof in App. {app:spinj}), (c) first-moment bound for pairs with proof; consistency with Theorems "
          "{thm:half}–{thm:onepair}; Table {tab:gj} with the values of the linear programme.",
          announce=["G3"], establish={"G2": "citation", "G1": "proof", "G7": "proof", "G5": "proof", "G6": "proof", "G4": "certificate"},
          pointers=["App. {app:spinj}: proof of (b)", "App. {app:numerics}: linear programmes"]),
        U("d13", "main", "Which decays are classical polarimeters", "Sec. {sec:apps} A, Table {tab:kappa}, Fig. {fig:half}",
          "Table {tab:kappa} of analysing powers (τ entries without reference here); muon decay on the threshold; the b-quark "
          "direction is nonclassical iff m_t > 2m_W, also after the QCD correction; the neutrino direction is within the corrections "
          "of the boundary.",
          announce=["A6"],
          partial={"A5": "QCD and finite-mass corrections of Ref. [Brandenburg, Si, Uwer]", "DV5": "value at the measured masses and distance to the boundary"}),
        U("d14", "main", "Top-quark pairs", "Sec. {sec:apps} B",
          "ATLAS and CMS values of D (ATLAS; CMS); by Corollary {cor:D} they exclude noncontextual models of the lepton-direction data at "
          "the significance quoted for entanglement (quadrature sum of the quoted uncertainties); three differences from the "
          "entanglement reading; channels with b quarks or neutrinos.",
          establish={"A1": "citation", "A2": "proof"}),
        U("d15", "main", "Hyperon pairs", "Sec. {sec:apps} C",
          "Closed-form joint distribution of J/ψ → ΛΛ̄ (Fäldt and Kupsc) with the BESIII parameters (BESIII); ‖c‖₁ above 1 at 90°; ρ_raw fails the "
          "test of Theorem {thm:pair} for |cos θ| below the computed bound although the state is entangled at all angles (Fig. "
          "{fig:half}); Σ⁺Σ̄⁻; a direct test on raw moments.",
          establish={"A3": "citation", "A4": "certificate"}),
        U("d16", "main", "Vector bosons and vector mesons", "Sec. {sec:apps} D",
          "Kernels of W → ℓν, Z → ℓℓ, V → PP, V → ℓℓ, all outside R; J/ψ → ΛΛ̄ nonclassical, J/ψ → Σ⁺Σ̄⁻ near the boundary, "
          "ψ(2S) → ττ classical, with cited parameters; pairs: Table {tab:pairs} and Eq. ({eq:dipole}) for arbitrary states.",
          establish={"A8": "proof"}, partial={"A7": "single-particle kernels listed"}),
        U("d17", "main", "The result as a three-layer concept graph", "Sec. {sec:graph}, Fig. {fig:network}, Table {tab:claims}",
          "The three layers; counts of nodes and of routes by grade; claims and verdicts; negative controls, lint and scope "
          "separation; the two released edges that reappear with the measurement fixed.",
          announce=["X2"], pointers=["App. {app:catalogue}: full encoding"]),
        U("d18", "main", "Discussion", "Sec. {sec:discussion}",
          "Assumptions (tomographic completeness, full acceptance); what is excluded; relation to entanglement measurements; five "
          "open problems.", announce=["H8", "H9"]),
        U("d19", "main", "Acknowledgments", "acknowledgments",
          "Not encoded: statement on the use of an AI system (derivations, code and text produced in a dialogue between the author "
          "and Claude; the written proofs are checked by no program and no reviewer) and on data and code.", encoded=False),
        U("d20", "methods", "Proof of Lemma 1", "App. {app:lemma1}",
          "The argument of Refs. [Schmid et al.; Selby et al.] recalled for the fragment at hand; degenerate kernels.",
          partial={"FW1": "argument recalled from the cited references"}),
        U("d21", "methods", "Charged-current kernels", "App. {app:va}",
          "Route DV1 named for Eq. ({eq:trace}); the muon spectrum by integration over the unobserved momenta (route DV3); helicity "
          "counting for t → bW (route DV4); quadrature (route DV5); the τ entries of Table {tab:kappa} from Ref. [Tsai].",
          establish={"A6": "citation"},
          partial={"DV1": "explicit Dirac matrices (route DV1)", "DV3": "integration over the unobserved momenta",
                   "DV4": "helicity counting", "DV5": "direct numerical quadrature (route DV5)"}),
        U("d22", "methods", "Range lemma", "App. {app:range}, Lemma {lem:range}",
          "Lemma {lem:range} with proof (Lorentz boost and orthogonal projection); its use in Theorem {thm:pair}; route H12 and "
          "negative control k15 named.",
          establish={"H12": "proof"}),
        U("d23", "methods", "Proof of Proposition 1", "App. {app:cov}, Eq. ({eq:lamdec})",
          "Lemma {lem:simplex} applied, the kernel moved to the operators Z, rotation average by Schur's lemma, Carathéodory; the "
          "icosahedral average for j = 1.",
          establish={"FW6": "proof"}),
        U("d24", "methods", "Nonnegative quadratic functions on the sphere", "App. {app:spin1} 1, Lemma {lem:sos}, Eqs. ({eq:pencil})–({eq:squares})",
          "Lemma {lem:sos} with proof (rank-one decomposition; S-lemma form, Sturm and Zhang; Pólik and Terlaky); route V2 named; the generators of Q.",
          establish={"V1": "proof", "V2": "proof"}),
        U("d25", "methods", "Proof of Theorem 3", "App. {app:spin1} 2, Eq. ({eq:Mt})",
          "Upper bound on the support function through Lemma {lem:sos}(a); attainment on the ellipse and at the apex ('routes V3, "
          "V6'); the cases η₁ = 0 and η₂ = 0 (route V7).",
          establish={"V3": "proof", "V5": "proof", "V6": "certificate"},
          partial={"V7": "computation under readings I and II (route V7)"}),
        U("d26", "methods", "Proof of Theorem 4", "App. {app:spin1} 3, Eq. ({eq:R2points})",
          "Steered states as images of the coherent cone; reduction to equal parameters by the arithmetic–geometric inequality; "
          "convexity in cos γ; the tangent point s = √3 − 1 (route P1).",
          establish={"P1": "proof"}),
        U("d27", "methods", "Finite models", "App. {app:finite}",
          "Icosahedral models; 'Route V4 verifies in exact arithmetic' the averaging identity at the extreme points of R and of R₂.",
          establish={"V4": "certificate", "P2": "certificate"}),
        U("d28", "methods", "Spin j: attainment", "App. {app:spinj}",
          "The extremal polynomial and kernel D*; the Haar model; nonzero multipole ratios for j ≤ 4 found by route G4; the "
          "perturbation argument for general j.",
          establish={"G3": "proof"},
          partial={"G2": "the extremal polynomial attains ξ_2j", "G4": "minimum multipole ratio and linear-programme value (route G4)"}),
        U("d29", "methods", "Numerical cross-checks", "App. {app:numerics}",
          "SDP for the support function of R (route V6); linear programmes without the covariant reduction (routes V6, P4, P5) "
          "and their refinement; the two-sided bracket for two spin-1/2 particles (route H10), whose two programmes define the "
          "witness; spin j (routes DV8, G4); first-moment bound (route G7); the lemmas on random instances (routes V2, H12).",
          establish={"DV8": "certificate", "FW7": "definition", "H10": "certificate", "P4": "certificate", "P5": "certificate"},
          partial={"V6": "description of the SDP and of the linear programmes", "G4": "linear programme for j ≤ 4",
                   "G7": "random non-zonal polynomials (route G7)", "V2": "random instances", "H12": "random instances"}),
        U("d30", "methods", "Nodes, routes and controls", "App. {app:catalogue}, Tables {tab:nodes}–{tab:routesb}",
          "The catalogue generated from the results file: every node with its source, every route with layers, grade and status "
          "('checked' with the certificate named, 'proof in text', 'cited'). For DV7 and DV9 it is the only place where the "
          "paper points to their support.",
          establish={"DV7": "certificate", "DV9": "certificate"},
          partial={"DV12": "listed with status 'proof in text'; the text contains neither the statement nor a proof"}),
    ],
    "added": {"routes": {}, "nodes": {}},
    "notes": [
        "Generated work (T. Hossain with Claude (Anthropic), 17 November 2026; unpublished, not peer reviewed). Its routes were "
        "written together with the text, so every route has a counterpart in the paper, at least as a line of the catalogue (App. {app:catalogue}).",
        "Support 'certificate': the paper points to an executed program and writes no derivation at that place. The support is "
        "dated where the text first names the check (a route named in the text, or a computation described in App. {app:numerics}); "
        "DV7 (spin-1 kernel, Eq. ({eq:spin1kernel})) and DV9 (raw coefficients, Eq. ({eq:pairdata})) are stated without derivation "
        "and named only in the catalogue, so their support is dated at App. {app:catalogue}.",
        "DV12 (the decay asymmetries of the released graph are first multipoles of the polarimeter) is listed in the catalogue as "
        "'proof in text', but the text neither states nor proves it; the identification is used in Sec. {sec:va} ('the V−A "
        "spectrum with its decay asymmetry'), hence 'implicit'.",
        "A7: the kernels of W → ℓν, Z → ℓℓ and V → PP are stated without derivation in Table {tab:pairs} and Sec. {sec:apps} D; "
        "they follow from the helicity weights of Sec. {sec:polarimeter} (Ref. [Jacob, Wick]); A_ℓ carries a citation (PDG).",
        "V2 and H12 have grade numeric in the encoding (checks on random instances); the text also gives written proofs of "
        "Lemma {lem:sos}(a) and Lemma {lem:range}, which are recorded as the support. G7 (numeric) is likewise proved in the proof "
        "of Theorem {thm:spinj}(a).",
        "The appendices are counted in the block 'methods' (proofs and computations after the main text).",
    ],
}


def resolve_locations(order, labels):
    """Replace {label} placeholders in the location strings, texts, pointers, partial notes and notes of an order."""
    import re as _re

    def sub(s):
        def rep(m):
            key = m.group(1)
            if key not in labels:
                raise KeyError(f"unresolved label {key}")
            return labels[key]
        return _re.sub(r"\{([a-z]+:[A-Za-z0-9]+)\}", rep, s)

    for u in order["units"]:
        u["loc"], u["text"] = sub(u["loc"]), sub(u["text"])
        u["pointers"] = [sub(p) for p in u["pointers"]]
        u["partial"] = {r: sub(w) for r, w in u["partial"].items()}
    order["notes"] = [sub(n) for n in order["notes"]]
    return order


def _decay_labels():
    import paper_decay
    return paper_decay.LABELS


resolve_locations(DECAY, _decay_labels())

ORDERS = {"battery": BATTERY, "realqm": REALQM, "top": TOP, "decay": DECAY}
