# Replay: the update of the graph as a paper is read

Run of 2026-11-19, extended on 2026-11-20 by a fourth paper, the generated work in `decay_contextuality/`.
Continues `SPEC.md` (the edge kernel). The kernel checks an encoded paper as a finished graph. The replay asks
in which order the paper builds that graph, and whether this order follows the update rules of the grand
network (R1 to R21, the temporal rules TE1 to TE6, the counting identity, the phases).
Built with AI assistance (Claude); not peer reviewed.

## 1. Objects

- Units. The text is cut into units in reading order: the abstract (unit 0), then sections, groups of
  paragraphs, blocks of numbered equations. `orders.py` holds the four orders.
- Node date. τ_n(v) is the unit that first names node v.
- Route dates. τ_a(r) is the unit that first states route r. τ_e(r) ≥ τ_a(r) is the unit that supplies its
  support. Support is one of: definition, proof, citation, measurement, simulation, certificate (an
  executed program to which the text points, with no derivation at that place; used for the generated
  paper), asserted (at most a verbal reason), implicit (used inside a derivation without being stated).
- Dependencies. D is the relation "r uses r′" of the encoding (`uses`). It is checked to be acyclic.
- Routes of the encoding without a counterpart in the text (`added` in `orders.py`) are excluded from all
  counts and shown with the unit they refer to.

Open routes after unit t: L_t = { r : τ_a(r) ≤ t < τ_e(r) }.
Waiting routes after unit t: K_t = { r : τ_e(r) ≤ t < δ(r) }, with δ(r) the largest τ_e over r and all routes
reachable from r through D.

## 2. Two propositions

Proposition 1. At the last unit L and K are empty, whatever the order of the text. K_t = ∅ for every t if and
only if τ_e(r′) ≤ τ_e(r) for every pair (r, r′) in D.
Proof. δ(r) ≤ T − 1 for every r, so both sets are empty at t = T − 1. K_t = ∅ for all t means δ(r) = τ_e(r) for
all r, which by transitivity of reachability is the inequality on the pairs of D. ∎

So the final verdict of the kernel does not depend on the order of the text, and the number of pairs of D with
τ_e(r′) > τ_e(r) measures how far the order of the text is from an order a proof checker accepts.

Proposition 2. If τ_a(r) < τ_e(r) and every end of r is named before τ_e(r), then r is a closure route for the
support date. ∎ (Definition of closure route.)

The counting identity E = Σ_v d_arr(v) − Σ_r (a(r) − 1)⁺ + C of the grand network (Part II) holds for the
statement date and for the support date; its proof uses only the definitions of a(r) and C.

## 3. Lookups

Operation and rule of a supported route, tested in this order (`replay.attribute_route`):

| Route | Operation | Rule |
|---|---|---|
| kind calibrates | CALIBRATE | R9 |
| kind flags | FLAG | R2 guard |
| kind witness | TEST | R18 effect |
| kind consistent | REFINE | R21 |
| kind composes | COMPOSE | R15 |
| kind satisfies or violates, with an axiom node at one end | MEMBER, EXCLUDE | R20 |
| kind equiv with two model nodes as inputs | REDUCE | R6/R16 |
| kind equiv from a witness to a free, resource or cluster set | TEST | R17 |
| kind defines, represents or predicts: into a model node, with two or more inputs or from a state | ROUTE | R4 form |
| the same kinds: defines, from a model into a set of states | CLUSTER | R17 |
| the same kinds: model into state | BACK | back-edge |
| the same kinds: among observables | AGGREGATE | R18 aggregate |
| the same kinds: model into observable | PREDICT | R2 route |
| the same kinds: model and state into observable | DERIVE | R11; lifts to R4 + R2 in a type-H graph |
| any other route whose nodes all appeared in earlier units | CLOSE | R14 |
| any other route | DERIVE | R11 |

A node is ADD (new), CARRY (exists in the released network) or SPLIT (split off an existing node, R21).

Phase of a route: the table of Part II (`growth.PHASE_OF_KIND`, copied from the engine). Kinds of the paper
checks that the table lacks: defines and import take the phase of the layer of their target; represents,
composes and consistent are restructure; trivialises is predict; flags is deficit; interpretive claims and
scope remarks have none. A carried-in node has no phase.

How a paper settles a supported route (`replay.closing_route`): literature fill (citation), measurement,
simulation, executed certificate, none in the paper (asserted, implicit), definition, counterexample (a no-go
kind with grade exact or witness), composition (grade compose), proof.

## 4. Tests

- R11: routes that precede one of their nodes, by support date and by statement date.
- Dependency order: pairs of D with τ_e(r′) > τ_e(r); pairs inside one unit are not ordered.
- R13/R14: size of L_t per unit; how each closure route is settled.
- R2: units between the naming of an observable and its first route from the model layer, directly or through
  an explained observable. Observables with no incoming route are primitive.
- R12: a route that rules its target out, the first other route into the target, the route that reconciles.
- R6: two model nodes with a predicting route into one target, and the route that identifies them.
- R18: the three legs of an effect node (no-go route with a model leg, route with a witness leg, route with a
  measured datum).
