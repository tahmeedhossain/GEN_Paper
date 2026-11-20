# Replay of four encoded papers in reading order (three published papers and one generated work)

Generated 2026-11-20 10:31 UTC by run_replay.py. Encoding: out/results.json of the edge kernel. Reading order: orders.py.

## 1. Summary of the order tests

| paper | units | nodes (carried in) | routes | stated before supported | median deferral (units) | routes supported on a route supported later | node forward links, support time | node forward links, statement time | not supported in the paper |
|---|---|---|---|---|---|---|---|---|---|
| battery | 23 | 23 (7) | 30 | 16 | 9 | 5 (4 of 33 dependency pairs) | 1 | 6 | 7 |
| realqm | 19 | 15 (4) | 20 | 12 | 9 | 2 (12 of 25 dependency pairs) | 0 | 7 | 3 |
| top | 14 | 20 (7) | 14 | 4 | 9 | 0 (0 of 10 dependency pairs) | 0 | 2 | 3 |
| decay | 31 | 35 (17) | 63 | 32 | 11 | 24 (17 of 57 dependency pairs) | 0 | 10 | 1 |

## 2. Growth quantities under three time conventions, with the branch values

| graph | time index | V | E | Σ d_arr − Σ(a−1)⁺ + C | closures | mean d_arr | α (R², points) | PA ratio (n) |
|---|---|---|---|---|---|---|---|---|
| branch EM (type D) | calendar year | 120 | 122 | 174 − 60 + 8 | 7% | 1.45 | 1.40 (0.98) | 1.16 (8) |
| branch HEP (type H) | calendar year | 78 | 214 | 234 − 24 + 4 | 2% | 3.00 | 1.62 (0.87) | 3.56 (4) |
| branch GPT (type E) | calendar year | 92 | 156 | 110 − 23 + 69 | 44% | 1.20 | 1.47 (0.99) | 2.86 (69) |
| branch QRT (type E) | calendar year | 116 | 86 | 87 − 20 + 19 | 22% | 0.75 | 1.30 (1.00) | 1.71 (19) |
| paper battery | stated | 23 | 30 | 20 − 5 + 15 | 50% | 0.87 | 2.07 (0.92, 12) | 1.56 (15) |
| paper battery | supported | 23 | 30 | 6 − 0 + 24 | 80% | 0.26 | 3.45 (0.80, 15) | 1.54 (24) |
| paper battery | supported, nodes dated by first route | 23 | 30 | 33 − 13 + 10 | 33% | 1.43 | 1.87 (0.95, 10) | 1.63 (10) |
| paper realqm | stated | 15 | 20 | 16 − 6 + 10 | 50% | 1.07 | 3.54 (0.89, 12) | 1.54 (8) |
| paper realqm | supported | 15 | 20 | 4 − 1 + 17 | 85% | 0.27 | 19.49 (0.49, 11) | 1.34 (17) |
| paper realqm | supported, nodes dated by first route | 15 | 20 | 22 − 9 + 7 | 35% | 1.47 | 2.08 (0.94, 7) | 1.40 (7) |
| paper top | stated | 20 | 14 | 21 − 12 + 5 | 36% | 1.05 | 2.40 (0.92, 6) | 1.00 (5) |
| paper top | supported | 20 | 14 | 13 − 8 + 9 | 64% | 0.65 | 4.98 (0.96, 8) | 0.83 (9) |
| paper top | supported, nodes dated by first route | 20 | 14 | 28 − 16 + 2 | 14% | 1.40 | 1.80 (0.97, 6) | 1.20 (2) |
| paper decay | stated | 35 | 63 | 61 − 32 + 34 | 54% | 1.74 | 2.16 (0.79, 21) | 1.71 (34) |
| paper decay | supported | 35 | 63 | 8 − 1 + 56 | 89% | 0.23 | 17.50 (0.98, 24) | 1.52 (56) |
| paper decay | supported, nodes dated by first route | 35 | 63 | 64 − 26 + 25 | 40% | 1.83 | 1.78 (0.93, 22) | 1.65 (25) |

Robustness (abstract merged into the introduction): battery: closures 50% stated, 80% supported; realqm: closures 45% stated, 85% supported; top: closures 36% stated, 64% supported; decay: closures 46% stated, 89% supported.

## 3. Phases

| graph | observe | deficit | hypothesize | restructure | predict | falsify | calibrate | reduce | τ_b(unit, rank in the loop) |
|---|---|---|---|---|---|---|---|---|---|
| branch EM | 43 (18%) | 0 (0%) | 52 (21%) | 25 (10%) | 116 (48%) | 6 (2%) | 0 (0%) | 0 (0%) | |
| branch HEP | 34 (12%) | 0 (0%) | 31 (11%) | 146 (50%) | 44 (15%) | 0 (0%) | 12 (4%) | 25 (9%) | |
| branch GPT | 62 (25%) | 10 (4%) | 49 (20%) | 14 (6%) | 53 (21%) | 45 (18%) | 0 (0%) | 15 (6%) | |
| branch QRT | 42 (21%) | 0 (0%) | 52 (26%) | 49 (24%) | 26 (13%) | 13 (6%) | 0 (0%) | 20 (10%) | |
| paper battery | 7 (15%) | 0 (0%) | 8 (17%) | 9 (20%) | 12 (26%) | 5 (11%) | 0 (0%) | 5 (11%) | 0.37 |
| paper realqm | 5 (17%) | 0 (0%) | 7 (23%) | 11 (37%) | 4 (13%) | 2 (7%) | 0 (0%) | 1 (3%) | 0.34 |
| paper top | 10 (37%) | 0 (0%) | 2 (7%) | 5 (19%) | 8 (30%) | 0 (0%) | 2 (7%) | 0 (0%) | 0.32 |
| paper decay | 15 (19%) | 0 (0%) | 11 (14%) | 7 (9%) | 38 (47%) | 4 (5%) | 0 (0%) | 6 (7%) | 0.19 |

