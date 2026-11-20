"""Numerical certificates (floating point; each states its tolerance) and readers of recorded long runs."""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, 'lib'))
import numpy as np
from spinlib import *
from regions import h_R, h_R2, radial_R, radial_R2

# ---------------------------------------------------------------- inputs quoted from the literature (imports)
INPUTS = {
    'm_t': (172.60, 0.27, 'PDG 2026 summary table, direct measurements (S = 1.5)'),
    'm_W': (80.3625, 0.0077, 'PDG 2026 summary table (does not include the CDF 2022 measurement)'),
    'A_e': (0.1515, 0.0019, 'PDG 2026 summary table, Z asymmetry parameter'),
    'alpha_psi_Sigma': (-0.508, (0.006 ** 2 + 0.004 ** 2) ** 0.5, 'BESIII PRL 125, 052004; J/psi -> Sigma+ anti-Sigma-'),
    'm_tau': (1776.93, 0.09, 'PDG 2024'),
    'alpha0_Sigma': (-0.998, (0.037 ** 2 + 0.009 ** 2) ** 0.5, 'BESIII PRL 125, 052004; Sigma+ -> p pi0'),
    'alpha0bar_Sigma': (0.990, (0.037 ** 2 + 0.011 ** 2) ** 0.5, 'BESIII PRL 125, 052004; anti-Sigma- -> pbar pi0'),
    'm_psi2S': (3686.10, 0.06, 'PDG 2024 (rounded)'),
    'alpha_psi': (0.4748, (0.0022 ** 2 + 0.0031 ** 2) ** 0.5, 'BESIII PRL 129, 131801'),
    'DeltaPhi': (0.7521, (0.0042 ** 2 + 0.0066 ** 2) ** 0.5, 'BESIII PRL 129, 131801'),
    'alpha_minus': (0.7519, (0.0036 ** 2 + 0.0024 ** 2) ** 0.5, 'BESIII PRL 129, 131801'),
    'alpha_plus': (-0.7559, (0.0036 ** 2 + 0.0030 ** 2) ** 0.5, 'BESIII PRL 129, 131801'),
    'alpha_avg': (0.7542, (0.0010 ** 2 + 0.0024 ** 2) ** 0.5, 'BESIII PRL 129, 131801'),
    'D_ATLAS': (-0.537, (0.002 ** 2 + 0.019 ** 2) ** 0.5, 'ATLAS Nature 633, 542; particle level, 340 < m_tt < 380 GeV'),
    'D_ATLAS_bound': (-0.322, 0.009, 'ATLAS: separability bound folded to particle level (Powheg+Pythia)'),
    'D_CMS': (-0.480, 0.029, 'CMS Rep. Prog. Phys. 87, 117801; parton level; upper uncertainty'),
}