- Growth quantities of Part II under three datings, computed with a port of the engine (`growth.py`) that
  reproduces the published values of the four dated branches (`validate_growth.py`).

## 5. Results

| Paper | Units | Nodes (carried in) | Routes | Stated before supported | Pairs of D out of order | Waiting routes | Routes before a node: support / statement | No proof and no reference |
|---|---|---|---|---|---|---|---|---|
| Entanglement battery (arXiv:2405.10599v2) | 23 | 23 (7) | 30 | 16 | 4 of 33 | 5 | 1 / 6 | 7 |
| Real-number QM (arXiv:2503.17307) | 19 | 15 (4) | 20 | 12 | 12 of 25 | 2 | 0 / 7 | 3 |
| Top-quark entanglement (arXiv:2311.07288v3) | 14 | 20 (7) | 14 | 4 | 0 of 10 | 0 | 0 / 2 | 3 |
| Decay contextuality (generated work, `decay_contextuality/paper`) | 31 | 35 (17) | 63 | 32 | 17 of 57 | 24 | 0 / 10 | 1 |

| Graph | Dating | E | Σ d_arr − Σ(a−1)⁺ + C | Closures | Mean d_arr | α (R², points) | Preferential closure (n) |
|---|---|---|---|---|---|---|---|
| branch EM (type D) | calendar year | 122 | 174 − 60 + 8 | 7% | 1.45 | 1.40 (0.98) | 1.16 (8) |
| branch HEP (type H) | calendar year | 214 | 234 − 24 + 4 | 2% | 3.00 | 1.62 (0.87) | 3.56 (4) |
| branch GPT (type E) | calendar year | 156 | 110 − 23 + 69 | 44% | 1.20 | 1.47 (0.99) | 2.86 (69) |
| branch QRT (type E) | calendar year | 86 | 87 − 20 + 19 | 22% | 0.75 | 1.30 (1.00) | 1.71 (19) |
| battery | statement | 30 | 20 − 5 + 15 | 50% | 0.87 | 2.07 (0.92, 12) | 1.56 (15) |
| battery | support | 30 | 6 − 0 + 24 | 80% | 0.26 | 3.45 (0.80, 15) | 1.54 (24) |
| battery | support, node dated by its first route | 30 | 33 − 13 + 10 | 33% | 1.43 | 1.87 (0.95, 10) | 1.63 (10) |
| realqm | statement | 20 | 16 − 6 + 10 | 50% | 1.07 | 3.54 (0.89, 12) | 1.54 (8) |
| realqm | support | 20 | 4 − 1 + 17 | 85% | 0.27 | 19.49 (0.49, 11) | 1.34 (17) |
| realqm | support, node dated by its first route | 20 | 22 − 9 + 7 | 35% | 1.47 | 2.08 (0.94, 7) | 1.40 (7) |
| top | statement | 14 | 21 − 12 + 5 | 36% | 1.05 | 2.40 (0.92, 6) | 1.00 (5) |
| top | support | 14 | 13 − 8 + 9 | 64% | 0.65 | 4.98 (0.96, 8) | 0.83 (9) |
| top | support, node dated by its first route | 14 | 28 − 16 + 2 | 14% | 1.40 | 1.80 (0.97, 6) | 1.20 (2) |
| decay | statement | 63 | 61 − 32 + 34 | 54% | 1.74 | 2.16 (0.79, 21) | 1.71 (34) |
| decay | support | 63 | 8 − 1 + 56 | 89% | 0.23 | 17.50 (0.98, 24) | 1.52 (56) |
| decay | support, node dated by its first route | 63 | 64 − 26 + 25 | 40% | 1.83 | 1.78 (0.93, 22) | 1.65 (25) |

Rules by paper (events attributed by the lookups): battery: R11 18, R14 17, R17 2, R20 6, R21 2, R4 form 1, carried in 7; realqm: R11 14, R11 (lifts to R4 + R2) 3, R14 1, R15 1, R18 aggregate 1, R20 3, R21 2, R4 form 2, R6/R16 1, back-edge 2, carried in 4, none 1; top: R11 14, R11 (lifts to R4 + R2) 3, R14 2, R18 aggregate 2, R18 effect 2, R9 2, back-edge 2, carried in 7; decay: R11 23, R14 48, R17 1, R18 effect 7, R4 form 2, carried in 17.

Phase profile, total-variation distance to the branches: battery: EM 0.28, HEP 0.34, GPT 0.23, QRT 0.19; realqm: EM 0.36, HEP 0.24, GPT 0.35, QRT 0.13; top: EM 0.35, HEP 0.43, GPT 0.41, QRT 0.40; decay: EM 0.11, HEP 0.47, GPT 0.30, QRT 0.34. Kendall τ_b between the unit of an event and the rank of its phase in the loop: battery 0.37, realqm 0.34, top 0.32, decay 0.19.

Kendall τ_b between the order of statement and the order of support of the routes: battery 0.37 (n = 30), realqm 0.32 (n = 20), top 0.23 (n = 14), decay 0.33 (n = 63). For comparison, the historical and the pedagogical order of the 41 concepts shared by the two readers have τ_b = 0.857 (Part I).

