"""Writes numbers.tex (macros) and the route / claim / control tables of the paper from out/results.json,
the recorded long runs and the certificate functions. Nothing in the paper's tables is typed by hand."""
import sys, os, json, re
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, 'net')); sys.path.insert(0, os.path.join(ROOT, 'lib'))
import numpy as np
import certs_numeric as cn, certs_extra as cx

d = json.load(open(os.path.join(ROOT, 'out', 'results.json')))
S = d['summary']; res = d['results']
rd = lambda f: json.load(open(os.path.join(ROOT, 'out', f)))
lpR, lpR2, ref, tq = rd('lp_R.json'), rd('lp_R2.json'), rd('lp_refine.json'), rd('two_qubit_sandwich.json')

top = cn.cert_top_powers(); lam = cn.cert_lambda_pairs(); tp = cn.cert_top_pair_numbers(); gj = cn.cert_general_j()
cur = [v for k, v in top['values'].items() if k.startswith('%.2f' % cn.INPUTS['m_t'][0])][0]
bsu = [v for k, v in top['values'].items() if k.startswith('175.00')][0]
mt, smt = cn.INPUTS['m_t'][:2]; mW, smW = cn.INPUTS['m_W'][:2]
def knu(m, w):
    xi = (m / w) ** 2
    return ((xi - 1) * (xi ** 2 - 11 * xi - 2) + 12 * xi * np.log(xi)) / ((xi + 2) * (xi - 1) ** 2)
dknu = abs(knu(mt + smt, mW) - knu(mt - smt, mW)) / 2
ratR = [r['lp'] / r['closed'] for r in lpR['rows']]; ratR2 = [r['lp'] / r['closed'] for r in lpR2['rows']]
fin = [r for r in tq['rows'] if r['N'] == max(x['N'] for x in tq['rows'])]

