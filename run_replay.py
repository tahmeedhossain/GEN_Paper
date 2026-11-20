"""
Run the replay of the four encoded papers (three published, one generated work), the controls and (when the data file of the grand network is
given) the validation of the growth code; write out/replay.json and out/replay_report.md.

usage: python3 run_replay.py [path to gen_evolution_network.json of the repository GEN_Grand_Evoluton]
"""
import json
import os
import sys
import time

import replay_controls
from growth import PHASES
from replay import BLOCKS, load_papers, run_all

HERE = os.path.dirname(os.path.abspath(__file__))

# Growth table of the four dated branches (thesis of the grand network, Part II, tables "arrival-closure identity"
# and "growth summary"; recomputed by validate_growth.py from data/gen_evolution_network.json, commit of 2026-11-18).
BRANCHES = {
    "EM":  {"type": "D", "V": 120, "E": 122, "sum_arrival_degree": 174, "excess": 60, "closures": 8,  "closure_pct": 7,  "mean_degree_at_arrival": 1.45, "alpha": 1.40, "alpha_r2": 0.98, "pa_ratio": 1.16, "pa_n": 8,  "and_routes": 118,
            "phases": {"observe": 43, "deficit": 0, "hypothesize": 52, "restructure": 25, "predict": 116, "falsify": 6, "calibrate": 0, "reduce": 0}},
    "HEP": {"type": "H", "V": 78,  "E": 214, "sum_arrival_degree": 234, "excess": 24, "closures": 4,  "closure_pct": 2,  "mean_degree_at_arrival": 3.00, "alpha": 1.62, "alpha_r2": 0.87, "pa_ratio": 3.56, "pa_n": 4,  "and_routes": 28,
            "phases": {"observe": 34, "deficit": 0, "hypothesize": 31, "restructure": 146, "predict": 44, "falsify": 0, "calibrate": 12, "reduce": 25}},
    "GPT": {"type": "E", "V": 92,  "E": 156, "sum_arrival_degree": 110, "excess": 23, "closures": 69, "closure_pct": 44, "mean_degree_at_arrival": 1.20, "alpha": 1.47, "alpha_r2": 0.99, "pa_ratio": 2.86, "pa_n": 69, "and_routes": 0,
            "phases": {"observe": 62, "deficit": 10, "hypothesize": 49, "restructure": 14, "predict": 53, "falsify": 45, "calibrate": 0, "reduce": 15}},
    "QRT": {"type": "E", "V": 116, "E": 86,  "sum_arrival_degree": 87,  "excess": 20, "closures": 19, "closure_pct": 22, "mean_degree_at_arrival": 0.75, "alpha": 1.30, "alpha_r2": 1.00, "pa_ratio": 1.71, "pa_n": 19, "and_routes": 0,
            "phases": {"observe": 42, "deficit": 0, "hypothesize": 52, "restructure": 49, "predict": 26, "falsify": 13, "calibrate": 0, "reduce": 20}},
}
BRANCH_OF_PAPER = {"battery": "QRT", "realqm": "GPT", "top": "HEP", "decay": "GPT+HEP"}   # decay: nodes of GEN_HEP and GEN_GPT_Level

# rule of the grand network that each operation of the net update (out/delta_<paper>.json, 2026-11-17) is an instance of
DELTA_RULE = {
    "ADD": "node or route added (R2 when a model node answers a deficit; R14 when a route closes a cell)",
    "ROUTE": "R4", "EXTEND": "R4", "SCOPE": "R21", "SPLIT": "R21", "RETARGET": "R21", "CITE": "R14 (literature fill)",
    "OPEN": "R13", "GLUE": "glue (shared concept); R6/R16 when two model nodes are identified", "REWRITE": "REWRITE",
    "PREDICT": "R2 route", "CALIBRATE": "R9", "FLAG": "R2 guard", "FIBRE": "contraction lemma",
}


def fmt(x, n=2):
    if x is None:
        return "–"
    if isinstance(x, float):
        return f"{x:.{n}f}"
    return str(x)


