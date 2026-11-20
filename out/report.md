# GEN edge kernel: check report

Run 2026-11-20 10:15 UTC · Python 3.13.18 · sympy 1.14.0 · z3 5.4.1 · 62.8 s

Edges: 133 (89 checked by certificate or kernel rule, 18 imported, 8 definitions, 17 written proof steps (grade compose), 1 interpretive, 0 failed). Negative controls: 28/28 planted errors detected.


## R. Ganardi, T. V. Kondra, N. H. Y. Ng, A. Streltsov, Second Law of Entanglement Manipulation with an Entanglement Battery, Phys. Rev. Lett. 135, 010202 (2025)

Resource-theory branch (GEN_QRT_Level v1.2). doi: 10.1103/kl56-p2vb; arxiv: 2405.10599.

Phases of the method cycle (read by hand): hypothesize (a new operation class, LOCC with a battery, is proposed); restructure (the process layer gains a node that is defined through a quantifier); predict (conversion rates E(ρ)/E(σ) for every pair of states).


### Claims

| Claim | Statement | Verdict | Imports | Instance-scoped | Written proof steps |
|---|---|---|---|---|---|
| A-C1 | Theorem 1: ρ can be converted into σ via LOCC with an entanglement battery iff E(ρ) ≥ E(σ), for additive, finite E. | verified on instances | – | GB2 | – |
| A-C2 | Theorem 2: the asymptotic rate is R(ρ→σ) = E(ρ)/E(σ) for finite, additive, asymptotically continuous E. | verified | – | – | – |
| A-C3 | Arbitrary mixed-state transformations are reversible: R(ρ→σ)R(σ→ρ) = 1. | verified | – | – | – |
| A-C4 | The theorems are not vacuous: squashed entanglement satisfies the hypotheses. | verified modulo imports | GB13a, GB13b, GB13c | – | – |
| A-C5 | Without additivity the construction trivialises (geometric entanglement). | verified modulo imports and written proof steps | GB15i | GB2 | GB15 |
| A-C6 | Theorem 3: the same statement for thermal operations with a free-energy battery. | verified modulo imports | GB18i | – | – |
| A-C7 | The result is compatible with the no-second-law theorem for non-entangling operations. | verified modulo imports | GB21i | GB2, GB21e | – |

### Edges

