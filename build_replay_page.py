"""Copy out/replay.json beside the replay page and write a standalone copy with the data embedded."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
src = os.path.join(HERE, "page_replay", "index.html")
data = json.load(open(os.path.join(HERE, "out", "replay.json")))
json.dump(data, open(os.path.join(HERE, "page_replay", "replay.json"), "w"), ensure_ascii=False, separators=(",", ":"))
html = open(src).read()
marker = '<script>\n"use strict";'
assert html.count(marker) == 1
blob = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
out = html.replace(marker, '<script type="application/json" id="replay-data">' + blob + "</script>\n" + marker)
open(os.path.join(HERE, "page_replay", "gen_paper_replay_standalone.html"), "w").write(out)
print("page_replay/replay.json", os.path.getsize(os.path.join(HERE, "page_replay", "replay.json")), "bytes; standalone",
      os.path.getsize(os.path.join(HERE, "page_replay", "gen_paper_replay_standalone.html")), "bytes")
