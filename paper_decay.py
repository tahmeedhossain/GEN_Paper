"""
Generated work: T. Hossain with Claude (Anthropic), "Particle decays as fixed measurements: exact noncontextuality
thresholds for decay-angle correlations", 17 November 2026.  Unpublished, not peer reviewed.

GENERATED WORK.  Unlike the three other papers checked in this repository, this paper was not written by human authors
and has not been published.  Its results, proofs, code and text were produced by an AI system (Claude, Anthropic) in a
session directed by T. Hossain on 17 November 2026.  Fifteen of its proofs are written in the paper and have not been
checked by any program or by an independent reviewer.

The project itself (paper sources, certificates, recorded runs, its own kernel run) is in decay_contextuality/.  This
module puts it on the footing of the other three papers: the same edge kernel runs the same certificates.

Taken unchanged from decay_contextuality/net/encoding.py: nodes, routes (inputs, target, kind, statement, grade, scope,
references, certificates) and claims.  Added here on 2026-11-20:
  uses     the routes each route relies on, read from the proofs in the paper (the original encoding has none);
  where    the location in the final text of the paper; the original fields use an earlier lettering of the appendices
           (it is kept in `note`);
  wrappers that turn the original certificate dictionaries into CertResult objects;
  delta, findings, sources and phases.
Grades are those of the original encoding; `compose` is a proof step written in the paper and checked by no program.
"""
from __future__ import annotations

import importlib.util
import os
import sys

from kernel import CertResult, Claim, Edge, Node, Paper

HERE = os.path.dirname(os.path.abspath(__file__))
DECAY = os.path.join(HERE, "decay_contextuality")
for _p in (os.path.join(DECAY, "net"), os.path.join(DECAY, "lib")):
    if _p not in sys.path:
        sys.path.append(_p)          # appended: the edge kernel's own modules (kernel, controls) keep precedence


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def encoding():
    return _load("decay_encoding", os.path.join(DECAY, "net", "encoding.py"))


def pretty_module():
    return _load("decay_pretty", os.path.join(DECAY, "page", "pretty.py"))


def controls_module():
    return _load("decay_controls", os.path.join(DECAY, "net", "controls.py"))


# ---------------------------------------------------------------------------------------------------------------------
# Locations in the final text.  Numbers of sections, theorems, equations, tables and figures are those of the compiled
# paper (decay_contextuality/paper/main.aux of 2026-11-20).
# Generated from main.aux by check_labels(); check_labels() compares this table with a fresh compilation.
LABELS = {
    "sec:setting": "II", "sec:polarimeter": "II A", "eq:born": "1", "eq:povm": "2", "eq:lambda": "3", "eq:firstmoment": "4",
    "eq:half": "5", "eq:spin1kernel": "6", "eq:symbol": "7", "sec:va": "II B", "eq:amp": "8", "eq:trace": "9",
    "eq:michel": "10", "eq:kappacut": "11", "eq:kappab": "12", "eq:kappanu": "13", "sec:models": "II C", "lem:simplex": "1",
    "eq:simplex": "14", "rem:lhv": "1", "sec:half": "III", "thm:half": "1", "eq:tetra": "15", "sec:pair": "III B",
    "eq:pairdata": "16", "eq:rhoraw": "17", "thm:pair": "2", "eq:localnc": "18", "eq:rangecond": "19", "cor:tstate": "1",
    "eq:svdmodel": "20", "cor:D": "2", "cor:weak": "3", "cor:ent": "4", "sec:one": "IV", "eq:ml": "21",
    "prop:cov": "1", "eq:Q1": "22", "eq:m12": "23", "thm:one": "3", "eq:R": "24", "eq:hR": "25",
    "cor:parity": "5", "rem:deg": "2", "prop:pairpoly": "2", "eq:pairpoly": "26", "thm:onepair": "4", "eq:R2": "27",
    "fig:regions": "1", "eq:hR2": "28", "cor:vis": "6", "tab:pairs": "I", "thm:spinj": "5", "eq:dipole": "29",
    "sec:apps": "V", "tab:gj": "II", "tab:kappa": "III", "fig:half": "2", "sec:graph": "VI", "fig:network": "3",
    "sec:discussion": "VII", "tab:claims": "IV", "app:lemma1": "A", "app:va": "B", "app:range": "C", "lem:range": "2",
    "app:cov": "D", "eq:lamdec": "D1", "app:spin1": "E", "lem:sos": "3", "eq:pencil": "E1", "eq:squares": "E2",
    "eq:Mt": "E3", "eq:R2points": "E6", "app:finite": "F", "app:spinj": "G", "app:numerics": "H", "app:catalogue": "I",
    "tab:nodes": "V", "tab:routesa": "VI", "tab:routesb": "VII",
}


