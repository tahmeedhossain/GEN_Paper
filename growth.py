"""
Growth quantities of a time-indexed concept graph.

The functions are a line-by-line port of gen_engine/evolution.py of the grand network
(repository GEN_Grand_Evoluton, Part II of the thesis), written against plain dictionaries so
that the same code path runs on the four dated branches (time = calendar year) and on a paper
replayed in reading order (time = reading step).

Definitions (thesis, Def. "arrival and closure" and Theorem "arrival-closure identity"):

    arrival route   : at least one endpoint u has t(u) = t(r)
    closure route   : every endpoint u has t(u) < t(r)
    d_arr(v)        : number of routes r containing v with t(r) = t(v)
    a(r)            : number of endpoints u of r with t(u) = t(r)
    latency(r)      : t(r) - max_u t(u)                (closure routes)
    identity        : E = sum_v d_arr(v) - sum_r (a(r) - 1)^+ + C

Endpoints of a route are its inputs and its target, counted with multiplicity as in the engine
(`ends = r.inputs + [r.target]`).
"""
from __future__ import annotations

import math
from collections import Counter, defaultdict
from typing import Any, Dict, List, Sequence, Tuple

# method phase of a route by universal kind: verbatim from gen_engine/evolution.py (PHASE_OF_KIND)
PHASE_OF_KIND = {
    "derives": "predict", "failed": "falsify",
    "enters": "restructure", "predicts": "predict", "calibrates": "calibrate", "frames": "hypothesize",
    "candidate": "hypothesize", "backedge": "restructure", "lineage": "reduce", "subset": "reduce",
    "implies": "predict", "necessary": "predict", "enables": "predict", "witness": "observe", "converts_to": "predict",
    "activates": "predict", "reversible": "predict", "hosts": "predict", "generates": "hypothesize",
    "equiv": "reduce", "specializes": "reduce", "contains": "reduce", "bounds": "predict",
    "pairs": "observe", "member_free": "restructure", "member_resource": "restructure", "satisfies": "restructure",
    "not_implies": "falsify", "forbids": "falsify", "hides": "falsify", "excludes": "falsify", "distinct": "falsify",
    "violates": "falsify", "irreversible": "falsify",
    "open": "deficit",
    "transport": "predict", "conversion": "predict",
}
PHASES = ("observe", "deficit", "hypothesize", "restructure", "predict", "falsify", "calibrate", "reduce")
PHASE_OF_LAYER = {"O": "observe", "M": "hypothesize", "S": "restructure"}


def ends_of(r: Dict[str, Any]) -> List[str]:
    return list(r["inputs"]) + [r["target"]]


