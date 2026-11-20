"""Figures of the paper, generated from the same code that the kernel checks.
Palette: slots 1-3 of the validated categorical palette (blue, orange, aqua); text in ink colours."""
import sys, os, json
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'lib')); sys.path.insert(0, os.path.join(ROOT, 'net'))
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Polygon, FancyArrowPatch
from regions import h_R, h_R2
import certs_numeric as cn

BLUE, ORANGE, AQUA = '#2a78d6', '#eb6834', '#1baf7a'
INK, INK2, MUTED, GRID = '#0b0b0b', '#52514e', '#8a8983', '#e4e3df'
plt.rcParams.update({'font.size': 8, 'font.family': 'DejaVu Sans', 'axes.edgecolor': INK2, 'axes.labelcolor': INK,
                     'xtick.color': INK2, 'ytick.color': INK2, 'axes.linewidth': 0.6, 'xtick.major.width': 0.6,
                     'ytick.major.width': 0.6, 'pdf.fonttype': 42, 'mathtext.fontset': 'dejavusans'})

def boundary(h, n=2000):
    """Boundary of a convex set from its support function (envelope of supporting lines)."""
    ph = np.linspace(0, 2 * np.pi, n, endpoint=False); d = 1e-5
    hv = np.array([h(np.cos(p), np.sin(p)) for p in ph])
    dh = np.array([(h(np.cos(p + d), np.sin(p + d)) - h(np.cos(p - d), np.sin(p - d))) / (2 * d) for p in ph])
    x = hv * np.cos(ph) - dh * np.sin(ph); y = hv * np.sin(ph) + dh * np.cos(ph)
    return x, y