Total-variation distance between the phase profile of each paper and of each branch: battery: EM 0.28, HEP 0.34, GPT 0.23, QRT 0.19; realqm: EM 0.36, HEP 0.24, GPT 0.35, QRT 0.13; top: EM 0.35, HEP 0.43, GPT 0.41, QRT 0.40; decay: EM 0.11, HEP 0.47, GPT 0.30, QRT 0.34.


## 4. Operations and rules, by paper

| rule | battery | realqm | top | decay |
|---|---|---|---|---|
| R11 | 18 | 14 | 14 | 23 |
| R11 (lifts to R4 + R2) | 0 | 3 | 3 | 0 |
| R14 | 17 | 1 | 2 | 48 |
| R15 | 0 | 1 | 0 | 0 |
| R17 | 2 | 0 | 0 | 1 |
| R18 aggregate | 0 | 1 | 2 | 0 |
| R18 effect | 0 | 0 | 2 | 7 |
| R20 | 6 | 3 | 0 | 0 |
| R21 | 2 | 2 | 0 | 0 |
| R4 form | 1 | 2 | 0 | 2 |
| R6/R16 | 0 | 1 | 0 | 0 |
| R9 | 0 | 0 | 2 | 0 |
| back-edge | 0 | 2 | 2 | 0 |
| carried in | 7 | 4 | 7 | 17 |
| none | 0 | 1 | 0 | 0 |

| operation | battery | realqm | top | decay |
|---|---|---|---|---|
| ADD | 15 | 10 | 13 | 18 |
| AGGREGATE | 0 | 1 | 2 | 0 |
| BACK | 0 | 2 | 2 | 0 |
| CALIBRATE | 0 | 0 | 2 | 0 |
| CARRY | 7 | 4 | 7 | 17 |
| CLAIM | 0 | 1 | 0 | 0 |
| CLOSE | 17 | 1 | 2 | 48 |
| CLUSTER | 1 | 0 | 0 | 1 |
| COMPOSE | 0 | 1 | 0 | 0 |
| DEFINE | 1 | 1 | 0 | 0 |
| DERIVE | 2 | 6 | 4 | 5 |
| EXCLUDE | 2 | 1 | 0 | 0 |
| MEMBER | 4 | 2 | 0 | 0 |
| REDUCE | 0 | 1 | 0 | 0 |
| REFINE | 1 | 1 | 0 | 0 |
| ROUTE | 1 | 2 | 0 | 2 |
| SPLIT | 1 | 1 | 0 | 0 |
| TEST | 1 | 0 | 2 | 7 |

## Paper: battery

R. Ganardi, T. V. Kondra, N. H. Y. Ng, A. Streltsov, Second Law of Entanglement Manipulation with an Entanglement Battery, Phys. Rev. Lett. 135, 010202 (2025). Text: arXiv:2405.10599v2.