def report(out, controls, validation):
    L = []
    A = L.append
    A("# Replay of four encoded papers in reading order (three published papers and one generated work)\n")
    A(f"Generated {time.strftime('%Y-%m-%d %H:%M UTC', time.gmtime())} by run_replay.py. Encoding: out/results.json of the edge kernel. "
      "Reading order: orders.py.\n")
    A("## 1. Summary of the order tests\n")
    A("| paper | units | nodes (carried in) | routes | stated before supported | median deferral (units) | routes supported on a route supported later | node forward links, support time | node forward links, statement time | not supported in the paper |")
    A("|---|---|---|---|---|---|---|---|---|---|")
    for k, r in out.items():
        ot, cv = r["order_tests"], r["coverage"]
        A(f"| {k} | {cv['units']} | {cv['nodes']} ({cv['nodes_carried']}) | {cv['routes']} | {len(ot['deferred'])} | {fmt(ot['deferred_latency']['median'])} | "
          f"{len(ot['conditional'])} ({len(ot['dependency_forward'])} of {ot['dependency_pairs']} dependency pairs) | {len(ot['forward_links_nodes_supported'])} | "
          f"{len(ot['forward_links_nodes_stated'])} | {len(ot['unsupported_in_paper'])} |")
    A("\n## 2. Growth quantities under three time conventions, with the branch values\n")
    A("| graph | time index | V | E | Σ d_arr − Σ(a−1)⁺ + C | closures | mean d_arr | α (R², points) | PA ratio (n) |")
    A("|---|---|---|---|---|---|---|---|---|")
    for b, v in BRANCHES.items():
        A(f"| branch {b} (type {v['type']}) | calendar year | {v['V']} | {v['E']} | {v['sum_arrival_degree']} − {v['excess']} + {v['closures']} | {v['closure_pct']}% | "
          f"{v['mean_degree_at_arrival']:.2f} | {v['alpha']:.2f} ({v['alpha_r2']:.2f}) | {v['pa_ratio']:.2f} ({v['pa_n']}) |")
    for k, r in out.items():
        for name in ("stated", "supported", "supported, nodes dated by first route"):
            s = r["growth"][name]
            A(f"| paper {k} | {name} | {s['V']} | {s['E']} | {s['sum_arrival_degree']} − {s['excess']} + {s['closures']} | {fmt(100 * s['closure_fraction'], 0)}% | "
              f"{fmt(s['mean_degree_at_arrival'])} | {fmt(s['alpha'])} ({fmt(s['alpha_r2'])}, {s['alpha_n']}) | {fmt(s['pa_ratio'])} ({s['pa_n']}) |")
    A("\nRobustness (abstract merged into the introduction): " + "; ".join(
        f"{k}: closures {fmt(100 * r['growth']['stated, abstract merged']['closure_fraction'], 0)}% stated, "
        f"{fmt(100 * r['growth']['supported, abstract merged']['closure_fraction'], 0)}% supported" for k, r in out.items()) + ".\n")
    A("## 3. Phases\n")
    A("| graph | " + " | ".join(PHASES) + " | τ_b(unit, rank in the loop) |")
    A("|---|" + "---|" * (len(PHASES) + 1))
    for b, v in BRANCHES.items():
        tot = sum(v["phases"].values())
        A(f"| branch {b} | " + " | ".join(f"{v['phases'][p]} ({100 * v['phases'][p] / tot:.0f}%)" for p in PHASES) + " | |")
    for k, r in out.items():
        pr = r["phases"]["profile"]
        tot = sum(pr.values())
        A(f"| paper {k} | " + " | ".join(f"{pr[p]} ({100 * pr[p] / tot:.0f}%)" for p in PHASES) + f" | {fmt(r['phases']['tau_unit_vs_loop_rank']['tau_b'])} |")
    A("\nTotal-variation distance between the phase profile of each paper and of each branch: " + "; ".join(
        f"{k}: " + ", ".join(f"{b} {d:.2f}" for b, d in r["phases"]["tv_to_branch"].items()) for k, r in out.items()) + ".\n")
    A("\n## 4. Operations and rules, by paper\n")
    rules = sorted({x for r in out.values() for x in r["counts"]["rules"]})
    A("| rule | " + " | ".join(out) + " |")
    A("|---|" + "---|" * len(out))
    for x in rules:
        A(f"| {x} | " + " | ".join(str(r["counts"]["rules"].get(x, 0)) for r in out.values()) + " |")
    ops = sorted({x for r in out.values() for x in r["counts"]["operations"]})
    A("\n| operation | " + " | ".join(out) + " |")
    A("|---|" + "---|" * len(out))
    for x in ops:
        A(f"| {x} | " + " | ".join(str(r["counts"]["operations"].get(x, 0)) for r in out.values()) + " |")
    for k, r in out.items():
        A(f"\n## Paper: {k}\n")
        A(f"{r['citation']}. Text: {r['text_version']}.\n")
        A("| # | unit | location | nodes | stated here, supported later | supported here: route [operation, rule, support] | V | stated | supported | open | conditional |")
        A("|---|---|---|---|---|---|---|---|---|---|---|")
        for u in r["units"]:
            nodes = ", ".join(f"{n['id']}{'°' if n['op'] == 'CARRY' else ('†' if n['op'] == 'SPLIT' else '')}" for n in u["nodes"]) or "–"
            est = "; ".join(f"{e['id']} [{e['op']}, {e['rule']}, {e['support']}{', cond.' if e['conditional_on'] else ''}]" for e in u["establish"]) or ("not encoded" if not u["encoded"] else "–")
            c = u["counts"]
            A(f"| {u['index']} | {u['label']} | {u['loc']} | {nodes} | {', '.join(u['announce']) or '–'} | {est} | {c['V']} | {c['stated']} | {c['supported']} | {c['debt']} | {c['conditional']} |")
        A("\n° carried in from the released network; † split off an existing node.\n")
        ot = r["order_tests"]
        A("Routes supported in a unit before a route they depend on: " + (", ".join(
            f"{a} (unit {c['stated_support']}, complete at unit {c['discharged']}; waits for {', '.join(c['direct']) or 'an indirect dependency'})" for a, c in ot["conditional"].items()) or "none") + ".\n")
        A("Not supported in the paper (stated with at most a verbal reason, or used without statement): " + (", ".join(ot["unsupported_in_paper"]) or "none") + ".\n")
        A("Added by the encoding and excluded from all counts: " + (", ".join(f"{x['id']} ({x['why']})" for x in r["added"]["routes"]) or "none") + ".\n")
        A("Guards: " + json.dumps(r["guards"], ensure_ascii=False) + "\n")
        for n in r["notes"]:
            A(f"- {n}")
    A("\n## Controls\n")
    for c in controls:
        A(f"- {'detected' if c['detected'] else 'MISSED'}: {c['control']}")
    if validation is not None:
        A("\n## Validation of the growth code on the four dated branches\n")
        for b, v in validation.items():
            A(f"- {b}: {'all published values reproduced' if v['ok'] else 'MISMATCH ' + str([k for k, x in v['checks'].items() if not x])}")
    return "\n".join(L) + "\n"


