"""
Replay of an encoded paper in reading order, and tests of its growth against the update rules of the
grand network (R1–R21, TE1–TE6, the arrival–closure identity, the method phases).

Input : out/results.json of the edge kernel (nodes, routes, grades, `uses`) and orders.py (reading order).
Output: for each paper a dictionary with the per-unit event log and every test below.

Time indices (reading units 0, 1, 2, ...):
    t_n(v)  unit in which node v first appears
    t_a(r)  unit in which route r is first stated          (equal to t_e(r) when it is supported where stated)
    t_e(r)  unit in which the paper supplies the support of r

Every attribution of an operation, a rule or a phase to an event is a lookup on the fields of the event
(kind, grade, layers and sub-layers of its ends, support, arrival or closure); the tables are below.
"""
from __future__ import annotations

import json
import os
from collections import Counter, defaultdict
from typing import Any, Dict, List, Tuple

from growth import (PHASE_OF_KIND, PHASE_OF_LAYER, PHASES, cumulative_curve, forward_links, growth_decomposition,
                    kendall_tau_b, signature, summarise)
from orders import ORDERS, SUPPORTS

HERE = os.path.dirname(os.path.abspath(__file__))
BLOCKS = ("abstract", "main", "methods", "supplement")

# kinds of the paper checks that are absent from the universal kind table: phase by this extension
PHASE_EXT = {"represents": "restructure", "composes": "restructure", "consistent": "restructure",
             "trivialises": "predict", "flags": "deficit"}
# kinds whose phase is read from the layer of the target, as for "defines": an imported statement enters as the kind
# of node it ends in (an observed value into an observable node, a model input into a model node)
PHASE_BY_TARGET_LAYER = {"defines", "import"}
NO_PHASE = {"claims", "scope"}                       # interpretive statements and scope remarks
NOGO_FAIL = {"forbids", "failed", "irreversible", "excludes", "flags"}
NOGO_ALL = NOGO_FAIL | {"violates", "distinct", "not_implies", "hides"}
SET_SUBS = {"free", "resource", "cluster", "dist"}
THEOREM_KINDS = {"necessary", "enables", "equiv", "implies", "bounds", "forbids", "distinct", "hosts", "predicts",
                 "trivialises", "violates", "satisfies"}


class OrderError(Exception):
    pass


# ----------------------------------------------------------------------------------------------------------------
# lookups
# ----------------------------------------------------------------------------------------------------------------
def phase_of_route(e: Dict[str, Any], layer: Dict[str, str]) -> Tuple[Any, str]:
    k = e["kind"]
    if k in PHASE_OF_KIND:
        return PHASE_OF_KIND[k], "table"
    if k in PHASE_BY_TARGET_LAYER:
        return PHASE_OF_LAYER[layer[e["target"]]], "extension"
    if k in PHASE_EXT:
        return PHASE_EXT[k], "extension"
    if k in NO_PHASE:
        return None, "none"
    return "predict", "default"


def closing_route(e: Dict[str, Any], support: str) -> str:
    """How the paper settles the route: the four routes of R14, plus what a paper adds to them."""
    if support == "citation":
        return "literature fill"
    if support in ("measurement", "simulation"):
        return support
    if support == "certificate":
        return "executed certificate"
    if support in ("asserted", "implicit"):
        return "none in the paper"
    if support == "definition":
        return "definition"
    if e["kind"] in NOGO_ALL and e["grade"] in ("exact", "witness"):
        return "counterexample"
    if e["grade"] == "compose":
        return "composition"
    return "proof"