| # | unit | location | nodes | stated here, supported later | supported here: route [operation, rule, support] | V | stated | supported | open | conditional |
|---|---|---|---|---|---|---|---|---|---|---|
| 0 | Abstract | abstract | sR-ent°, pF-ent°, s-bat, p-bat, wQ-E, t-conv, t-rate, e-rev | GB11, GB12, GB20 | – | 8 | 3 | 0 | 3 | 0 |
| 1 | Introduction | untitled opening, paragraphs A1–A6 | p-cat° | GB22 | – | 9 | 4 | 0 | 4 | 0 |
| 2 | Asymptotic transformations of entangled states and reversibility | B1–B6 | pX-ent° | – | GB15i [CLOSE, R14, citation]; GB21i [DERIVE, R11, citation] | 10 | 6 | 2 | 4 | 0 |
| 3 | Reversible manipulations with a battery: the setting | C1–C6, Eqs. (1)–(2) | ax-mono, ax-add, ax-ac, ax-fin | – | GB0 [ROUTE, R4 form, definition] | 14 | 7 | 3 | 4 | 0 |
| 4 | Theorem 1 | C7–C9, Eq. (3) | – | GB3, GB1, GB2 | – | 14 | 10 | 3 | 7 | 0 |
| 5 | Theorem 2 and reversibility | C10–C13, Eq. (4) | – | GB9, GB6 | GB12 [CLOSE, R14, proof, cond.] | 14 | 12 | 4 | 8 | 1 |
| 6 | Quantifiers that qualify | C14–C19, Eqs. (5)–(6) | wQ-sq, wQ-neg° | GB13a, GB13b, GB13c, GB17 | – | 16 | 16 | 4 | 12 | 1 |
| 7 | Relation to Ref. [7]; correlations; geometric entanglement | C20–C22 | ax-chan†, sF-ent°, wQ-geo | GB15 | GB19 [CLUSTER, R17, asserted, cond.]; GB21e [EXCLUDE, R20, asserted, cond.]; GB21 [REFINE, R21, asserted, cond.] | 19 | 20 | 7 | 13 | 4 |
| 8 | Quantum thermodynamics | D1–D10, Eqs. (7)–(8) | wQ-F°, p-thbat | GB18 | – | 21 | 21 | 7 | 14 | 4 |
| 9 | Conclusions | E1–E4 | – | – | – | 21 | 21 | 7 | 14 | 4 |
| 10 | Methods: LOCC with entanglement battery | Eqs. (9)–(11) | – | – | – | 21 | 21 | 7 | 14 | 4 |
| 11 | Methods: proof of Theorem 1 | Eqs. (12)–(17) | – | – | GB1 [CLOSE, R14, proof]; GB2 [CLOSE, R14, proof]; GB3 [CLOSE, R14, proof] | 21 | 21 | 10 | 11 | 2 |
| 12 | Methods: proof of Theorem 2 | Eqs. (18)–(27) | – | – | GB4 [CLOSE, R14, implicit]; GB9 [CLOSE, R14, proof]; GB10 [CLOSE, R14, proof]; GB6 [CLOSE, R14, proof]; GB7 [CLOSE, R14, proof]; GB11 [CLOSE, R14, proof] | 21 | 24 | 16 | 8 | 0 |
| 13 | Methods: proof of Theorem 3 | no numbered equation | – | – | GB18i [MEMBER, R20, asserted]; GB18 [CLOSE, R14, proof] | 21 | 25 | 18 | 7 | 0 |
| 14 | Methods: zero-error conversion | Eqs. (28)–(31) | – | – | GB5 [CLOSE, R14, proof]; GB8 [CLOSE, R14, proof] | 21 | 27 | 20 | 7 | 0 |
| 15 | Methods: measures that are additive and asymptotically continuous | Eqs. (32)–(34) | – | – | GB13a [MEMBER, R20, citation]; GB13b [TEST, R17, citation]; GB13c [MEMBER, R20, citation] | 21 | 27 | 23 | 4 | 0 |
| 16 | Methods: other entanglement measures | Eqs. (35)–(36) | s-order | GB17i | GB16 [DEFINE, R11, definition]; GB20 [DERIVE, R11, asserted, cond.] | 22 | 29 | 25 | 4 | 1 |
| 17 | Supplemental: connection to catalysis | Eq. (37) | – | – | GB22 [CLOSE, R14, definition] | 22 | 29 | 26 | 3 | 1 |
| 18 | Supplemental: relative entropy of entanglement | Eqs. (38)–(69), Proposition 4 | – | – | not encoded | 22 | 29 | 26 | 3 | 1 |
| 19 | Supplemental: logarithmic negativity | Eqs. (71)–(79) | – | – | GB17i [MEMBER, R20, citation]; GB17 [CLOSE, R14, proof] | 22 | 29 | 28 | 1 | 0 |
| 20 | Supplemental: geometric entanglement | Eqs. (80)–(84) | s-geo | – | GB14 [EXCLUDE, R20, proof]; GB15 [CLOSE, R14, asserted] | 23 | 30 | 30 | 0 | 0 |
| 21 | Supplemental: correlations between main system and battery | Eqs. (85)–(106) | – | – | not encoded | 23 | 30 | 30 | 0 | 0 |
| 22 | Supplemental: self-dilution in thermodynamics | Eqs. (107)–(111) | – | – | not encoded | 23 | 30 | 30 | 0 | 0 |

° carried in from the released network; † split off an existing node.

Routes supported in a unit before a route they depend on: GB12 (unit 5, complete at unit 12; waits for GB11), GB19 (unit 7, complete at unit 11; waits for GB3), GB20 (unit 16, complete at unit 19; waits for GB17i), GB21e (unit 7, complete at unit 11; waits for GB2), GB21 (unit 7, complete at unit 12; waits for an indirect dependency).

Not supported in the paper (stated with at most a verbal reason, or used without statement): GB15, GB18i, GB19, GB20, GB21, GB21e, GB4.

Added by the encoding and excluded from all counts: GB20i (existence of PPT entangled states; not cited at this place in the paper).

Guards: {"R2": [{"node": "e-rev", "sub": "effect", "appears": 0, "explained_unit": 5, "lag": 5, "primitive": false}, {"node": "t-conv", "sub": "task", "appears": 0, "explained_unit": 11, "lag": 11, "primitive": false}, {"node": "t-rate", "sub": "task", "appears": 0, "explained_unit": 2, "lag": 2, "primitive": false}, {"node": "wQ-E", "sub": "witness", "appears": 0, "explained_unit": 12, "lag": 12, "primitive": false}, {"node": "wQ-F", "sub": "witness", "appears": 8, "explained_unit": null, "lag": null, "primitive": true}, {"node": "wQ-geo", "sub": "witness", "appears": 7, "explained_unit": null, "lag": null, "primitive": true}, {"node": "wQ-neg", "sub": "witness", "appears": 6, "explained_unit": null, "lag": null, "primitive": true}, {"node": "wQ-sq", "sub": "witness", "appears": 6, "explained_unit": null, "lag": null, "primitive": true}], "R6": [], "R12": [{"no_go": "GB21i", "target": "e-rev", "unit": 2, "other_route_into_target": [{"route": "GB12", "unit": 5}], "reconciled_by": [{"route": "GB21", "unit": 7}]}], "R18_effect": [{"effect": "e-rev", "criterion": ["GB21i"], "test": ["GB12"], "member": [], "well_formed": false}]}

