"""
Validation of growth.py: recompute the growth table of the grand network (thesis Part II,
tables "arrival-closure identity" and "growth summary") from data/gen_evolution_network.json and
compare with the published values.  The data file is read only; none of the repository's code is run.

usage: python3 -I validate_growth.py <path to gen_evolution_network.json>
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from growth import PHASE_OF_KIND, PHASE_OF_LAYER, PHASES, summarise  # noqa: E402

# published values: thesis/tables/tab_evo_identity.tex and tab_evo_summary.tex (commit of 2026-11-18)
PUBLISHED = {
    "EM":  dict(V=120, E=122, sum_arrival_degree=174, excess=60, closures=8,  frac=7,  lat=(23.8, 17, 77), darr=1.45, alpha=1.40, r2=0.98, pa=1.16, pa_n=8),
    "HEP": dict(V=78,  E=214, sum_arrival_degree=234, excess=24, closures=4,  frac=2,  lat=(1.0, 1, 1),    darr=3.00, alpha=1.62, r2=0.87, pa=3.56, pa_n=4),
    "GPT": dict(V=92,  E=156, sum_arrival_degree=110, excess=23, closures=69, frac=44, lat=(15.7, 14, 41), darr=1.20, alpha=1.47, r2=0.99, pa=2.86, pa_n=69),
    "QRT": dict(V=116, E=86,  sum_arrival_degree=87,  excess=20, closures=19, frac=22, lat=(4.1, 4, 12),   darr=0.75, alpha=1.30, r2=1.00, pa=1.71, pa_n=19),
}


def load(path):
    d = json.load(open(path))
    out = {}
    for b in ("EM", "HEP", "GPT", "QRT"):
        nodes = [n for n in d["nodes"] if n["branch"] == b]
        routes = [r for r in d["routes"] if r["branch"] == b]
        out[b] = {
            "node_t": {n["uid"]: n["year"] for n in nodes},
            "layer": {n["uid"]: n["layer"] for n in nodes},
            "routes": [{"id": r["uid"], "inputs": r["inputs"], "target": r["target"], "t": r["year"],
                        "kind": r["kind"], "status": r["status"], "phase": r["phase"], "rule": r.get("rule")} for r in routes],
        }
    return out


def phase_profile(branch):
    c = {p: 0 for p in PHASES}
    for u, L in branch["layer"].items():
        c[PHASE_OF_LAYER[L]] += 1
    for r in branch["routes"]:
        c[r["phase"]] += 1
    return c


def run(path, verbose=True):
    br = load(path)
    report, ok_all = {}, True
    for b, pub in PUBLISHED.items():
        s = summarise(br[b]["node_t"], br[b]["routes"])
        checks = {
            "V": s["V"] == pub["V"], "E": s["E"] == pub["E"],
            "sum d_arr": s["sum_arrival_degree"] == pub["sum_arrival_degree"],
            "excess": s["excess"] == pub["excess"], "closures": s["closures"] == pub["closures"],
            "identity": s["identity_holds"],
            "closure %": round(100 * s["closure_fraction"]) == pub["frac"],
            "latency mean": round(s["latency_mean"], 1) == pub["lat"][0],
            "latency median": s["latency_median"] == pub["lat"][1],
            "latency max": s["latency_max"] == pub["lat"][2],
            "mean d_arr": round(s["mean_degree_at_arrival"], 2) == pub["darr"],
            "alpha": round(s["alpha"], 2) == pub["alpha"], "R2": round(s["alpha_r2"], 2) == pub["r2"],
            "PA ratio": round(s["pa_ratio"], 2) == pub["pa"], "PA n": s["pa_n"] == pub["pa_n"],
            "forward links": s["forward_links"] == 0,
        }
        # the phase stored on each route must equal the lookup table applied to its kind and status
        mism = [r["id"] for r in br[b]["routes"]
                if r["phase"] != ("deficit" if (r["status"] == "open" or r["kind"] == "open") else PHASE_OF_KIND.get(r["kind"], "predict"))]
        checks["phase lookup"] = not mism
        ok = all(checks.values())
        ok_all &= ok
        report[b] = {"summary": s, "checks": checks, "ok": ok, "phase_profile": phase_profile(br[b]),
                     "rules": {}, "and_routes": sum(1 for r in br[b]["routes"] if len(r["inputs"]) > 1)}
        for r in br[b]["routes"]:
            report[b]["rules"][r["rule"]] = report[b]["rules"].get(r["rule"], 0) + 1
        if verbose:
            print(f"{b}: V={s['V']} E={s['E']}  {s['sum_arrival_degree']} - {s['excess']} + {s['closures']} = {s['sum_arrival_degree'] - s['excess'] + s['closures']}"
                  f"  closure {100 * s['closure_fraction']:.1f}%  latency {s['latency_mean']:.1f}/{s['latency_median']}/{s['latency_max']}"
                  f"  d_arr {s['mean_degree_at_arrival']:.2f}  alpha {s['alpha']:.2f} (R2 {s['alpha_r2']:.2f}, n={s['alpha_n']})"
                  f"  PA {s['pa_ratio']:.2f} (n={s['pa_n']})  time points {s['time_points']}  -> {'OK' if ok else 'MISMATCH ' + str([k for k, v in checks.items() if not v])}")
    return report, ok_all


if __name__ == "__main__":
    rep, ok = run(sys.argv[1])
    for b in rep:
        print(b, "phases", rep[b]["phase_profile"], "AND routes", rep[b]["and_routes"])
        print("   rules", rep[b]["rules"])
    print("ALL PUBLISHED VALUES REPRODUCED" if ok else "MISMATCH")
    sys.exit(0 if ok else 1)