def main():
    papers = load_papers()
    out = run_all()
    for r in out.values():                 # total-variation distance between the phase profile of a paper and of each branch
        pr = r["phases"]["profile"]
        tp = sum(pr.values())
        r["phases"]["tv_to_branch"] = {
            b: round(0.5 * sum(abs(pr[p] / tp - v["phases"][p] / sum(v["phases"].values())) for p in PHASES), 3)
            for b, v in BRANCHES.items()}
    controls = replay_controls.run()
    validation = None
    if len(sys.argv) > 1:
        import validate_growth
        validation, _ = validate_growth.run(sys.argv[1], verbose=False)
    delta = {}
    for k, p in papers.items():
        delta[k] = [dict(op, rule=DELTA_RULE.get(op["op"], "–")) for op in p.get("delta", [])]
    doc = {
        "schema": "gen-replay/1",
        "generated_utc": time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime()),
        "phases": list(PHASES), "blocks": list(BLOCKS),
        "branches": BRANCHES, "branch_of_paper": BRANCH_OF_PAPER,
        "papers": out, "net_update": delta, "controls": controls,
        "validation": None if validation is None else {b: {"ok": v["ok"], "checks": v["checks"]} for b, v in validation.items()},
    }
    os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
    json.dump(doc, open(os.path.join(HERE, "out", "replay.json"), "w"), ensure_ascii=False, indent=1)
    open(os.path.join(HERE, "out", "replay_report.md"), "w").write(report(out, controls, validation))
    ok = all(c["detected"] for c in controls) and (validation is None or all(v["ok"] for v in validation.values()))
    print(f"papers: {len(out)}; controls detected {sum(c['detected'] for c in controls)}/{len(controls)}; "
          f"branch validation: {'not run' if validation is None else ('ok' if all(v['ok'] for v in validation.values()) else 'MISMATCH')}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