- s-order is an instance pair chosen by the encoding to exhibit GB20; the paper states the general claim (C5) and the PPT remark (Methods).
- GB0: Eqs. (1)–(2) define the exact single-copy class; Eqs. (9)–(11) restate it with error and rates.
- GB4 (E(ρ^{⊗k}) = kE(ρ)) is used in Eqs. (19), (22), (30) without being stated.

## Paper: realqm

P. Barrios Hita, A. Trushechkin, H. Kampermann, M. Epping, D. Bruß, Quantum Mechanics Based on Real Numbers: A Consistent Description, Phys. Rev. Lett. 136, 240202 (2026). Text: arXiv:2503.17307 (equation numbers (1)–(124)).

| # | unit | location | nodes | stated here, supported later | supported here: route [operation, rule, support] | V | stated | supported | open | conditional |
|---|---|---|---|---|---|---|---|---|---|---|
| 0 | Abstract | paragraph T1 | m-quantum°, m-realqm°, m-realflag, t-distinguish | RQ17, RQ19, RQ21 | – | 4 | 3 | 0 | 3 | 0 |
| 1 | Introduction | T2–T7 | ax-tensorR†, e-net | RQ9 | – | 6 | 4 | 0 | 4 | 0 |
| 2 | Postulates (P1)–(P4) | T8 | ax-P4 | – | – | 7 | 4 | 0 | 4 | 0 |
| 3 | Single system: the state map | T9–T11, Eqs. (1)–(2) | s-C°, f-real, s-Rflag | RQ2 | – | 10 | 5 | 0 | 5 | 0 |
| 4 | Single system: operators and expectation values | T12–T13, Eqs. (3)–(6) | ax-complex° | RQ1 | – | 11 | 6 | 0 | 6 | 0 |
| 5 | The naive tensor extension fails | T14–T16 | s-indep | RQ15 | – | 12 | 7 | 0 | 7 | 0 |
| 6 | Composite systems: quotient space and canonical representatives | T17–T18, Eqs. (7)–(8) | s-canon | – | RQ4 [BACK, back-edge, definition] | 13 | 8 | 1 | 7 | 0 |
| 7 | Composite systems: predictions | T19 | o-born | RQ10, RQ5, RQ12 | – | 14 | 11 | 1 | 10 | 0 |
| 8 | (P4) and reduced states | T20 | – | RQ8, RQ3 | – | 14 | 13 | 1 | 12 | 0 |
| 9 | Summary | T21 | – | – | RQ19 [REDUCE, R6/R16, asserted, cond.]; RQ20 [REFINE, R21, asserted, cond.]; RQ21 [CLAIM, none, asserted] | 14 | 14 | 4 | 10 | 2 |
| 10 | A. Uniqueness of the mapping | Eqs. (9)–(39), Propositions 1–3 | – | – | RQ5 [COMPOSE, R15, proof] | 14 | 14 | 5 | 9 | 2 |
| 11 | B. State map: general case | Eqs. (40)–(51), Remarks 4–5 | – | – | RQ6 [BACK, back-edge, proof]; RQ15 [EXCLUDE, R20, proof] | 14 | 15 | 7 | 8 | 2 |
| 12 | C. Alternative derivation of the map for operators | Eqs. (52)–(61) | – | – | RQ7 [ROUTE, R4 form, proof]; RQ9 [ROUTE, R4 form, proof] | 14 | 16 | 9 | 7 | 2 |
| 13 | D. Further properties of the construction | Eqs. (62)–(70), Propositions 6–7 | – | – | RQ1 [DEFINE, R11, proof]; RQ18 [MEMBER, R20, proof]; RQ2 [DERIVE, R11, proof] | 14 | 17 | 12 | 5 | 2 |
| 14 | E. Formalisation of postulate (P4) | Eqs. (71)–(82), Definitions 8–10, Proposition 11 | – | – | RQ8 [MEMBER, R20, proof] | 14 | 17 | 13 | 4 | 2 |
| 15 | F. Density operators and reduced density operators | Eqs. (83)–(94) | – | – | RQ3 [DERIVE, R11, proof]; RQ10 [DERIVE, R11 (lifts to R4 + R2), proof] | 14 | 17 | 15 | 2 | 1 |
| 16 | G. Myrheim approach | Eqs. (95)–(103) | – | – | not encoded | 14 | 17 | 15 | 2 | 1 |
| 17 | H. Renou et al.: complex calculation | Eqs. (104)–(112) | w-T | – | RQ13 [AGGREGATE, R18 aggregate, definition]; RQ11 [DERIVE, R11 (lifts to R4 + R2), proof]; RQ17 [CLOSE, R14, citation] | 15 | 19 | 18 | 1 | 1 |
| 18 | H. Renou et al.: real-number calculation | Eqs. (113)–(124) | – | – | RQ14 [DERIVE, R11, proof]; RQ12 [DERIVE, R11 (lifts to R4 + R2), proof] | 15 | 20 | 20 | 0 | 0 |

° carried in from the released network; † split off an existing node.

Routes supported in a unit before a route they depend on: RQ19 (unit 9, complete at unit 15; waits for RQ1, RQ10, RQ2, RQ3, RQ5, RQ6, RQ7, RQ8, RQ9), RQ20 (unit 9, complete at unit 18; waits for RQ12, RQ15, RQ17).

Not supported in the paper (stated with at most a verbal reason, or used without statement): RQ19, RQ20, RQ21.

Added by the encoding and excluded from all counts: RQ16 (dimension count behind local tomography; a check of the encoding, not a statement of the paper).

