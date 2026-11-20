"""GEN edge kernel (version used for the decay-polarimetry delta).

A result is encoded as nodes (layer S/M/O, sub-layer, definition; released nodes keep their ids) and routes
(inputs, target, statement, place in the paper).  Every route carries a grade, a scope and, where possible, a certificate.

Grades
  exact       symbolic or exact-arithmetic computation (SymPy; own exact arithmetic)
  logic       SMT entailment (Z3), each premise dropped in turn where stated
  numeric     floating-point optimisation or quadrature with a stated tolerance (LP, SDP)
  import      cited result or measured number, checked bibliographically only
  definition  definition
  compose     proof step written in words in the paper, not mechanised
  interpretive  reading, not a mathematical statement

Verdict of a headline claim, by precedence
  discrepancy  >  not decidable by the kernel  >  numerical support only  >
  verified modulo imports and written proof steps  >  verified modulo imports  >  verified on instances  >  verified
"""
import time, traceback
LAYERS = ('S', 'M', 'O')
GRADES = ('exact', 'logic', 'numeric', 'import', 'definition', 'compose', 'interpretive')

def run_routes(routes, verbose=True):
    results = {}
    for r in routes:
        res = {'grade': r['grade'], 'status': 'not run'}
        certs = r.get('certs', [])
        if not certs:
            res['status'] = {'import': 'imported', 'definition': 'definition', 'compose': 'written proof step',
                             'interpretive': 'interpretive'}.get(r['grade'], 'no certificate')
            res['ok'] = None
        else:
            oks = []; details = []; t0 = time.time()
            for c in certs:
                try:
                    out = c()
                    oks.append(bool(out['ok'])); details.append(out['detail'])
                except Exception as e:
                    oks.append(False); details.append('EXCEPTION ' + repr(e)[:200] + ' ' + traceback.format_exc(limit=1)[-200:])
            res['ok'] = all(oks); res['status'] = 'checked' if all(oks) else 'FAILED'
            res['detail'] = ' || '.join(details); res['seconds'] = round(time.time() - t0, 2)
        results[r['id']] = res
        if verbose:
            print('%-5s %-10s %-20s %s' % (r['id'], r['grade'], res['status'], (res.get('detail', '') or '')[:110]), flush=True)
    return results

def lint(nodes, routes):
    ids = {n['id'] for n in nodes}; layer = {n['id']: n['layer'] for n in nodes}; sub = {n['id']: n.get('sub', '') for n in nodes}
    issues = []
    sig = {a + b: 0 for a in LAYERS for b in LAYERS}
    for r in routes:
        for x in r['inputs'] + [r['target']]:
            if x not in ids: issues.append('route %s uses unknown node %s' % (r['id'], x))
        if r['grade'] not in GRADES: issues.append('route %s has unknown grade' % r['id'])
        if r['target'] in ids:
            for x in r['inputs']:
                if x in ids: sig[layer[x] + layer[r['target']]] += 1
    # observables without a model route; effects without a witness
    into = {}
    for r in routes: into.setdefault(r['target'], []).append(r)
    for n in nodes:
        if n['layer'] == 'O' and n.get('sub') == 'direct' and not n.get('released'):
            if not any(layer.get(x) == 'M' for r in into.get(n['id'], []) for x in r['inputs']):
                issues.append('direct observable %s has no route from the model layer' % n['id'])
        if n['layer'] == 'O' and n.get('sub') == 'effect' and not n.get('released'):
            if not any(sub.get(x) == 'witness' for r in into.get(n['id'], []) for x in r['inputs']):
                issues.append('effect %s has no witness route' % n['id'])
    used = {x for r in routes for x in r['inputs'] + [r['target']]}
    for n in nodes:
        if n['id'] not in used: issues.append('node %s is not used by any route' % n['id'])
    return {'issues': issues, 'signature': sig}

def close_claims(claims, routes, results):
    by = {r['id']: r for r in routes}
    out = {}
    for c in claims:
        rs = [by[i] for i in c['routes']]
        failed = [r['id'] for r in rs if results[r['id']]['ok'] is False]
        g = lambda name: [r['id'] for r in rs if r['grade'] == name]
        inst = [r['id'] for r in rs if str(r.get('scope', 'general')).startswith('instance')]
        mech = [r['id'] for r in rs if r['grade'] in ('exact', 'logic')]
        if failed: verdict = 'discrepancy'
        elif g('interpretive') and c.get('needs_interpretive'): verdict = 'not decidable by the kernel'
        elif not mech and not g('compose') and g('numeric'): verdict = 'numerical support only'
        elif g('compose'): verdict = 'verified modulo imports and written proof steps' if g('import') else 'verified modulo written proof steps'
        elif g('import'): verdict = 'verified modulo imports'
        elif inst: verdict = 'verified on instances'
        else: verdict = 'verified'
        out[c['id']] = {'verdict': verdict, 'failed': failed, 'imports': g('import'), 'written_steps': g('compose'),
                        'numeric_crosschecks': g('numeric'), 'instance_scoped': inst, 'mechanised': mech}
    return out

def scope_separation(nogo, possibility, missing_premise, violates_route_ok):
    """A no-go route and a possibility route are accepted together only if a premise of the no-go is absent from the
    possibility route and a checked route shows that the model lacks it."""
    return (missing_premise in nogo['premises']) and (missing_premise not in possibility['premises']) and bool(violates_route_ok)

