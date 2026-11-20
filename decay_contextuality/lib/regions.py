"""Closed forms claimed in the paper (spin-1 regions), kept in one place."""
import numpy as np

def h_R(a, b):
    """Support function of R = conv(ellipse 3x^2+25(y-1/5)^2<=1  U  {(0,-4/5)})."""
    ell = b / 5 + np.sqrt(b * b / 25 + a * a / 3)
    return max(ell, -0.8 * b)

def in_R(x, y, tol=0.0):
    """Membership in R via the explicit description: ellipse, or the triangle-like cap
    between the apex (0,-4/5) and the tangent points (+-2*sqrt2/5, 4/25)."""
    if 3 * x * x + 25 * (y - 0.2) ** 2 <= 1 + tol:
        return True
    xt, yt = 2 * np.sqrt(2) / 5, 4 / 25
    if -0.8 - tol <= y <= yt + tol:
        return abs(x) <= xt * (y + 0.8) / (yt + 0.8) + tol
    return False

def radial_R(theta, n=4000):
    """Largest t with t(cos,sin) in R, from the support function."""
    c, s = np.cos(theta), np.sin(theta)
    phis = np.linspace(0, 2 * np.pi, n, endpoint=False)
    best = np.inf
    for ph in phis:
        a, b = np.cos(ph), np.sin(ph)
        den = a * c + b * s
        if den > 1e-9:
            best = min(best, h_R(a, b) / den)
    return best

def h_R2(a, b):
    """Support function of R2 = conv(Gamma U mirror U {(0,-4/5)}),
    Gamma(s) = ((2/3)s(2-s), (2/5)s^2), s in [0,2]."""
    a = abs(a)
    # maximise phi(s) = (2a/3)s(2-s) + (2b/5)s^2 on [0,2]
    cands = [0.0, 2.0]
    den = (2 * a / 3 - 2 * b / 5)
    if abs(den) > 1e-14:
        s0 = (2 * a / 3) / den
        if 0 <= s0 <= 2:
            cands.append(s0)
    phi = max((2 * a / 3) * s * (2 - s) + (2 * b / 5) * s * s for s in cands)
    return max(phi, -0.8 * b)

def radial_R2(theta, n=4000):
    c, s = np.cos(theta), np.sin(theta)
    best = np.inf
    for ph in np.linspace(0, 2 * np.pi, n, endpoint=False):
        a, b = np.cos(ph), np.sin(ph)
        den = a * c + b * s
        if den > 1e-9:
            best = min(best, h_R2(a, b) / den)
    return best