Guards: {"R2": [{"node": "e-net", "sub": "effect", "appears": 1, "explained_unit": null, "lag": null, "primitive": false}, {"node": "o-born", "sub": "direct", "appears": 7, "explained_unit": 15, "lag": 8, "primitive": false}, {"node": "t-distinguish", "sub": "task", "appears": 0, "explained_unit": 9, "lag": 9, "primitive": false}, {"node": "w-T", "sub": "witness", "appears": 17, "explained_unit": 17, "lag": 0, "primitive": false}], "R6": [{"routes": ["RQ11", "RQ12"], "models": ["m-quantum", "m-realflag"], "target": "w-T", "signal_unit": 18, "merge_route": ["RQ19"], "merge_unit": [9]}], "R12": [{"no_go": "RQ17", "target": "e-net", "unit": 17, "other_route_into_target": [], "reconciled_by": [{"route": "RQ20", "unit": 9}]}], "R18_effect": [{"effect": "e-net", "criterion": ["RQ17"], "test": [], "member": [], "well_formed": false}]}

- Propositions 1 and 2 (uniqueness) are announced in the main text and are not encoded as a route.
- RQ7: the product relations are in Section C; the partial-trace identity of its statement is Eq. (91) of Section F.
- RQ17 is cited in general terms in T5; the network and the number 7.6605 appear in Section H.

## Paper: top

ATLAS Collaboration, Observation of quantum entanglement with top quarks at the ATLAS detector, Nature 633, 542–547 (2024). Text: arXiv:2311.07288v3.

| # | unit | location | nodes | stated here, supported later | supported here: route [operation, rule, support] | V | stated | supported | open | conditional |
|---|---|---|---|---|---|---|---|---|---|---|
| 0 | Abstract | abstract | s_t, s_lep°, s-ent°, s-ttavg, o-cosphi, w-D, o-Dobs, e-ttent, m-mc | TQ11, TQ14, TQ15 | – | 9 | 3 | 0 | 3 | 0 |
| 1 | Main: colliders, the top quark as a qubit | M1–M3 | – | – | – | 9 | 3 | 0 | 3 | 0 |
| 2 | Main: spin density matrix | M4–M6, first displayed equation | s-ttspin, m_A°, m-qcd | – | TQ1 [BACK, back-edge, definition] | 12 | 4 | 1 | 3 | 0 |
| 3 | Main: decay and lepton distribution | M7–M8, second displayed equation | s_W°, s_b, m_cc°, o-lepdir, o-joint | – | TQ2 [DERIVE, R11 (lifts to R4 + R2), asserted]; TQ3 [DERIVE, R11 (lifts to R4 + R2), asserted]; TQ5 [DERIVE, R11 (lifts to R4 + R2), citation] | 17 | 7 | 4 | 3 | 0 |
| 4 | Main: threshold, singlet, trace witness | M9 | d-singlet°, s-sep° | – | TQ12 [BACK, back-edge, citation]; TQ7 [DERIVE, R11, citation]; TQ9 [CLOSE, R14, citation] | 19 | 10 | 7 | 3 | 0 |
| 5 | Main: the marker D | M10, third displayed equation | – | – | TQ6 [AGGREGATE, R18 aggregate, asserted]; TQ6b [AGGREGATE, R18 aggregate, definition] | 19 | 12 | 9 | 3 | 0 |
| 6 | Main: the criterion D < −1/3 | M11–M12 | – | – | TQ8 [CLOSE, R14, citation]; TQ11 [TEST, R18 effect, citation] | 19 | 13 | 11 | 2 | 0 |
| 7 | 1.1 Detector and event samples | section 1.1 | – | – | – | 19 | 13 | 11 | 2 | 0 |
| 8 | 1.2 Analysis procedure | P1–P10 | o-limit | TQ13 | – | 20 | 14 | 11 | 3 | 0 |
| 9 | 1.3 Results | R1–R3 | – | – | TQ14 [CALIBRATE, R9, measurement]; TQ13 [CALIBRATE, R9, simulation] | 20 | 14 | 13 | 1 | 0 |
| 10 | 1.4 Discussion | D1–D5 | – | – | TQ15 [TEST, R18 effect, measurement] | 20 | 14 | 14 | 0 | 0 |
| 11 | Methods A.1–A.2 | objects, simulation | – | – | not encoded | 20 | 14 | 14 | 0 | 0 |
| 12 | Methods A.3: reweighting the cos φ distribution | two displayed equations | – | – | – | 20 | 14 | 14 | 0 | 0 |
| 13 | Methods A.4–A.6 | backgrounds, uncertainties, parton shower | – | – | not encoded | 20 | 14 | 14 | 0 | 0 |

° carried in from the released network; † split off an existing node.

Routes supported in a unit before a route they depend on: none.

Not supported in the paper (stated with at most a verbal reason, or used without statement): TQ2, TQ3, TQ6.

Added by the encoding and excluded from all counts: TQ4 (intermediate step of the regeneration of the lepton distribution; the paper cites the result), TQ10 (range of D and its value for the singlet; not stated in the paper), TQ16 (difference of the two values given in R1; the paper does not comment on it), TQ17 (scope remark of the encoding; the paper does not mention Bell tests).

