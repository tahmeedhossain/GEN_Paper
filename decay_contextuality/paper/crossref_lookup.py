import json, sys, time, urllib.parse, urllib.request
items = [
 ('spekkens2005', 'doi', '10.1103/PhysRevA.71.052108'),
 ('schmid2021', 'doi', '10.1103/PRXQuantum.2.010331'),
 ('gitton2022', 'doi', '10.22331/q-2022-06-07-732'),
 ('selby2023frag', 'doi', '10.1103/PhysRevA.107.062203'),
 ('selby2023incomp', 'doi', '10.1103/PhysRevLett.130.230201'),
 ('selby2024lp', 'doi', '10.1103/PhysRevLett.132.050202'),
 ('plavala2024', 'doi', '10.1103/PhysRevLett.132.100201'),
 ('jokinen2024', 'doi', '10.1103/PhysRevLett.133.240201'),
 ('mazurek2016', 'q', 'Mazurek Pusey Kunjwal Resch Spekkens An experimental test of noncontextuality without unphysical idealizations'),
 ('afik2021', 'q', 'Afik de Nova Entanglement and quantum tomography with top quarks at the LHC'),
 ('atlas2024', 'q', 'ATLAS Observation of quantum entanglement with top quarks at the ATLAS detector Nature 2024'),
 ('cms2024', 'doi', '10.1088/1361-6633/ad7e4d'),
 ('barr2024', 'q', 'Barr Fabbrichesi Floreanini Gabrielli Marzola Quantum entanglement and Bell inequality violation at colliders'),
 ('abel1992', 'q', 'Abel Dittmar Dreiner Testing locality at colliders via Bell\'s inequality?'),
 ('li2024', 'doi', '10.1140/epjc/s10052-024-13584-x'),
 ('fabbrichesi2025pra', 'doi', '10.1103/9bvc-2w4m'),
 ('fabbrichesi2025prd', 'doi', '10.1103/22zl-ltxm'),
 ('ashby2023', 'doi', '10.1007/JHEP05(2023)020'),
 ('brandenburg2002', 'doi', '10.1016/S0370-2693(02)02098-1'),
 ('tweedie2014', 'doi', '10.1103/PhysRevD.90.094010'),
 ('faldt2017', 'doi', '10.1016/j.physletb.2017.06.011'),
 ('besiii2022', 'doi', '10.1103/PhysRevLett.129.131801'),
 ('pdg2024', 'q', 'Navas Review of particle physics Phys. Rev. D 110 030001 2024'),
 ('tsai1971', 'q', 'Tsai Decay correlations of heavy leptons in e+ e- -> l+ l- Phys Rev D 4 2821'),
 ('horodecki1996t', 'q', 'Horodecki Horodecki Information-theoretic aspects of inseparability of mixed states Phys Rev A 54 1838'),
 ('peres1996', 'q', 'Peres Separability criterion for density matrices Phys Rev Lett 77 1413'),
 ('horodecki1996ppt', 'q', 'Horodecki Separability of mixed states: necessary and sufficient conditions Physics Letters A 223'),
 ('horodecki1999', 'q', 'Horodecki Horodecki Reduction criterion of separability and limits for a class of distillation protocols'),
 ('ruskai2003', 'q', 'Ruskai Qubit entanglement breaking channels Reviews in Mathematical Physics 15 643'),
 ('sturm2003', 'q', 'Sturm Zhang On cones of nonnegative quadratic functions Mathematics of Operations Research 28'),
 ('giraud2008', 'q', 'Giraud Braun Braun Classicality of spin states Phys Rev A 78 042112'),
 ('bohnet2016', 'q', 'Bohnet-Waldraff Braun Giraud Partial transpose criteria for symmetric states Phys Rev A 94 042343'),
 ('jacob1959', 'q', 'Jacob Wick On the general theory of collisions for particles with spin Annals of Physics 7 404'),
 ('wiseman2007', 'q', 'Wiseman Jones Doherty Steering, entanglement, nonlocality, and the Einstein-Podolsky-Rosen paradox'),
 ('brunner2014', 'q', 'Brunner Cavalcanti Pironio Scarani Wehner Bell nonlocality Rev Mod Phys 86 419'),
 ('sympy2017', 'q', 'Meurer SymPy: symbolic computing in Python PeerJ Computer Science'),
 ('z3', 'q', 'de Moura Bjorner Z3: An efficient SMT solver TACAS 2008'),
 ('cvxpy', 'q', 'Diamond Boyd CVXPY: A Python-embedded modeling language for convex optimization JMLR'),
 ('scipy', 'q', 'Virtanen SciPy 1.0: fundamental algorithms for scientific computing in Python Nature Methods'),
 ('highs', 'q', 'Huangfu Hall Parallelizing the dual revised simplex method Mathematical Programming Computation'),
 ('kunjwal2019', 'q', 'Kunjwal Lostaglio Pusey Anomalous weak values and contextuality: robustness, tightness, and imaginary parts'),
 ('pusey2018', 'q', 'Pusey Robust preparation noncontextuality inequalities in the simplest scenario Phys Rev A 98 022112'),
]
out = {}
for key, kind, val in items:
    try:
        if kind == 'doi':
            url = 'https://api.crossref.org/works/' + urllib.parse.quote(val, safe='/')
            m = json.load(urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'refcheck/1.0'}), timeout=40))['message']
        else:
            url = 'https://api.crossref.org/works?rows=1&query.bibliographic=' + urllib.parse.quote(val)
            m = json.load(urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'refcheck/1.0'}), timeout=40))['message']['items'][0]
        au = m.get('author', [])
        rec = {'doi': m.get('DOI'), 'title': (m.get('title') or [''])[0], 'journal': (m.get('container-title') or [''])[0],
               'short': (m.get('short-container-title') or [''])[0], 'volume': m.get('volume'), 'issue': m.get('issue'),
               'page': m.get('page'), 'article': m.get('article-number'), 'year': (m.get('issued', {}).get('date-parts') or [[None]])[0][0],
               'authors': [(a.get('family') or a.get('name') or '') + ', ' + (a.get('given') or '') for a in au[:8]], 'n_authors': len(au)}
    except Exception as e:
        rec = {'error': repr(e)[:150]}
    out[key] = rec
    print(key, '|', rec.get('year'), '|', rec.get('short') or rec.get('journal'), rec.get('volume'), rec.get('page') or rec.get('article'), '|',
          (rec.get('title') or rec.get('error', ''))[:70], '|', '; '.join(rec.get('authors', [])[:3]), '| n=%s' % rec.get('n_authors'), '|', rec.get('doi'), flush=True)
    time.sleep(0.15)
json.dump(out, open('crossref_lookup.json', 'w'), indent=1)