def check_labels(aux_path=os.path.join(DECAY, "paper", "main.aux")):
    """Compare LABELS with the labels of a compiled main.aux; return the list of differences (empty if equal)."""
    import re
    if not os.path.exists(aux_path):
        return [f"{aux_path} not found (compile the paper first)"]
    found = {}
    for m in re.finditer(r"\\newlabel\{([^}]*)\}\{\{([^}]*)\}", open(aux_path, encoding="utf-8").read()):
        if ":" in m.group(1):
            found[m.group(1)] = m.group(2).replace("\\,", " ")
    keys = sorted(set(found) | set(LABELS))
    return [f"{k}: table {LABELS.get(k)!r}, compiled {found.get(k)!r}" for k in keys if LABELS.get(k) != found.get(k)]


def _where(template: str) -> str:
    out = template
    for k, v in LABELS.items():
        out = out.replace("{" + k + "}", v)
    if "{" in out:
        raise KeyError(f"unresolved label in {template!r}")
    return out


WHERE = {
    "DV1": "Sec. {sec:va}, Eq. ({eq:trace}); App. {app:va}",
    "DV2": "Sec. {sec:va}, text after Eq. ({eq:trace})",
    "DV3": "Sec. {sec:va}, Eqs. ({eq:michel})–({eq:kappacut}); App. {app:va}",
    "DV4": "Sec. {sec:va}, Eq. ({eq:kappab}); App. {app:va}",
    "DV5": "Sec. {sec:va}, Eq. ({eq:kappanu}); Sec. {sec:apps} A, Table {tab:kappa}",
    "DV6": "Sec. {sec:polarimeter}, Eqs. ({eq:born})–({eq:povm})",
    "DV7": "Sec. {sec:polarimeter}, Eqs. ({eq:spin1kernel})–({eq:symbol})",
    "DV8": "Sec. {sec:polarimeter}, Eq. ({eq:firstmoment}); App. {app:numerics}",
    "DV9": "Sec. {sec:pair}, Eqs. ({eq:pairdata})–({eq:rhoraw}); sign flip: paragraph after Corollary {cor:ent}",
    "DV10": "Sec. {sec:pair}, Corollary {cor:D}",
    "DV11": "Sec. {sec:pair}, paragraph before Theorem {thm:pair} (remote preparation)",
    "DV12": "not stated in the text of the paper; catalogue only (App. {app:catalogue})",
    "FW1": "Sec. {sec:models}, Lemma {lem:simplex}, Eq. ({eq:simplex}); App. {app:lemma1}",
    "FW2": "Sec. {sec:models}, Remark {rem:lhv}; Sec. I",
    "FW3": "Sec. {sec:models}, Remark {rem:lhv}",
    "FW4": "Sec. {sec:models}, Remark {rem:lhv}",
    "FW5": "Sec. I (third paragraph); Sec. {sec:models}, Remark {rem:lhv}",
    "FW6": "Sec. {sec:one} A, Proposition {prop:cov}, Eq. ({eq:ml}); App. {app:cov}",
    "FW7": "App. {app:numerics}",
    "H1": "Sec. {sec:half} A, Theorem {thm:half}, Eq. ({eq:tetra})",
    "H2": "Sec. {sec:half} A, proof of Theorem {thm:half}",
    "H13": "Sec. {sec:half} A, paragraph after Theorem {thm:half}",
    "H3": "Sec. {sec:pair}, Theorem {thm:pair} and its proof",
    "H4": "Sec. {sec:pair}, Theorem {thm:pair} and its proof; App. {app:range}, Lemma {lem:range}",
    "H12": "App. {app:range}, Lemma {lem:range}; App. {app:numerics}",
    "H5": "Sec. {sec:pair}, Corollary {cor:tstate}, Eq. ({eq:svdmodel})",
    "H6": "Sec. {sec:pair}, Corollary {cor:D}",
    "H7": "Sec. {sec:pair}, Corollary {cor:weak}",
    "H8": "Sec. {sec:pair}, Corollary {cor:ent}(ii)–(iii)",
    "H9": "Sec. {sec:pair}, paragraph after Corollary {cor:ent}; Sec. {sec:discussion}",
    "H10": "App. {app:numerics}",
    "H11": "Sec. {sec:pair}, Corollary {cor:ent}(i)",
    "V1": "App. {app:spin1} 1, Lemma {lem:sos}, Eq. ({eq:pencil})",
    "V2": "App. {app:spin1} 1, Lemma {lem:sos}(a); App. {app:numerics}",
    "V3": "Sec. {sec:one} B, Theorem {thm:one}, Eqs. ({eq:R})–({eq:hR}); App. {app:spin1} 2",
    "V4": "Sec. {sec:one} B (announced); App. {app:finite}",
    "V5": "Sec. {sec:one} B, Theorem {thm:one}; proof in App. {app:spin1} 2",
    "V6": "App. {app:spin1} 2; App. {app:numerics}",
    "V7": "Sec. {sec:one} B, Remark {rem:deg}; App. {app:spin1} 2",
    "P1": "Sec. {sec:one} C, Theorem {thm:onepair}, Eqs. ({eq:R2})–({eq:hR2}); App. {app:spin1} 3",
    "P2": "App. {app:finite}",
    "P3": "Sec. {sec:one} C, Theorem {thm:onepair} and Corollary {cor:vis}; proof in App. {app:spin1} 3",
    "P6": "Sec. {sec:one} C, Table {tab:pairs} and Corollary {cor:vis}",
    "P4": "App. {app:numerics}",
    "P5": "App. {app:numerics}",
    "G1": "Sec. {sec:one} D, Theorem {thm:spinj}(a) and its proof",
    "G2": "Sec. {sec:one} D, text before Theorem {thm:spinj}; Table {tab:gj}; App. {app:spinj}",
    "G3": "Sec. {sec:one} D, Theorem {thm:spinj}(b); App. {app:spinj}",
    "G5": "Sec. {sec:one} C, Proposition {prop:pairpoly}; Sec. {sec:one} D, Theorem {thm:spinj}(c), Eq. ({eq:dipole})",
    "G7": "Sec. {sec:one} D, proof of Theorem {thm:spinj}(a); App. {app:numerics}",
    "G6": "Sec. {sec:one} D, paragraph after the proofs of Theorem {thm:spinj}",
    "G4": "Sec. {sec:one} D, Table {tab:gj}; App. {app:spinj}; App. {app:numerics}",
    "A1": "Sec. {sec:apps} B",
    "A2": "Sec. {sec:apps} B",
    "A3": "Sec. {sec:apps} C",
    "A4": "Sec. {sec:apps} C, Fig. {fig:half}",
    "A5": "Sec. {sec:apps} A, Table {tab:kappa}",
    "A6": "Sec. {sec:apps} A, Table {tab:kappa}; reference in App. {app:va}",
    "A7": "Sec. {sec:one} C, Table {tab:pairs} and proof of Corollary {cor:vis}; Sec. {sec:apps} D",
    "A8": "Sec. {sec:one} B, Corollary {cor:parity}; Sec. {sec:apps} D",
    "X1": "Sec. I (third paragraph); Sec. {sec:graph} (released edge A5 of GEN_GPT_Level)",
    "X2": "Sec. I (relation to earlier work); Sec. {sec:pair}, Corollary {cor:ent}; Sec. {sec:graph}",
    "X3": "Sec. {sec:polarimeter}, Eqs. ({eq:born})–({eq:povm}); glue of m_A and m-quantum: Sec. {sec:graph}",
}