# ------------------------------------------------------------------ Fig. 2: regions
def fig_regions():
    fig, axs = plt.subplots(1, 2, figsize=(7.0, 4.25), sharey=True)
    xR, yR = boundary(h_R); xR2, yR2 = boundary(h_R2)
    tri = np.array([[1, 1], [-1, 1], [0, -2]])
    for ax in axs:
        ax.add_patch(Polygon(tri, closed=True, fill=False, ec=MUTED, lw=0.8, ls=(0, (4, 3))))
        ax.axhline(0, color=GRID, lw=0.6, zorder=0); ax.axvline(0, color=GRID, lw=0.6, zorder=0)
        ax.set_xlim(-1.22, 1.22); ax.set_ylim(-2.25, 1.95); ax.set_aspect('equal')
        ax.set_xlabel(r'vector ratio  $\eta_1 = w_+ - w_-$')
        for s in ('top', 'right'): ax.spines[s].set_visible(False)
    a = axs[0]
    a.fill(xR, yR, color=BLUE, alpha=0.22, lw=0); a.plot(np.append(xR, xR[0]), np.append(yR, yR[0]), color=BLUE, lw=1.6)
    a.set_ylabel(r'tensor ratio  $\eta_2 = 1 - 3 w_0$   (panel b: $\eta_2^A\eta_2^B$)')
    a.set_title('(a) one spin-1 particle, all states', loc='left', fontsize=8.5, color=INK)
    a.text(0.0, 0.07, r'$\mathcal{R}$', color=INK, fontsize=10, ha='center')
    pts = [((1, 1), r'$W\!\to\ell\nu$', (-0.06, 0.12), 'right'), ((-1, 1), '', None, None), ((0.15, 1), r'$Z\!\to\ell^+\ell^-$', (0.0, 0.14), 'center'),
           ((0, -2), r'$V\!\to PP$', (0.08, -0.02), 'left')]
    for (x, y), lab, off, ha in pts:
        a.plot([x], [y], 'o', ms=4.5, color=INK, mfc='white', mew=1.0, zorder=5)
        if lab: a.text(x + off[0], y + off[1], lab, color=INK, ha=ha, va='center', fontsize=7.5)
    a.plot([1 / np.sqrt(3)], [0.2], 's', ms=4, color=BLUE, zorder=6)
    a.annotate(r'max. vector power' '\n' r'$(1/\sqrt{3},\,1/5)$', (1 / np.sqrt(3), 0.2), (0.66, -0.55), fontsize=7, color=INK2,
               arrowprops=dict(arrowstyle='-', lw=0.5, color=MUTED), ha='left')
    a.plot([0], [-0.8], 's', ms=4, color=BLUE, zorder=6); a.text(0.07, -0.86, r'$(0,-4/5)$', fontsize=7, color=INK2, va='top')
    a.plot([0], [0.4], 's', ms=4, color=BLUE, zorder=6); a.text(0.07, 0.47, r'$(0,\,2/5)$', fontsize=7, color=INK2)
    b = axs[1]
    b.fill(xR2, yR2, color=ORANGE, alpha=0.20, lw=0); b.plot(np.append(xR2, xR2[0]), np.append(yR2, yR2[0]), color=ORANGE, lw=1.6)
    b.plot(np.append(xR, xR[0]), np.append(yR, yR[0]), color=BLUE, lw=0.9, ls=(0, (2, 2)))
    b.set_title('(b) singlet pair, one decay on each side', loc='left', fontsize=8.5, color=INK)
    b.set_xlabel(r'product of vector ratios  $\eta_1^A\eta_1^B$')
    b.text(0.0, 0.62, r'$\mathcal{R}_2$', color=INK, fontsize=10, ha='center'); b.text(0.0, 0.07, r'$\mathcal{R}$', color=BLUE, fontsize=8, ha='center')
    b.plot([0, 1], [0, 1], color=INK2, lw=0.8, ls=(0, (1, 2)))
    for (x, y), lab, off, ha in [((1, 1), r'$WW$', (-0.05, 0.13), 'right'), ((0.15, 1), r'$WZ$', (0.06, 0.13), 'left'),
                                 ((0.0225, 1), r'$ZZ$', (-0.07, 0.13), 'right'), ((0, -2), r'$(\ell\ell)(PP)$', (0.08, -0.02), 'left')]:
        b.plot([x], [y], 'o', ms=4.5, color=INK, mfc='white', mew=1.0, zorder=5); b.text(x + off[0], y + off[1], lab, color=INK, ha=ha, va='center', fontsize=7.5)
    b.plot([0.625], [0.625], 's', ms=4, color=ORANGE, zorder=6)
    b.annotate(r'visibility $5/8$', (0.625, 0.625), (0.74, -0.02), fontsize=7, color=INK2, arrowprops=dict(arrowstyle='-', lw=0.5, color=MUTED))
    b.plot([0], [1.6], 's', ms=4, color=ORANGE, zorder=6); b.text(0.07, 1.66, r'$(0,\,8/5)$', fontsize=7, color=INK2)
    fig.tight_layout(w_pad=1.2)
    fig.savefig(os.path.join(ROOT, 'figs', 'fig_regions.pdf')); fig.savefig(os.path.join(ROOT, 'figs', 'fig_regions.png'), dpi=220); plt.close(fig)