def growth_decomposition(node_t: Dict[str, int], routes: Sequence[Dict[str, Any]]) -> Dict[str, Any]:
    """routes: dicts with keys id, inputs, target, t.  node_t: node id -> t."""
    times = sorted(set(node_t.values()) | {r["t"] for r in routes})
    arrival_degree = {u: 0 for u in node_t}
    closures, rows = [], []
    for y in times:
        arr = [u for u, t in node_t.items() if t == y]
        edges = [r for r in routes if r["t"] == y]
        a_edges, c_edges = [], []
        for r in edges:
            ends = ends_of(r)
            if any(node_t[u] == y for u in ends):
                a_edges.append(r)
                for u in ends:
                    if node_t[u] == y:
                        arrival_degree[u] += 1
            else:
                c_edges.append(r)
                closures.append({"id": r["id"], "t": y, "latency": y - max(node_t[u] for u in ends)})
        rows.append({"t": y, "arrivals": len(arr), "arrival_routes": len(a_edges), "closure_routes": len(c_edges)})
    lat = [c["latency"] for c in closures]
    E = len(routes)
    s_arr = sum(arrival_degree.values())
    excess = 0
    for r in routes:
        a = sum(1 for u in ends_of(r) if node_t[u] == r["t"])
        if a >= 1:
            excess += a - 1
    C = len(closures)
    return {
        "rows": rows, "closures": closures, "E": E, "V": len(node_t),
        "sum_arrival_degree": s_arr, "excess": excess, "n_closures": C,
        "identity_rhs": s_arr - excess + C, "identity_holds": s_arr - excess + C == E,
        "closure_fraction": (C / E) if E else None,
        "latency_mean": (sum(lat) / len(lat)) if lat else None,
        "latency_median": (sorted(lat)[len(lat) // 2] if lat else None),     # the engine's (upper) median
        "latency_max": max(lat) if lat else None,
        "mean_degree_at_arrival": s_arr / len(node_t) if node_t else None,
        "degree_at_arrival": dict(sorted(Counter(arrival_degree.values()).items())),
        "arrival_degree": arrival_degree,
    }


def cumulative_curve(node_t: Dict[str, int], routes: Sequence[Dict[str, Any]]) -> List[Dict[str, int]]:
    times = sorted(set(node_t.values()) | {r["t"] for r in routes})
    return [{"t": T, "V": sum(1 for t in node_t.values() if t <= T), "E": sum(1 for r in routes if r["t"] <= T)} for T in times]


def densification(curve: Sequence[Dict[str, int]], vmin: int = 10) -> Dict[str, Any]:
    """Least-squares fit log E = alpha log V + c over the filtration points with V >= vmin and E >= 1."""
    pts = [(r["V"], r["E"]) for r in curve if r["V"] >= vmin and r["E"] >= 1]
    if len(pts) < 3:
        return {"alpha": None, "r2": None, "n": len(pts)}
    xs = [math.log(v) for v, _ in pts]
    ys = [math.log(e) for _, e in pts]
    mx, my = sum(xs) / len(xs), sum(ys) / len(ys)
    sxx = sum((x - mx) ** 2 for x in xs)
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    if not sxx:
        return {"alpha": None, "r2": None, "n": len(pts)}
    a = sxy / sxx
    b = my - a * mx
    ss_res = sum((y - (a * x + b)) ** 2 for x, y in zip(xs, ys))
    ss_tot = sum((y - my) ** 2 for y in ys)
    return {"alpha": a, "r2": (1 - ss_res / ss_tot) if ss_tot else None, "n": len(pts)}


def preferential_closure(node_t: Dict[str, int], routes: Sequence[Dict[str, Any]]) -> Dict[str, Any]:
    """Mean degree of the endpoints of closure routes over the mean degree of all nodes present,
    both evaluated before the routes of the same time point are added; ratio of the two sums."""
    times = sorted(set(node_t.values()) | {r["t"] for r in routes})
    deg: Dict[str, int] = defaultdict(int)
    present = set()
    n = 0
    s_end = s_all = 0.0
    for y in times:
        present |= {u for u, t in node_t.items() if t == y}
        edges = [r for r in routes if r["t"] == y]
        for r in edges:
            ends = ends_of(r)
            if all(node_t[u] < y for u in ends) and present:
                s_all += sum(deg[u] for u in present) / len(present)
                s_end += sum(deg[u] for u in ends) / len(ends)
                n += 1
        for r in edges:
            for u in ends_of(r):
                deg[u] += 1
    return {"n": n, "ratio": (s_end / s_all) if s_all else None}


def forward_links(node_t: Dict[str, int], routes: Sequence[Dict[str, Any]]) -> List[Tuple[str, str]]:
    """Filtration test (thesis, Def. Filtration): a route must not precede an input or its target."""
    return [(r["id"], u) for r in routes for u in ends_of(r) if node_t[u] > r["t"]]


def signature(layer: Dict[str, str], routes: Sequence[Dict[str, Any]]) -> Dict[str, Dict[str, int]]:
    """Layer-pair signature: leg-route incidences from layer a into layer b."""
    S = {a: {b: 0 for b in "SMO"} for a in "SMO"}
    for r in routes:
        for u in r["inputs"]:
            S[layer[u]][layer[r["target"]]] += 1
    return S


def kendall_tau_b(x: Sequence[float], y: Sequence[float]) -> Dict[str, Any]:
    """Kendall tau-b with ties, O(n^2); returns the pair counts as well."""
    n = len(x)
    conc = disc = tx = ty = txy = 0
    for i in range(n):
        for j in range(i + 1, n):
            dx = (x[i] > x[j]) - (x[i] < x[j])
            dy = (y[i] > y[j]) - (y[i] < y[j])
            if dx == 0 and dy == 0:
                txy += 1
            elif dx == 0:
                tx += 1
            elif dy == 0:
                ty += 1
            elif dx == dy:
                conc += 1
            else:
                disc += 1
    den = math.sqrt((conc + disc + tx) * (conc + disc + ty))
    return {"tau_b": ((conc - disc) / den) if den else None, "concordant": conc, "discordant": disc,
            "ties_x_only": tx, "ties_y_only": ty, "ties_both": txy, "n": n}


def summarise(node_t: Dict[str, int], routes: Sequence[Dict[str, Any]], vmin: int = 10) -> Dict[str, Any]:
    g = growth_decomposition(node_t, routes)
    d = densification(cumulative_curve(node_t, routes), vmin)
    p = preferential_closure(node_t, routes)
    return {
        "V": g["V"], "E": g["E"], "sum_arrival_degree": g["sum_arrival_degree"], "excess": g["excess"],
        "closures": g["n_closures"], "identity_holds": g["identity_holds"],
        "closure_fraction": g["closure_fraction"], "latency_mean": g["latency_mean"],
        "latency_median": g["latency_median"], "latency_max": g["latency_max"],
        "mean_degree_at_arrival": g["mean_degree_at_arrival"],
        "arrival_degree_zero": g["degree_at_arrival"].get(0, 0),
        "alpha": d["alpha"], "alpha_r2": d["r2"], "alpha_n": d["n"],
        "pa_ratio": p["ratio"], "pa_n": p["n"],
        "forward_links": len(forward_links(node_t, routes)),
        "time_points": len(set(node_t.values()) | {r["t"] for r in routes}),
    }