# Routes each route relies on, read from the proofs in the paper (2026-11-20).  A theorem about the fragment defined
# by a polarimeter node does not use DV6: the covariant form is the definition of that node.
USES = {
    "DV1": [], "DV2": ["DV1"], "DV3": ["DV1"], "DV4": ["DV1"], "DV5": ["DV1"], "DV6": [], "DV7": [], "DV8": [],
    "DV9": [], "DV10": [], "DV11": [], "DV12": ["DV8"],
    "FW1": [], "FW2": [], "FW3": ["FW2"], "FW4": ["FW2"], "FW5": ["FW2"], "FW6": ["FW1"], "FW7": [],
    "H1": [], "H2": ["FW1"], "H13": ["FW1"],
    "H3": ["FW1", "DV9"], "H4": ["FW1", "DV9", "H12"], "H12": [],
    "H5": ["H3"], "H6": ["H3"], "H7": ["H1", "H4"], "H8": ["H3", "H4"], "H9": ["DV9"], "H10": [], "H11": ["H4"],
    "V1": [], "V2": [], "V3": ["FW6", "V1", "DV7"], "V4": ["FW6", "DV7"], "V5": ["FW6", "V1", "V3", "DV7"],
    "V6": [], "V7": ["FW1", "DV7"],
    "P1": ["V1", "DV7"], "P2": ["DV7"], "P3": ["P1"], "P6": ["P1", "A7"], "P4": [], "P5": [],
    "G1": ["FW1", "DV8"], "G2": [], "G3": ["G2", "FW6"], "G5": ["FW1", "G1"], "G7": [], "G6": ["G5", "H5", "P1"],
    "G4": [],
    "A1": [], "A2": ["A1", "H6"], "A3": [], "A4": ["A3", "H3", "DV9"], "A5": [], "A6": [], "A7": [], "A8": ["V5"],
    "X1": [], "X2": ["H8"], "X3": [],
}

