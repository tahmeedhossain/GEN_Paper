# Decay contextuality graph (generated work)

> **Generated work.** This result, its proofs, its code and its text were produced by an AI system
> (Claude, Anthropic) in a session directed by T. Hossain on 17 November 2026. It is unpublished and has not
> been peer reviewed. The 15 routes graded "written" are proof steps that no program and no independent
> reviewer has checked; 14 are proofs given in the paper, and one (DV12) is listed as written but is not
> stated in the text.

Code, recorded runs and paper sources for

> T. Hossain with Claude (Anthropic), *Particle decays as fixed measurements: exact noncontextuality thresholds
> for decay-angle correlations*, generated work, 17 November 2026 (unpublished, not peer reviewed).
> PDF: `paper/main.pdf`.

A particle decay records the spin of its parent through one fixed rotation-covariant measurement. This archive
contains the routes that connect the charged-current vertex of the Standard Model graph (`GEN_HEP`) to the
generalized-contextuality node of the Nonclassicality Network (`GEN_GPT_Level`), with one executable certificate
per route wherever a statement can be checked by a program.

In this repository the edge kernel at the root encodes the paper as its fourth paper (`paper_decay.py`, which
imports `net/encoding.py` unchanged) and replays it in reading order (`orders.DECAY`).

## Results recorded here

| Statement | Where | Status |
|---|---|---|
| Spin 1/2, one particle: noncontextual iff `P|kappa| <= 1/3` | Theorem 1 | exact model, logic check of the bound |
| Two spin-1/2 particles: noncontextual iff `rho_raw` and its partial transpose are positive | Theorem 2 | written proof, exact corollaries, LP bracket |
| Spin 1: noncontextual iff `(eta1, eta2)` lies in the hull of an ellipse and a point | Theorem 3 | written proof, exact formulas, SDP and LP cross-checks |
| Spin-singlet pair of spin-1 particles: region `R2`; two `W -> l nu` decays need visibility `> 5/8` | Theorem 4 | written proof, exact formulas, LP cross-check |
| Spin j: largest vector analysing power is a Gauss or Gauss-Radau node; `||<qA qB^T>||_1 <= xi xi` for pairs | Theorem 5 | written proof, LP for j <= 4, random tests |
| Top pairs, hyperon pairs, top polarimeters, vector mesons | Section V | arithmetic on cited numbers |

The verdict of each headline claim is the weakest status among its routes (`out/summary.txt`).
Fifteen routes are graded as written proofs; no program has checked them. One of them, DV12, is not stated in the text
(finding of the edge kernel, 20 November 2026).

## Reproduce

```
pip install numpy scipy sympy z3-solver cvxpy matplotlib      # versions used are listed in out/results.json
python3 run_all.py            # lint, 63 routes, 11 claims, 16 negative controls; about 40 s
python3 figs/make_figs.py     # the three figures
python3 paper/make_numbers.py # numbers.tex and the tables of the paper
python3 page/make_page.py     # page/index.html
cd paper && pdflatex main && bibtex main && pdflatex main && pdflatex main
```

The long linear programmes are recorded in `out/` and only read by `run_all.py`. To rerun them
(several minutes each, two cores):

```
python3 checks/slow_spin1_lp.py R  900 out/lp_R.json  0 20 45 70 90 135 180 225 250 270 300 340
python3 checks/slow_spin1_lp.py R2 700 out/lp_R2.json 0 30 45 66.2 80 90 270 300 330
python3 checks/slow_two_qubit.py
python3 checks/slow_refine.py
```

The directions (degrees in the plane of the ratios) are those recorded in the two JSON files.

## Layout

```
lib/        spinlib.py (spin operators, multipoles, rotations), regions.py (closed forms of R and R2), simplex_lp.py
net/        encoding.py (35 nodes, 63 routes, 11 claims), certs_*.py (certificates), kernel.py (lint, closure), controls.py
checks/     exploratory checks t01..t08 and the long runs slow_*.py
out/        results.json, summary.txt, lp_R.json, lp_R2.json, lp_refine.json, two_qubit_sandwich.json, logs/
figs/       make_figs.py and the figures
paper/      main.tex and sections, refs.bib (make_bib.py from Crossref records), numbers and tables (make_numbers.py), main.pdf
page/       make_page.py, index.html (interactive three-layer view)
run_all.py  runs everything except the long linear programmes
SPEC.md     format of nodes, routes, grades and verdicts
```

## What is and is not verified

* `exact`: identity or equivalence checked in exact arithmetic (SymPy).
* `logic`: the negation is unsatisfiable (Z3).
* `numeric`: floating point with a stated tolerance, or a recorded run. The brute-force linear programmes agree
  with the closed forms of `R` and `R2` to about one per cent before refinement and to 0.2 per cent after; they are not proofs.
* `written`: a proof in the paper. Not mechanised, not independently reviewed.
* `import`: cited. Experimental inputs are quoted from the publications listed in `net/certs_numeric.py` (`INPUTS`).

Statements about data are conditional on the published fitted forms and on unfolding to the full phase space.
The released repositories `GEN_HEP`, `GEN_GPT_Level`, `GEN_QRT_Level` are read only; nothing here modifies them.

The derivations, code and text were produced in a dialogue between the author and an AI system (Claude, Anthropic).

## Provenance of this copy

The files were rebuilt on 20 November 2026 from the record of the session that wrote them (the files it wrote,
its here-documents, its file patches and its `sed` edits, replayed in order; one conditional edit that removes
`\usepackage{lmodern}` when that font package is missing was not replayed). Checks of the rebuild:

* the encoding agrees with the published page of 17 November in all 35 nodes, 63 route statements and 11 claims;
* `run_all.py` and the four long linear programmes were run again on 20 November 2026; the certificate outputs
  of all 63 routes agree with the outputs recorded on that page, the 11 verdicts are unchanged and 16 of 16
  negative controls are rejected;
* before the generated-work notice was added, `page/make_page.py` reproduced the published page except for the run time;
* `paper/numbers.tex` and the tables of the paper are regenerated by `paper/make_numbers.py`; apart from the run
  time they are fixed by the certificate outputs and the recorded runs, which agree with those of 17 November.

Changes against the sources of 17 November: the date line of `paper/main.tex` and the header of
`page/make_page.py` carry the generated-work notice above, and this README has the notice, this section and a
corrected sentence on the written proofs (DV12). Nothing else was changed. The paper was compiled
with REVTeX 4.2 (TeX Live package `revtex`).
