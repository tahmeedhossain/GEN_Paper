"""
Exact arithmetic in the number field Q(sqrt2, i) and small tensor helpers.

An element is  a + b*sqrt2 + i*(c + d*sqrt2)  with a, b, c, d rational (Fractions).
All quantities of the entanglement-swapping experiment live in this field, so the
checks built on it are exact: no floating point, no tolerance.
The real-number model must only ever produce elements with c = d = 0; the helper
`is_real` is used to assert that.
"""
from fractions import Fraction as Fr
from itertools import product

import numpy as np


class Alg:
    __slots__ = ("a", "b", "c", "d")

    def __init__(self, a=0, b=0, c=0, d=0):
        self.a, self.b, self.c, self.d = Fr(a), Fr(b), Fr(c), Fr(d)

    # arithmetic -------------------------------------------------------------
    def __add__(self, o):
        o = _co(o)
        return Alg(self.a + o.a, self.b + o.b, self.c + o.c, self.d + o.d)

    __radd__ = __add__

    def __neg__(self):
        return Alg(-self.a, -self.b, -self.c, -self.d)

    def __sub__(self, o):
        return self + (-_co(o))

    def __rsub__(self, o):
        return _co(o) + (-self)

    def __mul__(self, o):
        o = _co(o)
        a, b, c, d = self.a, self.b, self.c, self.d
        e, f, g, h = o.a, o.b, o.c, o.d
        return Alg(a * e + 2 * b * f - c * g - 2 * d * h,
                   a * f + b * e - c * h - d * g,
                   a * g + 2 * b * h + c * e + 2 * d * f,
                   a * h + b * g + c * f + d * e)

    __rmul__ = __mul__

    def conj(self):
        return Alg(self.a, self.b, -self.c, -self.d)

    # predicates -------------------------------------------------------------
    def __eq__(self, o):
        o = _co(o)
        return (self.a, self.b, self.c, self.d) == (o.a, o.b, o.c, o.d)

    def __hash__(self):
        return hash((self.a, self.b, self.c, self.d))

    def is_zero(self):
        return self.a == 0 and self.b == 0 and self.c == 0 and self.d == 0

    def is_real(self):
        return self.c == 0 and self.d == 0

    def __float__(self):
        if not self.is_real():
            raise ValueError("not real")
        return float(self.a) + float(self.b) * 2 ** 0.5

    def __repr__(self):
        def part(x, y):
            s = []
            if x != 0:
                s.append(str(x))
            if y != 0:
                s.append(("" if y == 1 else "-" if y == -1 else str(y) + "*") + "√2")
            return "+".join(s).replace("+-", "-") if s else "0"
        re, im = part(self.a, self.b), part(self.c, self.d)
        if im == "0":
            return re
        if re == "0":
            return f"i({im})"
        return f"{re}+i({im})"


def _co(x):
    return x if isinstance(x, Alg) else Alg(x)


ZERO, ONE, IMAG = Alg(0), Alg(1), Alg(0, 0, 1)
SQ2, ISQ2 = Alg(0, 1), Alg(0, Fr(1, 2))          # sqrt2 and 1/sqrt2


def mat(rows):
    """Matrix (numpy object array) from nested lists of numbers / Alg."""
    return np.array([[_co(x) for x in r] for r in rows], dtype=object)


def vec(xs):
    return np.array([_co(x) for x in xs], dtype=object)


def kron(*ms):
    out = ms[0]
    for m in ms[1:]:
        r1, c1 = out.shape
        r2, c2 = m.shape
        new = np.empty((r1 * r2, c1 * c2), dtype=object)
        for i, j in product(range(r1), range(c1)):
            for k, l in product(range(r2), range(c2)):
                new[i * r2 + k, j * c2 + l] = out[i, j] * m[k, l]
        out = new
    return out


def kronv(*vs):
    out = vs[0]
    for v in vs[1:]:
        out = np.array([x * y for x in out for y in v], dtype=object)
    return out


def matmul(a, b):
    r, n = a.shape
    n2, c = b.shape
    assert n == n2
    out = np.empty((r, c), dtype=object)
    for i in range(r):
        for j in range(c):
            s = ZERO
            for k in range(n):
                x, y = a[i, k], b[k, j]
                if x.is_zero() or y.is_zero():
                    continue
                s = s + x * y
            out[i, j] = s
    return out


def eye(n):
    return mat([[1 if i == j else 0 for j in range(n)] for i in range(n)])


def scal(s, m):
    s = _co(s)
    out = np.empty(m.shape, dtype=object)
    for idx in np.ndindex(m.shape):
        out[idx] = s * m[idx]
    return out