CLAIM_WHERE = {
    "C1": "Sec. {sec:polarimeter}–{sec:va}",
    "C2": "Sec. I; Sec. {sec:models}, Remark {rem:lhv}",
    "C3": "Sec. {sec:half} A, Theorem {thm:half}",
    "C4": "Sec. {sec:pair}, Theorem {thm:pair}, Corollaries {cor:tstate}–{cor:weak}",
    "C5": "Sec. {sec:one} B, Theorem {thm:one}",
    "C6": "Sec. {sec:one} C, Theorem {thm:onepair}, Corollary {cor:vis}",
    "C7": "Sec. {sec:one} D, Theorem {thm:spinj}",
    "C8": "Sec. {sec:apps} B",
    "C9": "Sec. {sec:apps} C",
    "C10": "Sec. {sec:va}; Sec. {sec:apps} A",
    "C11": "Sec. {sec:one} B, Corollary {cor:parity}; Sec. {sec:apps} D",
}
CLAIM_KIND = {"C8": "empirical", "C9": "empirical", "C11": "empirical"}


def _clean(o):
    """JSON-safe copy of certificate output (numpy scalars and arrays, sympy numbers, tuples)."""
    if isinstance(o, dict):
        return {str(k): _clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [_clean(v) for v in o]
    if hasattr(o, "tolist"):
        try:
            return _clean(o.tolist())
        except Exception:
            pass
    if hasattr(o, "item"):
        try:
            return o.item()
        except Exception:
            return str(o)
    if isinstance(o, (str, int, float, bool)) or o is None:
        return o
    return str(o)


def _cert_name(f, en):
    if f is getattr(en, "lpR", None):
        return "cert_lp_region('R')"
    if f is getattr(en, "lpR2", None):
        return "cert_lp_region('R2')"
    return getattr(f, "__name__", "certificate")


def _wrap(funcs, en):
    """One CertResult from the original certificates of a route (all must pass), as in the original kernel."""
    names = [_cert_name(f, en) for f in funcs]

    def cert():
        oks, summaries, data = [], [], {}
        for f, name in zip(funcs, names):
            out = f()
            oks.append(bool(out["ok"]))
            summaries.append(str(out["detail"]))
            data[name] = _clean({k: v for k, v in out.items() if k not in ("ok", "detail")})
        return CertResult(all(oks), " || ".join(summaries), data)

    return cert, names


# routes whose support in the text differs from what their grade says
METHOD_OVERRIDE = {
    "DV12": _where("graded as a written proof step, but the text gives neither the statement nor a proof (the catalogue "
                   "lists it as 'proof in text'); it is used without statement in Sec. {sec:va}; checked by no program"),
}


def build() -> Paper:
    en = encoding()
    pretty = pretty_module().pretty
    nodes = []
    for n in en.NODES:
        glue = [f"{n['released']}:{n['id']}"] if n["released"] else []
        glue += list(n["glue"])
        nodes.append(Node(n["id"], n["layer"], n["sub"], pretty(n["label"]), pretty(n["def"]),
                          status="existing" if n["released"] else "new", glue="; ".join(glue) or None))
    edges = []
    for r in en.ROUTES:
        cert, names = (None, [])
        if r["certs"]:
            cert, names = _wrap(r["certs"], en)
        edges.append(Edge(
            r["id"], list(r["inputs"]), r["target"], r["kind"], pretty(r["statement"]), _where(WHERE[r["id"]]),
            r["grade"], cert=cert, uses=list(USES[r["id"]]), scope=r["scope"],
            method=("certificates: " + ", ".join(names)) if names else METHOD_OVERRIDE.get(r["id"]) or
                   {"compose": "proof written in the paper; checked by no program", "import": "cited",
                    "definition": "definition"}.get(r["grade"], ""),
            note=f"location in the original encoding: {r['where']}", refs=list(r["refs"])))
    missing = {r["id"] for r in en.ROUTES} ^ set(USES)
    if missing:
        raise KeyError(f"uses table does not match the routes: {sorted(missing)}")
    claims = [Claim(c["id"], pretty(c["text"]), _where(CLAIM_WHERE[c["id"]]), list(c["routes"]),
                    kind=CLAIM_KIND.get(c["id"], "mathematical")) for c in en.CLAIMS]

    delta = [
        {"op": "ADD", "node": "s-spin, s-steer, s-tstate, s-iso1, s-ttbar, s-LLbar",
         "note": "state layer: spin states, steered ensembles, two families of pair states, two measured systems"},
        {"op": "ADD", "node": "p-decay, p-half, p-one, m-lhv1, m-ncom, ax-tomo",
         "note": "model layer: the decay polarimeter (general, spin 1/2, spin 1), the recorded-outcome model, the "
                 "noncontextual model and the tomographic-completeness assumption"},
        {"op": "ADD", "node": "o-ang1, o-ang2, o-D, w-rawppt, w-region1, w-kappa",
         "note": "observable layer: angular distributions, the opening-angle coefficient and three tests"},
        {"op": "ROUTE", "edge": "m_cc ∧ u_mh → p-half → o-ang2 → w-rawppt → e-ctx",
         "note": "closes the unconnected pair (GEN_HEP:m_cc, GEN_GPT_Level:e-ctx) that was taken as the question"},
        {"op": "GLUE", "edge": "X3", "note": "GEN_HEP:m_A (Born rule) with GEN_GPT_Level:m-quantum"},
        {"op": "GLUE", "node": "m-ncom", "note": "with GEN_GPT_Level:m-classical and GEN_QRT_Level:sF-ctx"},
        {"op": "SCOPE", "edge": "GEN_GPT_Level:A8",
         "note": "contextuality as a precondition of entanglement: with the measurement fixed to a decay the implication "
                 "is strict and becomes an equivalence only for |κ_A κ_B| = 1 (H8, X2)"},
        {"op": "OPEN", "gap": "s-iso1 → e-ctx outside the isotropic family (H → WW*, ZZ*)",
         "note": "open problem 1 of the paper"},
        {"op": "OPEN", "gap": "p-decay → m-ncom for j ≥ 3/2 beyond the vector direction", "note": "open problem 2"},
    ]
    findings = [
        {"level": "note", "title": "Generated work",
         "text": "This is not a published paper. Its results, proofs, code and text were produced by an AI system "
                 "(Claude, Anthropic) in a session directed by T. Hossain on 17 November 2026; nothing has been peer "
                 "reviewed. The 15 routes graded compose are proofs written in the paper that no program and no "
                 "independent reviewer has checked."},
        {"level": "note", "title": "Rebuilt from the session record",
         "text": "The project in decay_contextuality/ was rebuilt on 20 November 2026 from the tool calls of the session "
                 "that wrote it. The rebuilt encoding agrees with the published page of 17 November in all 35 nodes, "
                 "63 route statements and 11 claims. All certificates were executed again on 20 November 2026, "
                 "including the four long linear-programme runs (about 30 minutes): the outputs of all 63 routes agree "
                 "with the outputs recorded on the page, the 11 verdicts of the paper's own kernel are unchanged, and "
                 "16 of 16 negative controls are rejected."},
        {"level": "premise", "title": "Locations",
         "text": "The location fields of the original encoding use an earlier lettering of the appendices (for example "
                 "App. E for the numerical cross-checks, which are App. H of the paper) and give Lemma 2 for the lemma "
                 "on nonnegative quadratic functions, which is Lemma 3 in the paper. The locations used here are those "
                 "of the final text; the original ones are kept in the note of each route."},
        {"level": "premise", "title": "Dependencies added",
         "text": "The original encoding lists, for each claim, the routes named in it, and no route-to-route "
                 "dependencies. The dependencies used here were read from the proofs in the paper. With them the "
                 "closure of claim C8 (top pairs) contains the written necessity proof of Theorem 2 (H3) and Lemma 1 "
                 "(FW1, imported), and the closure of claim C10 (top polarimeters) contains Lemma 1 through the proof "
                 "of Theorem 1 (H2)."},
        {"level": "premise", "title": "A written step that the text does not contain",
         "text": _where("DV12 (the decay asymmetries of the released graph are the first multipoles of the polarimeter) has "
                        "grade compose and is listed in the catalogue of the paper (App. {app:catalogue}) as 'proof in text'. "
                        "The text neither states nor proves it; Sec. {sec:va} uses it ('the V-A spectrum with its decay "
                        "asymmetry'). No claim depends on it.")},
        {"level": "premise", "title": "Verdicts printed in the paper",
         "text": _where("Table {tab:claims} of the paper and the sentence of Sec. {sec:graph} 'Two claims are verified by executed certificates "
                 "alone' come from the paper's own kernel, which closes a claim over the routes named in it only. That "
                 "kernel gives C8 'verified modulo imports' and C10 'verified'. Closed over the dependencies of the "
                 "proofs, C8 is verified modulo imports and written proof steps and C10 modulo imports; one claim (C2) "
                 "rests on executed certificates alone. The other nine verdicts agree.")},
    ]
    sources = [
        {"title": "Paper sources and PDF: decay_contextuality/paper (this repository)", "url": "decay_contextuality/paper/"},
        {"title": "Schmid et al., PRX Quantum 2, 010331 (2021)", "url": "https://doi.org/10.1103/prxquantum.2.010331"},
        {"title": "Selby et al., Phys. Rev. Lett. 132, 050202 (2024)", "url": "https://doi.org/10.1103/physrevlett.132.050202"},
        {"title": "Plávala and Gühne, Phys. Rev. Lett. 132, 100201 (2024)", "url": "https://doi.org/10.1103/physrevlett.132.100201"},
        {"title": "ATLAS, Nature 633, 542 (2024)", "url": "https://doi.org/10.1038/s41586-024-07824-z"},
        {"title": "CMS, Rep. Prog. Phys. 87, 117801 (2024)", "url": "https://doi.org/10.1088/1361-6633/ad7e4d"},
        {"title": "BESIII, Phys. Rev. Lett. 129, 131801 (2022)", "url": "https://doi.org/10.1103/physrevlett.129.131801"},
    ]
    return Paper(
        key="decay",
        citation="T. Hossain with Claude (Anthropic), Particle decays as fixed measurements: exact noncontextuality "
                 "thresholds for decay-angle correlations, generated work, 17 November 2026 (unpublished, not peer reviewed)",
        ids={"status": "generated work", "location": "decay_contextuality/"},
        branch="Across branches: GEN_HEP v1.2 (charged-current vertex) and GEN_GPT_Level v2.6 (contextuality), "
               "glued to GEN_QRT_Level v1.2",
        summary="Treats a particle decay as one fixed rotation-covariant measurement of the parent spin and states exactly "
                "when decay-angle data admit a generalized-noncontextual model: spin 1/2, pairs of spin-1/2 particles, "
                "spin 1, spin-1 pairs and spin j, with applications to muon, top-quark, hyperon and vector-meson decays.",
        nodes=nodes, edges=edges, claims=claims, delta=delta, findings=findings, sources=sources, year=2026,
        phases=[["deficit", "two released nodes (GEN_HEP:m_cc, GEN_GPT_Level:e-ctx) have no route between them"],
                ["hypothesize", "a decay is modelled as one fixed covariant measurement (p-decay)"],
                ["falsify", "single-setting data cannot violate Bell or steering inequalities (FW3, FW4)"],
                ["predict", "thresholds for noncontextual models (Theorems 1–5)"],
                ["observe", "applied to measured top-pair and hyperon data (A1–A4)"]],
    )
