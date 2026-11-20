"""Builds refs.bib from the Crossref records (crossref_lookup*.json) and a short list of hand-entered items
(arXiv e-prints, books, software, repositories) whose metadata were checked on the arXiv listing or the publisher page."""
import json, re, os
HERE = os.path.dirname(os.path.abspath(__file__))
cr = json.load(open(os.path.join(HERE, 'crossref_lookup.json'))); cr.update(json.load(open(os.path.join(HERE, 'crossref_lookup2.json'))))
skip = {'pdg2026', 'marvian2020', 'fucci2026', 'bechtle2025', 'low2025', 'jokinen2026', 'cvxpy', 'kasday1971', 'clarabel_old', 'delsarte1977'}
collab = {'atlas2024': '{ATLAS Collaboration}', 'cms2024': '{CMS Collaboration}', 'cms2024ljets': '{CMS Collaboration}', 'besiii2022': '{BESIII Collaboration}',
          'besiii2025': '{BESIII Collaboration}', 'besiii2020sigma': '{BESIII Collaboration}', 'pdg2024': 'Navas, S. and others'}
collab_field = {'pdg2024': 'Particle Data Group'}
journal_fix = {'Nat Commun': 'Nat. Commun.', 'Found Phys': 'Found. Phys.', 'Geom Dedicata': 'Geom. Dedicata', 'Nat Methods': 'Nat. Methods', 'J. High Energ. Phys.': 'J. High Energy Phys.',
               'Physics Letters B': 'Phys. Lett. B', 'Physics Letters A': 'Phys. Lett. A', 'Annals of Physics': 'Ann. Phys. (N.Y.)', 'Progress in Particle and Nuclear Physics': 'Prog. Part. Nucl. Phys.',
               'Mathematics of OR': 'Math. Oper. Res.', 'Quantum': 'Quantum', 'J. Phys. A: Gen. Phys.': 'J. Phys. A', 'PeerJ Computer Science': 'PeerJ Comput. Sci.',
               'Lecture Notes in Computer Science': 'Lect. Notes Comput. Sci.'}
def clean(t):
    t = re.sub(r'<[^>]+>', ' ', t or ''); t = re.sub(r'\$\$[^$]*\$\$', ' ', t); t = re.sub(r'\s+', ' ', t).strip()
    return t.replace('&', '\\&').replace('%', '\\%').replace('#', '\\#').replace('_', '\\_')
def tex(s):
    rep = {'á': "{\\'a}", 'é': "{\\'e}", 'í': "{\\'\\i}", 'ó': "{\\'o}", 'ö': '{\\"o}', 'ü': '{\\"u}', 'ä': '{\\"a}', 'ī': '{\\=\\i}', 'ì': '{\\`\\i}', 'è': '{\\`e}', 'ø': '{\\o}',
           'ł': '{\\l}', 'ń': "{\\'n}", 'ç': '{\\c c}', 'ñ': '{\\~n}', '’': "'", '–': '--', '—': '---', 'Ø': '{\\O}', 'ã': '{\\~a}', 'å': '{\\aa}', 'Å': '{\\AA}', 'ý': "{\\'y}", 'š': '{\\v s}', 'č': '{\\v c}',
           'ž': '{\\v z}', 'ř': '{\\v r}', 'ê': '{\\^e}', 'ô': '{\\^o}', 'â': '{\\^a}', 'ő': '{\\H o}', 'Č': '{\\v C}', 'Ž': '{\\v Z}', 'Š': '{\\v S}', 'É': "{\\'E}", 'ú': "{\\'u}", 'ě': '{\\v e}', 'ą': '{\\k a}', 'ę': '{\\k e}', 'ż': '{\\.z}', 'ś': "{\\'s}", '�': '{\\"o}'}
    return ''.join(rep.get(ch, ch) for ch in s)
title_fix = {
 'besiii2020sigma': r'$\Sigma^+$ and $\bar\Sigma^-$ polarization in the $J/\psi$ and $\psi(3686)$ decays',
 'faldt2017': r'Hadronic structure functions in the $e^+e^-\to\bar\Lambda\Lambda$ reaction',
 'leeyang1957': r'General Partial Wave Analysis of the Decay of a Hyperon of Spin 1/2',
 'tornqvist1981': r'Suggestion for {E}instein-{P}odolsky-{R}osen experiments using reactions like $e^+e^-\to\Lambda\bar\Lambda\to\pi^-p\pi^+\bar p$',
 'besiii2022': r'Precise Measurements of Decay Parameters and $CP$ Asymmetry with Entangled $\Lambda$-$\bar\Lambda$ Pairs',
 'besiii2025': r'Test of local realism via entangled $\Lambda\bar\Lambda$ system',
 'cms2024': r'Observation of quantum entanglement in top quark pair production in proton-proton collisions at $\sqrt{s}=13$ {TeV}',
 'cms2024ljets': r'Measurements of polarization and spin correlation and observation of entanglement in top quark pairs using lepton+jets events from proton-proton collisions at $\sqrt{s}=13$ {TeV}',
 'tsai1971': r'Decay Correlations of Heavy Leptons in $e^+ + e^- \to l^+ + l^-$',
 'michel1950': r'Interaction between Four Half-Spin Particles and the Decay of the $\mu$-Meson',
}
title_fix['li2024'] = 'Can Bell inequalities be tested via scattering cross-section at colliders?'
author_fix = {'horodecki1996t': r'Horodecki, Ryszard and Horodecki, Micha{\l}', 'horodeckiEB2003': r'Horodecki, Micha{\l} and Shor, Peter W. and Ruskai, Mary Beth'}
out = []
for key, r in cr.items():
    if key in skip or 'error' in r or not r.get('doi'): continue
    if key in collab: au = collab[key]
    else:
        names = [a.strip().rstrip(',') for a in r['authors'] if a.strip(', ')]
        au = ' and '.join(names) + (' and others' if r.get('n_authors', 0) > len(names) else '')
    j = r.get('short') or r.get('journal') or ''; j = journal_fix.get(j, j)
    pages = r.get('article') or (r.get('page') or '').split('-')[0]
    if key == 'ashby2023': pages = '020'; r['volume'] = '05'
    if key == 'bernreuther2015': pages = '026'; r['volume'] = '12'
    if key == 'abel2025': pages = '067'; r['volume'] = '08'
    if key == 'z3': pages = '337'; r['volume'] = '4963'
    if key == 'highs': r['year'] = 2018
    if key in author_fix: au = author_fix[key]
    if key == 'mazurek2016': pages = '11780'
    ttl = title_fix[key] if key in title_fix else tex(clean(r.get('title')))
    f = ['  author = {%s}' % (au if key in author_fix else tex(au))] + (['  collaboration = {%s}' % collab_field[key]] if key in collab_field else []) + [ '  title = {{%s}}' % ttl, '  journal = {%s}' % tex(j)]
    if r.get('volume'): f.append('  volume = {%s}' % r['volume'])
    if pages: f.append('  pages = {%s}' % pages)
    f.append('  year = {%s}' % r['year']); f.append('  doi = {%s}' % r['doi'])
    out.append('@article{%s,\n%s\n}' % (key, ',\n'.join(f)))
