"""Run the edge kernel on the decay-polarimetry delta: lint, certificates, claims, negative controls.
Writes out/results.json and out/summary.txt.   Usage: python3 run_all.py"""
import sys, os, json, time, platform
ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, 'net')); sys.path.insert(0, os.path.join(ROOT, 'lib'))
import kernel, encoding as en, controls

t0 = time.time()
lint = kernel.lint(en.NODES, en.ROUTES)
print('lint issues:', lint['issues'] or 'none'); print('layer-pair signature:', lint['signature'])
results = kernel.run_routes(en.ROUTES)
claims = kernel.close_claims(en.CLAIMS, en.ROUTES, results)
print('\nclaims')
for c in en.CLAIMS:
    v = claims[c['id']]; print(' %-4s %-48s %s' % (c['id'], v['verdict'], c['text'][:90]))
print('\nnegative controls')
ctrl = []
for k in controls.CONTROLS:
    try: r = k()
    except Exception as e: r = {'rejected': False, 'detail': 'EXCEPTION ' + repr(e)[:200]}
    ctrl.append({'id': k.__name__, 'planted': (k.__doc__ or '').strip(), 'rejected': bool(r['rejected']), 'detail': r['detail']})
    print(' %-4s %-12s %s' % (k.__name__, 'rejected' if r['rejected'] else 'NOT REJECTED', ctrl[-1]['planted'][:90]))
# scope separation: no-go (single setting forbids Bell tests) versus possibility (contextuality with a single setting)
sep = kernel.scope_separation({'premises': ['one setting per side', 'outcome determinism allowed', 'no operational-equivalence constraint']},
                              {'premises': ['one setting per side', 'operational equivalences respected']},
                              'no operational-equivalence constraint', results['FW5']['ok'])
from collections import Counter
grades = Counter(r['grade'] for r in en.ROUTES)
status = Counter(results[r['id']]['status'] for r in en.ROUTES)
import sympy, numpy, scipy, cvxpy, z3
summary = {
 'python': platform.python_version(), 'sympy': sympy.__version__, 'numpy': numpy.__version__, 'scipy': scipy.__version__,
 'cvxpy': cvxpy.__version__, 'z3': z3.get_version_string(),
 'nodes': len(en.NODES), 'nodes_released': sum(1 for n in en.NODES if n['released']), 'nodes_new': sum(1 for n in en.NODES if not n['released']),
 'nodes_by_layer': dict(Counter(n['layer'] for n in en.NODES)),
 'routes': len(en.ROUTES), 'grades': dict(grades), 'status': dict(status),
 'checked': sum(1 for r in en.ROUTES if results[r['id']]['ok'] is True), 'checked_by_grade': {g: sum(1 for r in en.ROUTES if r['grade'] == g and results[r['id']]['ok'] is True) for g in ('exact', 'logic', 'numeric', 'import')}, 'failed': sum(1 for r in en.ROUTES if results[r['id']]['ok'] is False),
 'claims': {c['id']: claims[c['id']]['verdict'] for c in en.CLAIMS}, 'verdict_counts': dict(Counter(v['verdict'] for v in claims.values())),
 'controls': len(ctrl), 'controls_rejected': sum(1 for c in ctrl if c['rejected']),
 'scope_separation_single_setting': bool(sep), 'lint_issues': lint['issues'], 'signature': lint['signature'],
 'seconds': round(time.time() - t0, 1)}
def clean(o):
    if isinstance(o, dict): return {str(k): clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [clean(v) for v in o]
    if hasattr(o, 'item'):
        try: return o.item()
        except Exception: return str(o)
    if callable(o): return getattr(o, '__name__', 'certificate')
    return o
out = {'summary': summary,
       'nodes': en.NODES,
       'routes': [{k: (v if k != 'certs' else [getattr(c, '__name__', 'recorded-run') for c in v]) for k, v in r.items()} for r in en.ROUTES],
       'results': results, 'claims': [{**c, **claims[c['id']]} for c in en.CLAIMS], 'controls': ctrl,
       'inputs': {k: {'value': v[0], 'sigma': v[1], 'source': v[2]} for k, v in __import__('certs_numeric').INPUTS.items()}}
json.dump(clean(out), open(os.path.join(ROOT, 'out', 'results.json'), 'w'), indent=1)
lines = ['%d routes: %d checked (%s), %d failed; %d imported, %d definitions, %d written proof steps'
         % (summary['routes'], summary['checked'], ', '.join('%d %s' % (sum(1 for r in en.ROUTES if r['grade'] == g and results[r['id']]['ok'] is True), lab) for g, lab in (('exact', 'exact'), ('logic', 'logic'), ('numeric', 'numeric'), ('import', 'import with a consistency check'))),
            summary['failed'], status.get('imported', 0), status.get('definition', 0), status.get('written proof step', 0)),
         '%d nodes (%d released, %d new); layers %s' % (summary['nodes'], summary['nodes_released'], summary['nodes_new'], summary['nodes_by_layer']),
         'claims: ' + '; '.join('%s: %s' % kv for kv in summary['claims'].items()),
         'negative controls rejected: %d of %d' % (summary['controls_rejected'], summary['controls']),
         'scope separation (single setting: no Bell test, yet contextuality testable): %s' % sep,
         'lint: %s' % (lint['issues'] or 'no issues'), 'run time %.0f s' % summary['seconds']]
open(os.path.join(ROOT, 'out', 'summary.txt'), 'w').write('\n'.join(lines) + '\n')
print('\n' + '\n'.join(lines))

