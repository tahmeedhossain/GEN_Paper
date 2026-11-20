"""Builds page/index.html: the three-layer graph of the decay-polarimetry routes, from out/results.json.
One self-contained HTML file (data embedded); fonts from Google Fonts."""
import json, os, sys, html
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from pretty import pretty

d = json.load(open(os.path.join(ROOT, 'out', 'results.json')))
S = d['summary']; res = d['results']
NET = {'GEN_HEP': 'Standard Model graph', 'GEN_GPT_Level': 'Nonclassicality Network', None: 'This work'}
SUBS = {'uir': 'particle', 'hilbert': 'state space', 'cluster': 'family of states', 'free': 'free states', 'resource': 'resource states', 'sector': 'physical system',
        'frame': 'postulate', 'fund': 'interaction term', 'eff': 'effective term', 'model': 'theory or model', 'process': 'measurement', 'axiom': 'assumption',
        'direct': 'recorded quantity', 'witness': 'test', 'effect': 'effect'}
CLAIM_NAMES = {'C1': 'Decay as a measurement', 'C2': 'No Bell test, yet a test', 'C3': 'Theorem 1 · spin 1/2', 'C4': 'Theorem 2 · spin-1/2 pairs', 'C5': 'Theorem 3 · spin 1',
               'C6': 'Theorem 4 · spin-1 pairs', 'C7': 'Theorem 5 · spin j', 'C8': 'Top-quark pairs', 'C9': 'Hyperon pairs', 'C10': 'Top-quark polarimeters', 'C11': 'Vector mesons'}
STATUS = {'checked': 'checked by certificate', 'written proof step': 'proof written in the paper', 'imported': 'cited', 'definition': 'definition'}
GRADE = {'exact': 'exact', 'logic': 'logic', 'numeric': 'numeric', 'import': 'import', 'definition': 'definition', 'compose': 'written'}

def lst(v):
    if isinstance(v, list): return v
    return []
nodes = [{'id': n['id'], 'layer': n['layer'], 'type': SUBS.get(n['sub'], n['sub']), 'label': n['label'], 'def': pretty(n['def']),
          'net': NET[n['released']], 'repo': n['released'] or '', 'glue': lst(n.get('glue'))} for n in d['nodes']]
routes = []
for r in d['routes']:
    x = res[r['id']]
    det = x.get('detail')
    if isinstance(det, list): det = ' | '.join(str(t) for t in det)
    routes.append({'id': r['id'], 'inputs': lst(r['inputs']), 'target': r['target'], 'kind': r['kind'].replace('_', ' '), 'statement': pretty(r['statement']), 'where': r['where'],
                   'grade': GRADE[r['grade']], 'status': STATUS[x['status']], 'ok': x.get('ok'), 'certs': [c.replace('cert_', '').replace('<lambda>', 'lp_region') for c in lst(r['certs'])],
                   'scope': r.get('scope', 'general'), 'refs': lst(r.get('refs')), 'detail': pretty(det) if det else ''})
claims = [{'id': c['id'], 'name': CLAIM_NAMES[c['id']], 'text': pretty(c['text']), 'routes': c['routes'], 'verdict': c['verdict'],
           'mechanised': c.get('mechanised', []), 'numeric': c.get('numeric_crosschecks', []), 'written': c.get('written_steps', []), 'imports': c.get('imports', [])} for c in d['claims']]
controls = [{'id': c['id'], 'planted': pretty(' '.join(c['planted'].split())), 'rejected': c['rejected'], 'detail': pretty(c['detail'])} for c in d['controls']]
data = {'summary': {'routes': S['routes'], 'checked': S['checked'], 'by': S['checked_by_grade'], 'imported': S['status'].get('imported', 0), 'definitions': S['status'].get('definition', 0),
                    'written': S['status'].get('written proof step', 0), 'nodes': S['nodes'], 'released': S['nodes_released'], 'new': S['nodes_new'], 'controls': S['controls'],
                    'rejected': S['controls_rejected'], 'failed': S['failed'], 'seconds': S['seconds']},
        'nodes': nodes, 'routes': routes, 'claims': claims, 'controls': controls}