# ------------------------------------------------------------------ Fig. 3: spin-1/2 applications
def fig_half():
    fig, axs = plt.subplots(1, 2, figsize=(7.0, 2.9))
    a = axs[0]
    al, dphi = cn.INPUTS['alpha_psi'][0], cn.INPUTS['DeltaPhi'][0]; a1, a2 = cn.INPUTS['alpha_minus'][0], cn.INPUTS['alpha_plus'][0]
    cs = np.linspace(-0.999, 0.999, 801); raw = []; st = []
    for c in cs:
        R = cn.lambda_R(np.arccos(c), al, dphi)
        Rr = np.diag([1, a1, a1, a1]) @ R @ np.diag([1, a2, a2, a2]); rho = cn._rho_from_R(Rr)
        raw.append(min(np.linalg.eigvalsh(rho).min(), np.linalg.eigvalsh(cn._pt(rho)).min()))
        st.append(np.linalg.eigvalsh(cn._pt(cn._rho_from_R(R))).min())
    raw = np.array(raw); st = np.array(st)
    cc = cn.cert_lambda_pairs()['cos_c']
    a.axvspan(-cc, cc, color=BLUE, alpha=0.10, lw=0)
    a.axhline(0, color=INK2, lw=0.7)
    a.plot(cs, st, color=ORANGE, lw=1.8, label='pair state (entanglement test)')
    a.plot(cs, raw, color=BLUE, lw=1.8, label='raw coefficients (this work)')
    a.set_xlabel(r'$\cos\theta$ of the $\Lambda$ in $e^+e^-\!\to J/\psi\to\Lambda\bar\Lambda$'); a.set_ylabel('smallest eigenvalue of the\npartial transpose')
    a.text(0, 0.045, 'no noncontextual\nmodel', ha='center', va='bottom', fontsize=7, color=INK2)
    a.text(cc + 0.03, -0.20, r'$|\cos\theta| = %.3f$' % cc, fontsize=7, color=INK2)
    a.plot([cc, cc], [-0.26, 0], color=MUTED, lw=0.6, ls=(0, (2, 2))); a.plot([-cc, -cc], [-0.26, 0], color=MUTED, lw=0.6, ls=(0, (2, 2)))
    a.set_ylim(-0.26, 0.13); a.set_xlim(-1, 1)
    a.legend(frameon=False, fontsize=7, loc='lower center', bbox_to_anchor=(0.5, 1.0), ncol=1, handlelength=1.6)
    a.set_title('(a)', loc='left', fontsize=8.5, color=INK, x=-0.18, y=1.0)
    b = axs[1]
    mW = cn.INPUTS['m_W'][0]; mt = np.linspace(150, 186, 400); xi = (mt / mW) ** 2
    kb = (xi - 2) / (xi + 2); kn = -((xi - 1) * (xi ** 2 - 11 * xi - 2) + 12 * xi * np.log(xi)) / ((xi + 2) * (xi - 1) ** 2)
    m0, s0 = cn.INPUTS['m_t'][0], cn.INPUTS['m_t'][1]
    b.axvspan(m0 - s0, m0 + s0, color=MUTED, alpha=0.30, lw=0)
    b.axhline(1 / 3, color=INK2, lw=0.7)
    b.plot(mt, kb, color=BLUE, lw=1.8, label=r'$b$-quark direction, $|\kappa_b|$')
    b.plot(mt, kn, color=ORANGE, lw=1.8, label=r'neutrino or up-type quark, $|\kappa_\nu|$')
    b.plot([2 * mW], [1 / 3], 'o', ms=4.5, color=BLUE, zorder=5); b.plot([cn.cert_top_powers()['mt_star']], [1 / 3], 'o', ms=4.5, color=ORANGE, zorder=5)
    b.text(2 * mW + 0.6, 1 / 3 - 0.012, r'$m_t = 2m_W$', fontsize=7, color=INK2, va='top')
    b.text(cn.cert_top_powers()['mt_star'] + 0.7, 1 / 3 - 0.012, r'$173.0$ GeV', fontsize=7, color=INK2, va='top')
    b.text(151, 1 / 3 + 0.006, r'classical boundary $1/3$', fontsize=7, color=INK2)
    b.text(m0 - 0.6, 0.265, 'measured\n$m_t$', fontsize=7, color=INK2, ha='right')
    b.set_xlabel(r'$m_t$ (GeV), with $m_W = 80.3625$ GeV'); b.set_ylabel('leading-order analysing power')
    b.set_xlim(150, 186); b.set_ylim(0.25, 0.47)
    b.legend(frameon=False, fontsize=7, loc='lower center', bbox_to_anchor=(0.5, 1.0), ncol=1, handlelength=1.6)
    b.set_title('(b)', loc='left', fontsize=8.5, color=INK, x=-0.18, y=1.0)
    for ax in axs:
        for s in ('top', 'right'): ax.spines[s].set_visible(False)
    fig.tight_layout(w_pad=1.6)
    fig.savefig(os.path.join(ROOT, 'figs', 'fig_half.pdf')); fig.savefig(os.path.join(ROOT, 'figs', 'fig_half.png'), dpi=220); plt.close(fig)

