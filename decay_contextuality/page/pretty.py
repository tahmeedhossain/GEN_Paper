"""Light transliteration of the ASCII statements of the encoding into readable text for the page."""
import re
SUB = str.maketrans('0123456789+-', '₀₁₂₃₄₅₆₇₈₉₊₋')
SUP = str.maketrans('0123456789+-', '⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻')
def pretty(s):
    if not s: return s
    t = s
    t = t.replace('<=', '≤').replace('>=', '≥').replace('!=', '≠').replace('+-', '±').replace(' -> ', ' → ')
    t = re.sub(r'\bsqrt\(([^()]+)\)', r'√(\1)', t); t = re.sub(r'\bsqrt(\d+)', r'√\1', t)
    greek = {'kappa': 'κ', 'eta': 'η', 'xi': 'ξ', 'alpha': 'α', 'rho': 'ρ', 'sigma': 'σ', 'theta': 'θ', 'tau': 'τ', 'Lambda': 'Λ', 'Lambdabar': 'Λ̄',
             'psi': 'ψ', 'Phi': 'Φ', 'Psi': 'Ψ', 'mu': 'μ', 'nu': 'ν', 'gamma': 'γ', 'Gamma': 'Γ', 'pi': 'π', 'Delta': 'Δ', 'Sigma': 'Σ', 'Sigmabar': 'Σ̄', 'lambda': 'λ'}
    for k in sorted(greek, key=len, reverse=True):
        t = re.sub(r'(?<![A-Za-z])%s(?![a-zA-Z])' % k, greek[k], t)
    t = re.sub(r'\b4π\b', '4π', t)
    t = re.sub(r'η([12])', lambda m: 'η' + m.group(1).translate(SUB), t)
    t = re.sub(r'\bR2\b', 'R₂', t); t = re.sub(r'\bw0\b', 'w₀', t); t = t.replace('κ_1', 'κ₁').replace('η_1', 'η₁').replace('η_2j', 'η₂ⱼ')
    t = re.sub(r'ξ_2j([AB]?)', r'ξ₂ⱼ\1', t); t = re.sub(r'ξ_(\d)', lambda m: 'ξ' + m.group(1).translate(SUB), t)
    t = re.sub(r'\^2\b', '²', t); t = re.sub(r'\^T\b', 'ᵀ', t); t = re.sub(r'\^-1\b', '⁻¹', t); t = re.sub(r'\^dagger', '†', t)
    t = re.sub(r'\^\(2j\+1\)', '⁽²ʲ⁺¹⁾', t)
    t = t.replace('||', '‖').replace('‖_1', '‖₁').replace(' (x) ', ' ⊗ ').replace(' x ', ' ⊗ ').replace('(+)', '⊕')
    t = t.replace('ξ(2jA)', 'ξ(2j_A)').replace('ξ(2jB)', 'ξ(2j_B)')
    t = t.replace('J/ψ', 'J/ψ').replace('ψ(2S)', 'ψ(2S)')
    return t
if __name__ == '__main__':
    import json, sys
    d = json.load(open('out/results.json'))
    for r in d['routes'][:63]:
        print(r['id'], '|', pretty(r['statement'])[:260])