blob = json.dumps(data, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')

TEMPLATE = r'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Decay Contextuality Graph</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600&family=Source+Serif+4:opsz,wght@8..60,600&display=swap" rel="stylesheet">
<style>
/* Layout idea: summary first; three layer columns (state, model, observable) with a sticky detail rail;
   the routes of the current selection are drawn across the columns; the full route table follows. */
:root{
  --bg:#f1f3f6; --surface:#ffffff; --band:#e6eaef; --ink:#11161b; --ink-2:#48535e; --ink-3:#76818d; --line:#cfd6dd;
  --accent:#2459b8; --exact:#2a78d6; --logic:#16936a; --numeric:#d4602a; --good:#157a4f; --tint:#e8f0fc;
  --display:"Source Serif 4", Georgia, "Times New Roman", serif;
  --body:"IBM Plex Sans", "Segoe UI", system-ui, sans-serif;
  --mono:"IBM Plex Mono", ui-monospace, "SFMono-Regular", Menlo, monospace;
}
@media (prefers-color-scheme: dark){
  :root:not([data-theme="light"]){
    color-scheme:dark;
    --bg:#0f1317; --surface:#181d23; --band:#141a20; --ink:#e7ebef; --ink-2:#a7b2bd; --ink-3:#7c8793; --line:#2a323b;
    --accent:#86b3ff; --exact:#5fa2ee; --logic:#3fc18f; --numeric:#f08d58; --good:#4ccf96; --tint:#1b2a44;
  }
}
:root[data-theme="dark"]{
  color-scheme:dark;
  --bg:#0f1317; --surface:#181d23; --band:#141a20; --ink:#e7ebef; --ink-2:#a7b2bd; --ink-3:#7c8793; --line:#2a323b;
  --accent:#86b3ff; --exact:#5fa2ee; --logic:#3fc18f; --numeric:#f08d58; --good:#4ccf96; --tint:#1b2a44;
}
*{box-sizing:border-box}
html,body{margin:0}
body{background:var(--bg);color:var(--ink);font-family:var(--body);font-size:15px;line-height:1.5;-webkit-font-smoothing:antialiased}
.wrap{max-width:1320px;margin:0 auto;padding:28px 20px 56px}
h1{font-family:var(--display);font-weight:600;font-size:34px;line-height:1.15;margin:0 0 10px;text-wrap:balance}
h2{font-family:var(--display);font-weight:600;font-size:21px;margin:0 0 12px;text-wrap:balance}
p{margin:0 0 10px}
.lede{max-width:68ch;color:var(--ink-2);font-size:16px}
.stats{display:flex;flex-wrap:wrap;gap:8px;margin:18px 0 0;padding:0;list-style:none}
.stats li{background:var(--surface);border:1px solid var(--line);border-radius:6px;padding:7px 11px;font-size:13.5px;color:var(--ink-2)}
.stats b{color:var(--ink);font-weight:600;font-variant-numeric:tabular-nums}
section{margin-top:34px}
.claims{display:flex;flex-wrap:wrap;gap:8px}
button{font:inherit;color:inherit}
.claim{background:var(--surface);border:1px solid var(--line);border-radius:6px;padding:7px 11px;cursor:pointer;text-align:left;display:flex;gap:8px;align-items:baseline}
.claim .cid{font-family:var(--mono);font-size:12.5px;color:var(--ink-3)}
.claim[aria-pressed="true"]{border-color:var(--accent);background:var(--tint)}
.claim:hover,.node:hover,tbody tr:hover{border-color:var(--accent)}
:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
.board{display:grid;grid-template-columns:minmax(0,1fr) 350px;gap:18px;align-items:start;margin-top:14px}
.cols{position:relative;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:46px}
.col{background:var(--band);border-radius:8px;padding:12px 30px 14px 12px;display:flex;flex-direction:column;gap:9px}
.col h3{font-size:12px;letter-spacing:.08em;text-transform:uppercase;font-weight:600;color:var(--ink-2);margin:0}
.col .sub{font-size:12.5px;color:var(--ink-3);margin:-6px 0 4px}
.node{position:relative;z-index:2;display:block;width:100%;text-align:left;background:var(--surface);border:1px solid var(--line);border-radius:6px;padding:7px 9px;cursor:pointer}
.node .net{display:block;font-size:11px;letter-spacing:.03em;color:var(--ink-3);text-transform:uppercase}
.node .lab{display:block;font-weight:500;font-size:14px;line-height:1.3}
.node .nid{display:block;font-family:var(--mono);font-size:11.5px;color:var(--ink-3);margin-top:2px}
.node.new{border-left:3px solid var(--accent)}
.node.on{border-color:var(--accent);box-shadow:0 0 0 1px var(--accent)}
.node.sel{background:var(--tint)}
.cols.active .node:not(.on){background:var(--band);border-color:var(--line)}
.cols.active .node:not(.on) .lab{color:var(--ink-3);font-weight:400}
svg.edges{position:absolute;left:0;top:0;z-index:1;pointer-events:none;overflow:visible}
svg.edges path{fill:none;stroke-width:1.6}
svg.edges text{font-family:var(--mono);font-size:10.5px;fill:var(--ink-2);paint-order:stroke;stroke:var(--band);stroke-width:4px;stroke-linejoin:round}
.rail{position:sticky;top:14px;background:var(--surface);border:1px solid var(--line);border-radius:8px;padding:16px;max-height:calc(100vh - 28px);overflow:auto}
.rail .eyebrow{font-size:11.5px;letter-spacing:.06em;text-transform:uppercase;color:var(--ink-3);margin-bottom:2px}
.rail h3{font-family:var(--display);font-size:19px;line-height:1.25;margin:0 0 8px;text-wrap:balance}
.rail .stmt{font-size:14.5px}
.rail dl{margin:12px 0 0;display:grid;grid-template-columns:auto 1fr;gap:5px 12px;font-size:13.5px}
.rail dt{color:var(--ink-3)}
.rail dd{margin:0;min-width:0;overflow-wrap:anywhere}
.out{font-family:var(--mono);font-size:12px;background:var(--band);border-radius:6px;padding:8px 10px;margin-top:10px;overflow-wrap:anywhere;white-space:pre-wrap}
.pill{display:inline-flex;align-items:center;gap:6px;border:1px solid var(--line);border-radius:999px;padding:1px 9px;font-size:12.5px;white-space:nowrap}
.pill i{width:14px;height:0;border-top:2px solid var(--ink-3);display:inline-block}
.g-exact i{border-color:var(--exact)} .g-logic i{border-color:var(--logic)} .g-numeric i{border-color:var(--numeric)}
.g-written i{border-top-style:dashed;border-color:var(--ink-2)} .g-import i{border-top-style:dotted;border-color:var(--ink-3)} .g-definition i{border-top-width:1px}
.ok{color:var(--good);font-weight:600}
.chips{display:flex;flex-wrap:wrap;gap:5px;margin-top:4px}
.chip{font-family:var(--mono);font-size:12px;background:var(--band);border:1px solid transparent;border-radius:4px;padding:1px 6px;cursor:pointer}
.chip:hover{border-color:var(--accent)}
.tools{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin-bottom:10px}
.filter{background:var(--surface);border:1px solid var(--line);border-radius:999px;padding:3px 11px;cursor:pointer;font-size:13px}
.filter[aria-pressed="true"]{border-color:var(--accent);background:var(--tint)}
.tablewrap{overflow-x:auto;background:var(--surface);border:1px solid var(--line);border-radius:8px}
table{border-collapse:collapse;width:100%;font-size:13.5px;min-width:760px}
th{font-size:11.5px;letter-spacing:.06em;text-transform:uppercase;color:var(--ink-3);text-align:left;font-weight:600;padding:9px 10px;border-bottom:1px solid var(--line)}
td{padding:7px 10px;border-bottom:1px solid var(--line);vertical-align:top}
tbody tr{cursor:pointer}
tbody tr.cur td{background:var(--tint)}
td.id,td.mono{font-family:var(--mono);font-size:12.5px;white-space:nowrap}
.ctl{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:10px;padding:0;margin:0;list-style:none}
.ctl li{background:var(--surface);border:1px solid var(--line);border-radius:6px;padding:9px 11px;font-size:13.5px}
.ctl .cid{font-family:var(--mono);font-size:12px;color:var(--ink-3)}
.ctl .why{color:var(--ink-2);font-size:12.5px;margin-top:4px;overflow-wrap:anywhere}
.legend{display:flex;flex-wrap:wrap;gap:8px 14px;margin-top:10px;font-size:13px;color:var(--ink-2)}
footer{margin-top:40px;color:var(--ink-2);font-size:13.5px;max-width:78ch}
a{color:var(--accent)}
@media (max-width:1080px){.board{grid-template-columns:minmax(0,1fr)}.rail{position:static;max-height:none}}
@media (max-width:760px){.cols{grid-template-columns:minmax(0,1fr);gap:16px}h1{font-size:28px}}
@media (prefers-reduced-motion:no-preference){.node,.claim{transition:border-color .12s, opacity .12s}}
</style>
</head>
<body>
<div class="wrap">
<header>
<h1>Decay Contextuality Graph</h1>
<p class="lede" style="border-left:3px solid currentColor;padding-left:10px"><b>Generated work.</b> The derivations, code and text of this result were produced by an AI system (Claude, Anthropic) in a session directed by T. Hossain on 17 November 2026. It is unpublished and has not been peer reviewed; the proofs graded &ldquo;written&rdquo; are checked by no program.</p>
<p class="lede">A particle decay measures the spin of its parent with one fixed setting, so decay-angle data cannot violate a Bell inequality. They can still fail to have a generalized-noncontextual model. The routes below say exactly when, and connect the charged-current vertex of the Standard Model graph to the contextuality node of the Nonclassicality Network across the state, model and observable layers.</p>
<ul class="stats" id="stats"></ul>
</header>

<section aria-labelledby="h-claims">
<h2 id="h-claims">Claims</h2>
<div class="claims" id="claims"></div>
</section>

<section aria-labelledby="h-graph">
<h2 id="h-graph">Three layers</h2>
<div class="tools"><button class="filter" id="showall" aria-pressed="false">Draw all routes</button><span class="legend" id="legend"></span></div>
<div class="board">
  <div class="cols" id="cols">
    <svg class="edges" id="edges" role="img" aria-label="Routes of the current selection drawn between the nodes of the three layers"></svg>
    <div class="col" data-layer="S"><h3>State layer</h3><p class="sub">what is prepared</p></div>
    <div class="col" data-layer="M"><h3>Model layer</h3><p class="sub">what assigns probabilities</p></div>
    <div class="col" data-layer="O"><h3>Observable layer</h3><p class="sub">what is recorded or decided</p></div>
  </div>
  <aside class="rail" id="rail" aria-live="polite"></aside>
</div>
</section>

<section aria-labelledby="h-routes">
<h2 id="h-routes">Routes</h2>
<div class="tools" id="filters"></div>
<div class="tablewrap"><table><thead><tr><th>Route</th><th>From</th><th>To</th><th>Relation</th><th>Grade</th><th>Statement</th></tr></thead><tbody id="rows"></tbody></table></div>
</section>

<section aria-labelledby="h-ctl">
<h2 id="h-ctl">Planted errors</h2>
<p class="lede" style="font-size:14.5px">Each control changes one accepted statement. The matching check has to reject it.</p>
<ul class="ctl" id="ctl"></ul>
</section>

<footer>
<p>Grades. Exact: an identity or equivalence checked in exact arithmetic. Logic: the negation is shown unsatisfiable by an SMT solver. Numeric: a floating-point computation with a stated tolerance, or a recorded long run. Written: a proof given in the paper that no program has checked. Import: cited from the literature. A claim is as strong as the weakest route it uses.</p>
<p>Released graphs: <a href="https://github.com/tahmeedhossain/GEN_HEP">GEN_HEP</a> (commit 4258f6e) and <a href="https://github.com/tahmeedhossain/GEN_GPT_Level">GEN_GPT_Level</a> (commit e18fa8c). Nodes marked “This work” are new. Section numbers refer to the paper “Particle decays as fixed measurements”.</p>
</footer>
</div>

<script id="data" type="application/json">__DATA__</script>
<script>
(function(){
var D = JSON.parse(document.getElementById('data').textContent);
var N = {}, R = {}, C = {};
D.nodes.forEach(function(n){N[n.id]=n}); D.routes.forEach(function(r){R[r.id]=r}); D.claims.forEach(function(c){C[c.id]=c});
var state = {type:'claim', id:'C4', all:false, grade:'all'};
var $ = function(id){return document.getElementById(id)};
function el(tag, cls, text){var e=document.createElement(tag); if(cls) e.className=cls; if(text!==undefined) e.textContent=text; return e}
function pill(grade){var p=el('span','pill g-'+grade); p.appendChild(el('i')); p.appendChild(document.createTextNode(grade)); return p}

// header numbers
var s = D.summary;
[[s.routes,'routes'],[s.checked,'checked by certificate'],[s.written,'proofs written in the paper'],[s.imported,'cited'],[s.definitions,'definitions'],
 [s.rejected+' of '+s.controls,'planted errors rejected'],[s.nodes,'nodes, '+s.released+' from released graphs']].forEach(function(x){
  var li=el('li'); var b=el('b',null,String(x[0])); li.appendChild(b); li.appendChild(document.createTextNode(' '+x[1])); $('stats').appendChild(li)});

// claims
D.claims.forEach(function(c){
  var b=el('button','claim'); b.type='button'; b.dataset.id=c.id; b.appendChild(el('span','cid',c.id)); b.appendChild(el('span',null,c.name));
  b.addEventListener('click',function(){select('claim',c.id)}); $('claims').appendChild(b)});

// nodes
var cols = {}; document.querySelectorAll('.col').forEach(function(c){cols[c.dataset.layer]=c});
D.nodes.forEach(function(n){
  var b=el('button','node'+(n.repo?'':' new')); b.type='button'; b.dataset.id=n.id;
  b.appendChild(el('span','net',n.net)); b.appendChild(el('span','lab',n.label)); b.appendChild(el('span','nid',n.id+' · '+n.type));
  b.addEventListener('click',function(){select('node',n.id)}); cols[n.layer].appendChild(b)});

// legend and filters
['exact','logic','numeric','written','import','definition'].forEach(function(g){$('legend').appendChild(pill(g))});
['all','exact','logic','numeric','written','import','definition'].forEach(function(g){
  var b=el('button','filter',g==='all'?'All grades':g); b.type='button'; b.setAttribute('aria-pressed', g==='all'?'true':'false');
  b.addEventListener('click',function(){state.grade=g; document.querySelectorAll('#filters .filter').forEach(function(x){x.setAttribute('aria-pressed', x===b?'true':'false')}); rows()});
  $('filters').appendChild(b)});

function rows(){
  var tb=$('rows'); tb.textContent='';
  D.routes.forEach(function(r){
    if(state.grade!=='all' && r.grade!==state.grade) return;
    var tr=el('tr'); tr.tabIndex=0; tr.dataset.id=r.id; if(state.type==='route' && state.id===r.id) tr.className='cur';
    tr.appendChild(el('td','id',r.id)); tr.appendChild(el('td','mono',r.inputs.join(', '))); tr.appendChild(el('td','mono',r.target)); tr.appendChild(el('td',null,r.kind));
    var g=el('td'); g.appendChild(pill(r.grade)); tr.appendChild(g); tr.appendChild(el('td',null,r.statement));
    var go=function(){select('route',r.id); $('rail').scrollIntoView({block:'nearest'})};
    tr.addEventListener('click',go); tr.addEventListener('keydown',function(e){if(e.key==='Enter'||e.key===' '){e.preventDefault(); go()}});
    tb.appendChild(tr)})}

// controls
D.controls.forEach(function(c){
  var li=el('li'); var h=el('div'); h.appendChild(el('span','cid',c.id+'  ')); h.appendChild(el('span', c.rejected?'ok':null, c.rejected?'rejected':'not rejected')); li.appendChild(h);
  li.appendChild(el('div',null,c.planted)); li.appendChild(el('div','why',c.detail)); $('ctl').appendChild(li)});

function current(){
  if(state.all) return D.routes.map(function(r){return r.id});
  if(state.type==='claim') return C[state.id].routes.slice();
  if(state.type==='route') return [state.id];
  return D.routes.filter(function(r){return r.target===state.id || r.inputs.indexOf(state.id)>=0}).map(function(r){return r.id})}

function chips(ids){var w=el('div','chips'); ids.forEach(function(id){var b=el('button','chip',id); b.type='button';
  b.addEventListener('click',function(){select(R[id]?'route':(N[id]?'node':'claim'),id)}); w.appendChild(b)}); return w}
function row(dl,k,v){dl.appendChild(el('dt',null,k)); var dd=el('dd'); if(typeof v==='string') dd.textContent=v; else dd.appendChild(v); dl.appendChild(dd)}

function rail(){
  var a=$('rail'); a.textContent='';
  if(state.type==='claim'){
    var c=C[state.id]; a.appendChild(el('div','eyebrow','Claim '+c.id)); a.appendChild(el('h3',null,c.name)); a.appendChild(el('p','stmt',c.text));
    var dl=el('dl'); row(dl,'Verdict',c.verdict);
    if(c.mechanised.length) row(dl,'Exact or logic',chips(c.mechanised));
    if(c.numeric.length) row(dl,'Numeric',chips(c.numeric));
    if(c.written.length) row(dl,'Written proofs',chips(c.written));
    if(c.imports.length) row(dl,'Cited',chips(c.imports));
    a.appendChild(dl)
  } else if(state.type==='node'){
    var n=N[state.id]; a.appendChild(el('div','eyebrow',n.net+(n.repo?' ('+n.repo+')':'')+' · '+{S:'state',M:'model',O:'observable'}[n.layer]+' layer'));
    a.appendChild(el('h3',null,n.label)); a.appendChild(el('p','stmt',n.def));
    var dl2=el('dl'); row(dl2,'Identifier',n.id); row(dl2,'Type',n.type); if(n.glue.length) row(dl2,'Linked to',n.glue.join(', '));
    var into=D.routes.filter(function(r){return r.target===n.id}).map(function(r){return r.id}), out=D.routes.filter(function(r){return r.inputs.indexOf(n.id)>=0}).map(function(r){return r.id});
    if(into.length) row(dl2,'Routes into it',chips(into)); if(out.length) row(dl2,'Routes from it',chips(out)); a.appendChild(dl2)
  } else {
    var r=R[state.id]; a.appendChild(el('div','eyebrow','Route '+r.id+' · '+r.where));
    a.appendChild(el('h3',null,r.inputs.map(function(i){return N[i].label}).join(' + ')+' → '+N[r.target].label));
    a.appendChild(el('p','stmt',r.statement));
    var dl3=el('dl'); row(dl3,'Relation',r.kind); var g=el('span'); g.appendChild(pill(r.grade)); g.appendChild(document.createTextNode('  '+r.status)); row(dl3,'Grade',g);
    row(dl3,'Inputs',chips(r.inputs)); row(dl3,'Target',chips([r.target]));
    if(r.scope!=='general') row(dl3,'Scope',r.scope);
    if(r.certs.length) row(dl3,'Certificate',r.certs.join(', '));
    if(r.refs.length) row(dl3,'References',r.refs.join('; '));
    a.appendChild(dl3);
    if(r.detail){a.appendChild(el('div','eyebrow','Certificate output')).style.marginTop='12px'; a.appendChild(el('div','out',r.detail))}
  }}

var COLOR={exact:'var(--exact)',logic:'var(--logic)',numeric:'var(--numeric)',written:'var(--ink-2)','import':'var(--ink-3)',definition:'var(--ink-3)'};
var DASH={written:'6 4','import':'2 4'};
function draw(){
  var box=$('cols'), svg=$('edges'), ns='http://www.w3.org/2000/svg';
  while(svg.firstChild) svg.removeChild(svg.firstChild);
  var b0=box.getBoundingClientRect(); svg.setAttribute('width',box.scrollWidth); svg.setAttribute('height',box.scrollHeight);
  var defs=document.createElementNS(ns,'defs'); svg.appendChild(defs);
  Object.keys(COLOR).forEach(function(g){
    var m=document.createElementNS(ns,'marker'); m.setAttribute('id','ah-'+g); m.setAttribute('viewBox','0 0 10 10'); m.setAttribute('refX','9'); m.setAttribute('refY','5');
    m.setAttribute('markerWidth','7'); m.setAttribute('markerHeight','7'); m.setAttribute('orient','auto-start-reverse');
    var p=document.createElementNS(ns,'path'); p.setAttribute('d','M0 0L10 5L0 10z'); p.style.fill=COLOR[g]; p.style.stroke='none'; m.appendChild(p); defs.appendChild(m);
    var t=document.createElementNS(ns,'marker'); t.setAttribute('id','bar-'+g); t.setAttribute('viewBox','0 0 4 12'); t.setAttribute('refX','2'); t.setAttribute('refY','6');
    t.setAttribute('markerWidth','4'); t.setAttribute('markerHeight','12'); t.setAttribute('orient','auto');
    var q=document.createElementNS(ns,'path'); q.setAttribute('d','M2 0V12'); q.style.stroke=COLOR[g]; q.style.strokeWidth='2.4'; t.appendChild(q); defs.appendChild(t)});
  var ids=current(), rect={}, used={}, lab={};
  document.querySelectorAll('.node').forEach(function(nd){var r=nd.getBoundingClientRect(); rect[nd.dataset.id]={l:r.left-b0.left,r:r.right-b0.left,t:r.top-b0.top,b:r.bottom-b0.top,cy:(r.top+r.bottom)/2-b0.top}});
  ids.forEach(function(id){
    var rt=R[id], B=rect[rt.target]; if(!B) return;
    rt.inputs.forEach(function(inp){
      var A=rect[inp]; if(!A || inp===rt.target) return;
      var key=inp+'>'+rt.target; used[key]=(used[key]||0)+1; var off=(used[key]-1)*7;
      var x1,y1,x2,y2,d, same=Math.abs(A.l-B.l)<8;
      if(same){x1=A.r; y1=A.cy+off; x2=B.r+3; y2=B.cy+off; var bulge=18+Math.min(10,off); d='M'+x1+' '+y1+' C'+(x1+bulge)+' '+y1+' '+(x2+bulge)+' '+y2+' '+x2+' '+y2}
      else if(A.l<B.l){x1=A.r; y1=A.cy+off; x2=B.l-3; y2=B.cy+off; var k=Math.max(24,(x2-x1)*0.45); d='M'+x1+' '+y1+' C'+(x1+k)+' '+y1+' '+(x2-k)+' '+y2+' '+x2+' '+y2}
      else {x1=A.l; y1=A.cy+off; x2=B.r+3; y2=B.cy+off; var k2=Math.max(24,(x1-x2)*0.45); d='M'+x1+' '+y1+' C'+(x1-k2)+' '+y1+' '+(x2+k2)+' '+y2+' '+x2+' '+y2}
      var p=document.createElementNS(ns,'path'); p.setAttribute('d',d); p.style.stroke=COLOR[rt.grade]; if(DASH[rt.grade]) p.setAttribute('stroke-dasharray',DASH[rt.grade]);
      if(rt.grade==='definition') p.style.strokeWidth='1';
      if(state.all) p.style.opacity='.55';
      var bar=(rt.kind==='forbids'||rt.kind==='not implies'); p.setAttribute('marker-end','url(#'+(bar?'bar-':'ah-')+rt.grade+')'); svg.appendChild(p);
      if(!state.all && !lab[id]){lab[id]=1; var tx=document.createElementNS(ns,'text'); var mx=same?Math.max(x1,x2)+16:(x1+x2)/2, my=(y1+y2)/2-3;
        tx.setAttribute('x',mx); tx.setAttribute('y',my); tx.setAttribute('text-anchor', same?'start':'middle'); tx.textContent=id; svg.appendChild(tx)}
    })})}

function paint(){
  var ids=current(), on={};
  ids.forEach(function(id){on[R[id].target]=1; R[id].inputs.forEach(function(i){on[i]=1})});
  if(state.type==='node') on[state.id]=1;
  document.querySelectorAll('.node').forEach(function(nd){nd.classList.toggle('on',!!on[nd.dataset.id]); nd.classList.toggle('sel',state.type==='node'&&state.id===nd.dataset.id)});
  $('cols').classList.toggle('active',!state.all);
  document.querySelectorAll('.claim').forEach(function(b){b.setAttribute('aria-pressed', state.type==='claim'&&state.id===b.dataset.id&&!state.all?'true':'false')});
  $('showall').setAttribute('aria-pressed', state.all?'true':'false');
  rail(); rows(); draw()}
function select(type,id){state.type=type; state.id=id; state.all=false; paint()}
$('showall').addEventListener('click',function(){state.all=!state.all; paint()});
var tmr; window.addEventListener('resize',function(){clearTimeout(tmr); tmr=setTimeout(draw,80)});
if(document.fonts && document.fonts.ready) document.fonts.ready.then(draw);
paint();
})();
</script>
</body>
</html>
'''
out = TEMPLATE.replace('__DATA__', blob)
open(os.path.join(HERE, 'index.html'), 'w', encoding='utf-8').write(out)
print('index.html: %d bytes; %d nodes, %d routes, %d claims, %d controls' % (len(out.encode('utf-8')), len(nodes), len(routes), len(claims), len(controls)))