Guards: {"R2": [{"node": "e-ttent", "sub": "effect", "appears": 0, "explained_unit": 6, "lag": 6, "primitive": false}, {"node": "o-Dobs", "sub": "direct", "appears": 0, "explained_unit": 9, "lag": 9, "primitive": false}, {"node": "o-cosphi", "sub": "direct", "appears": 0, "explained_unit": 5, "lag": 5, "primitive": false}, {"node": "o-joint", "sub": "direct", "appears": 3, "explained_unit": 3, "lag": 0, "primitive": false}, {"node": "o-lepdir", "sub": "direct", "appears": 3, "explained_unit": 3, "lag": 0, "primitive": false}, {"node": "o-limit", "sub": "direct", "appears": 8, "explained_unit": 9, "lag": 1, "primitive": false}, {"node": "w-D", "sub": "witness", "appears": 0, "explained_unit": 5, "lag": 5, "primitive": false}], "R6": [], "R12": [], "R18_effect": [{"effect": "e-ttent", "criterion": [], "test": ["TQ11", "TQ15"], "member": ["TQ15"], "well_formed": false}]}

- TQ9: the location recorded on 2026-11-17 pointed to a phrase of M11 about the order of the calculation, whose meaning the text does not fix; the statement on averaging over the top-quark directions is in M9.
- TQ1 and TQ12 were recorded under 'Methods' on 2026-11-17; in arXiv v3 both are in section 1 (Main).
- TQ6: the relation ⟨cos φ⟩ = −D/3 is used in M10; the linear form of the distribution is in Methods A.3; neither is derived.

## Paper: decay

T. Hossain with Claude (Anthropic), Particle decays as fixed measurements: exact noncontextuality thresholds for decay-angle correlations, generated work, 17 November 2026 (unpublished, not peer reviewed). Text: generated paper, decay_contextuality/paper (source of 2026-11-17, compiled 2026-11-20).

