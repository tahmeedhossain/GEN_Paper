"""Nodes, routes and headline claims of the decay-polarimetry delta.
Released nodes keep their ids (GEN_HEP 4258f6e, GEN_GPT_Level e18fa8c / v2.6, GEN_QRT_Level 198ca02 / v1.2)."""
import certs_exact as ce, certs_spin1 as cs, certs_numeric as cn, certs_extra as cx

def N(id, layer, sub, label, definition, released=None, glue=None):
    return {'id': id, 'layer': layer, 'sub': sub, 'label': label, 'def': definition, 'released': released, 'glue': glue or []}

NODES = [
 # ---------------- state layer
 N('u_mh', 'S', 'uir', 'Massive spin-1/2 particle', 'Wigner class m > 0, s = 1/2 (t, tau, mu, Lambda).', 'GEN_HEP'),
 N('u_m1', 'S', 'uir', 'Massive spin-1 particle', 'Wigner class m > 0, s = 1 (W, Z, J/psi).', 'GEN_HEP'),
 N('s-spin', 'S', 'hilbert', 'All spin states of one particle', 'Density operators on C^(2j+1) of a particle at rest; data Bloch vector v = kappa r for j = 1/2.'),
 N('s-steer', 'S', 'cluster', 'Steered ensemble', 'States of particle A conditioned on the recorded decay direction of particle B (remote preparations).'),
 N('s-sep', 'S', 'free', 'Separable states', 'Convex hull of product states.', 'GEN_GPT_Level', ['GEN_QRT_Level:sF-ent']),
 N('s-ent', 'S', 'resource', 'Entangled states', 'Non-separable bipartite states.', 'GEN_GPT_Level', ['GEN_QRT_Level:sR-ent']),
 N('s-tstate', 'S', 'cluster', 'Unpolarised pair states', 'Two spin-1/2 particles with vanishing single-particle polarisation; correlation matrix C.'),
 N('s-iso1', 'S', 'cluster', 'Isotropic spin-1 pair states', 'v |singlet><singlet| + (1-v) 1/9 for two spin-1 particles.'),
 N('s-ttbar', 'S', 'sector', 'Top-pair spin state', 'Spin state of a t tbar pair at fixed kinematics.'),
 N('s-LLbar', 'S', 'sector', 'Hyperon-pair spin state', 'Lambda anti-Lambda from e+ e- -> J/psi at production angle theta.'),
 # ---------------- model layer
 N('m_A', 'M', 'frame', 'Observable postulate, Born rule', 'Hermitian observables and the Born rule.', 'GEN_HEP'),
 N('m_cc', 'M', 'fund', 'Charged-current vertex', '(g/sqrt2) W_mu J^mu_CC + h.c.', 'GEN_HEP'),
 N('m_va', 'M', 'eff', 'Universal V-A current-current term', '(G_F/sqrt2) J_mu J^mu dagger.', 'GEN_HEP'),
 N('m_mu', 'M', 'eff', 'Muon-decay contact term', '(G_F/sqrt2)(nubar_mu gamma^mu mu)(ebar gamma_mu nu_e) with V-A structure.', 'GEN_HEP'),
 N('m_nc', 'M', 'fund', 'Neutral-current vertex', '(g/cos theta_W) Z_mu J^mu_NC.', 'GEN_HEP'),
 N('m-quantum', 'M', 'model', 'Quantum theory', 'Complex quantum theory.', 'GEN_GPT_Level'),
 N('m-classical', 'M', 'model', 'Classical probability (simplex)', 'Simplicial state space with all response functions.', 'GEN_GPT_Level'),
 N('p-decay', 'M', 'process', 'Decay polarimeter', 'The measurement a decay implements on the parent spin: one fixed SU(2)-covariant POVM '
   'E_w(q) = (d/4pi) R_q D_w R_q^dagger with kernel w (helicity weights of the recorded direction).'),
 N('p-half', 'M', 'process', 'Spin-1/2 polarimeter', 'E(q) = (1 + kappa q.sigma)/4pi; kappa is the spin analysing power.'),
 N('p-one', 'M', 'process', 'Spin-1 polarimeter', 'Kernel (w+, w0, w-); eta1 = w+ - w-, eta2 = 1 - 3 w0.'),
 N('m-lhv1', 'M', 'model', 'Recorded-outcome hidden-variable model', 'Local hidden-variable model of single-setting data whose hidden variables are the recorded outcomes (Kasday; Abel-Dittmar-Dreiner).'),
 N('m-ncom', 'M', 'model', 'Noncontextual ontological model', 'Finite ontic set, convex-linear epistemic states and response functions that respect all operational equivalences of the fragment (simplex embedding).', None, ['GEN_GPT_Level:m-classical', 'GEN_QRT_Level:sF-ctx']),
 N('ax-tomo', 'M', 'axiom', 'Mutual tomographic completeness', 'The accessible states and effects span each other\'s dual space; operational equivalences are then those read off the data.'),
 # ---------------- observable layer
 N('o_wu', 'O', 'direct', 'Parity-violating decay asymmetries', 'Angular asymmetries in weak decays (60Co, muon decay).', 'GEN_HEP'),
 N('o-ang1', 'O', 'direct', 'Decay-angle distribution', 'p(q) = Tr[rho E_w(q)] of one particle; multipole coefficients.'),
 N('o-ang2', 'O', 'direct', 'Joint decay-angle distribution', '(4pi)^2 p(qA,qB) = 1 + a.qA + b.qB + qA^T c qB; raw coefficients (a, b, c).'),
 N('o-D', 'O', 'direct', 'Opening-angle coefficient D', 'D = -3 <cos phi> = -tr(c)/3.'),
 N('w-rawppt', 'O', 'witness', 'Raw-PPT test', 'rho_raw = (1/4)(1 + a.sigma x 1 + 1 x b.sigma + sum c_ij sigma_i x sigma_j) and its partial transpose are positive semidefinite; for a = b = 0: ||c||_1 <= 1.'),
 N('w-ncineq', 'O', 'witness', 'Noncontextuality inequalities / simplex-embedding LP', 'Linear programme deciding simplex embeddability of a fragment.', 'GEN_GPT_Level', ['GEN_QRT_Level:wD-ctx']),
 N('w-entw', 'O', 'witness', 'Entanglement witness / PPT', 'Witness operators and the PPT test on the state.', 'GEN_GPT_Level', ['GEN_QRT_Level:wD-ent']),
 N('w-region1', 'O', 'witness', 'Spin-1 region test', '(eta1, eta2) outside R (all states) or the product of ratios outside R2 (pair, one decay each).'),
 N('w-kappa', 'O', 'witness', 'Vector analysing power bound', '|kappa_1| > xi_2j with xi_n the largest Gauss (n even) or Gauss-Radau (n odd) node.'),
 N('e-ctx', 'O', 'effect', 'Generalized contextuality', 'No noncontextual ontological model of the accessible fragment exists.', 'GEN_GPT_Level', ['GEN_QRT_Level:sR-ctx']),
 N('e-bell', 'O', 'effect', 'Bell inequality violation', 'No local hidden-variable model of a multi-setting behaviour.', 'GEN_GPT_Level'),
 N('e-steer', 'O', 'effect', 'EPR steering', 'No local hidden-state model of an assemblage.', 'GEN_GPT_Level'),
]