def cert_top_powers():
    """Leading-order analysing powers of t -> b l+ nu (narrow W, m_b = 0) by direct integration of
    |M|^2 ~ (p_b.p_nu)((p_t - m s).p_l) over the decay angles, against the closed forms
       kappa_l = 1,  kappa_b = -(xi-2)/(xi+2),
       kappa_nu = [(xi-1)(xi^2-11 xi-2) + 12 xi ln xi] / [(xi+2)(xi-1)^2],  xi = m_t^2/m_W^2."""
    def kappas(mt, mW, n=64):
        x, w = np.polynomial.legendre.leggauss(n)
        cb, wb = x, w                                             # cos(theta_b) w.r.t. spin axis z
        cs, ws = x, w                                             # cos(theta*) of lepton in W frame
        ph = (np.arange(2 * n) + 0.5) * np.pi / n; wph = np.full(2 * n, np.pi / n)
        CB, CS, PH = np.meshgrid(cb, cs, ph, indexing='ij')
        Wt = wb[:, None, None] * ws[None, :, None] * wph[None, None, :]
        Eb = (mt ** 2 - mW ** 2) / (2 * mt); EW = mt - Eb; pW = Eb
        sb = np.sqrt(1 - CB ** 2)
        bhat = np.stack([sb, 0 * sb, CB], -1)                     # b direction (phi_b = 0)
        what = -bhat
        # orthonormal frame around what
        e1 = np.stack([CB, 0 * CB, -sb], -1); e2 = np.stack([0 * CB, np.ones_like(CB), 0 * CB], -1)
        ss = np.sqrt(1 - CS ** 2)
        lstar = (ss * np.cos(PH))[..., None] * e1 + (ss * np.sin(PH))[..., None] * e2 + CS[..., None] * what
        g = EW / mW; bg = pW / mW
        def boost(En, pvec):                                      # from W frame to top frame along what
            ppar = np.sum(pvec * what, -1)
            E2 = g * En + bg * ppar
            p2 = pvec + ((g - 1) * ppar + bg * En)[..., None] * what
            return E2, p2
        El, pl = boost(mW / 2, (mW / 2) * lstar); En, pn = boost(mW / 2, -(mW / 2) * lstar)
        pb = Eb * bhat
        b_nu = Eb * En - np.sum(pb * pn, -1)
        base = b_nu * mt * El                                     # unpolarised part: (p_b.p_nu)(p_t.p_l)
        lz = pl[..., 2] / El; nz = pn[..., 2] / En
        spin = b_nu * mt * El * lz                                # coefficient of the polarisation along z
        tot = np.sum(Wt * base)
        # <cos theta_f> = kappa_f/3 for a fully polarised top: weight = base + spin
        k_l = 3 * np.sum(Wt * (base + spin) * lz) / tot
        k_b = 3 * np.sum(Wt * (base + spin) * CB) / tot
        k_n = 3 * np.sum(Wt * (base + spin) * nz) / tot
        return k_l, k_b, k_n
    def kb_closed(xi): return -(xi - 2) / (xi + 2)
    def kn_closed(xi): return ((xi - 1) * (xi ** 2 - 11 * xi - 2) + 12 * xi * np.log(xi)) / ((xi + 2) * (xi - 1) ** 2)
    out = {}; ok = True
    for mt, mW in ((175.0, 80.41), (INPUTS['m_t'][0], INPUTS['m_W'][0])):
        xi = (mt / mW) ** 2; kl, kb, kn = kappas(mt, mW)
        ok = ok and abs(kl - 1) < 1e-6 and abs(kb - kb_closed(xi)) < 1e-6 and abs(kn - kn_closed(xi)) < 1e-5
        out['%.2f/%.4f' % (mt, mW)] = {'xi': xi, 'kappa_l': kl, 'kappa_b': kb, 'kappa_nu': kn,
                                       'kappa_b_closed': kb_closed(xi), 'kappa_nu_closed': kn_closed(xi)}
    # literature cross-check (Brandenburg, Si, Uwer: m_t = 175, m_W = 80.41, m_b = 0, narrow width): -0.40622, -0.31817
    r = out['175.00/80.4100']
    ok = ok and abs(r['kappa_b'] + 0.40622) < 2e-5 and abs(r['kappa_nu'] + 0.31817) < 2e-5
    # root of |kappa_nu| = 1/3
    from scipy.optimize import brentq
    xi_star = brentq(lambda x: kn_closed(x) + 1 / 3, 4.2, 5.0)
    mt_star = INPUTS['m_W'][0] * np.sqrt(xi_star)
    cur = out['%.2f/%.4f' % (INPUTS['m_t'][0], INPUTS['m_W'][0])]
    dkn = (kn_closed((INPUTS['m_t'][0] + INPUTS['m_t'][1]) ** 2 / INPUTS['m_W'][0] ** 2) - cur['kappa_nu_closed'])
    return {'ok': bool(ok), 'detail': 'quadrature reproduces kappa_l=1, kappa_b, kappa_nu closed forms and the published LO values '
            '(-0.40622, -0.31817); at PDG 2026 masses kappa_b = %.4f, kappa_nu = %.4f (+-%.4f from m_t); |kappa_nu| = 1/3 at xi = %.4f '
            '(m_t = %.2f GeV for the PDG 2026 m_W)' % (cur['kappa_b'], cur['kappa_nu'], abs(dkn), xi_star, mt_star),
            'values': out, 'xi_star': xi_star, 'mt_star': mt_star}