def add(a, b):
    out = np.empty(a.shape, dtype=object)
    for idx in np.ndindex(a.shape):
        out[idx] = a[idx] + b[idx]
    return out


def sub(a, b):
    return add(a, scal(-1, b))


def transpose(m):
    return m.T.copy()


def dagger(m):
    out = np.empty((m.shape[1], m.shape[0]), dtype=object)
    for i, j in np.ndindex(m.shape):
        out[j, i] = m[i, j].conj()
    return out


def all_zero(m):
    return all(x.is_zero() for x in m.flat)


def all_real(m):
    return all(x.is_real() for x in m.flat)


def re_part(m):
    out = np.empty(m.shape, dtype=object)
    for idx in np.ndindex(m.shape):
        out[idx] = Alg(m[idx].a, m[idx].b)
    return out


def im_part(m):
    out = np.empty(m.shape, dtype=object)
    for idx in np.ndindex(m.shape):
        out[idx] = Alg(m[idx].c, m[idx].d)
    return out


def apply(state, op, axes):
    """Apply `op` (2^k x 2^k) to the qubit axes `axes` of a state tensor of shape (2,)*n."""
    n = state.ndim
    k = len(axes)
    rest = [ax for ax in range(n) if ax not in axes]
    moved = np.transpose(state, list(axes) + rest).reshape(2 ** k, -1)
    out = np.empty(moved.shape, dtype=object)
    for i in range(2 ** k):
        row = op[i]
        nz = [(j, row[j]) for j in range(2 ** k) if not row[j].is_zero()]
        for col in range(moved.shape[1]):
            s = ZERO
            for j, x in nz:
                y = moved[j, col]
                if not y.is_zero():
                    s = s + x * y
            out[i, col] = s
    out = out.reshape([2] * n)
    inv = np.argsort(list(axes) + rest)
    return np.transpose(out, inv)


def inner(u, v):
    s = ZERO
    for x, y in zip(u.flat, v.flat):
        if x.is_zero() or y.is_zero():
            continue
        s = s + x.conj() * y
    return s


def expect(state, ops_axes):
    """<state| prod of local operators |state>, the operators acting on disjoint axes."""
    w = state
    for op, axes in ops_axes:
        w = apply(w, op, axes)
    return inner(state, w)


# standard objects ------------------------------------------------------------
I2 = eye(2)
X = mat([[0, 1], [1, 0]])
Y = mat([[0, -IMAG], [IMAG, 0]])
Z = mat([[1, 0], [0, -1]])
J = mat([[0, -1], [1, 0]])                      # J^2 = -1, J|0> = |1>, J|1> = -|0>


def bell(name):
    """Bell vectors on two qubits, in the convention of Renou et al.:
    phi+- = (|00> +- |11>)/sqrt2,  psi+- = (|10> +- |01>)/sqrt2."""
    h = ISQ2
    v = {
        "phi+": [h, 0, 0, h], "phi-": [h, 0, 0, -h],
        "psi+": [0, h, h, 0], "psi-": [0, -h, h, 0],
    }[name]
    return vec(v)


def proj(v):
    n = len(v)
    out = np.empty((n, n), dtype=object)
    for i in range(n):
        for j in range(n):
            out[i, j] = v[i] * v[j].conj()
    return out


def flag_vectors(N):
    """psi_even^(N), psi_odd^(N) of Barrios Hita et al., Eqs. (44)-(45), as exact vectors.
    Normalisation 2^{-(N-1)/2}."""
    half = Fr(1, 2)
    # 2^{-(N-1)/2} = (1/2)^{(N-1)//2} * (1/sqrt2 if N-1 odd else 1)
    pref = Alg(half ** ((N - 1) // 2))
    if (N - 1) % 2:
        pref = pref * ISQ2
    e, o = [], []
    for k in product((0, 1), repeat=N):
        w = sum(k)
        if w % 2 == 0:
            e.append(pref * ((-1) ** (w // 2)))
            o.append(ZERO)
        else:
            e.append(ZERO)
            o.append(pref * ((-1) ** ((w - 1) // 2)))
    return vec(e), vec(o)


def flag_IJ(N):
    """I^(N) = |e><e| + |o><o|,  J^(N) = |o><e| - |e><o|   (Eq. (57))."""
    e, o = flag_vectors(N)
    n = len(e)
    I = np.empty((n, n), dtype=object)
    Jn = np.empty((n, n), dtype=object)
    for i in range(n):
        for j in range(n):
            I[i, j] = e[i] * e[j] + o[i] * o[j]
            Jn[i, j] = o[i] * e[j] - e[i] * o[j]
    return I, Jn
