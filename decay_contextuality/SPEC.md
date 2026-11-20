# Encoding format

The encoding is the Python module `net/encoding.py`; `run_all.py` writes its evaluated form to `out/results.json`.

## Nodes

`N(id, layer, sub, label, definition, released=None, glue=None)`

* `layer`: `S` (state: what is prepared), `M` (model: what assigns probabilities), `O` (observable: what is recorded or decided).
* `sub`: type inside the layer. State: `uir` (particle as a representation), `hilbert`, `cluster` (family of states), `free`, `resource`,
  `sector`. Model: `frame` (postulate), `fund` and `eff` (interaction terms), `model`, `process` (measurement), `axiom`.
  Observable: `direct` (recorded quantity), `witness` (test), `effect`.
* `released`: name of the released graph whose node identifier is kept (`GEN_HEP`, `GEN_GPT_Level`), or `None` for a new node.
* `glue`: identifiers of the same concept in another released graph.

## Routes

`R(id, inputs, target, kind, statement, where, grade, certs=None, scope='general', refs=None)`

* `kind`: `derives`, `implies`, `equiv`, `forbids`, `not_implies`, `necessary`, `witness`, `defines`, `import`.
* `where`: place of the statement in the paper.
* `grade`:
  * `exact`: symbolic or exact-arithmetic check (SymPy);
  * `logic`: SMT entailment (Z3);
  * `numeric`: floating point with a stated tolerance, or the reading of a recorded long run;
  * `import`: cited statement or measured number (a consistency certificate may be attached);
  * `definition`;
  * `compose`: proof written in the paper, not mechanised (shown as "written").
* `certs`: functions returning `{'ok': bool, 'detail': str, ...}`. A route with certificates is `checked` if all return `ok`.
* `scope`: `general`, or `instance: ...` when the certificate covers instances only.

## Claims

`{'id', 'text', 'routes'}`. The verdict is computed by `kernel.close_claims`, by precedence:

1. `discrepancy` if any route fails;
2. `numerical support only` if no route is exact, logic or written;
3. `verified modulo imports and written proof steps` / `verified modulo written proof steps` if a written route is used;
4. `verified modulo imports` if an import is used;
5. `verified on instances` if an instance-scoped route is used;
6. `verified` otherwise.

## Lint, scope separation, negative controls

* `kernel.lint`: unknown nodes or grades; new recorded quantities without a route from the model layer; new effects without a witness;
  unused nodes; the count of (input layer, target layer) pairs.
* `kernel.scope_separation`: a no-go route and a possibility route are accepted together only if a premise of the no-go is absent
  from the possibility route and a checked route shows that the model lacks it. Used for "single-setting data violate no Bell
  inequality" against "single-setting data can fail noncontextuality".
* `net/controls.py`: each control plants one error in an accepted statement and must be rejected by the corresponding check.

## Recorded runs

`out/lp_R.json`, `out/lp_R2.json`, `out/lp_refine.json`, `out/two_qubit_sandwich.json` are written by `checks/slow_*.py` and read by
the certificates `cert_lp_region`, `cert_lp_refine`, `cert_two_qubit_sandwich`. Inputs quoted from the literature are in
`net/certs_numeric.py` (`INPUTS`), each with its source.