def attribute_route(e: Dict[str, Any], layer: Dict[str, str], sub: Dict[str, str], closure: bool) -> Tuple[str, str]:
    """(operation, rule) of a supported route: a decision list on its kind, then on the layers of its ends.

    Kinds that name an operation of the grand network map to it directly.  Constructive kinds (defines, represents,
    predicts) are read by layer pattern, as in the table of primitive operations: M -> S is a back-edge, an AND route
    into a model node has the form of R4, a route with model and state legs into a state or an observable is the
    derivation of the readers (in a type-H graph it lifts to an R4 route followed by an R2 route), a route among
    observables is an aggregate.  Every other route is a relation between nodes: a closure (R14) when all its ends
    appeared in earlier units, a derivation arriving with a node (R11) otherwise.
    """
    k, ins, tgt = e["kind"], e["inputs"], e["target"]
    Lt, in_layers = layer[tgt], [layer[u] for u in ins]
    in_subs = [sub[u] for u in ins]
    if k == "calibrates":
        return "CALIBRATE", "R9"
    if k == "flags":
        return "FLAG", "R2 guard"
    if k == "witness":
        return "TEST", "R18 effect"
    if k == "consistent":
        return "REFINE", "R21"
    if k == "composes":
        return "COMPOSE", "R15"
    if k == "claims":
        return "CLAIM", "none"
    if k in ("satisfies", "violates") and (sub[tgt] == "axiom" or "axiom" in in_subs):
        return ("MEMBER" if k == "satisfies" else "EXCLUDE"), "R20"
    if k == "equiv" and sum(1 for x in in_subs if x == "model") >= 2:
        return "REDUCE", "R6/R16"
    if k == "equiv" and all(x == "witness" for x in in_subs) and Lt == "S" and sub[tgt] in SET_SUBS:
        return "TEST", "R17"
    if k in ("defines", "represents", "predicts"):
        if Lt == "M":
            return ("ROUTE", "R4 form") if (len(ins) >= 2 or in_layers == ["S"]) else ("DEFINE", "R11")
        if Lt == "S":
            if k == "defines" and "M" in in_layers and sub[tgt] in SET_SUBS:
                return "CLUSTER", "R17"
            if all(L == "M" for L in in_layers):
                return "BACK", "back-edge"
            return "DERIVE", "R11"
        if all(L == "O" for L in in_layers):
            return "AGGREGATE", "R18 aggregate"
        if all(L == "M" for L in in_layers):
            return "PREDICT", "R2 route"
        if "M" in in_layers and "S" in in_layers:
            return "DERIVE", "R11 (lifts to R4 + R2)"
        return "DEFINE", "R11"
    if closure:
        return "CLOSE", "R14"
    return "DERIVE", "R11"


def attribute_node(n: Dict[str, Any]) -> Tuple[str, str]:
    if n["status"] == "existing":
        return "CARRY", "carried in"
    if n["status"] == "split":
        return "SPLIT", "R21"
    return "ADD", "R11"


# ----------------------------------------------------------------------------------------------------------------
# the replay
# ----------------------------------------------------------------------------------------------------------------
def load_papers(path: str = None) -> Dict[str, Dict[str, Any]]:
    d = json.load(open(path or os.path.join(HERE, "out", "results.json")))
    return {p["key"]: p for p in d["papers"]}