def R(id, inputs, target, kind, statement, where, grade, certs=None, scope='general', refs=None):
    return {'id': id, 'inputs': inputs, 'target': target, 'kind': kind, 'statement': statement, 'where': where,
            'grade': grade, 'certs': certs or [], 'scope': scope, 'refs': refs or []}

lpR = lambda: cn.cert_lp_region('R'); lpR2 = lambda: cn.cert_lp_region('R2')

ROUTES = [
 # ---- decay vertex -> measurement
 R('DV1', ['m_cc', 'u_mh'], 'p-half', 'derives', 'For [ubar_2 gamma^mu P_L u_1(s)][ubar_3 gamma_mu P_L v_4] with massless 2,3,4: sum |M|^2 = 8 ((p1 - m s).p4)(p2.p3).', 'Sec. II, App. A', 'exact', [ce.cert_va_trace]),
 R('DV2', ['p-half', 's-spin'], 'o-ang1', 'derives', 'In the parent rest frame (p1 - m s).p4 = m E4 (1 + s.q): recording the direction of fermion 4 (charged lepton or down-type quark of a top decay) is the rank-one covariant effect (1 + q.sigma)/4pi, kappa = +1, at every value of the other variables.', 'Sec. II, App. A', 'exact', [ce.cert_rank_one_effect]),
 R('DV3', ['m_mu', 'u_mh'], 'p-half', 'derives', 'Three-body V-A decay with fermion 3 recorded (electron of mu decay, charged lepton of leptonic tau decay): effects x^2[(3-2x) - (2x-1) q.sigma]; direction only: |kappa| = 1/3; with the energy recorded the sharpest effect has |kappa| = 1.', 'Sec. II, App. A', 'exact', [ce.cert_leptonic_spectrum]),
 R('DV4', ['m_cc', 'u_mh'], 'p-half', 'derives', 't -> b W, narrow width, m_b = 0, b direction: kappa_b = -(xi-2)/(xi+2), xi = m_t^2/m_W^2; |kappa_b| > 1/3 iff m_t > 2 m_W.', 'Sec. II, App. A', 'exact', [ce.cert_top_b_power]),
 R('DV5', ['m_cc', 'u_mh'], 'p-half', 'derives', 'Neutrino or up-type-quark direction: kappa_nu = [(xi-1)(xi^2-11xi-2)+12 xi ln xi]/[(xi+2)(xi-1)^2]; quadrature of the matrix element reproduces it and the published leading-order values; kappa_nu = -0.336 at the PDG 2026 masses, |kappa_nu| = 1/3 at m_t = 173.0 GeV.', 'Sec. V', 'numeric', [cn.cert_top_powers], refs=['Brandenburg, Si, Uwer, PLB 539, 235 (2002)']),
 R('DV6', ['m_A', 'u_mh'], 'p-decay', 'derives', 'Rotational covariance of the decay and the Born rule give E(q) = (d/4pi) R_q D R_q^dagger with D >= 0, Tr D = 1, [D, J_z] = 0.', 'Sec. II', 'compose'),
 R('DV7', ['m_A', 'u_m1'], 'p-one', 'derives', 'Spin 1: R_q D_w R_q^dagger = 1/3 + (eta1/2) q.S + (eta2/6)(3 (q.S)^2 - 2); symbol of sigma = (1/3, p, A): 1/3 + (eta1/2) p.q + (eta2/2) q^T A q.', 'Sec. IV, App. C', 'exact', [cs.cert_spin1_algebra]),
 R('DV8', ['p-decay', 's-spin'], 'o-ang1', 'derives', 'First moment of the polarimeter: int q E_w(q) dq = kappa_1 J/(j+1); the coefficient of P.q in 4 pi p(q) is 3 j kappa_1/(j+1).', 'Sec. IV', 'numeric', [cn.cert_general_j], scope='instance: j <= 4'),
 R('DV9', ['p-half', 's-ent'], 'o-ang2', 'derives', 'Two decays: (4pi)^2 p = 1 + a.qA + b.qB + qA^T c qB with a = kappa_A B_A, b = kappa_B B_B, c = kappa_A kappa_B C; rho_raw = (D_kA x D_kB) rho; a sign flip of one analysing power is a partial transpose up to a local unitary.', 'Sec. III', 'exact', [ce.cert_raw_operator]),
 R('DV10', ['o-ang2'], 'o-D', 'derives', 'D = -3 <cos phi> = -tr(c)/3.', 'Sec. III', 'definition'),
 R('DV11', ['p-half', 's-ent'], 's-steer', 'defines', 'Back-edge: conditioning on the direction recorded by the partner polarimeter prepares the state of A with data Bloch vector v(qB) = (a + c qB)/(1 + b.qB).', 'Sec. III', 'definition'),
 R('DV12', ['m_va', 'm_mu'], 'o_wu', 'derives', 'The decay asymmetries of the released graph are first multipoles of the polarimeter: o_wu is the l = 1 coefficient of o-ang1.', 'Sec. II', 'compose'),
 # ---- framework
 R('FW1', ['ax-tomo', 'm-classical'], 'm-ncom', 'defines', 'A fragment (states Omega, effects E) has a noncontextual model iff id_V = sum_l Z_l g_l with g_l >= 0 on Omega and e(Z_l) >= 0 for all e in E.', 'Sec. II, Lemma 1', 'import', refs=['Schmid et al., PRX Quantum 2, 010331 (2021)', 'Gitton, Woods, Quantum 6, 732 (2022)', 'Selby et al., PRL 132, 050202 (2024)']),
 R('FW2', ['o-ang2'], 'm-lhv1', 'implies', 'With one setting per side the recorded outcomes are themselves local hidden variables.', 'Sec. I', 'exact', [cx.cert_single_setting_lhv], refs=['Abel, Dittmar, Dreiner, PLB 280, 304 (1992)', 'Abel et al., arXiv:2507.15949', 'Fucci et al., arXiv:2609.09294 (Theorem 1)']),
 R('FW3', ['m-lhv1'], 'e-bell', 'forbids', 'Single-setting data cannot violate a Bell inequality.', 'Sec. I', 'logic', [cx.cert_single_setting_lhv]),
 R('FW4', ['m-lhv1'], 'e-steer', 'forbids', 'A single-measurement assemblage always has a local hidden-state model (lambda = outcome).', 'Sec. I', 'logic', [cx.cert_single_setting_lhv]),
 R('FW5', ['m-lhv1', 'p-half'], 'm-ncom', 'not_implies', 'The recorded-outcome model is not noncontextual: outcome functions differing by an l >= 2 harmonic define the same effect and are given different response functions.', 'Sec. II', 'exact', [cx.cert_single_setting_lhv]),
 R('FW6', ['p-decay', 's-spin'], 'm-ncom', 'equiv', 'Covariant reduction (all multipole ratios nonzero): the fragment (all states, E_w) is noncontextual iff (eta_1, ..., eta_2j) lies in the convex hull of the points m_l(psi, Z) = d Tr(Pi_l[psi psi^dagger] Pi_l[Z])/(2l+1), psi a unit vector, Z unit-trace with nonnegative Husimi function.', 'Sec. IV, Prop. 1', 'compose'),
 R('FW7', ['p-decay'], 'w-ncineq', 'witness', 'Simplex-embedding LPs on finite sub-fragments: infeasible implies contextual; LPs on finite subsets of the dual cones: feasible implies noncontextual.', 'App. E', 'definition'),
 # ---- spin 1/2
 R('H1', ['p-half', 's-spin'], 'm-ncom', 'implies', 'Polarisation P and analysing power kappa with P|kappa| <= 1/3: explicit four-state (tetrahedral) model.', 'Sec. III, Thm 1', 'exact', [ce.cert_spin_half_model]),
 R('H13', ['p-half', 's-spin'], 'm-ncom', 'equiv', 'Polarisation vectors filling an ellipsoid with semi-axes P1, P2, P3: noncontextual iff |kappa|(P1+P2+P3) <= 1 (six ontic states along the principal axes); planar ensembles: P|kappa| <= 1/2.', 'Sec. III', 'exact', [cx.cert_ellipsoid]),
 R('H2', ['p-half', 's-spin', 'w-ncineq'], 'e-ctx', 'implies', 'P|kappa| > 1/3 implies no noncontextual model: 3 = sum_l t_l.b_l <= sum_l |b_l| <= 1/(P|kappa|).', 'Sec. III, Thm 1', 'logic', [ce.cert_spin_half_necessity], refs=['Horodecki, Shor, Ruskai, Rev. Math. Phys. 15, 629 (2003); Ruskai, ibid. 643 (entanglement-breaking threshold 1/3)', 'Marvian, arXiv:2003.05984 (preparation noncontextuality alone: average gate fidelity <= 3/4, i.e. 1/2)']),
 R('H3', ['m-ncom', 'o-ang2'], 'w-rawppt', 'implies', 'If the joint data have a noncontextual model then rho_raw and its partial transpose are positive semidefinite.', 'Sec. III, Thm 2(i); App. B', 'compose'),
 R('H4', ['w-rawppt', 'ax-tomo'], 'm-ncom', 'implies', 'If rho_raw passes the test, a noncontextual model exists: from a separable decomposition, directly if the coefficient matrix is invertible and after the cone-preserving projections of the range lemma otherwise.', 'Sec. III, Thm 2; App. B', 'compose'),
 R('H12', ['w-rawppt', 'ax-tomo'], 'm-ncom', 'implies', 'Range lemma: a subspace meeting the interior of the Bloch cone has a projection onto it that maps the cone into itself; a separable decomposition of a singular coefficient matrix can therefore be moved into its range and row space.', 'App. B, Lemma 2', 'numeric', [cx.cert_range_projection], scope='instance: 200 random singular matrices'),
 R('H5', ['s-tstate', 'w-rawppt'], 'e-ctx', 'equiv', 'Unpolarised pairs, any rank of c: noncontextual iff ||c||_1 <= 1; explicit model with at most seven ontic states from the singular value decomposition.', 'Sec. III, Cor. 1', 'exact', [ce.cert_tstate]),
 R('H6', ['o-D', 'w-rawppt'], 'e-ctx', 'implies', '|D| > 1/3 implies contextual data: <Phi+| rho_raw^T_B |Phi+> = (1 + tr c)/4 and <Psi-| rho_raw |Psi-> = (1 - tr c)/4.', 'Sec. III, Cor. 2', 'exact', [ce.cert_trace_witness]),
 R('H7', ['p-half', 's-ent'], 'm-ncom', 'implies', '|kappa_A| <= 1/3 or |kappa_B| <= 1/3: the corresponding local map is entanglement breaking, rho_raw passes the test for every state.', 'Sec. III, Cor. 3', 'exact', [cx.cert_eb_threshold]),
 R('H8', ['e-ctx', 'o-ang2'], 's-ent', 'implies', 'Contextual decay data imply an entangled pair state; the converse holds for all states iff |kappa_A kappa_B| = 1.', 'Sec. III', 'compose', refs=['Plavala, Guhne, PRL 132, 100201 (2024)']),
 R('H9', ['w-rawppt', 'w-entw'], 'e-ctx', 'witness', 'The test acts on the raw angular coefficients; the entanglement test acts on the coefficients divided by the analysing powers. The two coincide iff |kappa_A kappa_B| = 1.', 'Sec. III', 'compose'),
 R('H10', ['s-steer', 'w-ncineq'], 'e-ctx', 'witness', 'Two-sided LP bracket of the threshold on random pair states and on the hyperon pair.', 'App. E', 'numeric', [cn.cert_two_qubit_sandwich], scope='instance: three families'),
 # ---- spin 1, single particle
 R('V1', ['p-one'], 'w-region1', 'derives', 'Nonnegative quadratic functions on the sphere (Lemma 3): 2/3 + p.q + q^T A q >= 0 on the sphere iff a 4x4 matrix pencil is positive semidefinite, i.e. iff it is a sum of squares of affine functions; moment form: (t, z, N) are moments of a positive measure on the sphere iff [[t, z^T],[z, N]] >= 0 with tr N = t.', 'App. C, Lemma 2', 'compose', refs=['Sturm, Zhang, Math. Oper. Res. 28, 246 (2003)']),
 R('V2', ['p-one'], 'w-region1', 'derives', 'Rank-one decomposition lemma (Lemma 3a), checked constructively on random instances.', 'App. C', 'numeric', [cn.cert_rank_one_lemma], scope='instance: 200 random matrices'),
 R('V3', ['p-one', 's-spin'], 'w-region1', 'derives', 'Support function of the region: h_R(a,b) = max{ b/5 + sqrt(b^2/25 + a^2/3), -4b/5 }; R = conv(ellipse 3 eta1^2 + 25 (eta2 - 1/5)^2 <= 1, apex (0,-4/5)).', 'Sec. IV, Thm 3; App. C', 'exact', [cs.cert_region_R_formulas]),
 R('V4', ['p-one', 's-spin'], 'm-ncom', 'implies', 'Explicit finite noncontextual models (icosahedral orbits of one pair) at the extreme points of R.', 'Sec. IV, App. D', 'exact', [cs.cert_finite_models]),
 R('V5', ['p-one', 's-spin', 'w-region1'], 'e-ctx', 'equiv', 'For eta2 != 0 the fragment (all spin-1 states, E_w) is noncontextual iff (eta1, eta2) in R.', 'Sec. IV, Thm 3', 'compose'),
 R('V6', ['w-region1', 'w-ncineq'], 'e-ctx', 'witness', 'Independent numerical values of the support function (SDP) and of the boundary (brute-force LP without the covariant reduction).', 'App. E', 'numeric', [cn.cert_support_sdp, lpR]),
 R('V7', ['p-one', 's-spin'], 'm-ncom', 'equiv', 'Exactly degenerate kernel eta2 = 0: noncontextual iff |eta1| <= 2/9 (fragment-relative equivalences); the limit eta2 -> 0 of R gives sqrt2/3.', 'Sec. IV, Remark', 'exact', [cx.cert_degenerate_line]),
 # ---- spin 1, pair
 R('P1', ['p-one', 's-iso1'], 'w-region1', 'derives', 'Maximally entangled pair, one decay on each side: steered states are images of the coherent cone; noncontextual iff (eta1^A eta1^B, eta2^A eta2^B) in R2 = conv(Gamma, mirror image, (0,-4/5)), Gamma(s) = ((2/3)s(2-s), (2/5)s^2), 0 <= s <= 2.', 'Sec. IV, Thm 4; App. C', 'exact', [cs.cert_region_R2_formulas]),
 R('P2', ['p-one', 's-iso1'], 'm-ncom', 'implies', 'Explicit finite models at extreme points of R2, including the alignment-only point (0, 8/5).', 'App. D', 'exact', [cs.cert_finite_models]),
 R('P3', ['p-one', 's-iso1', 'w-region1'], 'e-ctx', 'equiv', 'Isotropic state of visibility v: products scale by v; two ideal W decays are contextual iff v > 5/8 (entangled iff v > 1/4); with one Z -> l+ l- decay on a side the data are noncontextual for every v.', 'Sec. IV, Cor. 4', 'compose'),
 R('P6', ['p-one', 's-iso1', 'w-region1'], 'e-ctx', 'derives', 'Critical visibilities for pairs of kernels: 5/8 (W W), 2/5 (two decays into pseudoscalar pairs; one such decay with a dilepton or W decay); dilepton pairs, W Z and Z Z are noncontextual for every visibility.', 'Sec. IV, Table II', 'exact', [cx.cert_pair_thresholds]),
 R('P4', ['w-region1', 'w-ncineq'], 'e-ctx', 'witness', 'Brute-force LP for the pair region.', 'App. E', 'numeric', [lpR2]),
 R('P5', ['w-region1', 'w-ncineq'], 'e-ctx', 'witness', 'Refinement of the three LP directions that deviated by more than 0.5 per cent: the deviations shrink with the grids.', 'App. E', 'numeric', [cn.cert_lp_refine]),
 # ---- general spin
 R('G1', ['p-decay', 's-spin', 'w-kappa'], 'e-ctx', 'implies', 'If |kappa_1(w)| > xi_2j the spin-j polarimeter is contextual on all states.', 'Sec. IV, Thm 5', 'compose'),
 R('G2', ['w-kappa'], 'w-kappa', 'derives', 'xi_1 = 1/3, xi_2 = 1/sqrt3, xi_3 = (1+sqrt6)/5, xi_4 = sqrt(3/5); extremal polynomials attain them.', 'Sec. IV', 'exact', [cs.cert_gauss_nodes]),
 R('G3', ['p-decay', 's-spin'], 'm-ncom', 'implies', 'The bound is the supremum: the kernel D* = (d/4pi) int Q*(q)|q><q| dq, Q* the extremal polynomial, is noncontextual with kappa_1 = xi_2j when its multipole ratios are nonzero (checked for j <= 4); in general by a perturbation.', 'Sec. IV, Thm 5', 'compose'),
 R('G5', ['m-ncom', 'o-ang2'], 'w-kappa', 'implies', 'Pairs of arbitrary spins: a noncontextual model has the form p = sum_l r_l(qA) s_l(qB) with nonnegative polynomials of degree 2jA, 2jB (Prop. 2), hence || <qA qB^T> ||_1 <= xi(2jA) xi(2jB) (Thm 5c).', 'Sec. IV, Prop. 2, Thm 5(c)', 'compose'),
 R('G7', ['p-decay'], 'w-kappa', 'derives', 'First-moment bound behind Thm 5: a nonnegative polynomial of degree n on the sphere with unit integral has first moment at most xi_n; random non-zonal instances stay below, the extremal zonal polynomial attains it.', 'Sec. IV, Thm 5', 'numeric', [cx.cert_first_moment_bound], scope='instance: degrees 1 to 8'),
 R('G6', ['w-kappa', 'w-rawppt', 'w-region1'], 'w-kappa', 'derives', 'Consistency of the first-moment inequality with the exact criteria: ||c||_1 <= 1 for spin 1/2; v |eta1A eta1B| <= 2/3, the largest abscissa of R2, for the spin-1 pair.', 'Sec. IV', 'numeric', [cx.cert_pair_dipole_bound]),
 R('G4', ['w-kappa', 'w-ncineq'], 'e-ctx', 'witness', 'LP value of max |<J>| over operators with nonnegative Husimi function and positivity of the attaining kernels, j <= 4.', 'App. E', 'numeric', [cn.cert_general_j], scope='instance: j <= 4'),
 # ---- applications
 R('A1', ['s-ttbar', 'p-half'], 'o-D', 'import', 'ATLAS: D = -0.537 +- 0.002 +- 0.019 (particle level, 340 < m_tt < 380 GeV), folded bound -0.322 +- 0.009; CMS: D = -0.480 +0.026 -0.029 (parton level).', 'Sec. V', 'import', refs=['ATLAS, Nature 633, 542 (2024)', 'CMS, Rep. Prog. Phys. 87, 117801 (2024)']),
 R('A2', ['o-D', 's-ttbar'], 'e-ctx', 'implies', 'Arithmetic on the quoted numbers: 10.2 sigma (ATLAS, with its folded bound) and 5.1 sigma (CMS, bound -1/3).', 'Sec. V', 'exact', [cn.cert_top_pair_numbers]),
 R('A3', ['s-LLbar', 'p-half'], 'o-ang2', 'import', 'Joint angular distribution of e+e- -> J/psi -> Lambda Lambdabar and the fitted parameters alpha_psi, Delta Phi, alpha_-, alpha_+.', 'Sec. V', 'import', refs=['Faldt, Kupsc, PLB 772, 16 (2017)', 'BESIII, PRL 129, 131801 (2022)']),
 R('A4', ['s-LLbar', 'w-rawppt'], 'e-ctx', 'implies', 'With the fitted form: the production state is a valid rank-2 state; ||c||_1 = 1.108 at 90 degrees; rho_raw fails the test for |cos theta| < 0.517 (46% of events).', 'Sec. V', 'numeric', [cn.cert_lambda_pairs]),
 R('A5', ['m_cc', 'p-half'], 'p-half', 'import', 'Leading-order and QCD-corrected analysing powers of top decay products.', 'Sec. V, Table I', 'import', refs=['Brandenburg, Si, Uwer, PLB 539, 235 (2002)', 'Tweedie, PRD 90, 094010 (2014)']),
 R('A6', ['m_va', 'u_mh'], 'p-half', 'import', 'tau -> pi nu: kappa = 1; tau -> rho nu (rho direction): (m_tau^2 - 2 m_rho^2)/(m_tau^2 + 2 m_rho^2) = 0.45.', 'Sec. V, Table I', 'import', [cx.cert_tau_rho], refs=['Tsai, PRD 4, 2821 (1971)']),
 R('A7', ['m_nc', 'u_m1'], 'p-one', 'import', 'Z -> f fbar: kernel (eta1, eta2) = (A_f, 1) for massless fermions; W -> l nu: (+-1, 1); vector -> two pseudoscalars: (0, -2).', 'Sec. V, Table II', 'import', refs=['PDG 2026 (A_e = 0.1515 +- 0.0019)']),
 R('A8', ['u_m1', 'p-one', 'w-region1'], 'e-ctx', 'implies', 'Fermion-pair decays of vector mesons (direction only): J/psi -> Lambda Lambdabar has w0 = 0.151 < 1/5 (contextual on all states); J/psi -> Sigma+ Sigmabar- sits at the boundary w0 = 3/5 within about one standard deviation; psi(2S) -> tau tau lies inside the window.', 'Sec. V', 'numeric', [cn.cert_vector_pair_kernels], refs=['BESIII, PRL 129, 131801 (2022)', 'BESIII, PRL 125, 052004 (2020)']),
 # ---- relation to the released edges
 R('H11', ['s-sep', 'p-half'], 'm-ncom', 'implies', 'Separable pair states give noncontextual decay data for all analysing powers: the local scaling maps preserve separability.', 'Sec. III', 'compose'),
 R('X3', ['m-quantum', 'm_A'], 'p-decay', 'defines', 'The polarimeter is a POVM of quantum theory on C^(2j+1); the released frame node m_A (GEN_HEP) and model node m-quantum (GEN_GPT_Level) are glued here.', 'Sec. II', 'definition'),
 R('X1', ['e-ctx'], 'm-classical', 'forbids', 'Released edge A5 (simplex embedding) is the definition used here.', 'Sec. II', 'import', refs=['GEN_GPT_Level v2.6: A5']),
 R('X2', ['s-ent', 'p-decay'], 'e-ctx', 'necessary', 'Released edge A8 (contextuality is a precondition for entanglement) with the measurement fixed to the decay polarimeter: holds for |kappa_A kappa_B| = 1 and fails otherwise (H8).', 'Sec. III', 'compose', refs=['GEN_GPT_Level v2.6: A8']),
]