M = {}
def put(name, val): M[name] = val
put('nRoutes', S['routes']); put('nChecked', S['checked']); put('nFailed', S['failed'])
put('nExact', S['checked_by_grade']['exact']); put('nLogic', S['checked_by_grade']['logic']); put('nNumeric', S['checked_by_grade']['numeric'])
put('nImportChecked', S['checked_by_grade']['import']); put('nImported', S['status'].get('imported', 0))
put('nDefinitions', S['status'].get('definition', 0)); put('nWritten', S['status'].get('written proof step', 0))
put('nNodes', S['nodes']); put('nReleased', S['nodes_released']); put('nNew', S['nodes_new'])
put('nS', S['nodes_by_layer']['S']); put('nM', S['nodes_by_layer']['M']); put('nO', S['nodes_by_layer']['O'])
put('nControls', S['controls']); put('nControlsRejected', S['controls_rejected']); put('nClaims', len(d['claims']))
put('runSeconds', '%.0f' % S['seconds'])
put('verPython', S['python']); put('verSympy', S['sympy']); put('verNumpy', S['numpy']); put('verScipy', S['scipy']); put('verCvxpy', S['cvxpy']); put('verZthree', S['z3'])
put('mtop', '%.2f' % mt); put('mtopErr', '%.2f' % smt); put('mW', '%.4f' % mW); put('mWErr', '%.4f' % smW)
put('kappab', '%.3f' % abs(cur['kappa_b'])); put('kappanu', '%.3f' % abs(cur['kappa_nu'])); put('kappanuErr', '%.3f' % dknu)
put('kappabBSU', '%.3f' % abs(bsu['kappa_b'])); put('kappanuBSU', '%.3f' % abs(bsu['kappa_nu']))
put('xistar', '%.3f' % top['xi_star']); put('mtstar', '%.1f' % top['mt_star']); put('mtstarFine', '%.2f' % top['mt_star'])
put('mtstarPull', '%.1f' % ((top['mt_star'] - mt) / smt))
put('twomW', '%.1f' % (2 * mW))
put('cnorm', '%.3f' % lam['nuc90']); put('cnormAvg', '%.3f' % lam['nuc90_avg']); put('cnormErr', '%.3f' % lam['sigma'])
put('cosc', '%.3f' % lam['cos_c']); put('coscLo', '%.3f' % min(lam['edges'])); put('coscHi', '%.3f' % max(lam['edges'])); put('fracEvents', '%.1f' % (100 * lam['frac']))
a_m, a_p = cn.INPUTS['alpha_minus'][0], cn.INPUTS['alpha_plus'][0]
put('alphaprod', '%.3f' % abs(a_m * a_p)); put('alphapsi', '%.4f' % cn.INPUTS['alpha_psi'][0]); put('dphi', '%.4f' % cn.INPUTS['DeltaPhi'][0])
put('alpham', '%.4f' % a_m); put('alphap', '%.4f' % a_p)
al = cn.INPUTS['alpha_psi'][0]; put('wzeroLambda', '%.3f' % ((1 - al) / (3 + al)))
put('zATLAS', '%.1f' % tp['z_atlas']); put('zCMS', '%.1f' % tp['z_cms'])
put('lpRlo', '%.4f' % min(ratR)); put('lpRhi', '%.4f' % max(ratR)); put('lpRtwolo', '%.4f' % min(ratR2)); put('lpRtwohi', '%.4f' % max(ratR2))
put('lpRdirs', len(ratR)); put('lpRtwodirs', len(ratR2)); put('lpRK', lpR['K']); put('lpRnq', lpR['nq'])
put('lpRtwoK', lpR2['K']); put('lpRtwonq', lpR2['nq'])
rr = ref['rows']
for nm, i in (('refA', 0), ('refB', 1), ('refC', 2), ('refD', 3), ('refE', 4), ('refF', 5)): put(nm, '%.4f' % (rr[i]['lp'] / rr[i]['closed']))
put('refAnq', rr[0]['nq']); put('refBnq', rr[1]['nq']); put('refCnq', rr[2]['nq']); put('refDnq', rr[3]['nq'])
put('bracketN', fin[0]['N']); put('bracketWidth', '%.3f' % max(r['outer'] - r['inner'] for r in fin))
put('sdpDev', re.search(r'pure states: ([0-9.e+-]+)', cn.cert_support_sdp()['detail']).group(1))
put('gjDev', re.search(r'max dev ([0-9.e+-]+)', gj['detail']).group(1))
put('etaStarMin', '%.3f' % min(min(abs(v) for v in r['m']) for r in gj['rows']))
put('taurho', re.search(r'= ([0-9.]+) for', cx.cert_tau_rho()['detail']).group(1))
put('Ae', '%.4f' % cn.INPUTS['A_e'][0]); put('AeErr', '%.4f' % cn.INPUTS['A_e'][1])
vp = cn.cert_vector_pair_kernels()
put('wzeroSigma', '%.3f' % vp['w0_S']); put('wzeroSigmaErr', '%.3f' % vp['sw0_S']); put('zSigma', '%.1f' % vp['z_S']); put('zLambdaKernel', '%.0f' % vp['z_L'])
put('alphaSigma', '%.3f' % cn.INPUTS['alpha_psi_Sigma'][0]); put('alphaSigmaErr', '%.3f' % cn.INPUTS['alpha_psi_Sigma'][1])
put('xtau', '%.3f' % vp['x_tau']); put('alphatau', '%.3f' % vp['alpha_tau'])
put('cnormSigma', '%.2f' % vp['nuc90_Sigma']); put('cnormSigmaErr', '%.2f' % vp['snuc90_Sigma'])
put('cnormSigma', '%.2f' % vp['nuc90_Sigma']); put('zcnorm', '%.0f' % ((lam['nuc90_avg'] - 1) / lam['sigma']))
put('kbsq', '%.3f' % (cur['kappa_b'] ** 2)); put('Cneed', '%.2f' % (1 / abs(cur['kappa_b'])))
put('alphapsiErr', '%.4f' % cn.INPUTS['alpha_psi'][1]); put('dphiErr', '%.4f' % cn.INPUTS['DeltaPhi'][1]); put('alphamErr', '%.4f' % cn.INPUTS['alpha_minus'][1]); put('alphapErr', '%.4f' % cn.INPUTS['alpha_plus'][1])
put('DATLAS', '%.3f' % cn.INPUTS['D_ATLAS'][0]); put('DATLASbound', '%.3f' % cn.INPUTS['D_ATLAS_bound'][0]); put('DCMS', '%.3f' % cn.INPUTS['D_CMS'][0])
put('trcCMS', '%.2f' % (3 * abs(cn.INPUTS['D_CMS'][0])))

def sci(x):
    m = re.match(r'^([0-9.]+)e([+-]?)0*([0-9]+)$', str(x))
    return ('%s\\times 10^{%s%s}' % (m.group(1), '-' if m.group(2) == '-' else '', m.group(3))) if m else str(x)
lines = ['%% generated by make_numbers.py from out/results.json; do not edit']
for k, v in M.items():
    v = sci(v) if re.match(r'^[0-9.]+e[+-]?[0-9]+$', str(v)) else str(v)
    lines.append('\\newcommand{\\%s}{%s}' % (k, v))
open(os.path.join(HERE, 'numbers.tex'), 'w').write('\n'.join(lines) + '\n')

# ---------------------------------------------------------------- tables
def esc(s):
    return (s.replace('\\', '\\textbackslash{}').replace('&', '\\&').replace('%', '\\%').replace('#', '\\#').replace('_', '\\_')
             .replace('^', '\\^{}').replace('~', '\\~{}').replace('<', '$<$').replace('>', '$>$').replace('|', '$|$'))
layer = {n['id']: n['layer'] for n in d['nodes']}
tt = lambda s: '\\texttt{%s}' % esc(s)
gname = {'exact': 'exact', 'logic': 'logic', 'numeric': 'numeric', 'import': 'import', 'definition': 'definition', 'compose': 'written'}
def status(r):
    x = res[r['id']]
    if x['status'] == 'checked': return 'checked'
    return {'written proof step': 'proof in text', 'imported': 'cited', 'definition': '--'}[x['status']]