def index_order(paper: Dict[str, Any], order: Dict[str, Any]) -> Dict[str, Any]:
    """Validate the order against the encoding and return the three time indices."""
    units = order["units"]
    nodes = {n["id"]: n for n in paper["nodes"]}
    edges = {e["id"]: e for e in paper["edges"]}
    added_r, added_n = set(order["added"]["routes"]), set(order["added"]["nodes"])
    t_n, t_a, t_e, support, restated = {}, {}, {}, {}, defaultdict(list)
    for i, u in enumerate(units):
        if u["block"] not in BLOCKS:
            raise OrderError(f"{u['id']}: unknown block {u['block']}")
        for v in u["nodes"]:
            if v not in nodes:
                raise OrderError(f"{u['id']}: unknown node {v}")
            if v in t_n:
                raise OrderError(f"node {v} placed twice")
            t_n[v] = i
        for r in u["announce"]:
            if r not in edges:
                raise OrderError(f"{u['id']}: unknown route {r}")
            if r in t_a:
                restated[r].append(i)
            else:
                t_a[r] = i
        for r, s in u["establish"].items():
            if r not in edges:
                raise OrderError(f"{u['id']}: unknown route {r}")
            if s not in SUPPORTS:
                raise OrderError(f"{u['id']}: unknown support {s}")
            if r in t_e:
                raise OrderError(f"route {r} established twice")
            t_e[r], support[r] = i, s
        for r in u["partial"]:
            if r not in edges:
                raise OrderError(f"{u['id']}: unknown route {r} in partial")
    for v in nodes:
        if v not in t_n and v not in added_n:
            raise OrderError(f"node {v} is not placed")
    for v in added_n:
        if v in t_n:
            raise OrderError(f"node {v} is both placed and listed as added")
    for r in edges:
        if r in added_r:
            if r in t_e or r in t_a:
                raise OrderError(f"route {r} is both placed and listed as added")
            continue
        if r not in t_e:
            raise OrderError(f"route {r} is not established in any unit")
        if r in t_a and t_a[r] >= t_e[r]:
            raise OrderError(f"route {r}: announced in unit {t_a[r]}, not before its support in unit {t_e[r]}")
        t_a.setdefault(r, t_e[r])
    # effective dependencies: a dependency on an added route is replaced by that route's own dependencies
    def eff(rid, seen=()):
        out = []
        for d in edges[rid]["uses"]:
            if d in seen:
                raise OrderError(f"cyclic `uses` through {d}")
            if d in added_r:
                out += eff(d, seen + (rid,))
            else:
                out.append(d)
        return sorted(set(out))
    uses = {r: eff(r) for r in edges if r not in added_r}
    # acyclicity of the dependency relation (Kahn)
    indeg = {r: len(us) for r, us in uses.items()}
    users = defaultdict(list)
    for r, us in uses.items():
        for d in us:
            users[d].append(r)
    queue, depth, done = [r for r, k in indeg.items() if k == 0], {}, 0
    for r in queue:
        depth[r] = 0
    while queue:
        r = queue.pop()
        done += 1
        for w in users[r]:
            depth[w] = max(depth.get(w, 0), depth[r] + 1)
            indeg[w] -= 1
            if indeg[w] == 0:
                queue.append(w)
    if done != len(uses):
        raise OrderError("the `uses` relation has a cycle")
    return {"t_n": t_n, "t_a": t_a, "t_e": t_e, "support": support, "restated": dict(restated), "uses": uses,
            "depth": depth, "added_routes": sorted(added_r), "added_nodes": sorted(added_n)}


