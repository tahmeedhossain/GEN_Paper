"""
Run the kernel on the four encoded papers (three published, one generated work) and on the negative controls.

    python3 run_all.py

writes  out/results.json      everything the page shows (nodes, edges, certificate output, verdicts)
        out/report.md         the same as readable tables
        out/delta_<key>.json  proposed changes to the released networks, one file per paper
"""
import datetime
import json
import os
import platform
import sys
import time

import sympy
import z3

import controls
import kernel
import paper_battery
import paper_realqm
import paper_top
import paper_decay

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")


def md_escape(s):
    return str(s).replace("|", "\\|").replace("\n", " ")


def write_report(res, path):
    L = []
    L.append("# GEN edge kernel: check report\n")
    L.append(f"Run {res['meta']['run_utc']} · Python {res['meta']['python']} · sympy {res['meta']['sympy']} · "
             f"z3 {res['meta']['z3']} · {res['meta']['seconds']} s\n")
    t = res["totals"]
    L.append(f"Edges: {t['edges']} ({t['checked']} checked by certificate or kernel rule, {t['imported']} imported, "
             f"{t['definition']} definitions, {t['composed']} written proof steps (grade compose), {t['interpretive']} interpretive, "
             f"{t['failed']} failed). Negative controls: {t['controls_detected']}/{t['controls']} planted errors detected.\n")
    for p in res["papers"]:
        L.append(f"\n## {p['citation']}\n")
        L.append(f"{p['branch']}. " + "; ".join(f"{k}: {v}" for k, v in p['ids'].items()) + ".\n")
        L.append("Phases of the method cycle (read by hand): " + "; ".join(f"{a} ({b})" for a, b in p["phases"]) + ".\n")
        L.append("\n### Claims\n")
        L.append("| Claim | Statement | Verdict | Imports | Instance-scoped | Written proof steps |")
        L.append("|---|---|---|---|---|---|")
        for c in p["claims"]:
            L.append(f"| {c['id']} | {md_escape(c['text'])} | {c['verdict']} | {', '.join(c['imports']) or '–'} | "
                     f"{', '.join(c['instance_scoped']) or '–'} | {', '.join(c['unmechanised_steps']) or '–'} |")
        L.append("\n### Edges\n")
        L.append("| Edge | Route | Kind | Grade | Status | Scope | Statement | Result |")
        L.append("|---|---|---|---|---|---|---|---|")
        for e in p["edges"]:
            route = " ∧ ".join(e["inputs"]) + " → " + e["target"]
            L.append(f"| {e['id']} | {md_escape(route)} | {e['kind']} | {e['grade']} | {e['status']} | "
                     f"{md_escape(e['scope'])} | {md_escape(e['statement'])} | {md_escape(e['summary'])} |")
        L.append("\n### Findings\n")
        for f in p["findings"]:
            L.append(f"- **{f['title']}** ({f['level']}). {f['text']}")
        L.append("\n### Proposed network operations\n")
        for d in p["delta"]:
            body = "; ".join(f"{k}: {v}" for k, v in d.items() if k != "op")
            L.append(f"- `{d['op']}` {body}")
        lint = p["lint"]
        L.append("\n### Graph lint\n")
        L.append(f"- nodes {lint['counts']['nodes']} (existing {lint['counts']['nodes_existing']}, new or split "
                 f"{lint['counts']['nodes_new']}); S/M/O = {lint['counts']['S']}/{lint['counts']['M']}/{lint['counts']['O']}; "
                 f"edges {lint['counts']['edges']}, of which AND routes {lint['and_routes']}")
        L.append(f"- route types: {', '.join(f'{k} ×{v}' for k, v in sorted(lint['route_types'].items(), key=lambda kv: -kv[1]))}")
        L.append(f"- observables with no direct route from the model layer: {', '.join(lint['observables_without_model_route']) or 'none'}")
        L.append(f"- effects without a witness: {', '.join(lint['effects_without_witness']) or 'none'}")
        L.append(f"- problems: {'; '.join(lint['problems']) or 'none'}")
    L.append("\n## Negative controls\n")
    L.append("| Control | Planted error | Detected | Detail |")
    L.append("|---|---|---|---|")
    for c in res["controls"]:
        L.append(f"| {md_escape(c['control'])} | {md_escape(c['planted_error'])} | {'yes' if c['detected'] else 'NO'} | {md_escape(c['detail'])} |")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")