def cert_names(r):
    c = r['certs'] if isinstance(r['certs'], list) else []
    c = [x for x in c if x]
    return ', '.join(tt(x.replace('cert_', '').replace('<lambda>', 'lp_region')) for x in c) if c else '--'
rows = []
for r in d['routes']:
    ins = r['inputs'] if isinstance(r['inputs'], list) else []
    sig = ''.join(sorted(set(layer[i] for i in ins))) + '$\\to$' + layer[r['target']]
    rows.append('%s & %s & %s & %s & %s & %s & %s \\\\' % (r['id'], ', '.join(tt(i) for i in ins), tt(r['target']), sig, esc(r['kind'].replace('_', ' ')), gname[r['grade']] + (' / ' + status(r) if status(r) != '--' else ''), cert_names(r)))
half = (len(rows) + 1) // 2
head = ('\\begin{ruledtabular}\n\\begin{tabular}{lllllll}\nRoute & Inputs & Target & Layers & Relation & Grade / status & Certificate \\\\\n\\hline\n')
open(os.path.join(HERE, 'routes_table_a.tex'), 'w').write(head + '\n'.join(rows[:half]) + '\n\\end{tabular}\n\\end{ruledtabular}\n')
open(os.path.join(HERE, 'routes_table_b.tex'), 'w').write(head + '\n'.join(rows[half:]) + '\n\\end{tabular}\n\\end{ruledtabular}\n')

cl = []
short = {'verified': 'verified', 'verified modulo imports': 'verified modulo imports', 'verified modulo written proof steps': 'verified modulo written proofs',
         'verified modulo imports and written proof steps': 'verified modulo imports and written proofs'}
for c in d['claims']:
    cl.append('%s & %s & %s \\\\' % (c['id'], ', '.join(c['routes']), short.get(c['verdict'], c['verdict'])))
open(os.path.join(HERE, 'claims_table.tex'), 'w').write('\\begin{ruledtabular}\n\\begin{tabular}{lp{0.50\\columnwidth}p{0.30\\columnwidth}}\nClaim & Routes & Verdict \\\\\n\\hline\n' + '\n'.join(cl) + '\n\\end{tabular}\n\\end{ruledtabular}\n')

nd = []
for n in d['nodes']:
    nd.append('%s & %s & %s & %s \\\\' % (tt(n['id']), n['layer'], esc(n['label']), esc(n['released']) if n['released'] else 'new'))
open(os.path.join(HERE, 'nodes_table.tex'), 'w').write('\\begin{ruledtabular}\n\\begin{tabular}{llll}\nNode & Layer & Label & Source \\\\\n\\hline\n' + '\n'.join(nd) + '\n\\end{tabular}\n\\end{ruledtabular}\n')
h2 = (len(nd) + 1) // 2
nh = '\\begin{ruledtabular}\n\\begin{tabular}{llll}\nNode & Layer & Label & Source \\\\\n\\hline\n'
open(os.path.join(HERE, 'nodes_table_a.tex'), 'w').write(nh + '\n'.join(nd[:h2]) + '\n\\end{tabular}\n\\end{ruledtabular}\n')
open(os.path.join(HERE, 'nodes_table_b.tex'), 'w').write(nh + '\n'.join(nd[h2:]) + '\n\\end{tabular}\n\\end{ruledtabular}\n')

# general-j table
gr = []
for r in gj['rows']:
    j = r['j']; js = ('%d' % j) if abs(j - round(j)) < 1e-9 else ('%d/2' % round(2 * j))
    rule = 'Gauss--Legendre, %d nodes' % (round(j) + 1) if abs(j - round(j)) < 1e-9 else 'Gauss--Radau, %d nodes' % (round(j + 0.5) + 1)
    gr.append('$%s$ & %s & %.6f & %.6f \\\\' % (js, rule, r['xi'], r['lp']))
open(os.path.join(HERE, 'gj_table.tex'), 'w').write('\\begin{ruledtabular}\n\\begin{tabular}{llll}\n$j$ & Quadrature rule & $\\xi_{2j}$ & LP value \\\\\n\\hline\n' + '\n'.join(gr) + '\n\\end{tabular}\n\\end{ruledtabular}\n')
print('numbers.tex: %d macros; %d routes, %d claims, %d nodes' % (len(M), len(rows), len(cl), len(nd)))
print({k: M[k] for k in ['kappab', 'kappanu', 'kappanuErr', 'mtstar', 'mtstarPull', 'cnorm', 'cosc', 'fracEvents', 'zATLAS', 'zCMS', 'lpRlo', 'lpRhi', 'lpRtwolo', 'lpRtwohi', 'refA', 'refB', 'refC', 'refD', 'refE', 'refF', 'bracketWidth', 'sdpDev', 'gjDev', 'etaStarMin', 'taurho', 'alphaprod', 'wzeroLambda', 'kappabBSU', 'kappanuBSU']})