CLAIMS = [
 {'id': 'C1', 'text': 'A decay is one fixed covariant measurement; V-A decays give sharp effects for the antifermion direction and |kappa| = 1/3 for the direction-only leptonic three-body decay.', 'routes': ['DV1', 'DV2', 'DV3', 'DV6']},
 {'id': 'C2', 'text': 'With one setting per side Bell and steering tests are empty, and the recorded-outcome model is not noncontextual.', 'routes': ['FW2', 'FW3', 'FW4', 'FW5']},
 {'id': 'C3', 'text': 'Spin 1/2, one particle: noncontextual iff P|kappa| <= 1/3.', 'routes': ['FW1', 'H1', 'H2']},
 {'id': 'C4', 'text': 'Two spin-1/2 particles: the joint decay data are noncontextual iff rho_raw and its partial transpose are positive semidefinite; for unpolarised pairs iff ||c||_1 <= 1; |D| > 1/3 implies contextual data.', 'routes': ['FW1', 'DV9', 'H3', 'H4', 'H12', 'H5', 'H6', 'H7', 'H10']},
 {'id': 'C5', 'text': 'Spin 1, one particle: noncontextual iff (eta1, eta2) in R (eta2 != 0).', 'routes': ['FW1', 'FW6', 'DV7', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6', 'P5']},
 {'id': 'C6', 'text': 'Maximally entangled spin-1 pair with one decay on each side: noncontextual iff the product of ratios lies in R2; ideal W pairs need visibility above 5/8.', 'routes': ['FW1', 'FW6', 'DV7', 'V1', 'V2', 'P1', 'P2', 'P3', 'P6', 'P4', 'P5']},
 {'id': 'C7', 'text': 'Spin j: the largest vector analysing power of a noncontextual polarimeter is the largest Gauss or Gauss-Radau node xi_2j; for pairs || <qA qB^T> ||_1 <= xi(2jA) xi(2jB).', 'routes': ['FW1', 'FW6', 'G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7']},
 {'id': 'C8', 'text': 'Top pairs: the measured D certifies contextual lepton-direction data at the significance quoted for entanglement, without the value of the analysing power.', 'routes': ['H6', 'A1', 'A2']},
 {'id': 'C9', 'text': 'Hyperon pairs: with the fitted BESIII parameters the proton-antiproton angular data are contextual for |cos theta| < 0.517.', 'routes': ['H3', 'H4', 'DV9', 'A3', 'A4']},
 {'id': 'C10', 'text': 'The b-quark direction is a nonclassical top polarimeter iff m_t > 2 m_W; the neutrino direction sits within about one percent of the boundary.', 'routes': ['H1', 'H2', 'DV4', 'DV5']},
 {'id': 'C11', 'text': 'Vector mesons: the baryon direction of J/psi -> Lambda Lambdabar is a nonclassical polarimeter; J/psi -> Sigma+ Sigmabar- sits at the boundary; psi(2S) -> tau tau is classical.', 'routes': ['V3', 'V5', 'A7', 'A8']},
]

