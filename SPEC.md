# GEN edge kernel: specification, version 0.2 (2026-11-20)

Version 0.1 (2026-11-17) covered the three published papers. Version 0.2 adds the verdict rule 1.1
(Section 4), the grade `numeric` in use, and a fourth, generated paper (`paper_decay.py`).

A method for checking a physics paper against the GEN concept graphs. The paper is written as
nodes and routes; a small program, the kernel, regenerates each route from the definitions of its
end nodes; whatever cannot be regenerated is listed. The output is a verdict for each headline
claim together with the exact list of things the claim rests on, and a list of operations on the
released networks.

This file fixes the terms. `kernel.py` implements them.

## 1. Objects

**Concept graph.** Nodes `v` with a layer (S state, M model, O observable), a sub-layer and a
definition. Routes `r = (inputs, target, kind, statement)`. A route with several inputs is an AND
route. Several routes into one target are alternatives. This is the structure of the released
networks (`gen-grand/1`).

**Checked graph.** Every route also carries

| Field | Meaning |
|---|---|
| `statement` | one formal sentence in terms of the definitions of its end nodes |
| `where` | the place in the paper that asserts it |
| `cert` | a program that the kernel runs, or nothing |
| `grade` | how the statement is established (Section 3) |
| `scope` | `general`, or `instances: ...` when the certificate ran for some parameter values only |
| `uses` | the routes whose statements the certificate takes as premises |

**Paper.** New nodes and routes on top of the released networks (a node that already exists keeps
its identifier), a list of headline claims (each names the routes it rests on), and a list of
operations on the released networks (the delta).

## 2. What the kernel does

**K1, lint.** Checks identifiers, layers and sub-layers; counts the layer-pair signature (route
legs from each layer to each layer), the route types and the AND routes; lists observables that no
route reaches from the model layer, and effects that have no witness among their inputs.

**K2, certificates.** Runs every certificate. A certificate that raises an error has failed.

**K3, closure.** For each headline claim, collects all routes reachable through `uses` and assigns
one verdict (Section 4), together with the lists of imports, instance-scoped routes and
unmechanised compositions on the way.

**Rule: scope separation.** A no-go route `N` and a possibility route `P` are accepted together
if (i) some node `q` is an input of `N`, (ii) `q` is not an input of `P`, (iii) `P` is checked, and
(iv) a checked route of kind `violates` shows that the model of `P` lacks `q`. Otherwise the pair is
reported as a contradiction to be resolved.

## 3. Grades

| Grade | What is run | What it establishes |
|---|---|---|
| `exact` | symbolic or exact-arithmetic computation: matrix identities with symbolic entries or symbolic dimension, exact arithmetic in a number field, symbolic integration, polynomial identities | the statement for all values of its symbols; for the listed parameter values only when the scope says `instances` |
| `logic` | SMT entailment: premises and negated conclusion are unsatisfiable; then each premise is dropped in turn (a premise is *needed* if the solver finds a counter-model without it). Kernel rules also have this grade | the conclusion from exactly the listed premises |
| `import` | nothing | nothing; the route joins the trust list of every claim that uses it |
| `definition` | nothing | the route unfolds a definition |
| `numeric` | floating-point computation with a stated tolerance (linear and semidefinite programmes, quadrature, random instances), or the reading of a recorded long run | the statement at that tolerance and on the instances run; evidence, never proof |
| `compose` | nothing | a composition of other routes, or a proof given in the paper, written in words and not mechanised ("written proof step") |
| `interpretive` | nothing | the statement is not mathematical; the kernel does not decide it |

One more grade exists in the code and is not used: `witness` (an explicit object evaluated exactly, for
existence and counterexample claims). `numeric` is used only by the generated paper (13 routes).

## 4. Verdicts

Rule 1.1 (2026-11-20). One label per claim, the first that applies, over the routes of the claim and all
routes reachable from them through `uses`:

1. `discrepancy`: a route on the way failed.
2. `not decidable by the kernel`: an interpretive route is on the way.
3. `numerical support only`: a numeric route is on the way, and no route of grade exact, logic, witness or
   compose.