| Edge | Route | Kind | Grade | Status | Scope | Statement | Result |
|---|---|---|---|---|---|---|---|
| GB0 | pF-ent ∧ wQ-E ∧ s-bat → p-bat | defines | definition | definition | general | Definition of battery-assisted LOCC: the operation class is defined through the quantifier E. |  |
| GB1 | p-bat ∧ ax-add ∧ ax-mono ∧ ax-fin → t-conv | necessary | logic | checked | general | If ρ → σ under battery-assisted LOCC then E(ρ) ≥ E(σ). | SMT (linear real arithmetic): the four premises entail E(σ) ≤ E(ρ); each premise is needed (4/4 — dropping any one admits a counter-model) |
| GB2 | p-bat ∧ s-bat → t-conv | enables | exact | checked | instances: (dA,dB) = (2,2), (2,3) for the permutation identity (an index identity valid in every dimension) | If E(ρ) ≥ E(σ) then ρ → σ: take τ = σ and swap A↔A', B↔B'; then τ~ = ρ. | exact: the product of Alice's swap A↔A' and Bob's swap B↔B' maps X^{AB}⊗Y^{A'B'} to Y^{AB}⊗X^{A'B'} for symbolic X, Y; SMT: with τ = σ the battery condition is E(ρ) ≥ E(σ) |
| GB3 | p-bat ∧ wQ-E → t-conv | equiv | logic | checked | general | ρ → σ under battery-assisted LOCC iff E(ρ) ≥ E(σ). | SMT: the two implications give the equivalence |
| GB4 | ax-add → wQ-E | implies | logic | checked | general (induction step checked; schema assumed) | E(ρ^{⊗k}) = k E(ρ). | SMT: induction step holds (base case k = 1 is trivial); the induction schema itself is not a kernel rule |
| GB5 | p-bat ∧ ax-add ∧ ax-mono ∧ ax-fin → t-rate | bounds | logic | checked | general | Zero-error rates satisfy m/n ≤ E(ρ)/E(σ). | SMT (nonlinear real arithmetic): m/n ≤ E(ρ)/E(σ); every premise needed |
| GB6 | p-bat ∧ s-bat → t-rate | enables | logic | checked | general | Every pair (n, m) with m E(σ) ≤ n E(ρ) is achieved exactly by relabelling, with battery σ^{⊗m} → ρ^{⊗n}. | SMT: for every pair (n, m) with m E(σ) ≤ n E(ρ) the relabelling of the n source copies and the m battery copies satisfies the battery condition; output is exactly σ^{⊗m} (zero error) |
| GB7 | t-rate → t-rate | implies | logic | checked | general | Rational rates m/n approach E(ρ)/E(σ) from below. | SMT: with m = ⌊n x⌋ and n ≥ 1/δ one has x − δ < m/n ≤ x; existence of the floor is the Archimedean property of the reals (library fact) |
| GB8 | p-bat ∧ wQ-E → t-rate | equiv | logic | checked | general | R_ze(ρ → σ) = E(ρ)/E(σ) for additive, monotone, finite E with E(σ) > 0. | SMT: upper bound and approximation from below force R_ze = E(ρ)/E(σ) (the quantifiers over δ are instantiated by hand, as shown in the premises) |
| GB9 | p-bat ∧ ax-add ∧ ax-mono ∧ ax-fin ∧ ax-ac → t-rate | bounds | logic | checked | general | With error ε: m/n ≤ (E(ρ) + f(ε)/n)/(E(σ) − g(ε) log2 d) whenever g(ε) log2 d < E(σ). | SMT: m/n ≤ (E(ρ) + f/n)/(E(σ) − x) for any modulus x = g(ε)·log2 d with x < E(σ); Eq. (23) is the case g(ε) = Kε; every premise needed |
| GB10 | ax-ac → t-rate | implies | logic | checked | general | The bound of GB9 converges to E(ρ)/E(σ) as ε → 0. | SMT: for every η > 0, once x and f are below explicit thresholds the right-hand side of (23) is at most E(ρ)/E(σ) + η; since g(ε), f(ε) → 0 this gives R ≤ E(ρ)/E(σ) |
| GB11 | p-bat ∧ wQ-E ∧ ax-ac → t-rate | equiv | logic | checked | general | R(ρ → σ) = E(ρ)/E(σ) for finite, additive, monotone, asymptotically continuous E. | SMT: converse (for every η) and achievability (for every δ) force R = E(ρ)/E(σ) (quantifiers instantiated by hand, as shown in the premises) |
| GB12 | t-rate ∧ wQ-E → e-rev | implies | logic | checked | general | R(ρ→σ)·R(σ→ρ) = 1. | SMT: (E(ρ)/E(σ))·(E(σ)/E(ρ)) = 1 for positive finite values |
| GB13a | wQ-sq → ax-add | satisfies | import | imported | general | E_sq is additive on tensor products and does not increase under LOCC. |  |
| GB13b | wQ-sq → sF-ent | equiv | import | imported | general | E_sq(ρ) = 0 iff ρ is separable; E_sq is finite; E_sq of a pure state is the entropy of entanglement. |  |
| GB13c | wQ-sq → ax-ac | satisfies | import | imported | general | \|E_sq(ρ) − E_sq(σ)\| ≤ 16√(2ε) log d + 4h(2√(2ε)) for trace distance ≤ ε. |  |
| GB14 | s-geo ∧ wQ-geo → ax-add | violates | exact | checked | general | E_g(ψ_d^{⊗n}) = E_g(φ+^{⊗n}) = 1 − 2^{−n} while S(ψ_d^A) = 1 + ½ log2(d−1); E_g is not additive. | exact (symbolic d, n): Schmidt spectrum {1/2, 1/(2(d−1)) × (d−1)}; E_g equal to that of a Bell state for every number of copies, entropy of entanglement unbounded in d; E_g violates Eq. (12) |
| GB15 | wQ-geo ∧ p-bat → t-rate | trivialises | compose | composed | general | With E = E_g the battery condition permits φ+^{⊗n} → ψ_d^{⊗n} for every d, hence unbounded singlet yield. | GB14 (equal E_g for every n; entropy unbounded in d) and GB2 (swap protocol) give φ+^{⊗n} → ψ_d^{⊗n}; GB15i then distils ψ_d^{⊗n} to singlets at rate S(ψ_d^A), which exceeds any bound for large d |
| GB15i | pF-ent → t-rate | enables | import | imported | general | Pure states are distilled to singlets by LOCC at rate S(ψ^A). |  |
| GB16 | wQ-neg ∧ s-order → wQ-neg | defines | exact | checked | general | ‖(\|φ+><φ+\|)^{T_A}‖₁ = 2; for σ_ε the trace norm is 1 + 2√(ε(1−ε)). | exact: the partial transpose of √(1−ε)\|00>+√ε\|11> has eigenvalues 1−ε, ε, ±√(ε(1−ε)); trace norm 1 + 2√(ε(1−ε)), equal to 2 for the Bell state, so E_N(φ+) = 1 and E_N > 0 for all 0 < ε < 1 |
| GB17 | wQ-neg ∧ p-bat → t-rate | bounds | logic | checked | general | With error ε the singlet rate under the E_N battery obeys m/n ≤ E_N(ρ) − (1/n)log2(1−ε). | SMT: m/n ≤ E_N(ρ) − (1/n)·log2(1−ε)  (Eq. (79)) |
| GB17i | wQ-neg → ax-add | satisfies | import | imported | general | E_N is additive and LOCC monotone; ‖X^{T_A}‖₁ ≤ d_A‖X‖₁ (Eq. (76)). |  |
| GB18 | p-thbat ∧ wQ-F → t-conv | equiv | logic | checked | general | (ρ,H) → (σ,H') with thermal operations and a free-energy battery iff F(ρ,H) ≥ F(σ,H'). | SMT: the two directions of Theorem 1 with F in place of E |
| GB18i | wQ-F → ax-add | satisfies | import | imported | general | F is additive over non-interacting systems, non-increasing under thermal operations, finite for 0 < T < ∞; swapping system and battery with their Hamiltonians is a thermal operation. |  |
| GB19 | p-bat ∧ wQ-E → sF-ent | defines | logic | checked | general | The states reachable from separable states are exactly those with E = 0. | SMT: σ is reachable from a separable state iff E(σ) = 0 |
| GB20 | wQ-sq ∧ wQ-neg ∧ s-order → t-conv | distinct | logic | checked | general (given the imported properties of E_sq and the existence of PPT entangled states) | The pre-orders induced by E_sq and by E_N disagree on (ρ_PPT, σ_ε): each allows the conversion the other forbids. | exact + SMT: h(ε) → 0 as ε → 0+ and E_N(σ_ε) > 0; hence for small ε the E_N battery allows σ_ε → ρ_PPT and forbids ρ_PPT → σ_ε, while the E_sq battery does the reverse |
| GB20i | sR-ent → s-order | hosts | import | imported | general | PPT entangled states exist. |  |
| GB21i | pX-ent ∧ ax-chan → e-rev | forbids | import | imported | general | Under non-entangling operations, a fixed class of channels, entanglement manipulation is irreversible. |  |
| GB21e | p-bat ∧ ax-chan → p-bat | violates | exact | checked | instances: dA = dB = 2 for the partial-trace identity (valid in every dimension) | The pair (swap, τ = σ) induces the replacement channel X ↦ σ on the system and is admitted only for inputs with E(ρ) ≥ E(σ): battery-assisted LOCC is not a class of non-entangling channels. | exact: tracing the battery out of the swapped state gives σ·tr X for every input X, so the induced channel on the system is the replacement channel X ↦ σ, which maps separable inputs to the entangled target; SMT: for an input with E(ρ') < E(σ) the same pair (Λ, τ) violates the battery condition |
| GB21 | p-bat ∧ pX-ent → e-rev | consistent | logic | checked | general | GB12 (reversibility) does not contradict the irreversibility under non-entangling operations. | scope separation: no-go GB21i needs premise ax-chan; possibility GB12 does not use it; GB21e certifies its absence |
| GB22 | p-bat → p-cat | distinct | definition | definition | general | Battery-assisted LOCC is not catalysis: the battery may change state; only E(τ~) ≥ E(τ) is required. |  |

### Findings

- **Form of asymptotic continuity** (premise). Eq. (13) is linear in the trace norm, K‖ρ−σ‖₁ log2 d + f. The bound available for squashed entanglement from the cited route (Alicki–Fannes; Christandl's thesis, Cor. 4.16) is 16√(2ε) log d + 4h(2√(2ε)), which is not of that form. GB9–GB10 prove Theorem 2 for any modulus g(ε) log2 d + f(ε) with g, f → 0, so the theorem holds for E_sq; the premise node ax-ac is stated in that weaker form.
- **Monotonicity is a premise of Theorem 1** (premise). The statement lists 'additive and finite'; the SMT minimality test shows LOCC monotonicity is also needed for the 'only if' direction (it is implied by 'entanglement measure' in the text). Eq. (21) uses f(ε) for a distance < ε, which needs f nondecreasing (or its monotone envelope).
- **What each direction uses** (structure). Achievability (GB2, GB6) is a relabelling of system and battery whose initial battery state is the target; it uses no property of E. The converse (GB1, GB5, GB9) is three lines of additivity and monotonicity. The operation class is defined through E (GB0), so each admissible E gives its own theory.
- **Free set and order reversal (elementary corollaries, not claimed as new)** (derived). GB19: the free states of the theory are the zero set of E — SEP for E_sq, all PPT states for E_N. GB20: E_sq and E_N order the pair (PPT entangled state, weakly entangled pure state) oppositely.
- **Parts of the paper outside this encoding** (not encoded). Proposition 4 (continuity of E_r with a battery), the results for E_r and E_r^∞, the correlated-battery variant of the Supplement and the multipartite extension were not encoded.

### Proposed network operations

- `ADD` node: p-bat; layer: M.process; why: new operation class; closes the entanglement row of gap QG9 ('entanglement-battery second law, arXiv:2405.10599 [verify]')
- `ADD` node: wQ-sq; layer: O.witness (quantifier); why: the quantifier that makes Theorems 1–2 non-vacuous; currently absent from wQ-ent
- `ROUTE` edge: pF-ent ∧ wQ-E ∧ s-bat → p-bat; why: AND route into a process node with a witness-layer leg: the first operation class in the resource-theory network that is defined through a quantifier
- `ADD` edge: p-bat —reversible→ sR-ent (rate E(ρ)/E(σ); via LOCC + battery relative to E); why: Theorem 2; kernel-checked modulo the imported properties of E
- `SCOPE` edge: W15; note: 'no single monotone can govern all transformations' holds for LOCC and for non-entangling operations; under p-bat(E) the single monotone E governs all transformations by construction
- `SCOPE` edge: C18; note: replace 'candidate route around pX-ent via entanglement batteries (QG9)' by the theorem, with the distinction battery ≠ catalyst (GB22)
- `CITE` gap: QG9; note: citation verified: Phys. Rev. Lett. 135, 010202 (2025), DOI 10.1103/kl56-p2vb
- `OPEN` edge: wQ-(E_r^∞) → ax-add; note: full additivity of the regularised relative entropy of entanglement is stated as unknown in the paper; if it held, p-bat(E_r^∞) would reproduce the rate of F-STEIN

### Graph lint

- nodes 23 (existing 7, new or split 16); S/M/O = 5/10/8; edges 31, of which AND routes 20
- route types: M→O ×8, M∧O→O ×6, O→M ×4, M∧S→O ×2, O→O ×2, O∧S→O ×2, M→M ×2, M∧O∧S→M ×1, O→S ×1, O∧S→M ×1, M∧O→S ×1, S→S ×1
- observables with no direct route from the model layer: wQ-sq, wQ-neg, wQ-geo, wQ-F
- effects without a witness: none
- problems: none

## P. Barrios Hita, A. Trushechkin, H. Kampermann, M. Epping, D. Bruß, Quantum Mechanics Based on Real Numbers: A Consistent Description, Phys. Rev. Lett. 136, 240202 (2026)

GPT / nonclassicality branch (GEN_GPT_Level v2.6). doi: 10.1103/4k13-sdjh; arxiv: 2503.17307.

Phases of the method cycle (read by hand): restructure (the composition postulate is split off the real-QM model node); reduce (the new real-number model is identified with complex quantum theory); falsify (the no-go route of Renou et al. is kept and given its premises explicitly).


### Claims

| Claim | Statement | Verdict | Imports | Instance-scoped | Written proof steps |
|---|---|---|---|---|---|
| B-C1 | A real-number formulation with a modified composition rule reproduces the predictions of complex quantum mechanics, for single and composite systems. | verified modulo written proof steps | – | RQ2, RQ3, RQ5, RQ6, RQ7, RQ8, RQ9, RQ10 | RQ19 |
| B-C2 | The entanglement-swapping experiment of Renou et al. is reproduced by the real model: T = 6√2. | verified on instances | – | RQ6, RQ7 | – |
| B-C3 | This is compatible with the no-go theorem of Renou et al. because the tensor-product postulate is replaced. | verified modulo imports | RQ17 | RQ6, RQ7 | – |
| B-C4 | Real-valued quantum mechanics cannot be falsified, and the use of complex numbers is a matter of convenience. | not decidable by the kernel | – | RQ2, RQ3, RQ5, RQ6, RQ7, RQ8, RQ9, RQ10 | RQ19 |

### Edges

| Edge | Route | Kind | Grade | Status | Scope | Statement | Result |
|---|---|---|---|---|---|---|---|
| RQ1 | ax-complex → f-real | defines | exact | checked | general | T: M_d(C) → M_2d(R) is an injective unital real-algebra homomorphism with T(A†) = T(A)^T, and its image is the commutant of Jd = 1⊗J. | block-matrix identities with d x d matrix symbols (d symbolic): all hold |
| RQ2 | s-C ∧ f-real → s-Rflag | represents | exact | checked | instances: d = 2, 3 (each identity is real-bilinear; the expansion is the same for every d) | S is real-linear and bijective C^d → R^2d with T(A)S(ψ) = S(Aψ), S(iψ) = Jd S(ψ), S(φ)^T S(ψ) = Re<φ\|ψ>, S(φ)^T Jd S(ψ) = −Im<φ\|ψ>, S(ψ)^T T(A) S(ψ) = Re<ψ\|A\|ψ>. | symbolic identities with real symbols for all components, d = 2, 3: all hold |
| RQ3 | s-C ∧ f-real → s-Rflag | represents | exact | checked | instances: d = 2 (consequences of the d-independent identities of RQ1) | T1(ρ) = T(ρ)/2 has unit trace, tr[T1(ρ)T(A)] = Re tr(ρA), and A ≥ 0 ⇒ T(A) ≥ 0. | trace and positivity identities, symbolic 2x2: all hold |
| RQ4 | f-real → s-canon | defines | exact | checked | general | P = (1 − J⊗J)/2 is the orthogonal projector onto span{ψ_even^(2), ψ_odd^(2)}; its kernel is spanned by \|00>+\|11>, \|01>−\|10>; on its range J⊗1 = 1⊗J. | exact 4x4 computation on the two flags: all hold |
| RQ5 | s-Rflag ∧ s-canon → s-indep | composes | exact | checked | instances: (dA,dB) = (2,2), (2,3) (bilinear identities) | S(ψ)⊗_F S(φ) = R(ψ⊗φ): the class of S(ψ)⊗S(φ) has canonical representative R(ψ⊗φ)/√2, and Eq. (34) is R(ψ⊗φ). | symbolic vectors, (dA,dB) = (2,2), (2,3): all hold |
| RQ6 | f-real → s-canon | defines | exact | checked | instances: N = 1..6 (the product form makes the J_k statement immediate for every N) | ψ_even^(N) + iψ_odd^(N) = 2^{−(N−1)/2}(\|0>+i\|1>)^{⊗N}; J_k ψ_even = ψ_odd and J_k ψ_odd = −ψ_even for every flag k; the subspace on which all J_k agree is two-dimensional. | integer arithmetic, N = 1..6 flags (common-subspace dimension for N = 2..5): all hold |
| RQ7 | s-canon → f-real | defines | exact | checked | instances: N <= 5 | I^(N) is a projector, (J^(N))² = −I^(N); I^(N+M) = (I^(N)⊗I^(M) − J^(N)⊗J^(M))/2, J^(N+M) = (I^(N)⊗J^(M) + J^(N)⊗I^(M))/2; partial traces of I^(N), J^(N) are I^(N−M), J^(N−M). | exact rational matrices, N up to 5: all hold |
| RQ8 | f-real ∧ s-indep → ax-P4 | satisfies | exact | checked | instances: (dA,dB) = (2,2), (2,3) | (T(A)⊗1)R(Ψ) = R((A⊗1)Ψ) and (1⊗T(B))R(Ψ) = R((1⊗B)Ψ) for all A, B and all Ψ ∈ C^dA⊗C^dB. | 880 exact checks on real bases of operators and of C^dA (x) C^dB: (T(A) (x) 1) R(Psi) = R((A (x) 1) Psi) and the same on the B side, all hold |
| RQ9 | f-real ∧ s-canon → m-realflag | defines | exact | checked | instances: dA = dB = 2 (bilinear in A and B) | T(A)⊗T(B) commutes with P and P(T(A)⊗T(B)) = Re(A⊗B)⊗I^(2) + Im(A⊗B)⊗J^(2) = ½[T(A)⊗T(B) − T(iA)⊗T(iB)]. | 64 operator pairs (real basis of M_2(C) x M_2(C)): [P, T(A)(x)T(B)] = 0, P (T(A)(x)T(B)) = Re(A(x)B)(x)I^(2) + Im(A(x)B)(x)J^(2), and this equals (1/2)[T(A)(x)T(B) - T(iA)(x)T(iB)]: all hold |
| RQ10 | m-realflag ∧ s-indep → o-born | predicts | exact | checked | instances: dA = dB = 2 (real-multilinear identity) | R(Φ)^T [T(A)⊗T(B)] R(Ψ) = Re<Φ\|A⊗B\|Ψ>; hence all bipartite Born probabilities coincide with those of complex QT, entangled states included. | 16384 exact checks (real bases of A, B, Phi, Psi; d = 2 each): the real bilinear form equals Re<Phi\|A(x)B\|Psi> |
| RQ11 | m-quantum ∧ s-indep → w-T | predicts | exact | checked | general | Complex QT with \|φ+>_{AB1}\|φ+>_{B2C}, A = (Z, X, Y), C = ((X±Z), (Y±Z), (X±Y))/√2 and Bob's Bell measurement gives P(b) = 1/4 and T = 6√2. | exact in Q(√2, i): P(b) = 1/4 for all b; T_b = (3/2)√2 = 6√2·P(b) for all b; T = 6*√2 (= 6√2 ≈ 8.4853) |
| RQ12 | m-realflag ∧ s-indep → w-T | predicts | exact | checked | general | The real model with state \|φ+>\|φ+>\|ψ_even^(4)> and operators T(Π^A)⊗T(Π^B)⊗T(Π^C) gives the same probabilities P(a,b,c\|x,z) as complex QT for all outcomes and settings, hence T = 6√2. | 112 moments <Π_b>, <A_x Π_b>, <Π_b C_z>, <A_x Π_b C_z> (they fix all 288 probabilities P(a,b,c\|x,z)) agree exactly with complex QM; state, operators and values contain no imaginary part; T = 6*√2 |
| RQ13 | w-T → w-T | defines | exact | checked | general | The value 6√2 is obtained with the functional of Renou et al.; the form printed in the arXiv text (Eqs. (104)–(106), as extracted) differs in one sign prefactor and in the weighting. | T = 6√2 only with the prefactor (-1)^{b1} on (S_25 + S_26) and with either (joint correlators, plain sum over b) or (conditional correlators, P(b) weights); with (-1)^{b2} the outcomes b = 01, 10 give 4√2·P(b) and T = 5√2; joint correlators with an additional P(b) weight give 5√2/4 |
| RQ14 | m-realflag ∧ s-indep → s-canon | predicts | exact | checked | general | After Bob's outcome 00 the real Alice–Charlie state is \|φ+><φ+\|_AC ⊗ ½(\|φ−><φ−\| + \|ψ+><ψ+\|)_{A'C'}. | exact: P(00) = 1/4 and the normalised Alice-Charlie state equals \|φ+><φ+\|_AC ⊗ (1/2)(\|φ-><φ-\| + \|ψ+><ψ+\|)_{A'C'}; the flag factor is I^(2)/2 |
| RQ15 | s-canon ∧ ax-tensorR → s-indep | violates | exact | checked | general | The composite space has real dimension 2·dA·dB, not (2dA)(2dB), and the canonical state of two independent sources, ψ_even^(4) on flags (A'B1')(B2'C'), has Schmidt rank 2 across the source cut: the model does not satisfy postulate (iv) with product states for independent sources. | exact: the composite space of two qubits has real dimension 8 = 2·dA·dB, not 16 = (2dA)(2dB); ψ_even^(4) = (ψ_even^(2)⊗ψ_even^(2) − ψ_odd^(2)⊗ψ_odd^(2))/√2 has Schmidt rank 2 across (A'B1')\|(B2'C'); the product ψ_even^(2)⊗ψ_even^(2) projects onto ψ_even^(4)/√2 |
| RQ16 | m-realflag → ax-loctom | satisfies | exact | checked | general | dim SY_n = n² = dim Herm_n and (nm)² = n²m²: the flag composition is locally tomographic; the real tensor product on symmetric matrices is not (excess nm(n−1)(m−1)/4). | symbolic in n, m: the flag composition is locally tomographic on SY (same count as complex QT); the real tensor product on Sym has nm(n−1)(m−1)/4 extra parameters, > 0 for n, m ≥ 2 |
| RQ17 | m-realqm ∧ ax-tensorR ∧ s-indep → e-net | forbids | import | imported | general | Real QM with postulate (iv) and independent real sources obeys T ≤ 7.6605. |  |
| RQ18 | f-real ∧ m-realflag → ax-complex | satisfies | exact | checked | general | T(−iH) = −Jd T(H): the generator of the orthogonal group T(e^{−iHt}) is −Jd times the observable T(H). | T(−iH) = −Jd T(H) (d symbolic); for Hermitian H the generator −Jd T(H) is antisymmetric and the observable T(H) symmetric (d = 2 explicit) |
| RQ19 | m-realflag ∧ m-quantum → t-distinguish | equiv | compose | composed | general | The real model and complex QT are isomorphic as theories (states, effects, composition, probabilities), so no experiment discriminates them. | RQ1–RQ3 (single systems), RQ5–RQ9 (composition and local action) and RQ10 (Born rule on composites) give a bijection of states and observables that preserves every probability |
| RQ20 | m-realflag ∧ m-realqm ∧ e-net → t-distinguish | consistent | logic | checked | general | RQ12 (T = 6√2 in the flag model) does not contradict RQ17 (T ≤ 7.6605): the premise 'postulate (iv)' of RQ17 fails for the flag model (RQ15). | scope separation: no-go RQ17 needs premise ax-tensorR; possibility RQ12 does not use it; RQ15 certifies its absence |
| RQ21 | m-realflag → t-distinguish | claims | interpretive | not decidable | general | 'The use of complex numbers is a matter of convenience.' |  |

### Findings

- **Sign and weighting in the restated functional** (note). In the arXiv text (Eqs. (104)–(106) of the PDF, (S96)–(S98) in the HTML rendering of v2; both read by an automatic extractor) the prefactor of (S_25+S_26) is (−1)^{b2} and T is Σ_b P(b)T_b with joint-probability correlators. Renou et al. have (−1)^{b1} and T = Σ_b T_b. Only the latter gives 6√2 for every b (RQ13); the printed form gives 5√2/4. The paper's own evaluation uses b = 00 with conditional correlators ±1/√2, where the difference vanishes, so its results are unaffected. The journal's Supplemental Material was not checked.
- **Index in Eq. (123)** (note). The list of correlators contains S^00_44 where the functional uses S^00_34 (as extracted).
- **What the equivalence is** (structure). RQ4–RQ9 show that ⊗_F is the tensor product over C written in real coordinates, and RQ15 that the state of two independent sources is correlated across the sources inside the ambient real tensor product. The no-go edge of Renou et al. keeps all its premises; the new model does not satisfy one of them.
- **Two papers, one projector** (structure). The combination rule of Hoffreumon and Woods (arXiv:2504.02808, Eqs. (B.34)–(B.37)) and the flag product are the same compression by P = (1 − J⊗J)/2 (RQ9): two routes into the same target node.

### Proposed network operations

- `SPLIT` target: m-realqm; into: ['m-realqm (with ax-tensorR)', 'ax-tensorR']; why: the composition postulate is the premise that the 2025–26 papers change; it must be a node of its own so that edges D6 and F5 can name it
- `ADD` node: f-real; layer: M.frame; why: realification is a change of representation, not a model
- `GLUE` node: m-realflag; with: m-quantum; why: RQ19: same states, effects, composition and probabilities; if model nodes are identified as GPTs up to linear isomorphism (the layer is described as 'concrete GPTs'), this is one node with two representations
- `ADD` node: e-net; layer: O.effect; why: edge D6 currently targets e-bell; the theorem of Renou et al. concerns the network functional T, not Bell nonlocality
- `RETARGET` edge: D6; from: m-realqm → e-bell; to: m-realqm ∧ ax-tensorR ∧ s-indep → e-net; why: states the premises under which the no-go holds (RQ17) and survives RQ12
- `SCOPE` edge: GN7; note: 'In real QM the generator is not an observable without superselection' — the flag model is exactly the superselection case: observables commute with J (RQ1, RQ18)
- `REWRITE` node: ax-complex; note: definition in terms of a complex structure J rather than of the number field, since RQ18 realises it over R

### Graph lint

- nodes 16 (existing 5, new or split 11); S/M/O = 4/8/4; edges 21, of which AND routes 14
- route types: M∧S→S ×4, M∧S→O ×4, M→M ×3, M→S ×2, M∧S→M ×2, M→O ×2, S→S ×1, S→M ×1, O→O ×1, M∧O→O ×1
- observables with no direct route from the model layer: none
- effects without a witness: e-net
- problems: none

## ATLAS Collaboration, Observation of quantum entanglement with top quarks at the ATLAS detector, Nature 633, 542–547 (2024)

Particle-physics branch (GEN_HEP v1.2) glued to the quantum-information branches. doi: 10.1038/s41586-024-07824-z; arxiv: 2311.07288.

Phases of the method cycle (read by hand): predict (the vertex and the Born rule give the lepton distributions and the expected D); observe (D is measured in the threshold window); calibrate (the separability bound and the measurement are folded through simulation); deficit (the observed D lies below the expected one).


### Claims

| Claim | Statement | Verdict | Imports | Instance-scoped | Written proof steps |
|---|---|---|---|---|---|
| C-C1 | D = tr C/3 is measured as −3<cos φ> from the charged-lepton directions. | verified | – | – | – |
| C-C2 | D < −1/3 is a sufficient condition for entanglement. | verified | – | – | – |
| C-C3 | The criterion applies to the measured phase-space average. | verified | – | – | – |
| C-C4 | The observed D = −0.537 ± 0.002 ± 0.019 is more than five standard deviations from a scenario without entanglement. | verified modulo imports | TQ13, TQ14 | – | – |
| C-C5 | Entanglement is observed in top-quark pairs. | verified modulo imports | TQ13, TQ14 | – | – |

### Edges

| Edge | Route | Kind | Grade | Status | Scope | Statement | Result |
|---|---|---|---|---|---|---|---|
| TQ1 | m_A → s-ttspin | defines | exact | checked | general | Every two-qubit state is fixed by the 15 Pauli expectation values B+, B−, C. | exact: the 15 real coefficients (B+, B−, C) are the Pauli expectation values and determine ρ |
| TQ2 | m_cc ∧ s_t ∧ s_b ∧ s_W ∧ s_lep → o-lepdir | predicts | exact | checked | general (tree level, massless lepton and neutrino; no on-shell condition is used) | For t(p_t, s) → b ℓ+ ν through the V−A current: Σ\|M\|² ∝ (p_b·p_ν)((p_t − m s)·p_ℓ), so dΓ/dΩ ∝ 1 + ŝ·q̂+ in the top rest frame. | exact polynomial identity in all 20 momentum and spin components, m and m_b: Σ\|M\|² = 8·(p_b·p_ν)·((p_t − m s)·p_ℓ), independent of m_b; in the top rest frame (p_t − m s)·p_ℓ = m E_ℓ (1 + ŝ·q̂): analysing power κ = +1 |
| TQ3 | m_cc ∧ s_t ∧ s_b ∧ s_W ∧ s_lep → o-lepdir | predicts | exact | checked | general (tree level, massless lepton and neutrino) | For t̄ → b̄ ℓ− ν̄: Σ\|M\|² ∝ (p_b̄·p_ν̄)((p_t̄ + m s)·p_ℓ), so dΓ/dΩ ∝ 1 − ŝ·q̂−. | exact polynomial identity: Σ\|M\|² = 8·(p_b̄·p_ν̄)·((p_t̄ + m s)·p_ℓ); in the antitop rest frame (p_t̄ + m s)·p_ℓ = m E_ℓ (1 − ŝ·q̂): analysing power κ = −1 |
| TQ4 | o-lepdir ∧ m_A → o-joint | defines | exact | checked | general | The decays act on the spins as measurements with effects (1 + q̂+·σ)/4π and (1 − q̂−·σ)/4π. | exact: the unique Hermitian operators with expectation (1 ± ŝ·q̂)/4π on every pure spin state are (1 ± q̂·σ)/4π; they integrate to the identity over the sphere |
| TQ5 | s-ttspin ∧ m_cc ∧ m_A → o-joint | predicts | exact | checked | general | (1/σ) dσ/dΩ+dΩ− = [1 + B+·q̂+ − B−·q̂− − q̂+·C·q̂−]/(4π)². | exact: tr[ρ (1 + q̂+·σ)⊗(1 − q̂−·σ)] = 1 + B+·q̂+ − B−·q̂− − q̂+·C·q̂− (divide by (4π)² for the density) |
| TQ6 | o-joint → o-cosphi | predicts | exact | checked | general | (1/σ) dσ/dcos φ = ½(1 − D cos φ) with D = tr C/3, and <cos φ> = −D/3. | exact integration: the density of cos φ is (1 − D cos φ)/2 with D = tr C/3 (B+ and B− drop out), it is normalised, and <cos φ> = −D/3 |
| TQ6b | o-cosphi → w-D | defines | definition | definition | general | D = −3<cos φ>. |  |
| TQ7 | s-sep → w-D | bounds | exact | checked | general (finite mixtures; limits of mixtures by continuity of the linear functional) | Separable states satisfy tr C ≥ −1, i.e. D ≥ −1/3. | exact: for Bloch vectors with \|a\|, \|b\| ≤ 1 the identity writes 2(1 + a·b) as a sum of non-negative terms, so tr C = a·b ≥ −1 on product states; tr C is linear in ρ, so the bound holds on the convex hull (separable states). Hence D ≥ −1/3 |
| TQ8 | s-sep → w-D | bounds | exact | checked | general | tr C + 1 < 0 iff <Φ+\|ρ^{T_B}\|Φ+> < 0, which contradicts positivity of the partial transpose. | exact: tr C + 1 < 0 is the statement <Φ+\|ρ^{T_B}\|Φ+> < 0, so ρ^{T_B} is not positive and ρ is not separable (partial transposes of separable states are states). Equivalent form: D < −1/3 iff the singlet fraction exceeds 1/2 |
| TQ9 | s-ttavg → w-D | bounds | exact | checked | general (two-component mixtures; finite mixtures by induction) | The bound holds for the phase-space average with event-dependent common spin axes, and a violation implies entanglement of ρ(k) on a set of positive weight. | exact + SMT: tr C = 2 tr[ρ SWAP] − 1 is unchanged when both spins are referred to rotated common axes, and an average below −1 forces a component below −1 |
| TQ10 | d-singlet → w-D | predicts | exact | checked | general | −1 ≤ D ≤ 1/3 for every state; D = −1 for the spin singlet. | exact: −3 ≤ tr C ≤ 1, i.e. −1 ≤ D ≤ 1/3 for every state; the value D = −1 is attained only by the singlet (the eigenvalue −3 is non-degenerate) |
| TQ11 | w-D ∧ s-ttspin → e-ttent | witness | logic | checked | general | D < −1/3 implies that the state is entangled. | SMT: contraposition |
| TQ12 | m-qcd → s-ttspin | predicts | import | imported | general | Near threshold about 80% of t t̄ production comes from a spin-singlet state. |  |
| TQ13 | m-mc ∧ w-D → o-limit | calibrates | import | imported | general | The parton-level bound D = −1/3 corresponds to −0.322 ± 0.009 (Powheg+Pythia) or −0.27 (Powheg+Herwig) at particle level. |  |
| TQ14 | m-mc → o-Dobs | calibrates | import | imported | general | D = −0.537 ± 0.002 ± 0.019 observed; −0.470 ± 0.002 ± 0.017 expected. |  |
| TQ15 | o-Dobs ∧ o-limit ∧ w-D → e-ttent | witness | exact | checked | general | The observed D lies more than five standard deviations below the folded separability bound. | exact arithmetic on the quoted numbers: distance to the folded bound −0.322 is 0.215 = 10.2σ (uncertainties added in quadrature, bound uncertainty 0.009 included); to the alternative bound −0.27 it is 0.267 = 14.0σ; the separation stays above 5σ unless the total uncertainty exceeds 0.043 |
| TQ16 | o-Dobs ∧ m-mc → o-Dobs | flags | exact | checked | general (arithmetic only; not a statistical statement of the paper) | Observed − expected = −0.067 in the signal region. | exact arithmetic: observed − expected = -0.067; this is 2.6σ if the two uncertainties are treated as independent (their correlation is not given in the text used) |
| TQ17 | m_cc ∧ m_A ∧ w-D → e-ttent | scope | definition | definition | general | The witness presupposes the quantum description of the decay (TQ2–TQ4); it is not a Bell test. |  |

### Findings

- **What the witness certifies** (structure). TQ9: a violation certifies entangled spin states on a set of production kinematics of positive weight, with spins referred to event-dependent axes; it is a statement about an ensemble. TQ17: the inference uses the decay vertex and the Born rule as premises, so it is a witness, not a Bell test.
- **Two routes to the same bound** (structure). TQ7 (sum of squares on product states + convexity) and TQ8 (partial transpose) give the same threshold; D < −1/3 is the statement that the singlet fraction exceeds 1/2.
- **Quoted numbers** (arithmetic). TQ15: 10.2σ from the Powheg+Pythia bound and 14.0σ from the Powheg+Herwig bound under simple quadrature, consistent with 'more than five'. TQ16: the observed value is 0.067 below the expected one (2.6σ if the uncertainties were independent).
- **Imported edges** (premise). The folding of the bound to particle level (TQ13), the measured value with its systematics (TQ14) and the production dynamics (TQ12) are outside what the kernel can regenerate. TQ2–TQ3 are tree level with unit analysing power; radiative corrections to it are not included.
- **Versions** (note). The first arXiv version quotes D = −0.547 ± 0.002 ± 0.021; the published value is −0.537 ± 0.002 ± 0.019.

### Proposed network operations

- `EXTEND` node: m_cc; note: J_CC gains the term t̄_L γ^μ b_L; by Rule 4 (route composition) this is one more route t(1) ∧ b(1) ∧ W(1) into the same vertex
- `ADD` node: s_t, s_b; layer: S.sector; why: Rule 8 (sector refinement); the released graph omits the third generation and the strong sector
- `PREDICT` edge: m_cc ∧ m_A → o-lepdir, o-joint, o-cosphi; why: model → observable edges of status 'pred'; TQ2–TQ6 regenerate them from the vertex
- `GLUE` node: w-D; with: w-entw (GEN_GPT_Level), wD-ent (GEN_QRT_Level); why: D is an entanglement witness in the sense of those nodes: linear in ρ, bounded on the separable set (TQ7)
- `GLUE` node: e-ttent; with: s-ent / sR-ent; why: first shared concept between the particle-physics branch and the two quantum-information branches that is an observable on one side and a state property on the other
- `CALIBRATE` edge: m-mc → o-limit, o-Dobs; why: Rule 9: these edges carry the fitted and simulated inputs; the conclusion depends on them and they are imports for the kernel
- `FLAG` node: o-Dobs; note: observed more negative than expected (TQ16); the paper states that bound-state effects near threshold are not in the generators. A pseudoscalar excess at the t t̄ threshold was later reported by CMS (Rep. Prog. Phys. 88, 087801 (2025))
- `FIBRE` note: over the fixed model node (m_cc ∧ m_A) the observables o-cosphi in bins of m_tt̄ form one effect with one witness: an instance of the contraction lemma of the grand network (effect networks are fibres of the historical graph over a model node)

### Graph lint

- nodes 20 (existing 7, new or split 13); S/M/O = 9/4/7; edges 18, of which AND routes 9
- route types: M∧O→O ×4, S→O ×4, M∧S→O ×3, O→O ×3, M→S ×2, O∧S→O ×1, M→O ×1
- observables with no direct route from the model layer: o-cosphi, w-D
- effects without a witness: none
- problems: none

## T. Hossain with Claude (Anthropic), Particle decays as fixed measurements: exact noncontextuality thresholds for decay-angle correlations, generated work, 17 November 2026 (unpublished, not peer reviewed)

Across branches: GEN_HEP v1.2 (charged-current vertex) and GEN_GPT_Level v2.6 (contextuality), glued to GEN_QRT_Level v1.2. status: generated work; location: decay_contextuality/.

Phases of the method cycle (read by hand): deficit (two released nodes (GEN_HEP:m_cc, GEN_GPT_Level:e-ctx) have no route between them); hypothesize (a decay is modelled as one fixed covariant measurement (p-decay)); falsify (single-setting data cannot violate Bell or steering inequalities (FW3, FW4)); predict (thresholds for noncontextual models (Theorems 1–5)); observe (applied to measured top-pair and hyperon data (A1–A4)).


### Claims

| Claim | Statement | Verdict | Imports | Instance-scoped | Written proof steps |
|---|---|---|---|---|---|
| C1 | A decay is one fixed covariant measurement; V-A decays give sharp effects for the antifermion direction and \|κ\| = 1/3 for the direction-only leptonic three-body decay. | verified modulo written proof steps | – | – | DV6 |
| C2 | With one setting per side Bell and steering tests are empty, and the recorded-outcome model is not noncontextual. | verified | – | – | – |
| C3 | Spin 1/2, one particle: noncontextual iff P\|κ\| ≤ 1/3. | verified modulo imports | FW1 | – | – |
| C4 | Two spin-1/2 particles: the joint decay data are noncontextual iff ρ_raw and its partial transpose are positive semidefinite; for unpolarised pairs iff ‖c‖₁ ≤ 1; \|D\| > 1/3 implies contextual data. | verified modulo imports and written proof steps | FW1 | – | H3, H4 |
| C5 | Spin 1, one particle: noncontextual iff (η₁, η₂) in R (η₂ ≠ 0). | verified modulo imports and written proof steps | FW1 | – | FW6, V1, V5 |
| C6 | Maximally entangled spin-1 pair with one decay on each side: noncontextual iff the product of ratios lies in R₂; ideal W pairs need visibility above 5/8. | verified modulo imports and written proof steps | FW1, A7 | – | FW6, V1, P3 |
| C7 | Spin j: the largest vector analysing power of a noncontextual polarimeter is the largest Gauss or Gauss-Radau node ξ₂ⱼ; for pairs ‖ <qA qBᵀ> ‖₁ ≤ ξ(2j_A) ξ(2j_B). | verified modulo imports and written proof steps | FW1 | – | FW6, G1, G3, G5, H3, V1 |
| C8 | Top pairs: the measured D certifies contextual lepton-direction data at the significance quoted for entanglement, without the value of the analysing power. | verified modulo imports and written proof steps | FW1, A1 | – | H3 |
| C9 | Hyperon pairs: with the fitted BESIII parameters the proton-antiproton angular data are contextual for \|cos θ\| < 0.517. | verified modulo imports and written proof steps | FW1, A3 | – | H3, H4 |
| C10 | The b-quark direction is a nonclassical top polarimeter iff m_t > 2 m_W; the neutrino direction sits within about one percent of the boundary. | verified modulo imports | FW1 | – | – |
| C11 | Vector mesons: the baryon direction of J/ψ → Λ Λ̄ is a nonclassical polarimeter; J/ψ → Σ+ Σ̄- sits at the boundary; ψ(2S) → τ τ is classical. | verified modulo imports and written proof steps | FW1, A7 | – | FW6, V1, V5 |

### Edges

| Edge | Route | Kind | Grade | Status | Scope | Statement | Result |
|---|---|---|---|---|---|---|---|
| DV1 | m_cc ∧ u_mh → p-half | derives | exact | checked | general | For [ubar_2 γ^μ P_L u_1(s)][ubar_3 γ_μ P_L v_4] with massless 2,3,4: sum \|M\|² = 8 ((p1 - m s).p4)(p2.p3). | polynomial identity in 20 real symbols: sum \|M\|^2 = 8 ((p1-m s).p4)(p2.p3) |
| DV2 | p-half ∧ s-spin → o-ang1 | derives | exact | checked | general | In the parent rest frame (p1 - m s).p4 = m E4 (1 + s.q): recording the direction of fermion 4 (charged lepton or down-type quark of a top decay) is the rank-one covariant effect (1 + q.σ)/4π, κ = +1, at every value of the other variables. | (p1-ms).p4 = m E (1+s.q); effect 1+q.sigma has determinant 0 on \|q\|=1 |
| DV3 | m_mu ∧ u_mh → p-half | derives | exact | checked | general | Three-body V-A decay with fermion 3 recorded (electron of μ decay, charged lepton of leptonic τ decay): effects x²[(3-2x) - (2x-1) q.σ]; direction only: \|κ\| = 1/3; with the energy recorded the sharpest effect has \|κ\| = 1. | tensor coefficients 1/12, 1/6; spectrum x^2[(3-2x)-(2x-1)cos]; integrated analysing power = -1/3; endpoint analysing power = 1; with cut x>x0: \|kappa\|(x0) = -(3*x0**3 + x0**2 + x0 + 1)/(3*(x0**3 - x0**2 - x0 - 1)) |
| DV4 | m_cc ∧ u_mh → p-half | derives | exact | checked | general | t → b W, narrow width, m_b = 0, b direction: κ_b = -(ξ-2)/(ξ+2), ξ = m_t²/m_W²; \|κ_b\| > 1/3 iff m_t > 2 m_W. | kappa_b = -(xi-2)/(xi+2); equals -1/3 at xi = [4], i.e. m_t = 2 m_W |
| DV5 | m_cc ∧ u_mh → p-half | derives | numeric | checked | general | Neutrino or up-type-quark direction: κ_ν = [(ξ-1)(ξ²-11ξ-2)+12 ξ ln ξ]/[(ξ+2)(ξ-1)²]; quadrature of the matrix element reproduces it and the published leading-order values; κ_ν = -0.336 at the PDG 2026 masses, \|κ_ν\| = 1/3 at m_t = 173.0 GeV. | quadrature reproduces kappa_l=1, kappa_b, kappa_nu closed forms and the published LO values (-0.40622, -0.31817); at PDG 2026 masses kappa_b = -0.3951, kappa_nu = -0.3365 (+-0.0022 from m_t); \|kappa_nu\| = 1/3 at xi = 4.6338 (m_t = 172.99 GeV for the PDG 2026 m_W) |
| DV6 | m_A ∧ u_mh → p-decay | derives | compose | composed | general | Rotational covariance of the decay and the Born rule give E(q) = (d/4π) R_q D R_q† with D ≥ 0, Tr D = 1, [D, J_z] = 0. | proof written in the paper; checked by no program |
| DV7 | m_A ∧ u_m1 → p-one | derives | exact | checked | general | Spin 1: R_q D_w R_q† = 1/3 + (η₁/2) q.S + (η₂/6)(3 (q.S)² - 2); symbol of σ = (1/3, p, A): 1/3 + (η₁/2) p.q + (η₂/2) qᵀ A q. | Tr(QQ) identity; kernel = 1/3 + (eta1/2) q.S + (eta2/6)(3(q.S)^2-2); symbol 1/3 + (eta1/2) p.q + (eta2/2) q^T A q; pure-state (p,A); m1 = p.p'/2, m2 = (3/5) Tr(AA') |
| DV8 | p-decay ∧ s-spin → o-ang1 | derives | numeric | checked | instance: j <= 4 | First moment of the polarimeter: int q E_w(q) dq = κ₁ J/(j+1); the coefficient of P.q in 4 π p(q) is 3 j κ₁/(j+1). | j = 1/2..4: LP value of max\|<J>\|/(j+1) over Husimi-nonnegative operators equals the quadrature node (max dev 3.8e-07); attaining kernels are probability vectors (min weight 0.0008) |
| DV9 | p-half ∧ s-ent → o-ang2 | derives | exact | checked | general | Two decays: (4π)² p = 1 + a.qA + b.qB + qAᵀ c qB with a = κ_A B_A, b = κ_B B_B, c = κ_A κ_B C; ρ_raw = (D_kA ⊗ D_kB) ρ; a sign flip of one analysing power is a partial transpose up to a local unitary. | sign flip of one analysing power = partial transpose up to a local unitary |
| DV10 | o-ang2 → o-D | derives | definition | definition | general | D = -3 <cos phi> = -tr(c)/3. |  |
| DV11 | p-half ∧ s-ent → s-steer | defines | definition | definition | general | Back-edge: conditioning on the direction recorded by the partner polarimeter prepares the state of A with data Bloch vector v(qB) = (a + c qB)/(1 + b.qB). |  |
| DV12 | m_va ∧ m_mu → o_wu | derives | compose | composed | general | The decay asymmetries of the released graph are first multipoles of the polarimeter: o_wu is the l = 1 coefficient of o-ang1. | graded as a written proof step, but the text gives neither the statement nor a proof (the catalogue lists it as 'proof in text'); it is used without statement in Sec. II B; checked by no program |
| FW1 | ax-tomo ∧ m-classical → m-ncom | defines | import | imported | general | A fragment (states Omega, effects E) has a noncontextual model iff id_V = sum_l Z_l g_l with g_l ≥ 0 on Omega and e(Z_l) ≥ 0 for all e in E. |  |
| FW2 | o-ang2 → m-lhv1 | implies | exact | checked | general | With one setting per side the recorded outcomes are themselves local hidden variables. | identity for the recorded-outcome model; int (3q_z^2-1)(1, k q) dq = 0, so two outcome functions with different response functions give the same effect |
| FW3 | m-lhv1 → e-bell | forbids | logic | checked | general | Single-setting data cannot violate a Bell inequality. | identity for the recorded-outcome model; int (3q_z^2-1)(1, k q) dq = 0, so two outcome functions with different response functions give the same effect |
| FW4 | m-lhv1 → e-steer | forbids | logic | checked | general | A single-measurement assemblage always has a local hidden-state model (λ = outcome). | identity for the recorded-outcome model; int (3q_z^2-1)(1, k q) dq = 0, so two outcome functions with different response functions give the same effect |
| FW5 | m-lhv1 ∧ p-half → m-ncom | not_implies | exact | checked | general | The recorded-outcome model is not noncontextual: outcome functions differing by an l ≥ 2 harmonic define the same effect and are given different response functions. | identity for the recorded-outcome model; int (3q_z^2-1)(1, k q) dq = 0, so two outcome functions with different response functions give the same effect |
| FW6 | p-decay ∧ s-spin → m-ncom | equiv | compose | composed | general | Covariant reduction (all multipole ratios nonzero): the fragment (all states, E_w) is noncontextual iff (η₁, ..., η₂ⱼ) lies in the convex hull of the points m_l(ψ, Z) = d Tr(Pi_l[ψ ψ†] Pi_l[Z])/(2l+1), ψ a unit vector, Z unit-trace with nonnegative Husimi function. | proof written in the paper; checked by no program |
| FW7 | p-decay → w-ncineq | witness | definition | definition | general | Simplex-embedding LPs on finite sub-fragments: infeasible implies contextual; LPs on finite subsets of the dual cones: feasible implies noncontextual. |  |
| H1 | p-half ∧ s-spin → m-ncom | implies | exact | checked | general | Polarisation P and analysing power κ with P\|κ\| ≤ 1/3: explicit four-state (tetrahedral) model. | sum_j mu xi = (1+v.q)/4pi; mu >= 0 iff \|v\| <= 1/3; four ontic states |
| H13 | p-half ∧ s-spin → m-ncom | equiv | exact | checked | general | Polarisation vectors filling an ellipsoid with semi-axes P1, P2, P3: noncontextual iff \|κ\|(P1+P2+P3) ≤ 1 (six ontic states along the principal axes); planar ensembles: P\|κ\| ≤ 1/2. | six-state model reproduces (1+v.q)/4pi; weights nonnegative iff alpha_k >= r_k; with sum alpha_k = 1 this requires r1+r2+r3 <= 1 (Z3, unsat otherwise) |
| H2 | p-half ∧ s-spin ∧ w-ncineq → e-ctx | implies | logic | checked | general | P\|κ\| > 1/3 implies no noncontextual model: 3 = sum_l t_l.b_l ≤ sum_l \|b_l\| ≤ 1/(P\|κ\|). | premises entail rho <= 1/3 (unsat); each premise needed: [True, True, True, True] |
| H3 | m-ncom ∧ o-ang2 → w-rawppt | implies | compose | composed | general | If the joint data have a noncontextual model then ρ_raw and its partial transpose are positive semidefinite. | proof written in the paper; checked by no program |
| H4 | w-rawppt ∧ ax-tomo → m-ncom | implies | compose | composed | general | If ρ_raw passes the test, a noncontextual model exists: from a separable decomposition, directly if the coefficient matrix is invertible and after the cone-preserving projections of the range lemma otherwise. | proof written in the paper; checked by no program |
| H12 | w-rawppt ∧ ax-tomo → m-ncom | implies | numeric | checked | instance: 200 random singular matrices | Range lemma: a subspace meeting the interior of the Bloch cone has a projection onto it that maps the cone into itself; a separable decomposition of a singular coefficient matrix can therefore be moved into its range and row space. | 200 random singular matrices (rank 3 and 2): projections idempotent (1.8e-15), images inside the cone (min margin 3.2e-12), in the row space (2.0e-15), decomposition reproduced (6.7e-16); the original h_j were outside the row space (min distance 0.01) |
| H5 | s-tstate ∧ w-rawppt → e-ctx | equiv | exact | checked | general | Unpolarised pairs, any rank of c: noncontextual iff ‖c‖₁ ≤ 1; explicit model with at most seven ontic states from the singular value decomposition. | spectra of rho_raw and its partial transpose are the eight forms (1+-c1+-c2+-c3)/4; all >= 0 iff \|c1\|+\|c2\|+\|c3\| <= 1; product-form identity for the explicit model |
| H6 | o-D ∧ w-rawppt → e-ctx | implies | exact | checked | general | \|D\| > 1/3 implies contextual data: <Φ+\| ρ_raw^T_B \|Φ+> = (1 + tr c)/4 and <Ψ-\| ρ_raw \|Ψ-> = (1 - tr c)/4. | PSD of rho_raw and of its partial transpose imply -1 <= tr c <= 1 |
| H7 | p-half ∧ s-ent → m-ncom | implies | exact | checked | general | \|κ_A\| ≤ 1/3 or \|κ_B\| ≤ 1/3: the corresponding local map is entanglement breaking, ρ_raw passes the test for every state. | Choi spectrum {1+3k, 1-k (x3)}/4, partial transpose {1-3k, 1+k (x3)}/4: PPT iff -1/3 <= k <= 1/3 |
| H8 | e-ctx ∧ o-ang2 → s-ent | implies | compose | composed | general | Contextual decay data imply an entangled pair state; the converse holds for all states iff \|κ_A κ_B\| = 1. | proof written in the paper; checked by no program |
| H9 | w-rawppt ∧ w-entw → e-ctx | witness | compose | composed | general | The test acts on the raw angular coefficients; the entanglement test acts on the coefficients divided by the analysing powers. The two coincide iff \|κ_A κ_B\| = 1. | proof written in the paper; checked by no program |
| H10 | s-steer ∧ w-ncineq → e-ctx | witness | numeric | checked | instance: three families | Two-sided LP bracket of the threshold on random pair states and on the hyperon pair. | inner <= exact <= outer in all 6 runs; bracket width at N = 250: 0.0229; hyperon pair: sub-fragment LP infeasible at cos theta = [0.0, 0.4], dual-cone LP feasible at [0.65] |
| V1 | p-one → w-region1 | derives | compose | composed | general | Nonnegative quadratic functions on the sphere (Lemma 3): 2/3 + p.q + qᵀ A q ≥ 0 on the sphere iff a 4x4 matrix pencil is positive semidefinite, i.e. iff it is a sum of squares of affine functions; moment form: (t, z, N) are moments of a positive measure on the sphere iff [[t, zᵀ],[z, N]] ≥ 0 with tr N = t. | proof written in the paper; checked by no program |
| V2 | p-one → w-region1 | derives | numeric | checked | instance: 200 random matrices | Rank-one decomposition lemma (Lemma 3a), checked constructively on random instances. | 200 random instances: residual 2.0e-13 (lightlike columns and M reproduced) |
| V3 | p-one ∧ s-spin → w-region1 | derives | exact | checked | general | Support function of the region: h_R(a,b) = max{ b/5 + √(b²/25 + a²/3), -4b/5 }; R = conv(ellipse 3 η₁² + 25 (η₂ - 1/5)² ≤ 1, apex (0,-4/5)). | t_B root; ellipse 3x^2+25(y-1/5)^2=1 traced by tau in [1/2,2]; apex (0,-4/5); top (0,2/5); tangent points (+-2sqrt2/5, 4/25); alpha window [-1/2,1/3]; x >= 1/8 |
| V4 | p-one ∧ s-spin → m-ncom | implies | exact | checked | general | Explicit finite noncontextual models (icosahedral orbits of one pair) at the extreme points of R. | \|I\| = 60; R top (0, 2/5):ok; R coherent (1/2, 1/10):ok; R max vector (1/sqrt3, 1/5):ok; R tangent (2sqrt2/5, 4/25):ok; R apex (0, -4/5):ok; R2 top (0, 8/5):ok; R2 isotropic WW (5/8, 5/8):ok; R2 tangent Gamma(sqrt3-1):ok |
| V5 | p-one ∧ s-spin ∧ w-region1 → e-ctx | equiv | compose | composed | general | For η₂ ≠ 0 the fragment (all spin-1 states, E_w) is noncontextual iff (η₁, η₂) in R. | proof written in the paper; checked by no program |
| V6 | w-region1 ∧ w-ncineq → e-ctx | witness | numeric | checked | general | Independent numerical values of the support function (SDP) and of the boundary (brute-force LP without the covariant reduction). | max \|SDP - closed form\| over 24 directions x 16 pure states: 8.4e-09 \|\| 12 directions, K = 220 operators, 900 grid directions: LP/closed in [1.0001, 1.0079] |
| V7 | p-one ∧ s-spin → m-ncom | equiv | exact | checked | general | Exactly degenerate kernel η₂ = 0: noncontextual iff \|η₁\| ≤ 2/9 (fragment-relative equivalences); the limit η₂ → 0 of R gives √2/3. | symbol (1/3)(1 + (3 eta1/2) p.q); eigenvalues 1/3, 1/3 +- \|p\|/2; threshold eta1 = 2/9 |
| P1 | p-one ∧ s-iso1 → w-region1 | derives | exact | checked | general | Maximally entangled pair, one decay on each side: steered states are images of the coherent cone; noncontextual iff (η₁^A η₁^B, η₂^A η₂^B) in R₂ = conv(Γ, mirror image, (0,-4/5)), Γ(s) = ((2/3)s(2-s), (2/5)s²), 0 ≤ s ≤ 2. | AM-GM step (Z3, unsat); stationary value 2a^2/(9(a/3-b/5)); Gamma convex (x'y''-y'x'' = 16/15); tangent at s = sqrt3-1; diagonal point (5/8,5/8); eta2 = 1 at eta1 = -5/3 + 2*sqrt(10)/3; axis range [-4/5, 8/5] |
| P2 | p-one ∧ s-iso1 → m-ncom | implies | exact | checked | general | Explicit finite models at extreme points of R₂, including the alignment-only point (0, 8/5). | \|I\| = 60; R top (0, 2/5):ok; R coherent (1/2, 1/10):ok; R max vector (1/sqrt3, 1/5):ok; R tangent (2sqrt2/5, 4/25):ok; R apex (0, -4/5):ok; R2 top (0, 8/5):ok; R2 isotropic WW (5/8, 5/8):ok; R2 tangent Gamma(sqrt3-1):ok |
| P3 | p-one ∧ s-iso1 ∧ w-region1 → e-ctx | equiv | compose | composed | general | Isotropic state of visibility v: products scale by v; two ideal W decays are contextual iff v > 5/8 (entangled iff v > 1/4); with one Z → l+ l- decay on a side the data are noncontextual for every v. | proof written in the paper; checked by no program |
| P6 | p-one ∧ s-iso1 ∧ w-region1 → e-ctx | derives | exact | checked | general | Critical visibilities for pairs of kernels: 5/8 (W W), 2/5 (two decays into pseudoscalar pairs; one such decay with a dilepton or W decay); dilepton pairs, W Z and Z Z are noncontextual for every visibility. | v_c = 5/8 (W W), 2/5 (PP PP), 2/5 (PP with l l or with W); (l l)(l l), W Z and Z Z noncontextual for every v (boundary at eta2 product 1: eta1 product 0.4415; A_e = 0.1515) |
| P4 | w-region1 ∧ w-ncineq → e-ctx | witness | numeric | checked | general | Brute-force LP for the pair region. | 9 directions, K = 264 operators, 700 grid directions: LP/closed in [0.9879, 1.0086] |
| P5 | w-region1 ∧ w-ncineq → e-ctx | witness | numeric | checked | general | Refinement of the three LP directions that deviated by more than 0.5 per cent: the deviations shrink with the grids. | R at 90 deg: 1.0069 -> 1.0019 (grid 900 -> 3600); R2 at 270 deg: 1.0100 -> 1.0022 (grid 700 -> 2800); R2 at 80 deg: 0.9879 -> 1.0001 (tau = 1.8 added) |
| G1 | p-decay ∧ s-spin ∧ w-kappa → e-ctx | implies | compose | composed | general | If \|κ₁(w)\| > ξ₂ⱼ the spin-j polarimeter is contextual on all states. | proof written in the paper; checked by no program |
| G2 | w-kappa → w-kappa | derives | exact | checked | general | ξ₁ = 1/3, ξ₂ = 1/√3, ξ₃ = (1+√6)/5, ξ₄ = √(3/5); extremal polynomials attain them. | xi_1 = 1/3, xi_2 = 1/sqrt3, xi_3 = (1+sqrt6)/5, xi_4 = sqrt(3/5); extremal polynomials attain them; j=1 kernel w = (0.6553, 0.2667, 0.0780) |
| G3 | p-decay ∧ s-spin → m-ncom | implies | compose | composed | general | The bound is the supremum: the kernel D* = (d/4π) int Q*(q)\|q><q\| dq, Q* the extremal polynomial, is noncontextual with κ₁ = ξ₂ⱼ when its multipole ratios are nonzero (checked for j ≤ 4); in general by a perturbation. | proof written in the paper; checked by no program |
| G5 | m-ncom ∧ o-ang2 → w-kappa | implies | compose | composed | general | Pairs of arbitrary spins: a noncontextual model has the form p = sum_l r_l(qA) s_l(qB) with nonnegative polynomials of degree 2jA, 2jB (Prop. 2), hence ‖ <qA qBᵀ> ‖₁ ≤ ξ(2j_A) ξ(2j_B) (Thm 5c). | proof written in the paper; checked by no program |
| G7 | p-decay → w-kappa | derives | numeric | checked | instance: degrees 1 to 8 | First-moment bound behind Thm 5: a nonnegative polynomial of degree n on the sphere with unit integral has first moment at most ξ_n; random non-zonal instances stay below, the extremal zonal polynomial attains it. | degrees 1..8: largest first moment over random nonnegative polynomials stays below xi_n (closest: 1.000 of the bound); the extremal zonal polynomial attains xi_n (max dev 1.6e-15) |
| G6 | w-kappa ∧ w-rawppt ∧ w-region1 → w-kappa | derives | numeric | checked | general | Consistency of the first-moment inequality with the exact criteria: ‖c‖₁ ≤ 1 for spin 1/2; v \|η₁A η₁B\| ≤ 2/3, the largest abscissa of R₂, for the spin-1 pair. | spin 1/2: bound is \|\|c\|\|_1 <= 1; spin 1: POVM first moment eta1 S/2 (dev 3.8e-06), singlet <S_i S_k> = -(2/3) delta_ik (dev 2.2e-16), bound v\|eta1A eta1B\| <= 2/3 = h_R2(1,0); thresholds (j+1) xi^2/j = 1/3 (j = 1/2), 2/3 (j = 1) |
| G4 | w-kappa ∧ w-ncineq → e-ctx | witness | numeric | checked | instance: j <= 4 | LP value of max \|<J>\| over operators with nonnegative Husimi function and positivity of the attaining kernels, j ≤ 4. | j = 1/2..4: LP value of max\|<J>\|/(j+1) over Husimi-nonnegative operators equals the quadrature node (max dev 3.8e-07); attaining kernels are probability vectors (min weight 0.0008) |
| A1 | s-ttbar ∧ p-half → o-D | import | import | imported | general | ATLAS: D = -0.537 ± 0.002 ± 0.019 (particle level, 340 < m_tt < 380 GeV), folded bound -0.322 ± 0.009; CMS: D = -0.480 +0.026 -0.029 (parton level). |  |
| A2 | o-D ∧ s-ttbar → e-ctx | implies | exact | checked | general | Arithmetic on the quoted numbers: 10.2 σ (ATLAS, with its folded bound) and 5.1 σ (CMS, bound -1/3). | ATLAS: (bound - D)/sigma = 10.2 with the quoted particle-level bound; CMS parton level: (-1/3 - D)/sigma = 5.06; \|tr c\| = 3\|D\| = 1.44 (CMS), bound for noncontextual data: 1 |
| A3 | s-LLbar ∧ p-half → o-ang2 | import | import | imported | general | Joint angular distribution of e+e- → J/ψ → Λ Λ̄ and the fitted parameters α_ψ, Δ Φ, α_-, α_+. |  |
| A4 | s-LLbar ∧ w-rawppt → e-ctx | implies | numeric | checked | general | With the fitted form: the production state is a valid rank-2 state; ‖c‖₁ = 1.108 at 90 degrees; ρ_raw fails the test for \|cos θ\| < 0.517 (46% of events). | production state PSD with rank <= 2 at all angles (min eigenvalue -3.1e-16); \|\|c\|\|_1 at 90 deg = 1.1081 (1.1090 +- 0.0088 with alpha_avg^2); raw operator fails PPT for \|cos theta\| < 0.5172 (range 0.501-0.535 under one-sigma shifts), 46.5% of events; min \|det R_raw\| in the window 2.44e-02 |
| A5 | m_cc ∧ p-half → p-half | import | import | imported | general | Leading-order and QCD-corrected analysing powers of top decay products. |  |
| A6 | m_va ∧ u_mh → p-half | import | import | checked | general | τ → π ν: κ = 1; τ → ρ ν (ρ direction): (m_τ² - 2 m_ρ²)/(m_τ² + 2 m_ρ²) = 0.45. | kappa = (m_tau^2 - 2 m_rho^2)/(m_tau^2 + 2 m_rho^2) = 0.449 for m_tau = 1776.93 MeV, m_rho = 775.26 MeV |
| A7 | m_nc ∧ u_m1 → p-one | import | import | imported | general | Z → f fbar: kernel (η₁, η₂) = (A_f, 1) for massless fermions; W → l ν: (±1, 1); vector → two pseudoscalars: (0, -2). |  |
| A8 | u_m1 ∧ p-one ∧ w-region1 → e-ctx | implies | numeric | checked | general | Fermion-pair decays of vector mesons (direction only): J/ψ → Λ Λ̄ has w₀ = 0.151 < 1/5 (contextual on all states); J/ψ → Σ+ Σ̄- sits at the boundary w₀ = 3/5 within about one standard deviation; ψ(2S) → τ τ lies inside the window. | w0(alpha) = (1-alpha)/(3+alpha); window alpha in [-1/2, 1/3]; J/psi -> Lambda Lambdabar: w0 = 0.151, 39 sigma below 1/5; J/psi -> Sigma+ Sigmabar-: w0 = 0.605 +- 0.005, 1.1 sigma above 3/5; psi(2S) -> tau tau: x = 0.232 >= 1/8, alpha = 0.037 |
| H11 | s-sep ∧ p-half → m-ncom | implies | compose | composed | general | Separable pair states give noncontextual decay data for all analysing powers: the local scaling maps preserve separability. | proof written in the paper; checked by no program |
| X3 | m-quantum ∧ m_A → p-decay | defines | definition | definition | general | The polarimeter is a POVM of quantum theory on C⁽²ʲ⁺¹⁾; the released frame node m_A (GEN_HEP) and model node m-quantum (GEN_GPT_Level) are glued here. |  |
| X1 | e-ctx → m-classical | forbids | import | imported | general | Released edge A5 (simplex embedding) is the definition used here. |  |
| X2 | s-ent ∧ p-decay → e-ctx | necessary | compose | composed | general | Released edge A8 (contextuality is a precondition for entanglement) with the measurement fixed to the decay polarimeter: holds for \|κ_A κ_B\| = 1 and fails otherwise (H8). | proof written in the paper; checked by no program |

### Findings

- **Generated work** (note). This is not a published paper. Its results, proofs, code and text were produced by an AI system (Claude, Anthropic) in a session directed by T. Hossain on 17 November 2026; nothing has been peer reviewed. The 15 routes graded compose are proofs written in the paper that no program and no independent reviewer has checked.
- **Rebuilt from the session record** (note). The project in decay_contextuality/ was rebuilt on 20 November 2026 from the tool calls of the session that wrote it. The rebuilt encoding agrees with the published page of 17 November in all 35 nodes, 63 route statements and 11 claims. All certificates were executed again on 20 November 2026, including the four long linear-programme runs (about 30 minutes): the outputs of all 63 routes agree with the outputs recorded on the page, the 11 verdicts of the paper's own kernel are unchanged, and 16 of 16 negative controls are rejected.
- **Locations** (premise). The location fields of the original encoding use an earlier lettering of the appendices (for example App. E for the numerical cross-checks, which are App. H of the paper) and give Lemma 2 for the lemma on nonnegative quadratic functions, which is Lemma 3 in the paper. The locations used here are those of the final text; the original ones are kept in the note of each route.
- **Dependencies added** (premise). The original encoding lists, for each claim, the routes named in it, and no route-to-route dependencies. The dependencies used here were read from the proofs in the paper. With them the closure of claim C8 (top pairs) contains the written necessity proof of Theorem 2 (H3) and Lemma 1 (FW1, imported), and the closure of claim C10 (top polarimeters) contains Lemma 1 through the proof of Theorem 1 (H2).
- **A written step that the text does not contain** (premise). DV12 (the decay asymmetries of the released graph are the first multipoles of the polarimeter) has grade compose and is listed in the catalogue of the paper (App. I) as 'proof in text'. The text neither states nor proves it; Sec. II B uses it ('the V-A spectrum with its decay asymmetry'). No claim depends on it.
- **Verdicts printed in the paper** (premise). Table IV of the paper and the sentence of Sec. VI 'Two claims are verified by executed certificates alone' come from the paper's own kernel, which closes a claim over the routes named in it only. That kernel gives C8 'verified modulo imports' and C10 'verified'. Closed over the dependencies of the proofs, C8 is verified modulo imports and written proof steps and C10 modulo imports; one claim (C2) rests on executed certificates alone. The other nine verdicts agree.

### Proposed network operations

- `ADD` node: s-spin, s-steer, s-tstate, s-iso1, s-ttbar, s-LLbar; note: state layer: spin states, steered ensembles, two families of pair states, two measured systems
- `ADD` node: p-decay, p-half, p-one, m-lhv1, m-ncom, ax-tomo; note: model layer: the decay polarimeter (general, spin 1/2, spin 1), the recorded-outcome model, the noncontextual model and the tomographic-completeness assumption
- `ADD` node: o-ang1, o-ang2, o-D, w-rawppt, w-region1, w-kappa; note: observable layer: angular distributions, the opening-angle coefficient and three tests
- `ROUTE` edge: m_cc ∧ u_mh → p-half → o-ang2 → w-rawppt → e-ctx; note: closes the unconnected pair (GEN_HEP:m_cc, GEN_GPT_Level:e-ctx) that was taken as the question
- `GLUE` edge: X3; note: GEN_HEP:m_A (Born rule) with GEN_GPT_Level:m-quantum
- `GLUE` node: m-ncom; note: with GEN_GPT_Level:m-classical and GEN_QRT_Level:sF-ctx
- `SCOPE` edge: GEN_GPT_Level:A8; note: contextuality as a precondition of entanglement: with the measurement fixed to a decay the implication is strict and becomes an equivalence only for |κ_A κ_B| = 1 (H8, X2)
- `OPEN` gap: s-iso1 → e-ctx outside the isotropic family (H → WW*, ZZ*); note: open problem 1 of the paper
- `OPEN` gap: p-decay → m-ncom for j ≥ 3/2 beyond the vector direction; note: open problem 2

### Graph lint

- nodes 35 (existing 17, new or split 18); S/M/O = 10/13/12; edges 63, of which AND routes 53
- route types: M∧S→M ×17, O→O ×9, M∧S→O ×8, M→O ×7, M∧O∧S→O ×6, M→M ×4, O∧S→O ×4, O→M ×2, M∧O→O ×2, M∧O→M ×2, M∧S→S ×1, O→S ×1
- observables with no direct route from the model layer: w-entw
- effects without a witness: e-bell, e-steer
- problems: none

## Negative controls

| Control | Planted error | Detected | Detail |
|---|---|---|---|
| battery necessity, reversed conclusion | claim E(σ) ≥ E(ρ) instead of E(σ) ≤ E(ρ) | yes |  |
| battery necessity without monotonicity | drop LOCC monotonicity | yes |  |
| battery necessity with subadditivity only | replace additivity on the output by E(σ⊗τ~) ≤ E(σ)+E(τ~) | yes | a merely subadditive quantifier does not give Theorem 1 |
| swap protocol with Alice's swap only | Bob does not swap B and B' | yes |  |
| T with a 'J' that squares to +1 | T(A) = [[A1,-A2],[-A2,A1]] | yes | multiplicativity fails without J² = −1 |
| real model with product flag state | flags of the two sources in ψ_even^(2)⊗ψ_even^(2) instead of ψ_even^(4) | yes | Σ_b <Π_b> = 1/2 instead of 1: the product vector is not a state of the model |
| network functional with the printed prefactor | (−1)^{b2} on (S_25 + S_26) | yes | T = 5*√2 |
| Charlie's C3 with its imaginary part removed | C3 = Z/√2 instead of (Y+Z)/√2 | yes | <A3 Π00 C3> = 0 instead of -1/8*√2 |
| top decay with a right-handed quark current | γ^μ P_R instead of γ^μ P_L at the t–b–W vertex | yes | the squared amplitude is no longer proportional to (p_b·p_ν)((p_t − m s)·p_ℓ) |
| separability bound tr C ≥ −1/2 | claim a stronger bound than −1 | yes | the sum-of-squares identity does not hold; \|↑↓> attains −1 |
| witness with a value above the bound | conclude entanglement from D < −0.30 | yes |  |
| scope separation with a shared premise | name a premise that both edges use | yes |  |
| decay paper k01 | spin-1/2 threshold 1/2 instead of 1/3: the tetrahedral weights (1+3 t.v)/4 must stay nonnegative at \|v\| = 1/2. | yes | weight -0.125 < 0 at \|v\| = 1/2 |
| decay paper k02 | direction-only leptonic analysing power 1/2 instead of 1/3. | yes | integral gives 1/3 |
| decay paper k03 | Dirac trace with (p1 + m s) instead of (p1 - m s). | yes | identity fails with the wrong sign of the spin vector |
| decay paper k04 | T-state criterion with the Frobenius norm instead of the trace norm: c = diag(1/2,1/2,1/2) would be accepted. | yes | Frobenius norm 0.866 <= 1 but raw-PPT margin -0.125 < 0 |
| decay paper k05 | ellipse centred at (0, 1/4) instead of (0, 1/5). | yes | extreme pair tau = 1 is not on the shifted ellipse |
| decay paper k06 | apex of R at (0, -1) instead of (0, -4/5): support value in direction (0,-1) from the dual cone. | yes | support value is 4/5, extreme pair gives -0.800 |
| decay paper k07 | twirl coefficient m2 = (1/2) Tr(AA') instead of (3/5) Tr(AA'): the finite model at the top of R must fail. | yes | icosahedral twirl differs from Pi_0 + 1/3 Pi_2 |
| decay paper k08 | top of R2 at 2 instead of 8/5, which would make two ideal W decays on a singlet noncontextual. | yes | h(1,1) = 1.600 < 2 = (1,1).(1,1) |
| decay paper k09 | isotropic W-pair threshold 1/2 instead of 5/8: (1/2,1/2) must be strictly inside R2 and (5/8,5/8) on its boundary. | yes | (1/2,1/2) is interior; boundary slack at (5/8,5/8) = 3.8e-08 |
| decay paper k10 | largest noncontextual vector analysing power for spin 1 claimed to be 0.6 instead of 1/sqrt3. | yes | LP value 0.57735 |
| decay paper k11 | b-quark polarimeter nonclassical iff m_t > 3 m_W (instead of 2 m_W). | yes | threshold xi = [4], not 9 |
| decay paper k12 | hyperon-pair state with the wrong sign of C_yy: must not be a density matrix. | yes | min eigenvalue -0.208 |
| decay paper k13 | \|D\| <= 1/2 claimed as the noncontextuality bound: the witness values (1 +- tr c)/4 vanish at \|tr c\| = 1, i.e. \|D\| = 1/3. | yes | witness is zero at \|D\| = 1/3, negative at 1/2 |
| decay paper k14 | recorded-outcome model declared noncontextual: needs int (3 q_z^2 - 1) E(q) dq != 0, which is false. | yes | the l = 2 outcome function integrates to the zero effect |
| decay paper k15 | range lemma with the Euclidean orthogonal projector instead of the boosted one: for a subspace that does not contain the time axis the Euclidean projection throws lightlike vectors out of the cone. | yes | Euclidean projector: min Lorentz norm -0.877 < 0; boosted projector: 1.3e-06 |
| decay paper k16 | two decays into pseudoscalar pairs on a singlet: threshold visibility 1/2 instead of 2/5; the point (0, 2) must lie outside R2. | yes | h(0,1) = 1.600 < 2; boundary at 4 v = 8/5 |
