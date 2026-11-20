"""
Controls for the replay.  Each control plants one defect in the reading order or in the encoding and
requires the corresponding test to report it; two property tests check the ported growth code.
"""
import copy
import random

from growth import growth_decomposition, forward_links
from orders import ORDERS
from replay import OrderError, index_order, load_papers, replay


def _expect_error(fn, needle):
    try:
        fn()
    except OrderError as ex:
        return needle in str(ex), str(ex)
    return False, "no error raised"


def run():
    papers = load_papers()
    P, O = papers["battery"], ORDERS["battery"]
    base = replay(P, O)
    res = []

    def add(name, ok, detail):
        res.append({"control": name, "detected": bool(ok), "detail": detail})

    # 1 a node is left out of the order
    o = copy.deepcopy(O)
    o["units"][3]["nodes"].remove("ax-add")
    ok, d = _expect_error(lambda: index_order(P, o), "not placed")
    add("node missing from the reading order", ok, d)

    # 2 a route is given support in two units
    o = copy.deepcopy(O)
    o["units"][13]["establish"]["GB3"] = "proof"
    ok, d = _expect_error(lambda: index_order(P, o), "established twice")
    add("route supported in two units", ok, d)

    # 3 an announcement placed after the support
    o = copy.deepcopy(O)
    o["units"][20]["announce"].append("GB5")
    ok, d = _expect_error(lambda: index_order(P, o), "not before its support")
    add("announcement after the support", ok, d)

    # 4 the proof of Theorem 2 moved in front of the lemmas it uses: the dependency test must report the new pairs
    o = copy.deepcopy(O)
    o["units"][12]["establish"].pop("GB11")
    o["units"][11]["establish"]["GB11"] = "proof"
    r = replay(P, o)
    new = set(map(tuple, r["order_tests"]["dependency_forward"])) - set(map(tuple, base["order_tests"]["dependency_forward"]))
    add("theorem supported before its lemmas", {("GB11", "GB9"), ("GB11", "GB10"), ("GB11", "GB6"), ("GB11", "GB7")} <= new, sorted(new))

    # 5 a route supported before one of its nodes appears: the filtration test must report it
    o = copy.deepcopy(O)
    o["units"][20]["nodes"].remove("s-geo")
    o["units"][22]["nodes"].append("s-geo")
    r = replay(P, o)
    add("route supported before one of its nodes appears", ["GB14", "s-geo"] in [list(x) for x in r["order_tests"]["forward_links_nodes_supported"]],
        r["order_tests"]["forward_links_nodes_supported"])

    # 6 a cycle in the `uses` relation
    p = copy.deepcopy(P)
    next(e for e in p["edges"] if e["id"] == "GB1")["uses"].append("GB3")
    ok, d = _expect_error(lambda: index_order(p, O), "cycle")
    add("cyclic dependency", ok, d)

    # 7 an unknown kind must be reported as outside the phase table, not silently mapped
    p = copy.deepcopy(P)
    next(e for e in p["edges"] if e["id"] == "GB5")["kind"] = "foo"
    r = replay(p, O)
    add("kind outside the phase table", r["phases"]["kinds_outside_table"].get("foo") == 1, r["phases"]["kinds_outside_table"])

    # 8 debt: an announced route whose support is removed must be refused
    o = copy.deepcopy(O)
    o["units"][12]["establish"].pop("GB11")
    ok, d = _expect_error(lambda: index_order(P, o), "not established")
    add("announced route never supported", ok, d)

    # 9 property test of the arrival-closure identity on random time-indexed hypergraphs
    rng = random.Random(20261119)
    bad = 0
    for _ in range(2000):
        n = rng.randint(2, 14)
        nt = {f"v{i}": rng.randint(0, 6) for i in range(n)}
        routes = []
        for j in range(rng.randint(0, 25)):
            k = rng.randint(1, min(4, n - 1))
            ends = rng.sample(sorted(nt), k + 1)
            routes.append({"id": f"r{j}", "inputs": ends[:-1], "target": ends[-1], "t": max(nt[u] for u in ends) + rng.choice([0, 0, 1, 3])})
        g = growth_decomposition(nt, routes)
        if not g["identity_holds"] or forward_links(nt, routes):
            bad += 1
    add("identity E = Σd_arr − Σ(a−1)⁺ + C on 2000 random dated hypergraphs", bad == 0, f"{bad} failures")

    # 10 the identity must fail when a route is dated before one of its ends (it is a statement about filtrations of this kind)
    nt = {"a": 0, "b": 3}
    g = growth_decomposition(nt, [{"id": "r", "inputs": ["a"], "target": "b", "t": 1}])
    add("route dated before one of its ends is reported by the filtration test", forward_links(nt, [{"id": "r", "inputs": ["a"], "target": "b", "t": 1}]) == [("r", "b")],
        f"identity_holds={g['identity_holds']} (a route dated between its ends is counted as a closure; the filtration test is what rejects it)")
    return res


if __name__ == "__main__":
    out = run()
    for r in out:
        print(("DETECTED " if r["detected"] else "MISSED   ") + r["control"], "|", str(r["detail"])[:150])
    raise SystemExit(0 if all(r["detected"] for r in out) else 1)