def write_delta(p, path):
    new_nodes = [n for n in p["nodes"] if n["status"] != "existing"]
    kept = [n for n in p["nodes"] if n["status"] == "existing"]
    obj = {
        "schema": "gen-check-delta/1",
        "paper": {"citation": p["citation"], "year": p["year"], **p["ids"]},
        "phases": p["phases"],
        "base": p["branch"],
        "glued_existing_nodes": [{"id": n["id"], "glue": n["glue"]} for n in kept],
        "nodes": [{"id": n["id"], "layer": n["layer"], "sub": n["sub"], "label": n["title"], "def": n["definition"],
                   "status": n["status"], "glue": n["glue"], "refs": n["refs"]} for n in new_nodes],
        "edges": [{"id": e["id"], "inputs": e["inputs"], "target": e["target"], "kind": e["kind"],
                   "statement": e["statement"], "where": e["where"], "grade": e["grade"], "status": e["status"],
                   "scope": e["scope"], "check": e["summary"], "uses": e["uses"], "refs": e["refs"], "note": e["note"]}
                  for e in p["edges"]],
        "operations": p["delta"],
    }
    kernel.dump(obj, path)


def main():
    os.makedirs(OUT, exist_ok=True)
    t0 = time.time()
    papers = []
    for mod in (paper_battery, paper_realqm, paper_top, paper_decay):
        paper = mod.build()
        print(f"\n== {paper.citation}")
        papers.append(kernel.run_paper(paper))
    print("\n== negative controls")
    ctr = controls.run()
    for r in ctr:
        print(("  detected " if r["detected"] else "  MISSED   ") + r["control"])
    edges = [e for p in papers for e in p["edges"]]
    totals = {
        "papers": len(papers),
        "nodes": sum(len(p["nodes"]) for p in papers),
        "edges": len(edges),
        "checked": sum(e["status"] == "checked" for e in edges),
        "imported": sum(e["status"] == "imported" for e in edges),
        "definition": sum(e["status"] == "definition" for e in edges),
        "composed": sum(e["status"] == "composed" for e in edges),
        "interpretive": sum(e["status"] == "not decidable" for e in edges),
        "failed": sum(e["status"] == "FAILED" for e in edges),
        "by_grade": {g: sum(e["grade"] == g for e in edges) for g in kernel.GRADES},
        "claims": sum(len(p["claims"]) for p in papers),
        "claims_by_verdict": {},
        "controls": len(ctr),
        "controls_detected": sum(r["detected"] for r in ctr),
    }
    for p in papers:
        for c in p["claims"]:
            totals["claims_by_verdict"][c["verdict"]] = totals["claims_by_verdict"].get(c["verdict"], 0) + 1
    res = {
        "meta": {"run_utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
                 "python": platform.python_version(), "sympy": sympy.__version__, "z3": z3.get_version_string(),
                 "seconds": round(time.time() - t0, 1), "schema": "gen-check/1"},
        "totals": totals, "papers": papers, "controls": ctr,
    }
    kernel.dump(res, os.path.join(OUT, "results.json"))
    write_report(res, os.path.join(OUT, "report.md"))
    for p in papers:
        write_delta(p, os.path.join(OUT, f"delta_{p['key']}.json"))
    print("\n== totals")
    print(json.dumps(totals, ensure_ascii=False, indent=1))
    failed = totals["failed"] or totals["controls_detected"] != totals["controls"]
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
