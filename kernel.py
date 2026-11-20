"""
GEN edge kernel: a small checker for papers written as concept-graph deltas.

A paper is encoded as
  * nodes  : defined objects, each in one layer (S state, M model, O observable)
             with a sub-layer and a definition;
  * edges  : routes (inputs -> target; several inputs = AND route) that each carry
             ONE formal statement and ONE certificate;
  * claims : the paper's headline statements, each a set of edges it rests on.

The kernel does three things and nothing else:
  K1  lint the graph (layer signatures, in-degree-zero observables, effect/witness
      pairs, dangling references);
  K2  execute every certificate and record its grade and scope;
  K3  close each claim over its dependencies and report the trust base.

Certificate grades
  exact      symbolic / exact-arithmetic computation; holds for all values of the
             stated symbols, or for all elements of a basis when the statement is
             (multi)linear in them
  logic      entailment checked by an SMT solver (unsat of premises AND NOT conclusion)
  witness    an explicit object evaluated exactly (existence / counterexample claims)
  numeric    floating point or sampling: evidence, never proof
  import     a cited result that is not re-derived (trust base)
  definition true by unfolding a definition (nothing to run)
  compose    a proof step written out in words (a composition of other edges, or a
             proof given in the paper) that no program has checked
  interpretive  not a mathematical statement; the kernel does not decide it

Verdict of a claim (version 1.1, 2026-11-20), first match in this order, over the claim's
edges and everything they use:
  discrepancy                       a certificate failed
  not decidable by the kernel       an interpretive edge
  numerical support only            numeric edges and no exact, logic, witness or compose edge
  verified modulo imports and written proof steps
  verified modulo written proof steps
  verified modulo imports
  verified on instances             an exact, logic or witness edge with instance scope
  verified
Version 1.0 (2026-11-17) did not put written proof steps into the label and returned
'numerical support only' whenever a numeric edge occurred; 1.1 is the rule of the kernel
written with the generated decay-contextuality paper (session of 2026-11-17, UTC).

Kernel rule (no certificate needed): scope separation. A no-go edge and a possibility
edge are consistent if some input (premise) of the no-go edge is absent from the
possibility edge and a checked edge of kind 'violates' shows that the possibility's
model lacks that premise.

Scope
  'general'            the certificate covers the statement as written
  'instances: ...'     exact, but only for the listed parameter values
"""
from __future__ import annotations

import json
import time
import traceback
from dataclasses import dataclass, field
from typing import Callable, Optional

import z3

LAYERS = ("S", "M", "O")
GRADES = ("exact", "logic", "witness", "numeric", "import", "definition", "compose", "interpretive")
KERNEL_GRADES = ("exact", "logic", "witness", "definition")

SUBLAYERS = {
    "S": {"point", "field", "hilbert", "uir", "sector", "cluster", "free", "resource", "dist"},
    "M": {"law", "frame", "axiom", "model", "fund", "eff", "cand", "cluster", "process"},
    "O": {"direct", "effect", "witness", "task"},
}


@dataclass
class Node:
    id: str
    layer: str
    sub: str
    title: str
    definition: str
    status: str = "new"            # existing | new | split | out-of-scope
    glue: Optional[str] = None     # id in a released network, "REPO:node-id"
    refs: list = field(default_factory=list)


@dataclass
class CertResult:
    ok: bool
    summary: str
    data: dict = field(default_factory=dict)
    scope: Optional[str] = None    # overrides the edge's declared scope if set


@dataclass
class Edge:
    id: str
    inputs: list
    target: str
    kind: str
    statement: str
    where: str                     # location in the paper (equation / theorem)
    grade: str
    cert: Optional[Callable[[], CertResult]] = None
    uses: list = field(default_factory=list)   # edges whose statements this one relies on
    scope: str = "general"
    method: str = ""               # one-line description of how the edge is generated
    note: str = ""
    refs: list = field(default_factory=list)
    rule: Optional[dict] = None    # kernel rule instead of a certificate, e.g. scope separation


@dataclass
class Claim:
    id: str
    text: str
    where: str
    edges: list
    kind: str = "mathematical"     # mathematical | empirical | interpretive