# ---------------------------------------------------------------- Lambda pairs
_P = [np.eye(2, dtype=complex), np.array([[0, 1], [1, 0]], complex), np.array([[0, -1j], [1j, 0]]), np.diag([1, -1]).astype(complex)]
def _rho_from_R(R): return sum(R[m, n] * np.kron(_P[m], _P[n]) for m in range(4) for n in range(4)) / 4
def _pt(rho): return rho.reshape(2, 2, 2, 2).transpose(2, 1, 0, 3).reshape(4, 4)

def lambda_R(theta, al, dphi):
    """Bloch/correlation matrix of the Lambda anti-Lambda pair from e+e- -> J/psi (Faldt-Kupsc structure functions):
    axes z = Lambda direction, y = normal to the production plane, x in the plane."""
    s, c = np.sin(theta), np.cos(theta); be = np.sqrt(1 - al ** 2)
    N = 1 + al * c * c
    R = np.zeros((4, 4)); R[0, 0] = 1
    Py = be * s * c * np.sin(dphi) / N
    R[2, 0] = Py; R[0, 2] = Py
    R[1, 1] = s * s / N; R[2, 2] = -al * s * s / N; R[3, 3] = (al + c * c) / N
    R[1, 3] = R[3, 1] = be * np.cos(dphi) * s * c / N
    return R

def cert_lambda_pairs():
    al, dphi = INPUTS['alpha_psi'][0], INPUTS['DeltaPhi'][0]
    a1, a2 = INPUTS['alpha_minus'][0], INPUTS['alpha_plus'][0]
    ths = np.linspace(1e-3, np.pi - 1e-3, 2001)
    # (i) transcription check: the production state is a valid density matrix of rank 2 at every angle
    mins = []; ranks = []
    for th in ths:
        ev = np.linalg.eigvalsh(_rho_from_R(lambda_R(th, al, dphi)))
        mins.append(ev.min()); ranks.append(int((ev > 1e-9).sum()))
    ok = min(mins) > -1e-12 and max(ranks) <= 2
    # (ii) raw operator: scale by the decay parameters; data noncontextual iff rho_raw and its partial transpose are PSD
    def margin(th, al=al, dphi=dphi, a1=a1, a2=a2):
        Rr = np.diag([1, a1, a1, a1]) @ lambda_R(th, al, dphi) @ np.diag([1, a2, a2, a2])
        rho = _rho_from_R(Rr)
        return min(np.linalg.eigvalsh(rho).min(), np.linalg.eigvalsh(_pt(rho)).min()), np.linalg.det(Rr)
    marg = np.array([margin(th)[0] for th in ths])
    ctx = marg < 0
    cos_c = np.abs(np.cos(ths[ctx])).max() if ctx.any() else 0.0
    # refine the boundary
    from scipy.optimize import brentq
    thc = brentq(lambda t: margin(t)[0], np.arccos(min(cos_c + 0.02, 0.999)), np.pi / 2 - 1e-6) if ctx.any() else np.pi / 2
    cos_c = float(np.cos(thc))
    nuc90 = abs(a1 * a2) * (1 + 2 * al)
    # uncertainty of the trace norm at 90 degrees (alpha_avg^2 used for the product; correlations with alpha_psi neglected)
    aavg, saavg = INPUTS['alpha_avg'][0], INPUTS['alpha_avg'][1]; sal = INPUTS['alpha_psi'][1]
    nuc90_avg = aavg ** 2 * (1 + 2 * al)
    sig = np.sqrt((2 * aavg * saavg * (1 + 2 * al)) ** 2 + (aavg ** 2 * 2 * sal) ** 2)
    # fraction of events with |cos theta| < cos_c for dN/dcos ~ 1 + al cos^2
    frac = (cos_c + al * cos_c ** 3 / 3) / (1 + al / 3)
    # invertibility of the coefficient matrix inside the window (needed for the 'iff')
    dets = [abs(margin(th)[1]) for th in ths if abs(np.cos(th)) < cos_c]
    # sensitivity of the window edge to one-sigma shifts
    edges = []
    for d_al in (-sal, sal):
        for d_a in (-saavg, saavg):
            f = lambda t: margin(t, al=al + d_al, a1=aavg + d_a, a2=-(aavg + d_a))[0]
            try: edges.append(float(np.cos(brentq(f, 0.6, np.pi / 2 - 1e-6))))
            except Exception: edges.append(float('nan'))
    return {'ok': bool(ok and nuc90 > 1 and cos_c > 0), 'detail':
            'production state PSD with rank <= 2 at all angles (min eigenvalue %.1e); ||c||_1 at 90 deg = %.4f '
            '(%.4f +- %.4f with alpha_avg^2); raw operator fails PPT for |cos theta| < %.4f (range %.3f-%.3f under one-sigma shifts), '
            '%.1f%% of events; min |det R_raw| in the window %.2e'
            % (min(mins), nuc90, nuc90_avg, sig, cos_c, np.nanmin(edges), np.nanmax(edges), 100 * frac, min(dets)),
            'cos_c': cos_c, 'nuc90': nuc90, 'nuc90_avg': nuc90_avg, 'sigma': sig, 'frac': frac, 'edges': edges}