| # | unit | location | nodes | stated here, supported later | supported here: route [operation, rule, support] | V | stated | supported | open | conditional |
|---|---|---|---|---|---|---|---|---|---|---|
| 0 | Abstract | abstract | p-decay, e-bell°, e-steer°, m-lhv1, m-ncom, u_mh°, p-half, o-ang2, w-rawppt, s-tstate, o-D, u_m1°, p-one, w-region1, s-iso1, w-kappa, e-ctx°, s-ttbar, s-LLbar, s-ent°, o_wu° | FW2, FW3, FW4, H1, H2, H3, H4, H5, H6, V5, V3, P1, P3, G1, G3, G5, DV3, DV4, A2, A4 | – | 21 | 20 | 0 | 20 | 0 |
| 1 | Introduction | Sec. I: paragraphs 1–3, items (i)–(v), 'Relation to earlier work', 'The graph' | o-ang1, m-quantum°, m-classical°, w-ncineq°, w-entw°, m_cc°, s-steer | FW5, DV9, H9, H8, G2, X2 | X1 [DERIVE, R11, citation] | 28 | 27 | 1 | 26 | 0 |
| 2 | The decay polarimeter | Sec. II A, Eqs. (1)–(7) | s-spin, m_A° | DV8, DV7 | DV6 [DERIVE, R11, proof]; X3 [ROUTE, R4 form, definition] | 30 | 31 | 3 | 28 | 0 |
| 3 | Kernels from the charged-current vertex | Sec. II B, Eqs. (8)–(13) | m_va°, m_mu° | – | DV1 [CLOSE, R14, certificate]; DV2 [CLOSE, R14, proof]; DV3 [DERIVE, R11, certificate]; DV4 [CLOSE, R14, certificate]; DV5 [CLOSE, R14, certificate]; A5 [CLOSE, R14, citation]; DV12 [DERIVE, R11, implicit, cond.] | 32 | 36 | 10 | 26 | 1 |
| 4 | Fragments and noncontextual models | Sec. II C, Definitions 1–2, Lemma 1, Eq. (14), Remark 1 | ax-tomo | – | FW1 [ROUTE, R4 form, citation]; FW2 [CLOSE, R14, proof]; FW3 [CLOSE, R14, citation]; FW4 [CLOSE, R14, citation]; FW5 [CLOSE, R14, proof] | 33 | 37 | 15 | 22 | 1 |
| 5 | Spin 1/2, one particle | Sec. III A, Theorem 1, Eq. (15) | – | – | H1 [CLOSE, R14, proof]; H2 [CLOSE, R14, proof]; H13 [CLOSE, R14, proof] | 33 | 38 | 18 | 20 | 1 |
| 6 | Spin 1/2, two particles: data and remote preparation | Sec. III B, Eqs. (16)–(17) | – | – | DV11 [CLUSTER, R17, definition] | 33 | 39 | 19 | 20 | 1 |
| 7 | Theorem 2 | Sec. III B, Theorem 2, Eqs. (18)–(19) | s-sep° | H12 | H3 [CLOSE, R14, proof, cond.]; H4 [CLOSE, R14, proof, cond.] | 34 | 40 | 21 | 19 | 3 |
| 8 | Corollaries 1–4 | Sec. III B, Corollaries 1–4, Eq. (20), closing paragraph | – | – | H5 [CLOSE, R14, proof, cond.]; DV10 [CLOSE, R14, definition]; H6 [CLOSE, R14, proof, cond.]; H7 [CLOSE, R14, proof, cond.]; H11 [CLOSE, R14, proof, cond.]; H8 [CLOSE, R14, proof, cond.]; X2 [CLOSE, R14, proof, cond.]; H9 [TEST, R18 effect, proof, cond.] | 34 | 43 | 29 | 14 | 10 |
| 9 | Covariant reduction | Sec. IV A, Proposition 1, Eqs. (21)–(23) | – | FW6 | – | 34 | 44 | 29 | 15 | 10 |
| 10 | One spin-1 particle | Sec. IV B, Theorem 3, Eqs. (24)–(25), Corollary 5, Remark 2 | – | V4 | V7 [CLOSE, R14, proof, cond.] | 34 | 46 | 30 | 16 | 11 |
| 11 | Spin-singlet pair of spin-1 particles | Sec. IV C, Proposition 2, Theorem 4, Table I, Corollary 6 | m_nc° | – | A7 [DERIVE, R11, citation]; P3 [CLOSE, R14, proof, cond.]; P6 [CLOSE, R14, proof, cond.] | 35 | 48 | 33 | 15 | 13 |
| 12 | Spin j | Sec. IV D, Theorem 5, Eq. (29), Table II | – | – | G2 [CLOSE, R14, citation]; G1 [CLOSE, R14, proof, cond.]; G7 [CLOSE, R14, proof]; G5 [CLOSE, R14, proof, cond.]; G6 [CLOSE, R14, proof, cond.]; G4 [TEST, R18 effect, certificate] | 35 | 51 | 39 | 12 | 16 |
| 13 | Which decays are classical polarimeters | Sec. V A, Table III, Fig. 2 | – | A6 | – | 35 | 52 | 39 | 13 | 16 |
| 14 | Top-quark pairs | Sec. V B | – | – | A1 [CLOSE, R14, citation]; A2 [CLOSE, R14, proof, cond.] | 35 | 53 | 41 | 12 | 17 |
| 15 | Hyperon pairs | Sec. V C | – | – | A3 [CLOSE, R14, citation]; A4 [CLOSE, R14, certificate, cond.] | 35 | 54 | 43 | 11 | 18 |
| 16 | Vector bosons and vector mesons | Sec. V D | – | – | A8 [CLOSE, R14, proof, cond.] | 35 | 55 | 44 | 11 | 19 |
| 17 | The result as a three-layer concept graph | Sec. VI, Fig. 3, Table IV | – | – | – | 35 | 55 | 44 | 11 | 19 |
| 18 | Discussion | Sec. VII | – | – | – | 35 | 55 | 44 | 11 | 19 |
| 19 | Acknowledgments | acknowledgments | – | – | not encoded | 35 | 55 | 44 | 11 | 19 |
| 20 | Proof of Lemma 1 | App. A | – | – | – | 35 | 55 | 44 | 11 | 19 |
| 21 | Charged-current kernels | App. B | – | – | A6 [CLOSE, R14, citation] | 35 | 55 | 45 | 10 | 19 |
| 22 | Range lemma | App. C, Lemma 2 | – | – | H12 [CLOSE, R14, proof] | 35 | 55 | 46 | 9 | 19 |
| 23 | Proof of Proposition 1 | App. D, Eq. (D1) | – | – | FW6 [CLOSE, R14, proof] | 35 | 55 | 47 | 8 | 19 |
| 24 | Nonnegative quadratic functions on the sphere | App. E 1, Lemma 3, Eqs. (E1)–(E2) | – | – | V1 [CLOSE, R14, proof]; V2 [CLOSE, R14, proof] | 35 | 57 | 49 | 8 | 19 |
| 25 | Proof of Theorem 3 | App. E 2, Eq. (E3) | – | – | V3 [CLOSE, R14, proof, cond.]; V5 [CLOSE, R14, proof, cond.]; V6 [TEST, R18 effect, certificate] | 35 | 58 | 52 | 6 | 21 |
| 26 | Proof of Theorem 4 | App. E 3, Eq. (E6) | – | – | P1 [CLOSE, R14, proof, cond.] | 35 | 58 | 53 | 5 | 22 |
| 27 | Finite models | App. F | – | – | V4 [CLOSE, R14, certificate, cond.]; P2 [CLOSE, R14, certificate, cond.] | 35 | 59 | 55 | 4 | 24 |
| 28 | Spin j: attainment | App. G | – | – | G3 [CLOSE, R14, proof] | 35 | 59 | 56 | 3 | 24 |
| 29 | Numerical cross-checks | App. H | – | – | DV8 [CLOSE, R14, certificate]; FW7 [TEST, R18 effect, definition]; H10 [TEST, R18 effect, certificate]; P4 [TEST, R18 effect, certificate]; P5 [TEST, R18 effect, certificate] | 35 | 63 | 61 | 2 | 21 |
| 30 | Nodes, routes and controls | App. I, Tables V–VII | – | – | DV7 [CLOSE, R14, certificate]; DV9 [CLOSE, R14, certificate] | 35 | 63 | 63 | 0 | 0 |

° carried in from the released network; † split off an existing node.