@dataclass
class Paper:
    key: str
    citation: str
    ids: dict
    branch: str
    summary: str
    nodes: list
    edges: list
    claims: list
    delta: list = field(default_factory=list)       # operations on the released networks
    findings: list = field(default_factory=list)    # filled by the encoding (static notes)
    sources: list = field(default_factory=list)
    year: int = 0                                   # year the paper enters the evolutionary network
    phases: list = field(default_factory=list)      # phases of the method cycle, read by hand: [name, reason]


# ----------------------------------------------------------------------------
# SMT helper (part of the trusted base)
# ----------------------------------------------------------------------------

def smt_entails(premises: dict, conclusion, timeout_ms: int = 60000, minimality: bool = True):
    """Check  AND(premises) => conclusion  by refutation.

    Returns (ok, info). With minimality=True every premise is dropped in turn; a
    premise is 'needed' if the conclusion fails without it (the solver returns a
    counter-model), 'redundant' if the entailment survives without it.
    """
    def run(prem_items):
        s = z3.Solver()
        s.set("timeout", timeout_ms)
        for _, p in prem_items:
            s.add(p)
        s.add(z3.Not(conclusion))
        return s.check()

    items = list(premises.items())
    r = run(items)
    ok = (r == z3.unsat)
    info = {"result": str(r), "premises": [k for k, _ in items]}
    if ok and minimality:
        needed, redundant, unknown = [], [], []
        for k, _ in items:
            rr = run([(kk, pp) for kk, pp in items if kk != k])
            (needed if rr == z3.sat else redundant if rr == z3.unsat else unknown).append(k)
        info.update({"needed": needed, "redundant": redundant, "undecided": unknown})
    return ok, info


def smt_sat(constraints: list, timeout_ms: int = 60000):
    """Satisfiability of a constraint set (used for consistency / counter-model checks)."""
    s = z3.Solver()
    s.set("timeout", timeout_ms)
    for c in constraints:
        s.add(c)
    r = s.check()
    model = {}
    if r == z3.sat:
        m = s.model()
        model = {str(d): str(m[d]) for d in m.decls()}
    return str(r), model


# ----------------------------------------------------------------------------
# K1 lint
# ----------------------------------------------------------------------------