def cert_top_pair_numbers():
    D, sD = INPUTS['D_ATLAS'][0], INPUTS['D_ATLAS'][1]; B, sB = INPUTS['D_ATLAS_bound'][0], INPUTS['D_ATLAS_bound'][1]
    z_atlas = (B - D) / np.hypot(sD, sB)
    Dc, sDc = INPUTS['D_CMS'][0], INPUTS['D_CMS'][1]
    z_cms = (-1 / 3 - Dc) / sDc
    ok = abs(z_atlas - 10.2) < 0.1 and abs(z_cms - 5.06) < 0.05
    return {'ok': bool(ok), 'detail': 'ATLAS: (bound - D)/sigma = %.1f with the quoted particle-level bound; CMS parton level: '
            '(-1/3 - D)/sigma = %.2f; |tr c| = 3|D| = %.2f (CMS), bound for noncontextual data: 1' % (z_atlas, z_cms, 3 * abs(Dc)),
            'z_atlas': z_atlas, 'z_cms': z_cms}

# ---------------------------------------------------------------- rank-one decomposition lemma (instances)
def cert_rank_one_lemma(trials=200, seed=0):
    """M >= 0 (4x4), <M,J> = 0 with J = diag(1,-1,-1,-1)  ==>  M = sum_k u_k u_k^T with u_k^T J u_k = 0.
    Constructive check on random instances (the proof is in the paper, App. B)."""
    rng = np.random.default_rng(seed); J = np.diag([1.0, -1, -1, -1]); worst = 0
    for _ in range(trials):
        r = rng.integers(1, 5)
        # random PSD M with tr(MJ)=0: sum of r random lightlike vectors, then mix by a J-orthogonal transformation
        Bm = np.array([np.concatenate([[1.0], v / np.linalg.norm(v)]) * rng.uniform(0.3, 2) for v in rng.normal(size=(r, 3))]).T
        Om = np.linalg.qr(rng.normal(size=(r, r)))[0]
        Bm = Bm @ Om                                              # columns no longer lightlike, M unchanged
        M = Bm @ Bm.T
        # algorithm: rotate the columns so that S = B^T J B has zero diagonal
        S = Bm.T @ J @ Bm; Bc = Bm.copy()
        for it in range(200):
            d = np.diag(S)
            if np.abs(d).max() < 1e-13: break
            i = int(np.argmax(d)); k = int(np.argmin(d))
            if d[i] <= 1e-15 or d[k] >= -1e-15: break
            # Givens rotation mixing columns i,k to zero S_ii
            a_, b_, c_ = S[i, i], S[i, k], S[k, k]
            # solve a cos^2 + 2 b cos sin + c sin^2 = 0
            t = (-b_ + np.sqrt(b_ * b_ - a_ * c_)) / c_
            cth, sth = 1 / np.hypot(1, t), t / np.hypot(1, t)
            G = np.eye(r); G[i, i] = cth; G[k, i] = sth; G[i, k] = -sth; G[k, k] = cth
            Bc = Bc @ G; S = Bc.T @ J @ Bc
        worst = max(worst, np.abs(np.diag(S)).max(), np.abs(Bc @ Bc.T - M).max())
    return {'ok': bool(worst < 1e-9), 'detail': '%d random instances: residual %.1e (lightlike columns and M reproduced)' % (trials, worst)}

