# GEN_Paper: papers checked as concept-graph deltas, and replayed in reading order

Four papers are written as changes to the released GEN concept graphs (nodes in a state, model and observable
layer; routes that each carry one statement) and checked route by route by a small program, the edge kernel
(`SPEC.md`). Each paper is then replayed in reading order and its growth is tested against the update rules of
the grand network (`REPLAY.md`).

Three of the papers are published. The fourth is a **generated work**: a paper written, together with its
encoding and its certificates, by an AI system (Claude, Anthropic) in a session directed by T. Hossain on
17 November 2026. It is unpublished and has not been peer reviewed. Its sources, code, recorded runs and PDF are
in `decay_contextuality/`.

The checks, encodings, replays and pages of this repository were also built with an AI system (Claude); nothing
here is peer reviewed.

## Papers

| Key | Paper | Status | Network |
|---|---|---|---|
| `battery` | Ganardi, Kondra, Ng, Streltsov, *Second Law of Entanglement Manipulation with an Entanglement Battery*, Phys. Rev. Lett. 135, 010202 (2025), arXiv:2405.10599 | published | GEN_QRT_Level v1.2 |
| `realqm` | Barrios Hita, Trushechkin, Kampermann, Epping, Bruß, *Quantum Mechanics Based on Real Numbers: A Consistent Description*, Phys. Rev. Lett. 136, 240202 (2026), arXiv:2503.17307 | published | GEN_GPT_Level v2.6 |
| `top` | ATLAS Collaboration, *Observation of quantum entanglement with top quarks at the ATLAS detector*, Nature 633, 542 (2024), arXiv:2311.07288 | published | GEN_HEP v1.2, glued to GEN_GPT_Level and GEN_QRT_Level |
| `decay` | T. Hossain with Claude (Anthropic), *Particle decays as fixed measurements: exact noncontextuality thresholds for decay-angle correlations*, 17 November 2026 | **generated work**, unpublished, not peer reviewed (`decay_contextuality/`) | GEN_HEP v1.2 and GEN_GPT_Level v2.6, glued to GEN_QRT_Level v1.2 |

## Run

```
pip install sympy z3-solver numpy scipy cvxpy matplotlib
python3 run_all.py            # edge kernel on the four papers, about 70 s; exit code 0: no failed route, all controls rejected
python3 build_page.py         # page/results.json and the standalone explorer page
python3 run_replay.py [path to data/gen_evolution_network.json of GEN_Grand_Evoluton]   # replay; the path enables the growth validation
python3 build_replay_page.py  # page_replay/replay.json and the standalone replay page
```

The generated paper has its own pipeline (certificates, long linear programmes, figures, paper):
see `decay_contextuality/README.md`. The edge kernel reads its encoding from `decay_contextuality/net/` and the
recorded long runs from `decay_contextuality/out/`.

Tested with Python 3.13, SymPy 1.14.0, Z3 5.4.1, NumPy 2.5.3, SciPy 1.18.1, CVXPY 1.9.3.

## Pages

The repository is served by GitHub Pages at <https://tahmeedhossain.github.io/GEN_Paper/>, with this file as its front page.