def lint(paper: Paper) -> dict:
    ids = {n.id: n for n in paper.nodes}
    problems = []
    for n in paper.nodes:
        if n.layer not in LAYERS:
            problems.append(f"node {n.id}: unknown layer {n.layer}")
        elif n.sub not in SUBLAYERS[n.layer]:
            problems.append(f"node {n.id}: sub-layer {n.sub} not in the {n.layer} list")
        if not n.definition.strip():
            problems.append(f"node {n.id}: empty definition")
    eids = set()
    for e in paper.edges:
        if e.id in eids:
            problems.append(f"edge {e.id}: duplicate id")
        eids.add(e.id)
        for x in list(e.inputs) + [e.target]:
            if x not in ids:
                problems.append(f"edge {e.id}: unknown node {x}")
        if e.grade not in GRADES:
            problems.append(f"edge {e.id}: unknown grade {e.grade}")
        if e.grade in ("exact", "logic", "witness", "numeric") and e.cert is None and e.rule is None:
            problems.append(f"edge {e.id}: grade {e.grade} without a certificate")
    for e in paper.edges:
        for u in e.uses:
            if u not in eids:
                problems.append(f"edge {e.id}: uses unknown edge {u}")
    for c in paper.claims:
        for u in c.edges:
            if u not in eids:
                problems.append(f"claim {c.id}: unknown edge {u}")

    # layer-pair signature: 3x3 counts of (input layer -> target layer), one count per leg
    sig = {a: {b: 0 for b in LAYERS} for a in LAYERS}
    routes = {}
    and_routes = 0
    for e in paper.edges:
        if any(x not in ids for x in list(e.inputs) + [e.target]):
            continue
        tl = ids[e.target].layer
        for i in e.inputs:
            sig[ids[i].layer][tl] += 1
        key = "∧".join(sorted({ids[i].layer for i in e.inputs})) + "→" + tl
        routes[key] = routes.get(key, 0) + 1
        if len(e.inputs) > 1:
            and_routes += 1

    indeg = {}
    for e in paper.edges:
        indeg.setdefault(e.target, []).append(e.id)
    or_targets = {t: v for t, v in indeg.items() if len(v) > 1}

    # observables with no route from the model layer (Rule 2: in-degree-zero drive)
    unexplained = []
    for n in paper.nodes:
        if n.layer != "O" or n.status == "out-of-scope":
            continue
        has_m = any(e.target == n.id and any(ids[i].layer == "M" for i in e.inputs if i in ids)
                    for e in paper.edges)
        if not has_m:
            unexplained.append(n.id)

    # design principle of the nonclassicality network: no effect without a witness
    effects = [n.id for n in paper.nodes if n.layer == "O" and n.sub == "effect"]
    unpaired = []
    for ef in effects:
        paired = any(e.target == ef and any(ids[i].sub == "witness" for i in e.inputs if i in ids)
                     for e in paper.edges)
        if not paired:
            unpaired.append(ef)

    return {
        "problems": problems,
        "signature": sig,
        "route_types": routes,
        "and_routes": and_routes,
        "or_targets": {k: v for k, v in or_targets.items()},
        "observables_without_model_route": unexplained,
        "effects_without_witness": unpaired,
        "counts": {
            "nodes": len(paper.nodes),
            "nodes_existing": sum(1 for n in paper.nodes if n.status == "existing"),
            "nodes_new": sum(1 for n in paper.nodes if n.status != "existing"),
            "edges": len(paper.edges),
            "S": sum(1 for n in paper.nodes if n.layer == "S"),
            "M": sum(1 for n in paper.nodes if n.layer == "M"),
            "O": sum(1 for n in paper.nodes if n.layer == "O"),
        },
    }


# ----------------------------------------------------------------------------
# K2 run certificates
# ----------------------------------------------------------------------------

def run_edge(e: Edge) -> dict:
    out = {
        "id": e.id, "inputs": e.inputs, "target": e.target, "kind": e.kind,
        "statement": e.statement, "where": e.where, "grade": e.grade,
        "uses": e.uses, "scope": e.scope, "method": e.method, "note": e.note,
        "refs": e.refs,
    }
    if e.rule is not None:
        out.update({"status": "pending rule", "summary": "", "data": {"rule": e.rule}, "seconds": 0.0})
        return out
    if e.cert is None:
        out.update({"status": {"import": "imported", "definition": "definition", "compose": "composed",
                               "interpretive": "not decidable"}.get(e.grade, "no certificate"),
                    "summary": e.method if e.grade == "compose" else "", "data": {}, "seconds": 0.0})
        return out
    t0 = time.time()
    try:
        r = e.cert()
        out["status"] = "checked" if r.ok else "FAILED"
        out["summary"] = r.summary
        out["data"] = r.data
        if r.scope:
            out["scope"] = r.scope
    except Exception as ex:  # a crashing certificate is a failed certificate
        out["status"] = "FAILED"
        out["summary"] = f"certificate raised {type(ex).__name__}: {ex}"
        out["data"] = {"traceback": traceback.format_exc()[-1500:]}
    out["seconds"] = round(time.time() - t0, 3)
    return out


NOGO_KINDS = ("forbids", "irreversible", "excludes")


def apply_rule(e: Edge, edges: dict, results: dict) -> tuple:
    """Kernel rules that act on the graph itself. Returns (ok, summary)."""
    r = e.rule
    if r.get("type") != "scope_separation":
        return False, f"unknown rule {r.get('type')}"
    nogo, poss, prem, ev = (r.get(k) for k in ("nogo", "possibility", "premise", "evidence"))
    for x in (nogo, poss, ev):
        if x not in edges:
            return False, f"rule refers to unknown edge {x}"
    checks = {
        f"{nogo} is a no-go edge": edges[nogo].kind in NOGO_KINDS,
        f"premise {prem} is an input of {nogo}": prem in edges[nogo].inputs,
        f"premise {prem} is not an input of {poss}": prem not in edges[poss].inputs,
        f"{poss} is checked": results[poss]["status"] == "checked",
        f"{ev} is a checked 'violates' edge on {prem}": (edges[ev].kind == "violates"
                                                        and results[ev]["status"] == "checked"
                                                        and (prem in edges[ev].inputs or edges[ev].target == prem)),
    }
    ok = all(checks.values())
    bad = [k for k, v in checks.items() if not v]
    return ok, ("scope separation: no-go " + nogo + " needs premise " + prem + "; possibility " + poss
                + " does not use it; " + ev + " certifies its absence" if ok else "rule failed: " + "; ".join(bad))