4. `verified modulo imports and written proof steps`: a route of grade compose and an import are on the way.
5. `verified modulo written proof steps`: a route of grade compose is on the way, no import.
6. `verified modulo imports`: all certificates pass and at least one route is an import.
7. `verified on instances`: all certificates pass, no imports, at least one exact, logic or witness route has
   instance scope.
8. `verified`: all certificates pass with general scope.

The lists of imports, numeric routes, instance-scoped routes and unmechanised steps are always reported next
to the label.

Rule 1.0 (2026-11-17) had no labels 4 and 5 and returned label 3 whenever a numeric route was on the way. Rule
1.1 is the rule of the kernel written with the generated paper (session of 2026-11-17), which closes a claim
over the routes named in it only; the edge kernel closes over `uses`. Under rule 1.1 two verdicts of the
published papers change label, with the same lists: A-C5 (battery) from "verified modulo imports" to
"verified modulo imports and written proof steps", and B-C1 (real-number QM) from "verified on instances" to
"verified modulo written proof steps".

## 5. How to encode a paper

1. **Identity.** Citation, DOI, arXiv identifier and the version that was read.
2. **Nodes.** One per object the argument uses. Reuse released identifiers. A node that enters an
   `exact` route needs a definition that can be executed (a matrix, a polynomial, a set given by
   generators or constraints).
3. **Routes.** One statement each, with its place in the paper.
4. **Certificates.** Use the strongest grade available. An identity is never certified numerically.
5. **Premise audit.** For `logic` routes read the minimality result: every listed premise should be
   needed, and every needed premise should be stated in the paper. For imports, write the imported
   statement in the form the route needs and compare it with the form the source gives.
6. **Library check.** For each no-go route of the released networks that bears on a new
   possibility route, add a scope-separation rule.
7. **Controls.** Plant an error in each family of certificates and confirm it is rejected.
8. **Delta.** List the operations on the released networks.

## 6. Trusted base

The verdicts are relative to: the Python interpreter, SymPy (symbolic algebra and integration),
Z3 (SMT), the exact-arithmetic module `exact.py`, the kernel itself, and the fidelity of the
encoding to the paper. The last item is the weakest: nothing checks that a statement written into
a route is the statement the paper makes.

## 6a. A generated paper

`paper_decay.py` encodes a paper that is not published: a generated work, written with its encoding and its
certificates by an AI system (Claude, Anthropic) in a session directed by T. Hossain on 17 November 2026
(`decay_contextuality/`). Its nodes, routes and certificates are imported unchanged from
`decay_contextuality/net/`. The edge kernel adds the `uses` dependencies (read from the proofs of the paper),
the locations in the compiled text, the delta and the findings. Because the paper and its encoding come from
the same session, the check is not independent of the text; it tests the certificates and the closure, not
the fidelity of the encoding.

## 7. What the kernel does not do

- It does not find proofs. Certificates are written by the encoder (here an AI system) and only
  checked by the kernel.
- It does not handle limits, infinite-dimensional spaces or asymptotic statements except through
  explicit finite inequalities (as in routes GB9 to GB11) or imports.
- It does not audit imported theorems or measured values.
- It has no single logical foundation, so two routes can use the same word for different things
  without the kernel noticing. Lean excludes this by construction.

## 8. Files written by a run

- `out/results.json` (`gen-check/1`): metadata, totals, and for every paper its nodes, routes with
  certificate output, claims with verdicts, lint, delta and findings; the negative controls.
- `out/delta_<paper>.json` (`gen-check-delta/1`): new nodes, all routes with grade and status, the
  released nodes they are glued to, and the operations. Meant as input for a network release.
- `out/report.md`: the same content as tables.

Totals of the run of 2026-11-20 (four papers): 133 routes, 89 checked (54 exact, 21 logic, 13 numeric, 1 import
with a consistency check), 18 imported, 8 definitions, 17 written proof steps, 1 interpretive, 0 failed. 27
headline claims: 6 verified, 2 verified on instances, 8 verified modulo imports, 2 verified modulo written proof
steps, 8 verified modulo imports and written proof steps, 1 not decidable. 28 of 28 planted errors rejected.
