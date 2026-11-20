"""Simplex-embedding LP for a discretised qubit-type fragment.

Fragment in R^4 with pairing <e, s> = e.s :
    states   s = (1, v),  v in a finite set of points of R^3 (need not lie on a sphere),
    effects  e ~ (1, k u), u in a finite set of unit vectors (sharpness k).
Noncontextual  <=>  identity = sum_{a,b} X_ab  sigma_b (x) g_a ,  X >= 0,
with g_a the extreme rays of the dual of the state cone and sigma_b the extreme rays of the
dual of the effect cone (criterion of Schmid et al. / Gitton-Woods / Selby et al. LP).
Because a finite subset of states and effects enlarges both dual cones,
    LP infeasible  ==>  the continuous fragment is contextual   (one-sided, rigorous up to LP tolerance).
"""
import numpy as np
from scipy.spatial import ConvexHull
from scipy.optimize import linprog


def dual_rays_of_points(V):
    """Extreme rays g=(g0, gvec) of {g : g0 + gvec.v >= 0 for all v in V} when conv(V) is 3-dimensional:
    one ray per facet of conv(V)."""
    hull = ConvexHull(V)
    eq = hull.equations                      # n.x + off <= 0 inside
    eq = np.unique(np.round(eq, 10), axis=0)
    return np.hstack([-eq[:, 3:4], -eq[:, :3]])     # g0 = -off, gvec = -n


def nc_lp(V, U, k=1.0, return_res=False):
    """V: (Ns,3) data Bloch vectors of states; U: (Ne,3) unit vectors, effects (1, k u).
    Returns True if the LP is feasible (sub-fragment noncontextual)."""
    G = dual_rays_of_points(V)                                   # g_a(s) = g0 + gvec.v >= 0
    S = dual_rays_of_points(k * U)                               # sigma_b = (s0, svec): s0 + svec.(k u) >= 0
    na, nb = len(G), len(S)
    # identity_{ij} = sum_ab X_ab S[b,i] G[a,j]
    A = np.einsum('bi,aj->ijab', S, G).reshape(16, na * nb)
    res = linprog(np.zeros(na * nb), A_eq=A, b_eq=np.eye(4).reshape(-1), bounds=(0, None), method='highs')
    ok = (res.status == 0)
    return (ok, res, G, S) if return_res else ok