Routes supported in a unit before a route they depend on: DV12 (unit 3, complete at unit 29; waits for DV8), H3 (unit 7, complete at unit 30; waits for DV9), H4 (unit 7, complete at unit 30; waits for DV9, H12), H5 (unit 8, complete at unit 30; waits for an indirect dependency), H6 (unit 8, complete at unit 30; waits for an indirect dependency), H7 (unit 8, complete at unit 30; waits for an indirect dependency), H8 (unit 8, complete at unit 30; waits for an indirect dependency), H9 (unit 8, complete at unit 30; waits for DV9), V3 (unit 25, complete at unit 30; waits for DV7), V4 (unit 27, complete at unit 30; waits for DV7), V5 (unit 25, complete at unit 30; waits for DV7), V7 (unit 10, complete at unit 30; waits for DV7), P1 (unit 26, complete at unit 30; waits for DV7), P2 (unit 27, complete at unit 30; waits for DV7), P3 (unit 11, complete at unit 30; waits for P1), P6 (unit 11, complete at unit 30; waits for P1), G1 (unit 12, complete at unit 29; waits for DV8), G5 (unit 12, complete at unit 29; waits for an indirect dependency), G6 (unit 12, complete at unit 30; waits for P1), A2 (unit 14, complete at unit 30; waits for an indirect dependency), A4 (unit 15, complete at unit 30; waits for DV9), A8 (unit 16, complete at unit 30; waits for V5), H11 (unit 8, complete at unit 30; waits for an indirect dependency), X2 (unit 8, complete at unit 30; waits for an indirect dependency).

Not supported in the paper (stated with at most a verbal reason, or used without statement): DV12.

Added by the encoding and excluded from all counts: none.

Guards: {"R2": [{"node": "e-bell", "sub": "effect", "appears": 0, "explained_unit": null, "lag": null, "primitive": false}, {"node": "e-ctx", "sub": "effect", "appears": 0, "explained_unit": 5, "lag": 5, "primitive": false}, {"node": "e-steer", "sub": "effect", "appears": 0, "explained_unit": null, "lag": null, "primitive": false}, {"node": "o-D", "sub": "direct", "appears": 0, "explained_unit": 14, "lag": 14, "primitive": false}, {"node": "o-ang1", "sub": "direct", "appears": 1, "explained_unit": 3, "lag": 2, "primitive": false}, {"node": "o-ang2", "sub": "direct", "appears": 0, "explained_unit": 15, "lag": 15, "primitive": false}, {"node": "o_wu", "sub": "direct", "appears": 0, "explained_unit": 3, "lag": 3, "primitive": false}, {"node": "w-entw", "sub": "witness", "appears": 1, "explained_unit": null, "lag": null, "primitive": true}, {"node": "w-kappa", "sub": "witness", "appears": 0, "explained_unit": 12, "lag": 12, "primitive": false}, {"node": "w-ncineq", "sub": "witness", "appears": 1, "explained_unit": 29, "lag": 28, "primitive": false}, {"node": "w-rawppt", "sub": "witness", "appears": 0, "explained_unit": 7, "lag": 7, "primitive": false}, {"node": "w-region1", "sub": "witness", "appears": 0, "explained_unit": 24, "lag": 24, "primitive": false}], "R6": [], "R12": [{"no_go": "FW3", "target": "e-bell", "unit": 4, "other_route_into_target": [], "reconciled_by": []}, {"no_go": "FW4", "target": "e-steer", "unit": 4, "other_route_into_target": [], "reconciled_by": []}, {"no_go": "X1", "target": "m-classical", "unit": 1, "other_route_into_target": [], "reconciled_by": []}], "R18_effect": [{"effect": "e-bell", "criterion": ["FW3"], "test": [], "member": [], "well_formed": false}, {"effect": "e-ctx", "criterion": [], "test": ["A4", "A8", "G1", "G4", "H10", "H2", "H5", "H6", "H9", "P3", "P4", "P5", "P6", "V5", "V6"], "member": ["A2", "H6"], "well_formed": false}, {"effect": "e-steer", "criterion": ["FW4"], "test": [], "member": [], "well_formed": false}]}

- Generated work (T. Hossain with Claude (Anthropic), 17 November 2026; unpublished, not peer reviewed). Its routes were written together with the text, so every route has a counterpart in the paper, at least as a line of the catalogue (App. I).
- Support 'certificate': the paper points to an executed program and writes no derivation at that place. The support is dated where the text first names the check (a route named in the text, or a computation described in App. H); DV7 (spin-1 kernel, Eq. (6)) and DV9 (raw coefficients, Eq. (16)) are stated without derivation and named only in the catalogue, so their support is dated at App. I.
- DV12 (the decay asymmetries of the released graph are first multipoles of the polarimeter) is listed in the catalogue as 'proof in text', but the text neither states nor proves it; the identification is used in Sec. II B ('the V−A spectrum with its decay asymmetry'), hence 'implicit'.
- A7: the kernels of W → ℓν, Z → ℓℓ and V → PP are stated without derivation in Table I and Sec. V D; they follow from the helicity weights of Sec. II A (Ref. [Jacob, Wick]); A_ℓ carries a citation (PDG).
- V2 and H12 have grade numeric in the encoding (checks on random instances); the text also gives written proofs of Lemma 3(a) and Lemma 2, which are recorded as the support. G7 (numeric) is likewise proved in the proof of Theorem 5(a).
- The appendices are counted in the block 'methods' (proofs and computations after the main text).

## Controls

- detected: node missing from the reading order
- detected: route supported in two units
- detected: announcement after the support
- detected: theorem supported before its lemmas
- detected: route supported before one of its nodes appears
- detected: cyclic dependency
- detected: kind outside the phase table
- detected: announced route never supported
- detected: identity E = Σd_arr − Σ(a−1)⁺ + C on 2000 random dated hypergraphs
- detected: route dated before one of its ends is reported by the filtration test

## Validation of the growth code on the four dated branches

- EM: all published values reproduced
- HEP: all published values reproduced
- GPT: all published values reproduced
- QRT: all published values reproduced