manual = r'''
@misc{marvian2020,
  author = {Marvian, Iman},
  title = {{Inaccessible information in probabilistic models of quantum systems, non-contextuality inequalities and noise thresholds for contextuality}},
  year = {2020}, eprint = {2003.05984}, archivePrefix = {arXiv}, primaryClass = {quant-ph}
}
@misc{fucci2026,
  author = {Fucci, Danilo M. and Orthey, Alexandre C. and Barr, Alan J. and Timpson, Christopher G.},
  title = {{Bell tests for collider decay processes}},
  year = {2026}, eprint = {2609.09294}, archivePrefix = {arXiv}
}
@misc{bechtle2025,
  author = {Bechtle, Philip and Breuning, Cedric and Dreiner, Herbi K. and Duhr, Claude},
  title = {{A critical appraisal of tests of locality and of entanglement versus non-entanglement at colliders}},
  year = {2025}, eprint = {2507.15947}, archivePrefix = {arXiv}
}
@misc{low2025,
  author = {Low, Matthew},
  title = {{Addressing Local Realism through {B}ell Tests at Colliders}},
  year = {2025}, eprint = {2508.10979}, archivePrefix = {arXiv}
}
@misc{jokinen2026,
  author = {Jokinen, Pauli and Weilenmann, Mirjam and Pl{\'a}vala, Martin and Pellonp{\"a}{\"a}, Juha-Pekka and Kiukas, Jukka and Uola, Roope},
  title = {{Generalised contextuality of continuous variable quantum theory can be revealed with a single projective measurement}},
  year = {2026}, eprint = {2601.14067}, archivePrefix = {arXiv}
}
@article{pdg2026,
  author = {Takahashi, F. and others},
  collaboration = {Particle Data Group},
  title = {{Review of Particle Physics}},
  journal = {Int. J. Mod. Phys. A}, volume = {41}, pages = {2630011}, year = {2026}
}
@article{cvxpy,
  author = {Diamond, Steven and Boyd, Stephen},
  title = {{{CVXPY}: A {P}ython-embedded modeling language for convex optimization}},
  journal = {J. Mach. Learn. Res.}, volume = {17}, number = {83}, pages = {1}, year = {2016}
}
@book{gautschi2004,
  author = {Gautschi, Walter},
  title = {{Orthogonal Polynomials: Computation and Approximation}},
  publisher = {Oxford University Press}, address = {Oxford}, year = {2004}
}
@book{klein1956,
  author = {Klein, Felix},
  title = {{Lectures on the Icosahedron and the Solution of Equations of the Fifth Degree}},
  publisher = {Dover}, address = {New York}, year = {1956}
}
@misc{genhep,
  author = {Hossain, Tahmeed},
  title = {{A growing concept graph of particle physics: states, models and observables from one-particle quantum mechanics to the electroweak Standard Model}},
  howpublished = {\url{https://github.com/tahmeedhossain/GEN_HEP}}, note = {version 1.2, commit 4258f6e}, year = {2026}
}
@misc{gengpt,
  author = {Hossain, Tahmeed},
  title = {{Nonclassicality Network: a signed theorem graph for quantum foundations}},
  howpublished = {\url{https://github.com/tahmeedhossain/GEN_GPT_Level}}, note = {version 2.6, commit e18fa8c}, year = {2026}
}
@misc{genqrt,
  author = {Hossain, Tahmeed},
  title = {{Quantum Resource Network: a role-resolved typed graph of thirteen quantum resource theories}},
  howpublished = {\url{https://github.com/tahmeedhossain/GEN_QRT_Level}}, note = {version 1.2, commit 198ca02}, year = {2026}
}
'''
open(os.path.join(HERE, 'refs.bib'), 'w').write('% generated by make_bib.py\n' + '\n'.join(out) + '\n' + manual)
print(len(out), 'Crossref entries +', manual.count('@'), 'manual entries')