# ----------------------------------------------------------------------------
# K3 closure and trust base
# ----------------------------------------------------------------------------

def closure(claim: Claim, results: dict) -> dict:
    seen, order = set(), []

    def visit(eid):
        if eid in seen:
            return
        seen.add(eid)
        for u in results[eid]["uses"]:
            visit(u)
        order.append(eid)

    for eid in claim.edges:
        visit(eid)

    failed = [e for e in order if results[e]["status"] == "FAILED"]
    imports = [e for e in order if results[e]["grade"] == "import"]
    numeric = [e for e in order if results[e]["grade"] == "numeric"]
    interp = [e for e in order if results[e]["grade"] == "interpretive"]
    composed = [e for e in order if results[e]["grade"] == "compose"]
    instance = [e for e in order if results[e]["grade"] in ("exact", "witness", "logic")
                and not results[e]["scope"].startswith("general")]
    kernel = [e for e in order if results[e]["grade"] in KERNEL_GRADES
              and results[e]["status"] in ("checked", "definition")]

    mechanised = [e for e in order if results[e]["grade"] in ("exact", "logic", "witness")]

    # one label, in order of precedence (version 1.1); the qualifying lists are reported next to it
    if failed:
        verdict = "discrepancy"
    elif interp:
        verdict = "not decidable by the kernel"
    elif numeric and not mechanised and not composed:
        verdict = "numerical support only"
    elif composed:
        verdict = "verified modulo imports and written proof steps" if imports else "verified modulo written proof steps"
    elif imports:
        verdict = "verified modulo imports"
    elif instance:
        verdict = "verified on instances"
    else:
        verdict = "verified"

    return {
        "id": claim.id, "text": claim.text, "where": claim.where, "kind": claim.kind,
        "verdict": verdict, "depends_on": order, "kernel_checked": kernel,
        "imports": imports, "numeric_only": numeric, "instance_scoped": instance,
        "interpretive": interp, "failed": failed, "unmechanised_steps": composed,
    }


def run_paper(paper: Paper, verbose: bool = True) -> dict:
    lint_out = lint(paper)
    results = {}
    by_id = {e.id: e for e in paper.edges}
    for e in paper.edges:
        results[e.id] = run_edge(e)
    for e in paper.edges:                       # second pass: kernel rules need the other results
        if e.rule is not None:
            ok, summary = apply_rule(e, by_id, results)
            results[e.id].update({"status": "checked" if ok else "FAILED", "summary": summary})
    if verbose:
        for e in paper.edges:
            r = results[e.id]
            print(f"  [{r['status']:<13}] {e.id:<6} {r['grade']:<12} {r['seconds']:>7.2f}s  {r['summary'][:110]}")
    claims = [closure(c, results) for c in paper.claims]
    by_grade = {}
    for r in results.values():
        by_grade[r["grade"]] = by_grade.get(r["grade"], 0) + 1
    return {
        "key": paper.key, "citation": paper.citation, "ids": paper.ids, "branch": paper.branch,
        "summary": paper.summary, "sources": paper.sources, "year": paper.year, "phases": paper.phases,
        "nodes": [n.__dict__ for n in paper.nodes],
        "edges": [results[e.id] for e in paper.edges],
        "claims": claims, "lint": lint_out, "delta": paper.delta, "findings": paper.findings,
        "grade_counts": by_grade,
        "failed": [r["id"] for r in results.values() if r["status"] == "FAILED"],
    }


def dump(obj, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=1, default=str)
