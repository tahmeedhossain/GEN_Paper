import json, sys, time, urllib.parse, urllib.request
items = [
 ('zhang2025prx', 'doi', '10.1103/vqfz-wzjg'),
 ('besiii2025', 'doi', '10.1038/s41467-025-59498-4'),
 ('pdg2026', 'q', 'Takahashi Review of Particle Physics International Journal of Modern Physics A 41 2630011 2026'),
 ('tornqvist1981', 'q', 'Tornqvist Suggestion for Einstein-Podolsky-Rosen experiments using reactions like e+e- -> Lambda anti-Lambda Foundations of Physics 11 171'),
 ('leeyang1957', 'q', 'Lee Yang General partial wave analysis of the decay of a hyperon of spin 1/2 Physical Review 108 1645'),
 ('bernreuther2015', 'doi', '10.1007/JHEP12(2015)026'),
 ('polik2007', 'q', 'Polik Terlaky A survey of the S-lemma SIAM Review 49 371'),
 ('marvian2020', 'q', 'Marvian Inaccessible information in probabilistic models of quantum systems, non-contextuality inequalities and noise thresholds for contextuality'),
 ('delsarte1977', 'q', 'Delsarte Goethals Seidel Spherical codes and designs Geometriae Dedicata 6 363'),
 ('michel1950', 'q', 'Michel Interaction between four half-spin particles and the decay of the mu-meson Proceedings of the Physical Society A 63 514'),
 ('clarabel', 'q', 'Goulart Chen Clarabel: An interior-point solver for conic programs with quadratic objectives'),
 ('fucci2026', 'q', 'Fucci Orthey Barr Timpson Bell tests for collider decay processes'),
 ('abel2025', 'q', 'Abel Dreiner Sengupta Ubaldi Colliders are testing neither locality via Bell inequality nor entanglement versus non-entanglement'),
 ('bechtle2025', 'q', 'Bechtle Breuning Dreiner Duhr A critical appraisal of tests of locality and of entanglement versus non-entanglement at colliders'),
 ('low2025', 'q', 'Low Bell inequality colliders local hidden variable arXiv 2508.10979'),
 ('fabbrichesi2025bell', 'q', 'Fabbrichesi Floreanini Marzola About testing Bell locality at colliders'),
 ('jokinen2026', 'q', 'Generalised contextuality of continuous variable quantum theory can be revealed with a single projective measurement'),
 ('radcliffe1971', 'q', 'Radcliffe Some properties of coherent spin states Journal of Physics A 4 313'),
 ('cms2024ljets', 'q', 'CMS Measurements of polarization and spin correlation and observation of entanglement in top quark pairs using lepton+jets events'),
 ('kinoshita1957', 'q', 'Kinoshita Sirlin Muon decay with parity nonconserving interactions and radiative corrections in the two-component theory Physical Review 107 593'),
 ('horodeckiEB2003', 'q', 'Horodecki Shor Ruskai Entanglement breaking channels Reviews in Mathematical Physics 15 629'),
 ('spekkens2008', 'q', 'Spekkens Negativity and contextuality are equivalent notions of nonclassicality Physical Review Letters 101 020401'),
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
               'authors': [(a.get('family') or a.get('name') or '') + ', ' + (a.get('given') or '') for a in au[:8]], 'n_authors': len(au), 'type': m.get('type')}
    except Exception as e:
        rec = {'error': repr(e)[:150]}
    out[key] = rec
    print(key, '|', rec.get('year'), '|', rec.get('short') or rec.get('journal'), rec.get('volume'), rec.get('page') or rec.get('article'), '|',
          (rec.get('title') or rec.get('error', ''))[:95].replace('\n', ' '), '|', '; '.join(rec.get('authors', [])[:4]), '| n=%s' % rec.get('n_authors'), '|', rec.get('doi'), '|', rec.get('type'), flush=True)
    time.sleep(0.15)
json.dump(out, open('crossref_lookup2.json', 'w'), indent=1)