# ---------------------------------------------------------------- SDP support function of R
def cert_support_sdp(ndir=24, nal=16):
    import cvxpy as cp
    worst = 0
    p = cp.Variable(3); A = cp.Variable((3, 3), symmetric=True); lam = cp.Variable()
    z1 = cp.Parameter(3); Z2 = cp.Parameter((3, 3), symmetric=True)
    M = cp.bmat([[cp.reshape(2 / 3 - lam, (1, 1), order='C'), cp.reshape(p / 2, (1, 3), order='C')],
                 [cp.reshape(p / 2, (3, 1), order='C'), A + lam * np.eye(3)]])
    prob = cp.Problem(cp.Maximize(z1 @ p + cp.trace(Z2 @ A)), [M >> 0, cp.trace(A) == 0])
    for ph in np.linspace(0, 2 * np.pi, ndir, endpoint=False):
        a, b = np.cos(ph), np.sin(ph); best = -np.inf
        for al in np.linspace(0, np.pi / 4, nal):
            u = np.array([np.cos(al), 0, 0]); v = np.array([0, np.sin(al), 0])
            z1.value = a / 2 * 2 * np.cross(u, v); Z2.value = 3 * b / 5 * (np.eye(3) / 3 - np.outer(u, u) - np.outer(v, v))
            prob.solve(solver=cp.CLARABEL); best = max(best, prob.value)
        worst = max(worst, abs(best - h_R(a, b)))
    return {'ok': bool(worst < 1e-6), 'detail': 'max |SDP - closed form| over %d directions x %d pure states: %.1e' % (ndir, nal, worst)}

# ---------------------------------------------------------------- general j
def cert_general_j(jmax2=8):
    from math import comb
    from scipy.optimize import linprog
    from scipy.special import roots_legendre, roots_jacobi
    rows = []; ok = True
    for twoj in range(1, jmax2 + 1):
        j = twoj / 2; d = twoj + 1; k = twoj // 2
        xi = roots_legendre(k + 1)[0].max() if twoj % 2 == 0 else roots_jacobi(k + 1, 0, 1)[0].max()
        xs = np.cos(np.linspace(0, np.pi, 20001)); ms = np.array([j - i for i in range(d)])
        Bq = np.array([[comb(twoj, int(round(j + m))) * ((1 + x) / 2) ** (j + m) * ((1 - x) / 2) ** (j - m) for m in ms] for x in xs])
        res = linprog(-ms, A_ub=-Bq, b_ub=np.zeros(len(xs)), A_eq=np.ones((1, d)), b_eq=[1.0], bounds=(None, None), method='highs')
        pmax = -res.fun; sig = np.diag(res.x).astype(complex)
        G = np.zeros((d, d), complex); G[0, 0] = 1
        m = m_coeffs(j, G, sig); Dc = kernel_D(j, coherent_kernel(j))
        D = proj_l(j, Dc, 0) + sum(m[l - 1] * proj_l(j, Dc, l) for l in range(1, twoj + 1))
        w = np.real(np.diag(D)); k1 = float(sum(ms * w) / j)
        good = abs(pmax / (j + 1) - xi) < 2e-6 and w.min() > -1e-9 and abs(k1 - xi) < 2e-6 and np.abs(m).min() > 1e-3
        ok = ok and good; rows.append({'j': j, 'xi': float(xi), 'lp': float(pmax / (j + 1)), 'w_min': float(w.min()), 'kappa1_attained': k1, 'm': [float(v) for v in m],
                                       'w_star': [float(v) for v in w]})
    return {'ok': bool(ok), 'detail': 'j = 1/2..%g: LP value of max|<J>|/(j+1) over Husimi-nonnegative operators equals the quadrature node '
            '(max dev %.1e); attaining kernels are probability vectors (min weight %.4f)'
            % (jmax2 / 2, max(abs(r['lp'] - r['xi']) for r in rows), min(r['w_min'] for r in rows)), 'rows': rows}