The unit-by-unit logs are in `out/replay_report.md` and on the page `page_replay/`.

### 5.1 The generated paper

The fourth order (`orders.DECAY`) reads the generated paper of `decay_contextuality/paper` (source of
2026-11-17, compiled on 2026-11-20); its location strings carry label placeholders that are resolved from the
compiled text (`paper_decay.LABELS`, checked against `main.aux` by `paper_decay.check_labels()`). The paper
is cut into 31 units: abstract, Introduction, 17 units of Secs. II–VII, the acknowledgments (not encoded:
statement on the use of an AI system), and 11 units for Appendices A–I (counted in the block methods).

- The abstract names 21 of the 35 nodes and states 20 routes; the introduction names 7 more and states every
  theorem again with a pointer. 32 of the 63 routes are stated before they are supported (median 11 units
  later).
- Support: proof 33, certificate 15, citation 10, definition 4, implicit 1. A route supported by an executed
  certificate is dated where the text first names the check (for example "routes DV1–DV5 of Appendix I" in
  Sec. II B) or where App. H describes the computation.
- DV7 (spin-1 kernel, Eqs. (6)–(7)) and DV9 (raw coefficients of a pair, Eqs. (16)–(17)) are stated without
  derivation, and the only place the text points to their support is the catalogue of App. I, the last unit.
  The 21 routes that use them, directly or through other routes, wait until that unit, among them Theorems
  2, 3 and 4 (H3, H4, V3, V5, P1); 3 more routes (DV12, G1, G5) wait until App. H (unit 29), where the first
  moment DV8 is supported. 24 routes wait in all.
- DV12 (decay asymmetries of the released graph as first multipoles) has no support in the text: the
  catalogue lists it as "proof in text", the text neither states nor proves it, and Sec. II B uses it
  ("the V−A spectrum with its decay asymmetry"). It is recorded as implicit.
- Under the support date 56 of 63 routes are closures (89%), 31 of them deferred routes; with nodes dated by
  their first route, 40%, between the closure shares of its two branches (HEP 2%, GPT 44%).
- The phase profile is closest to the EM branch (total-variation distance 0.11), not to HEP or GPT.
- The no-go routes (FW3, FW4: no Bell violation and no steering with one setting) are not followed by another
  route into their targets; the paper reaches a different effect node, contextuality (R12 reads "not
  reconciled").

## 6. Corrections to the encoding of 2026-11-17

Re-reading the texts for the order changed 28 location fields (`where`): 24 of routes and 4 of claims. No statement,
grade, certificate or verdict changed (`out/results.json` differs from the earlier run only in these fields
and in the timings).

- Top-quark paper: the spin density matrix (TQ1) and the singlet fraction (TQ12) are in section 1 (Main) of
  arXiv v3, not in the Methods. The location of TQ9 pointed to a phrase about the order of the calculation,
  whose meaning the text does not fix; the statement meant is the sentence of the threshold paragraph on
  averaging over the top-quark directions. TQ10 (range of D, value for the singlet) is not
  stated in the paper. TQ4 is a step of the regeneration, not a statement of the paper.
- Real-number paper: no section is titled Discussion; RQ19 and RQ20 are in the closing paragraph of
  the main text and in Section H. The label Theorem 3 for the result of Renou et al. was not verified and
  is replaced by the reference number of the paper.
- Battery paper: locations of GB15i and GB19 made specific.

## 7. Limits

- The reading order is assigned by hand from headings, equation numbers, theorem labels and reference
  numbers of the arXiv texts, read through an automatic page reader. Paragraph labels are that reader's
  segmentation and are approximate. The journal versions were not read.
- The encodings cover part of each paper; units without encoded content are marked.
- A proof outline in the main text counts as a statement. Counting the outlines of Theorems 1 and 2 of the
  battery paper as support of the four routes they sketch would give 12 deferred routes instead of 16.
- Whether a generic mention in an abstract is the first naming of a node is a judgment. Merging the abstract
  into the introduction moves the closure shares by at most 5 points.
- Three published papers, one per branch, and one generated paper across two branches. With 6 to 24 points
  per paper the exponent α is not a test.
- The generated paper and its encoding were written together by the same AI system on 2026-11-17; its
  replay records the order of that text, not an independent reading. Its reading order was assigned on
  2026-11-20 from the LaTeX source. Dating a certificate-supported route at the first naming of the check,
  and at the catalogue when the text names none, is a convention of this replay; dating them at their first
  statement instead gives 25 deferred and 13 waiting routes in place of 32 and 24.
- Operations, rules and phases are lookups on the encoding and inherit its choices of kind and layer.

## 8. Run

```
python3 run_all.py                      # edge kernel on the four papers, writes out/results.json
python3 run_replay.py [gen_evolution_network.json]   # replay, controls, optional validation on the four branches
python3 build_replay_page.py            # page_replay/replay.json and the standalone page
```

The optional argument is `data/gen_evolution_network.json` of the repository GEN_Grand_Evoluton.
