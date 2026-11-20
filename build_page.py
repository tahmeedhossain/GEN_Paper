"""
Put the check results next to the page and build a standalone copy.

    python3 build_page.py

page/index.html                       loads page/results.json (the form that is published)
page/gen_edge_kernel_standalone.html  the same page with the results inlined (opens from disk)
"""
import json
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
PAGE = os.path.join(HERE, "page")
RESULTS = os.path.join(HERE, "out", "results.json")


def main():
    shutil.copyfile(RESULTS, os.path.join(PAGE, "results.json"))
    with open(RESULTS, encoding="utf-8") as f:
        data = json.load(f)
    with open(os.path.join(PAGE, "index.html"), encoding="utf-8") as f:
        html = f.read()
    blob = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    marker = "<script>\n(function(){"
    assert html.count(marker) == 1, "page script marker not found exactly once"
    standalone = html.replace(marker, "<script>window.__GEN_DATA__=" + blob + ";</script>\n" + marker)
    out = os.path.join(PAGE, "gen_edge_kernel_standalone.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(standalone)
    print("results.json:", os.path.getsize(os.path.join(PAGE, "results.json")), "bytes")
    print("standalone:", os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