# ---------------------------------------------------------------- recorded long runs
def _read(path):
    p = os.path.join(ROOT, 'out', path)
    return json.load(open(p)) if os.path.exists(p) else None

def cert_lp_region(mode='R', tol_out=0.012, tol_in=0.015):
    """Brute-force LP (checks/slow_spin1_lp.py): LP value / closed-form radius must lie in [1 - tol_in, 1 + tol_out]
    (inner approximation from the finite operator set, outer relaxation from the direction grid)."""
    d = _read('lp_%s.json' % mode)
    if d is None or not d['rows']: return {'ok': False, 'detail': 'recorded run missing (run checks/slow_spin1_lp.py)'}
    ratios = [r['lp'] / r['closed'] for r in d['rows'] if r['lp'] is not None]
    ok = len(ratios) >= 6 and min(ratios) > 1 - tol_in and max(ratios) < 1 + tol_out
    return {'ok': bool(ok), 'detail': '%d directions, K = %d operators, %d grid directions: LP/closed in [%.4f, %.4f]'
            % (len(ratios), d['K'], d['nq'], min(ratios), max(ratios)), 'rows': d['rows']}

def cert_two_qubit_sandwich():
    d = _read('two_qubit_sandwich.json')
    if d is None: return {'ok': False, 'detail': 'recorded run missing (run checks/slow_two_qubit.py)'}
    ok = all(r['inner'] <= r['exact'] + 1e-9 <= r['outer'] + 2e-9 for r in d['rows'])
    fin = [r for r in d['rows'] if r['N'] == max(x['N'] for x in d['rows'])]
    gap = max(r['outer'] - r['inner'] for r in fin)
    # hyperon pair: outer LP infeasible inside the window (contextual), inner LP feasible outside (noncontextual)
    lam = {round(r['cos'], 2): r for r in d.get('lambda', [])}
    ok_l = bool(lam) and all((not lam[c]['outer_feasible']) for c in lam if c < 0.5) and all(lam[c]['inner_feasible'] for c in lam if c > 0.55)
    return {'ok': bool(ok and gap < 0.04 and ok_l), 'detail': 'inner <= exact <= outer in all %d runs; bracket width at N = %d: %.4f; '
            'hyperon pair: sub-fragment LP infeasible at cos theta = %s, dual-cone LP feasible at %s'
            % (len(d['rows']), fin[0]['N'], gap, sorted(c for c in lam if c < 0.5), sorted(c for c in lam if c > 0.55)), 'rows': d['rows'], 'lambda': d.get('lambda', [])}