# ------------------------------------------------------------------ Fig. 1: the three-layer delta
def fig_network():
    fig, ax = plt.subplots(figsize=(7.0, 4.9)); ax.set_xlim(0, 100); ax.axis('off')
    cols = {'S': 16.5, 'M': 50, 'O': 83.5}
    for k, name in (('S', 'STATE LAYER'), ('M', 'MODEL LAYER'), ('O', 'OBSERVABLE LAYER')):
        ax.add_patch(FancyBboxPatch((cols[k] - 15.2, 5.2), 30.4, 60.2, boxstyle='round,pad=0.2,rounding_size=1.2', fc='#f6f5f2', ec=GRID, lw=0.8, zorder=0))
        ax.text(cols[k], 67.6, name, ha='center', va='center', fontsize=7.6, color=INK2, fontweight='bold')
    boxes = {}
    def box(key, layer, y, text, released=False, w=27, h=6.6):
        x = cols[layer]
        ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h, boxstyle='round,pad=0.15,rounding_size=0.9',
                                    fc='white' if released else '#e6eefb', ec=INK2 if released else BLUE, lw=0.9, zorder=3))
        ax.text(x, y, text, ha='center', va='center', fontsize=6.6, color=INK, zorder=4, linespacing=1.15)
        boxes[key] = (x, y, w, h)
    ys = [58.5, 47.5, 36.5, 25.5, 14.5]
    box('part', 'S', ys[0], 'massive spin-1/2 and spin-1\nparticles  ($u_{mh}$, $u_{m1}$)', True)
    box('spin', 'S', ys[1], 'all spin states of one particle')
    box('steer', 'S', ys[2], 'ensemble steered by the\npartner decay')
    box('ent', 'S', ys[3], 'separable / entangled pair\nstates  (s-sep, s-ent)', True)
    box('iso', 'S', ys[4], 'unpolarised pairs; isotropic\nspin-1 pairs; $t\\bar t$; $\\Lambda\\bar\\Lambda$')
    box('vert', 'M', ys[0], 'charged-current and V$-$A\nvertices  ($m_{cc}$, $m_{va}$, $m_\\mu$)', True)
    box('pol', 'M', ys[1], 'decay polarimeter: one fixed\ncovariant measurement $E_w(q)$')
    box('lhv', 'M', ys[2], 'recorded-outcome hidden-\nvariable model')
    box('nc', 'M', ys[3], 'noncontextual ontological\nmodel  (glued to m-classical)')
    box('tomo', 'M', ys[4], 'mutual tomographic\ncompleteness')
    box('ang', 'O', ys[0], 'decay-angle distributions:\n$p(q)$;  raw $(a, b, c)$;  $D$')
    box('wit', 'O', ys[1], 'tests: raw-PPT, $\\|c\\|_1$; regions\n$\\mathcal{R}$, $\\mathcal{R}_2$;  $|\\kappa_1|\\leq\\xi_{2j}$')
    box('ctx', 'O', ys[2], 'generalized contextuality\n(e-ctx)', True)
    box('lp', 'O', ys[3], 'simplex-embedding LP\n(w-ncineq)', True)
    box('bell', 'O', ys[4], 'Bell violation, steering\n(e-bell, e-steer)', True)
    LS = {'solid': '-', 'dashed': (0, (4, 2)), 'dotted': (0, (1, 2))}
    def anchor(key, side, shift=0.0):
        x, y, w, h = boxes[key]
        return {'right': (x + w / 2 + 0.3, y + shift), 'left': (x - w / 2 - 0.3, y + shift),
                'bottom': (x + shift, y - h / 2 - 0.3), 'top': (x + shift, y + h / 2 + 0.3)}[side]
    def edge(a, b, style='solid', color=INK2, term='->', rad=0.0, sa='right', sb='left', lw=1.0, sha=0.0, shb=0.0):
        pa = anchor(a, sa, sha); pb = anchor(b, sb, shb)
        astyle = '-|>' if term == '->' else '-[,widthB=1.6,lengthB=0.01'
        ax.add_patch(FancyArrowPatch(pa, pb, arrowstyle=astyle, mutation_scale=7 if term == '->' else 3.0, lw=lw, color=color,
                                     ls=LS[style], connectionstyle='arc3,rad=%s' % rad, zorder=2, shrinkA=0, shrinkB=0))
    edge('part', 'vert')                                            # particle sectors enter the vertex (DV1-DV5)
    edge('vert', 'pol', sa='bottom', sb='top')                      # vertex -> polarimeter (DV1-DV5)
    edge('spin', 'pol')                                             # states measured by the polarimeter
    edge('pol', 'ang', rad=-0.14, shb=-1.2)                         # Born rule (DV2, DV8, DV9)
    edge('ent', 'pol', rad=-0.12, shb=-1.6)                         # pair states (DV9)
    edge('pol', 'steer', style='dotted', sa='left', sb='right', sha=-2.0, shb=1.2)   # partner decay prepares the ensemble (DV11)
    edge('ang', 'wit', sa='bottom', sb='top')                       # coefficients -> tests
    edge('pol', 'wit', color=BLUE, lw=1.7)                          # thresholds (Thms 1-5)
    edge('wit', 'ctx', sa='bottom', sb='top', color=BLUE, lw=1.7)
    edge('lp', 'ctx', sa='top', sb='bottom')                        # numerical cross-checks
    edge('lhv', 'bell', term='-|', rad=-0.16, sha=-1.8)             # single setting: no Bell test, no steering (FW3, FW4)
    edge('lhv', 'nc', style='solid', sa='bottom', sb='top', term='-|')   # recorded-outcome model is not noncontextual (FW5)
    edge('tomo', 'nc', style='dotted', sa='top', sb='bottom')       # FW1
    edge('nc', 'ctx', style='dotted', term='-|', rad=0.10, shb=-1.6)     # definition of e-ctx
    edge('ctx', 'ent', style='dashed', sa='left', sb='right', rad=-0.10, sha=1.4, shb=1.6)   # contextual data imply entanglement (H8)
    edge('iso', 'ent', style='dotted', sa='top', sb='bottom')
    # legend, two rows
    items = [('solid', INK2, '->', 'checked route (exact, logic or numeric)'), ('dashed', INK2, '->', 'written proof step'),
             ('dotted', INK2, '->', 'definition or import'), ('solid', INK2, '-|', 'forbids / does not hold'), ('solid', BLUE, '->', 'threshold theorems of this work')]
    pos = [(1.0, 1.6), (38.0, 1.6), (66.0, 1.6), (1.0, -2.2), (38.0, -2.2)]
    for (style, col, term, lab), (x, y) in zip(items, pos):
        astyle = '-|>' if term == '->' else '-[,widthB=1.6,lengthB=0.01'
        ax.add_patch(FancyArrowPatch((x, y), (x + 5, y), arrowstyle=astyle, mutation_scale=7 if term == '->' else 3.0,
                                     lw=1.7 if col == BLUE else 1.0, color=col, ls=LS[style], clip_on=False))
        ax.text(x + 6.2, y, lab, fontsize=6.4, color=INK2, va='center')
    ax.text(66.0, -2.2, 'white: released nodes; tinted: new nodes', fontsize=6.4, color=INK2, va='center')
    ax.set_ylim(-4.2, 70)
    fig.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)
    fig.savefig(os.path.join(ROOT, 'figs', 'fig_network.pdf')); fig.savefig(os.path.join(ROOT, 'figs', 'fig_network.png'), dpi=220); plt.close(fig)

if __name__ == '__main__':
    fig_regions(); fig_half(); fig_network(); print('figures written')