| Page | Content |
|---|---|
| [Edge-kernel explorer](https://tahmeedhossain.github.io/GEN_Paper/page/) | method, one view per paper (claims, layered graph, routes with certificate output, findings, delta, lint), negative controls. File `page/index.html`, which loads `page/results.json`; `page/gen_edge_kernel_standalone.html` opens from disk |
| [Replay in reading order](https://tahmeedhossain.github.io/GEN_Paper/page_replay/) | the update rule tested on the four papers, one view per paper with a unit-by-unit navigator, method. File `page_replay/index.html`, which loads `page_replay/replay.json`; `page_replay/gen_paper_replay_standalone.html` opens from disk |
| [Generated paper, PDF](https://tahmeedhossain.github.io/GEN_Paper/decay_contextuality/paper/main.pdf) | *Particle decays as fixed measurements* (generated work, unpublished, not peer reviewed) |
| [Page of the generated paper](https://tahmeedhossain.github.io/GEN_Paper/decay_contextuality/page/) | the page as published on 17 November 2026, with a generated-work notice; [folder README](https://tahmeedhossain.github.io/GEN_Paper/decay_contextuality/) |
| [SPEC](SPEC.md), [REPLAY](REPLAY.md) | method of the edge kernel and of the replay |
| [Check report](out/report.md), [replay report](out/replay_report.md) | the results as tables |

## Files

| File | Content |
|---|---|
| `SPEC.md` | the method: objects, kernel functions, grades, verdict rule 1.1, encoding steps, trusted base |
| `kernel.py` | lint, certificate runner, closure, SMT helper, scope-separation rule |
| `exact.py` | exact arithmetic in Q(√2, i) and small tensor helpers |
| `paper_battery.py`, `paper_realqm.py`, `paper_top.py` | the three published papers: nodes, routes, certificates, claims, delta, findings |
| `paper_decay.py` | the generated paper: imports its encoding from `decay_contextuality/net/` and adds dependencies, locations in the compiled text, delta and findings |
| `controls.py` | 12 planted errors for the published papers, and the 16 controls of the generated paper |
| `run_all.py` | runs the kernel and writes `out/` |
| `out/results.json`, `out/report.md`, `out/delta_*.json` | results (schema `gen-check/1`), tables, proposed operations on the released networks (schema `gen-check-delta/1`; not applied to any repository) |
| `REPLAY.md` | the replay: objects, two propositions, lookups, tests, results, corrections, limits |
| `orders.py` | reading order of the four papers: units, first naming of each node, statement and support of each route |
| `growth.py`, `validate_growth.py` | arrival and closure, counting identity, densification, preferential closure, Kendall τ_b (port of `gen_engine/evolution.py`), and its validation on the four dated branches |
| `replay.py`, `replay_controls.py`, `run_replay.py` | the replay, its controls (8 planted defects, 2 property tests), the runner; writes `out/replay.json` (schema `gen-replay/1`) and `out/replay_report.md` |
| `decay_contextuality/` | the generated paper: `paper/` (LaTeX sources, `refs.bib`, figures, `main.pdf`), `net/` (encoding, certificates, kernel, controls), `lib/`, `checks/`, `figs/`, `out/` (results and recorded runs), `page/` |

## Results of the run of 2026-11-20

Edge kernel, four papers: 133 routes, 89 checked by certificate (54 exact, 21 logic, 13 numeric, 1 import with
a consistency check), 18 imported, 8 definitions, 17 written proof steps, 1 interpretive, 0 failed. 27 headline
claims: 6 verified, 2 verified on instances, 8 verified modulo imports, 2 verified modulo written proof steps,
8 verified modulo imports and written proof steps, 1 not decidable by the kernel. 28 of 28 planted errors
rejected.

- Published papers: 70 routes, 51 checked (33 exact, 18 logic), 12 imported, 4 definitions, 2 written proof
  steps, 1 interpretive; 16 claims.
- Generated paper: 63 routes, 38 checked (21 exact, 3 logic, 13 numeric, 1 import with a consistency check),
  6 imported, 4 definitions, 15 written proof steps; 11 claims. Closed over the dependencies of its proofs, two
  verdicts printed in the paper are too strong (C8 and C10; finding "Verdicts printed in the paper").

Replay: the four reading orders are valid; 10 of 10 replay controls detected; the growth code reproduces the
published values of the four dated branches (data of GEN_Grand_Evoluton, commit 6638f22 of 2026-11-18).
Results per paper are in `REPLAY.md`, section 5.

## Changes against the bundles of 17 and 19 November 2026

- Fourth paper: the generated work in `decay_contextuality/`, encoded in the edge kernel and replayed.
- Verdict rule 1.1 (`SPEC.md`, section 4). Two labels of the published papers change, with the same lists of
  imports and unmechanised steps: A-C5 (battery) and B-C1 (real-number QM).
- On 2026-11-19 the location fields (`where`) of 24 routes and 4 claims of the published papers were corrected
  against the arXiv texts (`REPLAY.md`, section 6). No statement, grade or certificate changed.

## What was read

The statements of the published papers were taken from the arXiv texts through an automatic reader, not from
the journal PDFs: arXiv:2405.10599v2 (HTML), arXiv:2503.17307 (PDF and the HTML rendering of v2),
arXiv:2311.07288 (PDF), arXiv:2101.10873v2 (PDF), arXiv:2504.02808v2 (HTML), and the pages listed in each
encoding's `sources`. References marked `[from knowledge]` in the encodings were not looked up again. The
reading order of the generated paper was taken from its LaTeX source. Confirm any finding about a published
paper against its published version before quoting it.