def cert_lp_refine():
    """Grid refinement of the three largest LP deviations: the deviation must shrink."""
    d = _read('lp_refine.json')
    if d is None or len(d['rows']) < 6: return {'ok': False, 'detail': 'recorded run missing or incomplete (run checks/slow_refine.py)'}
    rows = d['rows']; dev = [abs(r['lp'] / r['closed'] - 1) for r in rows]
    ok = dev[1] < dev[0] and dev[3] < dev[2] and dev[5] < dev[4] and max(dev[1], dev[3], dev[5]) < 0.004
    return {'ok': bool(ok), 'detail': 'R at 90 deg: %.4f -> %.4f (grid %d -> %d); R2 at 270 deg: %.4f -> %.4f (grid %d -> %d); '
            'R2 at 80 deg: %.4f -> %.4f (tau = 1.8 added)' % (rows[0]['lp'] / rows[0]['closed'], rows[1]['lp'] / rows[1]['closed'], rows[0]['nq'], rows[1]['nq'],
               rows[2]['lp'] / rows[2]['closed'], rows[3]['lp'] / rows[3]['closed'], rows[2]['nq'], rows[3]['nq'],
               rows[4]['lp'] / rows[4]['closed'], rows[5]['lp'] / rows[5]['closed']), 'rows': rows}


def cert_vector_pair_kernels():
    """Parity-symmetric spin-1 kernels from fermion-pair decays: w0 = (1 - alpha)/(3 + alpha) for a 1 + alpha cos^2 distribution.
    Noncontextual on all states iff 1/5 <= w0 <= 3/5, i.e. -1/2 <= alpha <= 1/3 (Theorem 3 at eta1 = 0)."""
    from sympy import Rational as Q, symbols, solve, simplify
    al = symbols('alpha', real=True)
    w0 = (1 - al) / (3 + al)
    ok_alg = (solve(w0 - Q(1, 5), al) == [Q(1, 3)] and solve(w0 - Q(3, 5), al) == [Q(-1, 2)] and simplify(1 - 3 * w0 - 4 * al / (3 + al)) == 0)
    aL, sL = INPUTS['alpha_psi'][:2]; aS, sS = INPUTS['alpha_psi_Sigma'][:2]
    w = lambda a: (1 - a) / (3 + a); dw = lambda a: 4 / (3 + a) ** 2
    zL = (0.2 - w(aL)) / (dw(aL) * sL); zS = (w(aS) - 0.6) / (dw(aS) * sS)
    x = (INPUTS['m_tau'][0] / INPUTS['m_psi2S'][0]) ** 2; a_tau = (1 - 4 * x) / (1 + 4 * x)
    ok = ok_alg and w(aL) < 0.2 and zL > 5 and abs(zS) < 2 and x > 0.125 and -0.5 < a_tau < 1 / 3
    a0, s0 = INPUTS['alpha0_Sigma'][:2]; a0b, s0b = INPUTS['alpha0bar_Sigma'][:2]
    nucS = abs(a0 * a0b) * (1 + 2 * abs(aS)); snucS = nucS * ((s0 / a0) ** 2 + (s0b / a0b) ** 2 + (2 * sS / (1 + 2 * abs(aS))) ** 2) ** 0.5
    ok = ok and nucS - 1 > 5 * snucS
    return {'ok': bool(ok), 'detail': 'w0(alpha) = (1-alpha)/(3+alpha); window alpha in [-1/2, 1/3]; J/psi -> Lambda Lambdabar: w0 = %.3f, %.0f sigma below 1/5; '
            'J/psi -> Sigma+ Sigmabar-: w0 = %.3f +- %.3f, %.1f sigma above 3/5; psi(2S) -> tau tau: x = %.3f >= 1/8, alpha = %.3f'
            % (w(aL), zL, w(aS), dw(aS) * sS, zS, x, a_tau),
            'w0_L': w(aL), 'z_L': zL, 'w0_S': w(aS), 'sw0_S': dw(aS) * sS, 'z_S': zS, 'x_tau': x, 'alpha_tau': a_tau, 'nuc90_Sigma': nucS, 'snuc90_Sigma': snucS}