def replay(paper: Dict[str, Any], order: Dict[str, Any]) -> Dict[str, Any]:
    ix = index_order(paper, order)
    t_n, t_a, t_e, support, uses = ix["t_n"], ix["t_a"], ix["t_e"], ix["support"], ix["uses"]
    units = order["units"]
    nodes = {n["id"]: n for n in paper["nodes"] if n["id"] in t_n}
    edges = {e["id"]: e for e in paper["edges"] if e["id"] in t_e}
    layer = {n["id"]: n["layer"] for n in paper["nodes"]}
    sub = {n["id"]: n["sub"] for n in paper["nodes"]}
    T = len(units)

    ends = lambda e: list(e["inputs"]) + [e["target"]]
    is_closure = {r: all(t_n[u] < t_e[r] for u in ends(e)) for r, e in edges.items()}

    # ---- dependency order against reading order -----------------------------------------------------------------
    dep_pairs = [(r, d) for r in edges for d in uses[r]]
    fwd = [(r, d) for r, d in dep_pairs if t_e[d] > t_e[r]]
    same = [(r, d) for r, d in dep_pairs if t_e[d] == t_e[r]]
    # a route is unconditional once every route it depends on, directly or not, is supported
    memo: Dict[str, int] = {}

    def discharged(r):
        if r not in memo:
            memo[r] = max([t_e[r]] + [discharged(d) for d in uses[r]])
        return memo[r]
    def all_deps(r, acc=None):
        acc = set() if acc is None else acc
        for d in uses[r]:
            if d not in acc:
                acc.add(d)
                all_deps(d, acc)
        return acc
    conditional = {r: {"stated_support": t_e[r], "discharged": discharged(r),
                       "on": sorted(d for d in all_deps(r) if t_e[d] > t_e[r]),
                       "direct": sorted(d for d in uses[r] if t_e[d] > t_e[r])}
                   for r in edges if discharged(r) > t_e[r]}

    has_in = {e["target"] for e in edges.values() if e["target"] not in e["inputs"]}   # observables with no route into them are primitive
    # ---- per-unit log ---------------------------------------------------------------------------------------------
    log = []
    cumV = cumA = cumE = 0
    debt = 0
    explained: Dict[str, int] = {}
    for i, u in enumerate(units):
        ev = {"id": u["id"], "index": i, "block": u["block"], "label": u["label"], "loc": u["loc"], "text": u["text"],
              "encoded": u["encoded"], "pointers": u["pointers"], "nodes": [], "announce": [], "restate": [], "establish": [],
              "partial": [{"route": r, "what": w} for r, w in u["partial"].items()], "added": []}
        for v in u["nodes"]:
            op, rule = attribute_node(nodes[v])
            ev["nodes"].append({"id": v, "layer": layer[v], "sub": sub[v], "status": nodes[v]["status"], "op": op, "rule": rule,
                                "phase": None if op == "CARRY" else PHASE_OF_LAYER[layer[v]]})
        for r in u["announce"]:
            (ev["announce"] if t_a[r] == i else ev["restate"]).append(r)
        for r, s in u["establish"].items():
            e = edges[r]
            op, rule = attribute_route(e, layer, sub, is_closure[r])
            ph, ph_src = phase_of_route(e, layer)
            ev["establish"].append({
                "id": r, "kind": e["kind"], "grade": e["grade"], "support": s, "op": op, "rule": rule, "phase": ph, "phase_source": ph_src,
                "closure": is_closure[r], "closing_route": closing_route(e, s), "announced_in": t_a[r] if t_a[r] < i else None,
                "conditional_on": conditional.get(r, {}).get("on", []), "discharged": memo[r], "uses": uses[r]})
        changed = True
        while changed:                       # an observable is explained by a supported route with a model leg,
            changed = False                  # or with an observable leg that is itself explained (family rule of the history)
            for r, e in edges.items():
                if t_e[r] > i or layer[e["target"]] != "O" or e["target"] in explained or e["kind"] in NOGO_ALL:
                    continue
                if any(layer[x] == "M" for x in e["inputs"]) or any(x in explained and x != e["target"] for x in e["inputs"]):
                    explained[e["target"]] = i
                    changed = True
        for r, (uid, why) in order["added"]["routes"].items():
            if uid == u["id"]:
                ev["added"].append({"id": r, "why": why, "kind": paper_edge(paper, r)["kind"], "grade": paper_edge(paper, r)["grade"]})
        cumV += len(ev["nodes"])
        cumA += len(ev["announce"])
        cumE += len(ev["establish"])
        debt = sum(1 for r in edges if t_a[r] <= i < t_e[r])
        ev["counts"] = {"V": cumV, "stated": cumE + debt, "supported": cumE, "debt": debt,
                        "conditional": sum(1 for r, c in conditional.items() if c["stated_support"] <= i < c["discharged"]),
                        "unexplained_O": sorted(v for v in nodes if layer[v] == "O" and t_n[v] <= i and v in has_in
                                                and explained.get(v, T + 1) > i)}
        log.append(ev)

    op_rule = {r: attribute_route(e, layer, sub, is_closure[r]) for r, e in edges.items()}
    # deferral and closure: a route stated before it is supported, all of whose ends appear before the supporting unit,
    # is a closure route under the support index
    deferred_all = [r for r in edges if t_a[r] < t_e[r]]
    deferred_closures = [r for r in deferred_all if is_closure[r]]
    # forward pointers of the text: first statements outside the abstract that sit in a unit with a pointer to a later part
    outside = [r for r in deferred_all if units[t_a[r]]["block"] != "abstract"]
    with_pointer = [r for r in outside if units[t_a[r]]["pointers"]]

    # ---- growth under three time conventions -------------------------------------------------------------------
    def rts(tr):
        return [{"id": r, "inputs": e["inputs"], "target": e["target"], "t": tr[r]} for r, e in edges.items()]
    first_route = {v: min([t_e[r] for r, e in edges.items() if v in ends(e)], default=t_n[v]) for v in t_n}
    merged = lambda t: max(t, 1) - 1                                          # abstract merged into the introduction
    block_of = {i: BLOCKS.index(u["block"]) for i, u in enumerate(units)}
    conv = {
        "stated": summarise(t_n, rts(t_a)),
        "supported": summarise(t_n, rts(t_e)),
        "supported, nodes dated by first route": summarise(first_route, rts(t_e)),
        "stated, abstract merged": summarise({v: merged(t) for v, t in t_n.items()}, rts({r: merged(t) for r, t in t_a.items()})),
        "supported, abstract merged": summarise({v: merged(t) for v, t in t_n.items()}, rts({r: merged(t) for r, t in t_e.items()})),
        "supported, by block": summarise({v: block_of[t] for v, t in t_n.items()}, rts({r: block_of[t] for r, t in t_e.items()}), vmin=1),
    }
    fl_stated = forward_links(t_n, rts(t_a))
    fl_supported = forward_links(t_n, rts(t_e))

    # ---- statement order against support order ------------------------------------------------------------------
    rs = sorted(edges)
    deferred = sorted(r for r in rs if t_a[r] < t_e[r])
    tau_as = kendall_tau_b([t_a[r] for r in rs], [t_e[r] for r in rs])
    tau_depth = kendall_tau_b([t_e[r] for r in rs], [ix["depth"][r] for r in rs])
    lat = sorted(t_e[r] - t_a[r] for r in deferred)

    # ---- phases -----------------------------------------------------------------------------------------------------
    phase_events = []
    for i, ev in enumerate(log):
        for n in ev["nodes"]:
            if n["phase"]:
                phase_events.append((i, n["phase"], "node"))
        for e in ev["establish"]:
            if e["phase"]:
                phase_events.append((i, e["phase"], "route"))
    profile = {p: sum(1 for _, q, _ in phase_events if q == p) for p in PHASES}
    first_phase = {p: min([i for i, q, _ in phase_events if q == p], default=None) for p in PHASES}
    tau_phase = kendall_tau_b([i for i, _, _ in phase_events], [PHASES.index(q) for _, q, _ in phase_events])
    by_block = {b: {p: 0 for p in PHASES} for b in BLOCKS}
    for i, q, _ in phase_events:
        by_block[units[i]["block"]][q] += 1
    ext_kinds = Counter(e["kind"] for ev in log for e in ev["establish"] if e["phase_source"] in ("extension", "default"))

    # ---- rule guards evaluated on the growing graph ------------------------------------------------------------
    # R12: a route that rules its target out, and the first later route into the same target that does not
    r12 = []
    for r, e in edges.items():
        if e["kind"] in NOGO_FAIL:
            res = sorted((t_e[q], q) for q, f in edges.items()
                         if f["target"] == e["target"] and q != r and f["kind"] not in NOGO_ALL and f["kind"] != "consistent")
            rec = sorted((t_e[q], q) for q, f in edges.items() if f["kind"] == "consistent" and r in uses[q])
            r12.append({"no_go": r, "target": e["target"], "unit": t_e[r],
                        "other_route_into_target": [{"route": q, "unit": t} for t, q in res],
                        "reconciled_by": [{"route": q, "unit": t} for t, q in rec]})
    # R6 guard: two different model nodes with a predicting route into the same target
    r6 = []
    preds = [(r, e) for r, e in edges.items() if e["kind"] == "predicts"]
    for a in range(len(preds)):
        for b in range(a + 1, len(preds)):
            (r1, e1), (r2, e2) = preds[a], preds[b]
            m1 = {x for x in e1["inputs"] if sub[x] == "model"}
            m2 = {x for x in e2["inputs"] if sub[x] == "model"}
            if e1["target"] == e2["target"] and m1 and m2 and m1 != m2:
                merge = sorted(q for q, f in edges.items() if f["kind"] == "equiv" and (m1 | m2) <= set(f["inputs"]))
                r6.append({"routes": [r1, r2], "models": sorted(m1 | m2), "target": e1["target"], "signal_unit": max(t_e[r1], t_e[r2]),
                           "merge_route": merge, "merge_unit": [t_e[q] for q in merge]})
    # R2 guard: observables and the first supported route into them that has a model leg
    r2 = [{"node": v, "sub": sub[v], "appears": t_n[v], "explained_unit": explained.get(v),
           "lag": (explained[v] - t_n[v]) if v in explained else None, "primitive": v not in has_in}
          for v in sorted(nodes) if layer[v] == "O"]
    # R18, effect form: criterion (no-go route with a model leg), test (route with a witness leg), member (measured datum)
    effects = []
    for v in sorted(nodes):
        if sub[v] != "effect":
            continue
        inc = [(r, e) for r, e in edges.items() if e["target"] == v]
        crit = sorted(r for r, e in inc if e["kind"] in NOGO_ALL and any(layer[x] == "M" for x in e["inputs"]))
        test = sorted(r for r, e in inc if any(sub[x] in ("witness", "task") for x in e["inputs"]))
        memb = sorted(r for r, e in inc if any(sub[x] == "direct" for x in e["inputs"]))
        effects.append({"effect": v, "criterion": crit, "test": test, "member": memb, "well_formed": bool(crit and test and memb)})

    # ---- counts ----------------------------------------------------------------------------------------------------
    ops = Counter()
    rules = Counter()
    closing = Counter()
    for ev in log:
        for n in ev["nodes"]:
            ops[n["op"]] += 1
            rules[n["rule"]] += 1
        for e in ev["establish"]:
            ops[e["op"]] += 1
            rules[e["rule"]] += 1
            if e["closure"]:
                closing[e["closing_route"]] += 1
    sup_grade = Counter((support[r], edges[r]["grade"]) for r in edges)
    Sg = signature(layer, [edges[r] for r in edges])
    and_routes = sum(1 for e in edges.values() if len(e["inputs"]) > 1)
    supp = {(a, b) for a in "SMO" for b in "SMO" if Sg[a][b]}
    types = {
        "D: support contains (M,S), (M,O), (S,O)": {("M", "S"), ("M", "O"), ("S", "O")} <= supp,
        "D: AND routes present": and_routes > 0,
        "H: support inside {(S,M),(M,O),(M,S),(M,M),(O,O)}": supp <= {("S", "M"), ("M", "O"), ("M", "S"), ("M", "M"), ("O", "O")},
        "E: all routes are single edges": and_routes == 0,
        "E: support contains (S,O)": ("S", "O") in supp,
    }

    by_blk = {b: {"units": 0, "nodes": 0, "carried": 0, "announce": 0, "establish": 0, "closure": 0,
                  "support": {s: 0 for s in SUPPORTS}} for b in BLOCKS}
    for ev in log:
        b = by_blk[ev["block"]]
        b["units"] += 1
        b["nodes"] += sum(1 for n in ev["nodes"] if n["op"] != "CARRY")
        b["carried"] += sum(1 for n in ev["nodes"] if n["op"] == "CARRY")
        b["announce"] += len(ev["announce"])
        b["establish"] += len(ev["establish"])
        b["closure"] += sum(1 for e in ev["establish"] if e["closure"])
        for e in ev["establish"]:
            b["support"][e["support"]] += 1

    return {
        "key": paper["key"], "citation": paper["citation"], "text_version": order["text_version"], "notes": order["notes"],
        "units": log,
        "nodes": [{"id": v, "layer": layer[v], "sub": sub[v], "title": n["title"], "definition": n["definition"], "status": n["status"],
                   "glue": n["glue"], "t": t_n[v]} for v, n in nodes.items()],
        "routes": [{"id": r, "inputs": e["inputs"], "target": e["target"], "kind": e["kind"], "grade": e["grade"],
                    "statement": e["statement"], "where": e["where"], "t_a": t_a[r], "t_e": t_e[r], "support": support[r],
                    "closure": is_closure[r], "uses": uses[r], "depth": ix["depth"][r], "restated": ix["restated"].get(r, []),
                    "discharged": memo[r], "waits_for": conditional.get(r, {}).get("on", []),
                    "op": op_rule[r][0], "rule": op_rule[r][1], "phase": phase_of_route(e, layer)[0],
                    "closing_route": closing_route(e, support[r])}
                   for r, e in edges.items()],
        "added_routes": [{"id": r, "unit": u, "why": w, "inputs": paper_edge(paper, r)["inputs"], "target": paper_edge(paper, r)["target"],
                          "kind": paper_edge(paper, r)["kind"], "grade": paper_edge(paper, r)["grade"],
                          "statement": paper_edge(paper, r)["statement"]} for r, (u, w) in order["added"]["routes"].items()],
        "added": {"routes": [{"id": r, "unit": u, "why": w} for r, (u, w) in order["added"]["routes"].items()],
                  "nodes": [{"id": v, "unit": u} for v, u in order["added"]["nodes"].items()]},
        "coverage": {"units": T, "units_not_encoded": [u["id"] for u in units if not u["encoded"]],
                     "nodes": len(nodes), "nodes_carried": sum(1 for n in nodes.values() if n["status"] == "existing"),
                     "routes": len(edges), "routes_added_by_encoding": len(ix["added_routes"]),
                     "pointers": sum(len(u["pointers"]) for u in units)},
        "order_tests": {
            "forward_links_nodes_stated": fl_stated, "forward_links_nodes_supported": fl_supported,
            "dependency_pairs": len(dep_pairs), "dependency_forward": fwd, "dependency_same_unit": len(same),
            "deferred_that_are_closures": len(deferred_closures),
            "deferred_outside_abstract": len(outside), "deferred_outside_abstract_with_pointer": len(with_pointer),
            "deferred": deferred, "deferred_latency": {"n": len(lat), "mean": (sum(lat) / len(lat)) if lat else None,
                                                         "median": (lat[len(lat) // 2] if lat else None), "max": max(lat) if lat else None},
            "conditional": conditional, "max_debt": max(ev["counts"]["debt"] for ev in log), "final_debt": log[-1]["counts"]["debt"],
            "tau_statement_vs_support": tau_as, "tau_support_vs_depth": tau_depth,
            "unsupported_in_paper": sorted(r for r in edges if support[r] in ("asserted", "implicit")),
        },
        "growth": conv,
        "phases": {"profile": profile, "first_unit": first_phase, "tau_unit_vs_loop_rank": tau_phase, "by_block": by_block,
                   "kinds_outside_table": dict(ext_kinds)},
        "guards": {"R2": r2, "R6": r6, "R12": r12, "R18_effect": effects},
        "counts": {"operations": dict(ops), "rules": dict(rules), "closing_routes": dict(closing),
                   "support_by_grade": [{"support": s, "grade": g, "n": n} for (s, g), n in sorted(sup_grade.items())],
                   "by_block": by_blk, "and_routes": and_routes, "signature": Sg, "type_tests": types},
    }


def paper_edge(paper, rid):
    return next(e for e in paper["edges"] if e["id"] == rid)


def run_all(results_path: str = None) -> Dict[str, Any]:
    papers = load_papers(results_path)
    return {k: replay(papers[k], ORDERS[k]) for k in ("battery", "realqm", "top", "decay")}


if __name__ == "__main__":
    out = run_all()
    for k, r in out.items():
        print(k, r["coverage"])
