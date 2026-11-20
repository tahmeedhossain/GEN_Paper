"""
Paper B.  P. Barrios Hita, A. Trushechkin, H. Kampermann, M. Epping, D. Bruss,
"Quantum Mechanics Based on Real Numbers: A Consistent Description",
Phys. Rev. Lett. 136, 240202 (2026); arXiv:2503.17307.

Encoded against the nonclassicality network GEN_GPT_Level v2.6 (nodes m-realqm,
m-quantum, ax-complex, ax-loctom; edges D6, F5, GN6, GN7).

Conventions used in the certificates
  J = [[0,-1],[1,0]]  (J|0> = |1>, J|1> = -|0>, J^2 = -1)
  A = A1 + i A2  (A1, A2 real)      T(A) = A1 (x) 1 + A2 (x) J     on  system (x) flag
  psi = p1 + i p2                   S(psi) = p1 (x) |0> + p2 (x) |1>
  block form (flag index first):    T(A) = [[A1, -A2], [A2, A1]],   S(psi) = (p1 ; p2)
"""
from itertools import product

import sympy as sp

import exact as ex
from exact import Alg, ISQ2, SQ2, ZERO
from kernel import CertResult, Claim, Edge, Node, Paper

sqrt2 = sp.sqrt(2)
Jm = sp.Matrix([[0, -1], [1, 0]])
I2 = sp.eye(2)


# ----------------------------------------------------------------------------
# helpers (sympy, small explicit dimensions)
# ----------------------------------------------------------------------------

def zero(M):
    return all(sp.simplify(x) == 0 for x in M)


def Tmap(A):
    """T(A) = Re A (x) 1 + Im A (x) J  on system (x) flag (sympy Matrix, any size)."""
    A1 = A.applyfunc(sp.re)
    A2 = A.applyfunc(sp.im)
    return sp.kronecker_product(A1, I2) + sp.kronecker_product(A2, Jm)


def Smap(psi):
    p1 = psi.applyfunc(sp.re)
    p2 = psi.applyfunc(sp.im)
    return sp.kronecker_product(p1, sp.Matrix([1, 0])) + sp.kronecker_product(p2, sp.Matrix([0, 1]))


def real_basis_ops(d):
    out = []
    for j, k in product(range(d), repeat=2):
        E = sp.zeros(d, d)
        E[j, k] = 1
        out += [E, sp.I * E]
    return out


def real_basis_vecs(d):
    out = []
    for j in range(d):
        e = sp.zeros(d, 1)
        e[j] = 1
        out += [e, sp.I * e]
    return out


def flag_e_o(N):
    """Normalised psi_even^(N), psi_odd^(N) as sympy column vectors (Eqs. (44)-(45))."""
    pref = sp.Integer(2) ** sp.Rational(-(N - 1), 2)
    e, o = [], []
    for k in product((0, 1), repeat=N):
        w = sum(k)
        e.append(pref * (-1) ** (w // 2) if w % 2 == 0 else 0)
        o.append(pref * (-1) ** ((w - 1) // 2) if w % 2 == 1 else 0)
    return sp.Matrix(e), sp.Matrix(o)


def flag_I_J(N):
    e, o = flag_e_o(N)
    return (e * e.T + o * o.T).applyfunc(sp.nsimplify), (o * e.T - e * o.T).applyfunc(sp.nsimplify)


def perm_sys_flag(dA, dB):
    """Permutation matrix taking the ordering (a, fa, b, fb) to (a, b, fa, fb)."""
    n = dA * 2 * dB * 2
    P = sp.zeros(n, n)
    for a, fa, b, fb in product(range(dA), range(2), range(dB), range(2)):
        src = ((a * 2 + fa) * dB + b) * 2 + fb
        dst = ((a * dB + b) * 2 + fa) * 2 + fb
        P[dst, src] = 1
    return P


def Rmap2(Psi):
    """R(Psi) = Re Psi (x) psi_even^(2) + Im Psi (x) psi_odd^(2); ordering (a, b, fa, fb)."""
    e, o = flag_e_o(2)
    return sp.kronecker_product(Psi.applyfunc(sp.re), e) + sp.kronecker_product(Psi.applyfunc(sp.im), o)


# ----------------------------------------------------------------------------
# certificates
# ----------------------------------------------------------------------------

def blocks_equal(L, R, Zd):
    """Equality of two 2x2 block matrices of d x d matrix expressions (d symbolic)."""
    L, R = sp.block_collapse(L), sp.block_collapse(R)
    for i in range(2):
        for j in range(2):
            diff = sp.expand((L.blocks[i, j] - R.blocks[i, j]).doit())
            if not (diff == Zd or diff == 0 or getattr(diff, "is_ZeroMatrix", False)):
                return False, (i, j, diff)
    return True, None


def T_block(P, Q, sign=1):
    """Block form of T(P + iQ). sign = -1 plants an error (used by controls.py)."""
    return sp.BlockMatrix([[P, -Q], [sign * Q, P]])


def cert_RQ1():
    """T is a unital real-algebra *-homomorphism onto the commutant of 1 (x) J (any d)."""
    d = sp.Symbol("d", positive=True, integer=True)
    A1, A2, B1, B2 = (sp.MatrixSymbol(n, d, d) for n in ("A1", "A2", "B1", "B2"))
    Zd, Id = sp.ZeroMatrix(d, d), sp.Identity(d)
    T = T_block

    def beq(L, R):                   # block equality with the zero block fixed
        return blocks_equal(L, R, Zd)[0]

    checks = {}
    # multiplicativity: (A1 + iA2)(B1 + iB2) = (A1B1 - A2B2) + i(A1B2 + A2B1)
    checks["T(A)T(B) = T(AB)"] = beq(T(A1, A2) * T(B1, B2), T(A1 * B1 - A2 * B2, A1 * B2 + A2 * B1))
    # adjoint: A^dagger = A1^T - i A2^T
    checks["T(A^dagger) = T(A)^T"] = beq(T(A1.T, -A2.T), sp.BlockMatrix([[A1.T, A2.T], [-A2.T, A1.T]]))
    lhsT = sp.block_collapse(sp.Transpose(T(A1, A2)))
    checks["block transpose of T(A) has the stated form"] = beq(lhsT, sp.BlockMatrix([[A1.T, A2.T], [-A2.T, A1.T]]))
    # unit and imaginary unit
    Jd = sp.BlockMatrix([[Zd, -Id], [Id, Zd]])
    checks["T(1) = 1"] = beq(T(Id, Zd), sp.BlockMatrix([[Id, Zd], [Zd, Id]]))
    checks["T(i 1) = 1 (x) J =: Jd,  Jd^2 = -1"] = beq(Jd * Jd, sp.BlockMatrix([[-Id, Zd], [Zd, -Id]]))
    checks["T(A) commutes with Jd"] = beq(Jd * T(A1, A2), T(A1, A2) * Jd)
    # commutant: a generic block matrix [[P,Q],[R,S]] commutes with Jd iff S = P and R = -Q
    P, Q, R, S = (sp.MatrixSymbol(n, d, d) for n in "PQRS")
    M = sp.BlockMatrix([[P, Q], [R, S]])
    com = sp.block_collapse(Jd * M - M * Jd)
    got = [sp.expand(com.blocks[i, j].doit()) for i in range(2) for j in range(2)]
    want = [sp.expand(x) for x in (-R - Q, -S + P, P - S, Q + R)]
    checks["commutator [Jd, M] has blocks (-(Q+R), P-S; P-S, Q+R)"] = all(
        sp.expand(g - w) == Zd or sp.expand(g - w) == 0 or getattr(sp.expand(g - w), "is_ZeroMatrix", False)
        for g, w in zip(got, want))
    ok = all(checks.values())
    return CertResult(ok, "block-matrix identities with d x d matrix symbols (d symbolic): "
                      + ("all hold" if ok else "FAILED: " + str([k for k, v in checks.items() if not v])),
                      {"checks": checks,
                       "reading": "the commutator vanishes iff S = P and R = -Q, i.e. M = T(P - iQ): "
                                  "the image of T is exactly the commutant of Jd; T is injective "
                                  "(T(A) = 0 forces A1 = A2 = 0)"})


def cert_RQ2():
    """State map S: explicit symbolic checks for d = 2, 3."""
    res = {}
    ok = True
    for d in (2, 3):
        p1 = sp.Matrix(sp.symbols(f"p1_0:{d}", real=True))
        p2 = sp.Matrix(sp.symbols(f"p2_0:{d}", real=True))
        q1 = sp.Matrix(sp.symbols(f"q1_0:{d}", real=True))
        q2 = sp.Matrix(sp.symbols(f"q2_0:{d}", real=True))
        a1 = sp.Matrix(d, d, sp.symbols(f"a1_0:{d * d}", real=True))
        a2 = sp.Matrix(d, d, sp.symbols(f"a2_0:{d * d}", real=True))
        psi, phi, A = p1 + sp.I * p2, q1 + sp.I * q2, a1 + sp.I * a2
        Jd = sp.kronecker_product(sp.eye(d), Jm)
        c = {}
        c["T(A) S(psi) = S(A psi)"] = zero(Tmap(A) * Smap(psi) - Smap((A * psi).applyfunc(sp.expand)))
        c["S(i psi) = Jd S(psi)"] = zero(Smap((sp.I * psi).applyfunc(sp.expand)) - Jd * Smap(psi))
        ip = (phi.H * psi)[0]
        c["S(phi)^T S(psi) = Re<phi|psi>"] = sp.simplify((Smap(phi).T * Smap(psi))[0] - sp.re(sp.expand(ip))) == 0
        c["S(phi)^T Jd S(psi) = -Im<phi|psi>"] = sp.simplify((Smap(phi).T * Jd * Smap(psi))[0] + sp.im(sp.expand(ip))) == 0
        ev = sp.expand((psi.H * A * psi)[0])
        c["S(psi)^T T(A) S(psi) = Re<psi|A|psi>"] = sp.simplify((Smap(psi).T * Tmap(A) * Smap(psi))[0] - sp.re(ev)) == 0
        # phase rotation, Eq. (2): S(e^{i alpha} psi) = (1 (x) R(alpha)) S(psi)
        al = sp.Symbol("alpha", real=True)
        Rot = sp.Matrix([[sp.cos(al), -sp.sin(al)], [sp.sin(al), sp.cos(al)]])
        lhs = Smap(((sp.cos(al) + sp.I * sp.sin(al)) * psi).applyfunc(sp.expand))
        c["S(e^{i alpha} psi) = (1 (x) R(alpha)) S(psi)"] = zero(lhs - sp.kronecker_product(sp.eye(d), Rot) * Smap(psi))
        # pure state: T(|psi><psi|) = S S^T + (Jd S)(Jd S)^T
        rho = (psi * psi.H).applyfunc(sp.expand)
        s = Smap(psi)
        c["T(|psi><psi|) = S S^T + (Jd S)(Jd S)^T"] = zero(Tmap(rho) - s * s.T - (Jd * s) * (Jd * s).T)
        c["tr T(A) = 2 Re tr A"] = sp.simplify(Tmap(A).trace() - 2 * sp.re(A.trace())) == 0
        res[f"d={d}"] = c
        ok &= all(c.values())
    return CertResult(ok, "symbolic identities with real symbols for all components, d = 2, 3: "
                      + ("all hold" if ok else "FAILED"), {"checks": res},
                      scope="instances: d = 2, 3 (each identity is real-bilinear; the expansion is the same for every d)")


def cert_RQ3():
    """Density operators: T1(rho) = T(rho)/2 (Eqs. (84)-(85)); consequences of RQ1."""
    d = 2
    r1 = sp.Matrix(d, d, sp.symbols("r1_0:4", real=True))
    r2 = sp.Matrix(d, d, sp.symbols("r2_0:4", real=True))
    a1 = sp.Matrix(d, d, sp.symbols("a1_0:4", real=True))
    a2 = sp.Matrix(d, d, sp.symbols("a2_0:4", real=True))
    rho, A = r1 + sp.I * r2, a1 + sp.I * a2
    T1 = Tmap(rho) / 2
    c = {
        "tr T1(rho) = Re tr rho": sp.simplify(T1.trace() - sp.re(rho.trace())) == 0,
        "tr[T1(rho) T(A)] = Re tr(rho A)": sp.simplify((T1 * Tmap(A)).trace() - sp.re(sp.expand((rho * A).trace()))) == 0,
    }
    # positivity transfer: A = B^dagger B  =>  T(A) = T(B)^T T(B)
    b1 = sp.Matrix(d, d, sp.symbols("b1_0:4", real=True))
    b2 = sp.Matrix(d, d, sp.symbols("b2_0:4", real=True))
    B = b1 + sp.I * b2
    c["T(B^dagger B) = T(B)^T T(B)  (so A >= 0 implies T(A) >= 0)"] = zero(
        Tmap((B.H * B).applyfunc(sp.expand)) - Tmap(B).T * Tmap(B))
    ok = all(c.values())
    return CertResult(ok, "trace and positivity identities, symbolic 2x2: " + ("all hold" if ok else "FAILED"),
                      {"checks": c}, scope="instances: d = 2 (consequences of the d-independent identities of RQ1)")


def cert_RQ4():
    """Flag projector P = (1 - J(x)J)/2 and the canonical subspace (Eq. (8))."""
    JJ = sp.kronecker_product(Jm, Jm)
    P = (sp.eye(4) - JJ) / 2
    e, o = flag_e_o(2)
    kp = sp.Matrix([1, 0, 0, 1])       # |00> + |11>
    km = sp.Matrix([0, 1, -1, 0])      # |01> - |10>
    c = {
        "P^2 = P": zero(P * P - P),
        "P^T = P": zero(P.T - P),
        "rank P = 2": P.rank() == 2,
        "P psi_even = psi_even, P psi_odd = psi_odd": zero(P * e - e) and zero(P * o - o),
        "psi_even = (|00>-|11>)/sqrt2, psi_odd = (|01>+|10>)/sqrt2": zero(e - sp.Matrix([1, 0, 0, -1]) / sqrt2) and zero(o - sp.Matrix([0, 1, 1, 0]) / sqrt2),
        "P kills |00>+|11> and |01>-|10>": zero(P * kp) and zero(P * km),
        "on range(P): J(x)1 = 1(x)J": zero((sp.kronecker_product(Jm, I2) - sp.kronecker_product(I2, Jm)) * P),
        "(J(x)J)^2 = 1 and tr(J(x)J) = 0 (so rank P is half the dimension for any system size)": zero(JJ * JJ - sp.eye(4)) and JJ.trace() == 0,
        "I^(2) = P, J^(2) = (J(x)1) P": zero(flag_I_J(2)[0] - P) and zero(flag_I_J(2)[1] - sp.kronecker_product(Jm, I2) * P),
    }
    ok = all(c.values())
    return CertResult(ok, "exact 4x4 computation on the two flags: " + ("all hold" if ok else "FAILED"), {"checks": c})


def cert_RQ5():
    """Prop. 3 and Eq. (34): the flag product of two realified vectors is the realified tensor product."""
    res, ok = {}, True
    for dA, dB in ((2, 2), (2, 3)):
        pa1 = sp.Matrix(sp.symbols(f"u1_0:{dA}", real=True))
        pa2 = sp.Matrix(sp.symbols(f"u2_0:{dA}", real=True))
        pb1 = sp.Matrix(sp.symbols(f"v1_0:{dB}", real=True))
        pb2 = sp.Matrix(sp.symbols(f"v2_0:{dB}", real=True))
        psi, phi = pa1 + sp.I * pa2, pb1 + sp.I * pb2
        Perm = perm_sys_flag(dA, dB)
        naive = Perm * sp.kronecker_product(Smap(psi), Smap(phi))          # S(psi) (x) S(phi), reordered
        Pfull = sp.kronecker_product(sp.eye(dA * dB), (sp.eye(4) - sp.kronecker_product(Jm, Jm)) / 2)
        Psi = sp.kronecker_product(psi, phi).applyfunc(sp.expand)
        R = Rmap2(Psi)
        e, o = flag_e_o(2)
        eq34 = (sp.kronecker_product(sp.kronecker_product(pa1, pb1) - sp.kronecker_product(pa2, pb2), e)
                + sp.kronecker_product(sp.kronecker_product(pa1, pb2) + sp.kronecker_product(pa2, pb1), o))
        c = {
            "Eq. (34) equals R(psi (x) phi)": zero(eq34 - R),
            "P [S(psi) (x) S(phi)] = R(psi (x) phi) / sqrt2": zero(Pfull * naive - R / sqrt2),
            "S(psi) (x) S(phi) - R/sqrt2 lies in the kernel of P": zero(Pfull * (naive - R / sqrt2)),
            "|R(psi (x) phi)|^2 = |psi|^2 |phi|^2": sp.simplify((R.T * R)[0] - (pa1.dot(pa1) + pa2.dot(pa2)) * (pb1.dot(pb1) + pb2.dot(pb2))) == 0,
        }
        res[f"dA={dA}, dB={dB}"] = c
        ok &= all(c.values())
    return CertResult(ok, "symbolic vectors, (dA,dB) = (2,2), (2,3): " + ("all hold" if ok else "FAILED"),
                      {"checks": res,
                       "reading": "the naive product S(psi)(x)S(phi) is not in the canonical subspace; its canonical "
                                  "representative is R(psi(x)phi)/sqrt2, so Eq. (34) carries a factor sqrt2 relative "
                                  "to the orthogonal projection"},
                      scope="instances: (dA,dB) = (2,2), (2,3) (bilinear identities)")


def cert_RQ6():
    """N-flag vectors (Eqs. (44)-(45)): product form, J_k action, dimension of the common subspace."""
    res, ok = {}, True
    for N in range(1, 7):
        # unnormalised integer vectors
        e, o = [], []
        for k in product((0, 1), repeat=N):
            w = sum(k)
            e.append((-1) ** (w // 2) if w % 2 == 0 else 0)
            o.append((-1) ** ((w - 1) // 2) if w % 2 == 1 else 0)
        # product form: e + i o = (|0> + i|1>)^{(x)N}
        prod_vec = [1]
        for _ in range(N):
            prod_vec = [x * y for x in prod_vec for y in (1, 1j)]
        c = {"e + i o = (|0> + i|1>)^(x)N": all(complex(a, b) == z for a, b, z in zip(e, o, prod_vec))}
        # J on flag k:  J_k e = o,  J_k o = -e
        def Jk(v, k):
            out = [0] * len(v)
            for idx, bits in enumerate(product((0, 1), repeat=N)):
                if v[idx] == 0:
                    continue
                b = list(bits)
                sign = 1 if b[k] == 0 else -1        # J|0> = |1>, J|1> = -|0>
                b[k] ^= 1
                j = int("".join(map(str, b)), 2)
                out[j] += sign * v[idx]
            return out
        c["J_k e = o and J_k o = -e for every flag k"] = all(
            Jk(e, k) == o and Jk(o, k) == [-x for x in e] for k in range(N))
        c["norms: |e|^2 = |o|^2 = 2^(N-1)"] = sum(x * x for x in e) == 2 ** (N - 1) and sum(x * x for x in o) == 2 ** (N - 1)
        if 2 <= N <= 5:
            # common subspace { v : (J_k - J_0) v = 0 for all k } has dimension exactly 2
            rows = []
            dim = 2 ** N
            for k in range(1, N):
                for col in range(dim):
                    pass
                M = sp.zeros(dim, dim)
                for idx in range(dim):
                    basis = [0] * dim
                    basis[idx] = 1
                    a = Jk(basis, k)
                    b = Jk(basis, 0)
                    for r in range(dim):
                        M[r, idx] = a[r] - b[r]
                rows.append(M)
            big = sp.Matrix.vstack(*rows)
            c["dim of the common subspace = 2"] = (dim - big.rank()) == 2
        res[f"N={N}"] = c
        ok &= all(c.values())
    return CertResult(ok, "integer arithmetic, N = 1..6 flags (common-subspace dimension for N = 2..5): "
                      + ("all hold" if ok else "FAILED"),
                      {"checks": res,
                       "reading": "psi_even + i psi_odd = 2^{-(N-1)/2} (|0>+i|1>)^{(x)N}: every local J_k acts on the "
                                  "canonical pair as the single complex structure J^(N), which is the content of the "
                                  "quotient construction"},
                      scope="instances: N = 1..6 (the product form makes the J_k statement immediate for every N)")


def cert_RQ7():
    """I^(N), J^(N): algebra, recursion (59), partial trace (91)."""
    res, ok = {}, True
    IJ = {N: flag_I_J(N) for N in range(1, 6)}

    def ptrace_first(M, N, m):
        """Trace out the first m of N qubits."""
        d1, d2 = 2 ** m, 2 ** (N - m)
        out = sp.zeros(d2, d2)
        for i in range(d2):
            for j in range(d2):
                out[i, j] = sum(M[k * d2 + i, k * d2 + j] for k in range(d1))
        return out

    for N in range(1, 6):
        I, Jn = IJ[N]
        c = {
            "I^2 = I": zero(I * I - I),
            "J^2 = -I": zero(Jn * Jn + I),
            "I J = J I = J": zero(I * Jn - Jn) and zero(Jn * I - Jn),
            "J^T = -J": zero(Jn.T + Jn),
        }
        res[f"N={N}"] = c
        ok &= all(c.values())
    c = {"I^(1) = 1, J^(1) = J = XZ": zero(IJ[1][0] - sp.eye(2)) and zero(IJ[1][1] - Jm)
         and zero(sp.Matrix([[0, 1], [1, 0]]) * sp.Matrix([[1, 0], [0, -1]]) - Jm)}
    for N, M in ((1, 1), (1, 2), (2, 1), (2, 2), (1, 3), (3, 1), (2, 3), (3, 2), (1, 4), (4, 1)):
        (In, Jn), (Im_, Jm_) = IJ[N], IJ[M]
        Inm, Jnm = IJ[N + M]
        c[f"recursion (59), N={N}, M={M}"] = (
            zero(Inm - (sp.kronecker_product(In, Im_) - sp.kronecker_product(Jn, Jm_)) / 2)
            and zero(Jnm - (sp.kronecker_product(In, Jm_) + sp.kronecker_product(Jn, Im_)) / 2))
    for N in range(2, 6):
        for m in range(1, N):
            c[f"partial trace (91), N={N}, trace out {m}"] = (
                zero(ptrace_first(IJ[N][0], N, m) - IJ[N - m][0])
                and zero(ptrace_first(IJ[N][1], N, m) - IJ[N - m][1]))
    res["recursion and partial trace"] = c
    ok &= all(c.values())
    return CertResult(ok, "exact rational matrices, N up to 5: " + ("all hold" if ok else "FAILED"),
                      {"checks": res}, scope="instances: N <= 5")


def cert_RQ8():
    """Postulate (P4), Eq. (75) / Prop. 11: local action on the realified composite."""
    res, ok, count = {}, True, 0
    for dA, dB in ((2, 2), (2, 3)):
        good = True
        idB = sp.eye(dB)
        idA = sp.eye(dA)
        # operator on (a, fa) embedded in ordering (a, b, fa, fb), and on (b, fb)
        def embA(TA):
            n = dA * dB * 4
            M = sp.zeros(n, n)
            for a, b, fa, fb, a2, fa2 in product(range(dA), range(dB), range(2), range(2), range(dA), range(2)):
                v = TA[a * 2 + fa, a2 * 2 + fa2]
                if v != 0:
                    M[((a * dB + b) * 2 + fa) * 2 + fb, ((a2 * dB + b) * 2 + fa2) * 2 + fb] = v
            return M

        def embB(TB):
            n = dA * dB * 4
            M = sp.zeros(n, n)
            for a, b, fa, fb, b2, fb2 in product(range(dA), range(dB), range(2), range(2), range(dB), range(2)):
                v = TB[b * 2 + fb, b2 * 2 + fb2]
                if v != 0:
                    M[((a * dB + b) * 2 + fa) * 2 + fb, ((a * dB + b2) * 2 + fa) * 2 + fb2] = v
            return M

        vecsA, vecsB = real_basis_vecs(dA), real_basis_vecs(dB)
        Psis = [sp.kronecker_product(u, v) for u in vecsA for v in vecsB]     # spans C^dA (x) C^dB over R
        for A in real_basis_ops(dA):
            EA = embA(Tmap(A))
            for Psi in Psis:
                lhs = EA * Rmap2(Psi)
                rhs = Rmap2((sp.kronecker_product(A, idB) * Psi).applyfunc(sp.expand))
                good &= zero(lhs - rhs)
                count += 1
        for B in real_basis_ops(dB):
            EB = embB(Tmap(B))
            for Psi in Psis:
                lhs = EB * Rmap2(Psi)
                rhs = Rmap2((sp.kronecker_product(idA, B) * Psi).applyfunc(sp.expand))
                good &= zero(lhs - rhs)
                count += 1
        res[f"dA={dA}, dB={dB}"] = good
        ok &= good
    return CertResult(ok, f"{count} exact checks on real bases of operators and of C^dA (x) C^dB: "
                      + ("(T(A) (x) 1) R(Psi) = R((A (x) 1) Psi) and the same on the B side, all hold" if ok else "FAILED"),
                      {"checks": res,
                       "reading": "both sides are real-linear in A and in Psi, so equality on real bases is equality "
                                  "for all operators and all (also entangled) vectors"},
                      scope="instances: (dA,dB) = (2,2), (2,3)")


def cert_RQ9():
    """Composite operators: compression of T(A)(x)T(B) to the canonical subspace; Hoffreumon-Woods (B.34)."""
    dA = dB = 2
    Perm = perm_sys_flag(dA, dB)
    I_2, J_2 = flag_I_J(2)
    Pfull = sp.kronecker_product(sp.eye(dA * dB), I_2)
    ok, count = True, 0
    for A in real_basis_ops(dA):
        for B in real_basis_ops(dB):
            TT = Perm * sp.kronecker_product(Tmap(A), Tmap(B)) * Perm.T
            AB = sp.kronecker_product(A, B).applyfunc(sp.expand)
            target = (sp.kronecker_product(AB.applyfunc(sp.re), I_2) + sp.kronecker_product(AB.applyfunc(sp.im), J_2))
            hw = (TT - Perm * sp.kronecker_product(Tmap(sp.I * A), Tmap(sp.I * B)) * Perm.T) / 2
            ok &= zero(Pfull * TT - TT * Pfull)            # local operators preserve the canonical subspace
            ok &= zero(Pfull * TT - target)                # and act there as the realified A (x) B
            ok &= zero(hw - target)                        # Hoffreumon-Woods Eq. (B.34)
            count += 1
    return CertResult(ok, f"{count} operator pairs (real basis of M_2(C) x M_2(C)): [P, T(A)(x)T(B)] = 0, "
                      "P (T(A)(x)T(B)) = Re(A(x)B)(x)I^(2) + Im(A(x)B)(x)J^(2), and this equals "
                      "(1/2)[T(A)(x)T(B) - T(iA)(x)T(iB)]: " + ("all hold" if ok else "FAILED"),
                      {"pairs": count,
                       "reading": "the flag product of Barrios Hita et al. and the combination rule (B.34)-(B.37) of "
                                  "Hoffreumon and Woods are the same compression by P = (1 - J(x)J)/2"},
                      scope="instances: dA = dB = 2 (bilinear in A and B)")


def cert_RQ10():
    """Born rule on the composite: R(Phi)^T [T(A)(x)T(B)] R(Psi) = Re <Phi| A(x)B |Psi>."""
    dA = dB = 2
    Perm = perm_sys_flag(dA, dB)
    vecs = [sp.kronecker_product(u, v) for u in real_basis_vecs(dA) for v in real_basis_vecs(dB)]
    Rs = [Rmap2(v) for v in vecs]
    ok, count = True, 0
    for A in real_basis_ops(dA):
        for B in real_basis_ops(dB):
            TT = Perm * sp.kronecker_product(Tmap(A), Tmap(B)) * Perm.T
            AB = sp.kronecker_product(A, B)
            for i, Phi in enumerate(vecs):
                left = Rs[i].T * TT
                for j, Psi in enumerate(vecs):
                    lhs = (left * Rs[j])[0]
                    rhs = sp.re(sp.expand((Phi.H * AB * Psi)[0]))
                    ok &= sp.simplify(lhs - rhs) == 0
                    count += 1
    return CertResult(ok, f"{count} exact checks (real bases of A, B, Phi, Psi; d = 2 each): "
                      + ("the real bilinear form equals Re<Phi|A(x)B|Psi>" if ok else "FAILED"),
                      {"checks": count,
                       "reading": "with Phi = Psi and Hermitian A, B this is the Born rule for arbitrary, also "
                                  "entangled, bipartite states"},
                      scope="instances: dA = dB = 2 (real-multilinear identity)")


# ---- entanglement-swapping experiment, exact in Q(sqrt2, i) --------------------

def _settings():
    A_ops = [ex.Z, ex.X, ex.Y]                                   # x = 1, 2, 3
    h = ISQ2
    def comb(P, Q, sign):
        return ex.scal(h, ex.add(P, ex.scal(sign, Q)))
    C_ops = [comb(ex.X, ex.Z, 1), comb(ex.Z, ex.X, -1),          # C1 = (X+Z)/√2, C2 = (Z-X)/√2
             comb(ex.Y, ex.Z, 1), comb(ex.Z, ex.Y, -1),          # C3 = (Y+Z)/√2, C4 = (Z-Y)/√2
             comb(ex.X, ex.Y, 1), comb(ex.X, ex.Y, -1)]          # C5 = (X+Y)/√2, C6 = (X-Y)/√2
    bells = {"00": "phi+", "01": "psi+", "10": "phi-", "11": "psi-"}
    Pi = {b: ex.proj(ex.bell(n)) for b, n in bells.items()}
    return A_ops, C_ops, Pi


def _complex_table():
    A_ops, C_ops, Pi = _settings()
    psi = ex.kronv(ex.bell("phi+"), ex.bell("phi+")).reshape([2] * 4)      # axes A, B1, B2, C
    tab = {"Pb": {}, "APi": {}, "PiC": {}, "S": {}}
    for b, P in Pi.items():
        tab["Pb"][b] = ex.expect(psi, [(P, [1, 2])])
        for x, A in enumerate(A_ops, 1):
            tab["APi"][(b, x)] = ex.expect(psi, [(A, [0]), (P, [1, 2])])
        for z, C in enumerate(C_ops, 1):
            tab["PiC"][(b, z)] = ex.expect(psi, [(P, [1, 2]), (C, [3])])
        for x, A in enumerate(A_ops, 1):
            for z, C in enumerate(C_ops, 1):
                tab["S"][(b, x, z)] = ex.expect(psi, [(A, [0]), (P, [1, 2]), (C, [3])])
    return tab


def _T_real(op, IN, JN):
    """T(A) = Re A (x) I^(N) + Im A (x) J^(N) on (systems) (x) (flags)."""
    return ex.add(ex.kron(ex.re_part(op), IN), ex.kron(ex.im_part(op), JN))


def _real_table(flag_identity=False, product_flags=False):
    A_ops, C_ops, Pi = _settings()
    e4, _ = ex.flag_vectors(4)
    if product_flags:      # planted error for controls.py: flags of the two sources in a product state
        e2, _ = ex.flag_vectors(2)
        e4 = ex.kronv(e2, e2)
    state = ex.kronv(ex.bell("phi+"), ex.bell("phi+"), e4).reshape([2] * 8)   # A,B1,B2,C | A',B1',B2',C'
    assert ex.all_real(state)
    I1, J1 = ex.flag_IJ(1)
    I2_, J2_ = ex.flag_IJ(2)
    if flag_identity:
        I2_ = ex.eye(4)
    TA = [_T_real(A, I1, J1) for A in A_ops]
    TC = [_T_real(C, I1, J1) for C in C_ops]
    TP = {b: _T_real(P, I2_, J2_) for b, P in Pi.items()}
    real_ops = all(ex.all_real(m) for m in TA + TC + list(TP.values()))
    axA, axB, axC = [0, 4], [1, 2, 5, 6], [3, 7]
    tab = {"Pb": {}, "APi": {}, "PiC": {}, "S": {}}
    for b, P in TP.items():
        tab["Pb"][b] = ex.expect(state, [(P, axB)])
        for x, A in enumerate(TA, 1):
            tab["APi"][(b, x)] = ex.expect(state, [(A, axA), (P, axB)])
        for z, C in enumerate(TC, 1):
            tab["PiC"][(b, z)] = ex.expect(state, [(P, axB), (C, axC)])
        for x, A in enumerate(TA, 1):
            for z, C in enumerate(TC, 1):
                tab["S"][(b, x, z)] = ex.expect(state, [(A, axA), (P, axB), (C, axC)])
    return tab, real_ops


def _T_values(tab, fifth="b1", weighting="plain-sum-joint"):
    """Evaluate the network functional under a stated reading of its definition."""
    vals = {}
    total = ZERO
    for b in ("00", "01", "10", "11"):
        b1, b2 = int(b[0]), int(b[1])
        S = lambda x, z: tab["S"][(b, x, z)]
        s1, s2, s12 = (-1) ** b1, (-1) ** b2, (-1) ** (b1 + b2)
        s5 = s1 if fifth == "b1" else s2
        Tb = (s2 * (S(1, 1) + S(1, 2)) + s1 * (S(2, 1) - S(2, 2)) + s2 * (S(1, 3) + S(1, 4))
              - s12 * (S(3, 3) - S(3, 4)) + s5 * (S(2, 5) + S(2, 6)) - s12 * (S(3, 5) - S(3, 6)))
        vals[b] = Tb                                   # built from joint correlators S^b_xz
        if weighting == "plain-sum-joint":             # Renou et al.:  T = sum_b T_b(joint S)
            total = total + Tb
        elif weighting == "P(b)-weighted-joint":       # joint S and an extra factor P(b)
            total = total + tab["Pb"][b] * Tb
    return total, vals


_CACHE = {}


def _tables():
    if "c" not in _CACHE:
        _CACHE["c"] = _complex_table()
        _CACHE["r"], _CACHE["real_ops"] = _real_table()
        _CACHE["r_id"], _ = _real_table(flag_identity=True)
    return _CACHE


def cert_RQ11():
    """Complex quantum value of the Renou functional."""
    tab = _tables()["c"]
    total, vals = _T_values(tab, fifth="b1", weighting="plain-sum-joint")
    six_rt2 = Alg(0, 6)
    pb_ok = all(v == Alg(ex.Fr(1, 4)) for v in tab["Pb"].values())
    cond_ok = all(v == Alg(0, ex.Fr(3, 2)) for v in vals.values())       # T_b(joint) = 6√2 * 1/4 = (3/2)√2
    ok = (total == six_rt2) and pb_ok and cond_ok
    return CertResult(ok, f"exact in Q(√2, i): P(b) = 1/4 for all b; T_b = (3/2)√2 = 6√2·P(b) for all b; "
                      f"T = {total} (= 6√2 ≈ 8.4853)" if ok else f"FAILED: T = {total}, T_b = {vals}",
                      {"P(b)": {k: repr(v) for k, v in tab["Pb"].items()},
                       "T_b (joint correlators)": {k: repr(v) for k, v in vals.items()},
                       "T": repr(total)})


def cert_RQ12():
    """Real flag model reproduces every probability of the experiment, using real numbers only."""
    c = _tables()
    tc, tr, tri = c["c"], c["r"], c["r_id"]
    n = 0
    same = True
    real_vals = True
    for fam in ("Pb", "APi", "PiC", "S"):
        for k, v in tc[fam].items():
            n += 1
            same &= (tr[fam][k] == v)
            real_vals &= tr[fam][k].is_real()
    same_id = all(tri[fam][k] == v for fam in ("Pb", "APi", "PiC", "S") for k, v in tc[fam].items())
    total, vals = _T_values(tr, fifth="b1", weighting="plain-sum-joint")
    ok = same and real_vals and c["real_ops"] and total == Alg(0, 6) and same_id
    return CertResult(ok, f"{n} moments <Π_b>, <A_x Π_b>, <Π_b C_z>, <A_x Π_b C_z> (they fix all 288 probabilities "
                      f"P(a,b,c|x,z)) agree exactly with complex QM; state, operators and values contain no "
                      f"imaginary part; T = {total}" if ok else "FAILED",
                      {"moments_compared": n, "all_equal": same, "real_model_all_real": real_vals and c["real_ops"],
                       "T_real_model": repr(total),
                       "T_b_real_model": {k: repr(v) for k, v in vals.items()},
                       "variant with identity on Bob's flags instead of I^(2) gives the same numbers": same_id,
                       "note": "the paper evaluates b = 00 only (Eq. (123)); here all four outcomes are computed"})


def cert_RQ13():
    """Readings of the functional: which definitions reproduce the stated value 6√2."""
    tab = _tables()["c"]
    out = {}
    for label, fifth, w in (
        ("Renou et al.: joint S, prefactors (b2,b1,b2,b1+b2,b1,b1+b2), T = Σ_b T_b", "b1", "plain-sum-joint"),
        ("fifth prefactor (-1)^{b2} as in arXiv:2503.17307 Eq. (105), T = Σ_b T_b", "b2", "plain-sum-joint"),
        ("Eqs. (104)-(106) of arXiv:2503.17307 read literally: joint S, fifth prefactor (-1)^{b2}, T = Σ_b P(b) T_b", "b2", "P(b)-weighted-joint"),
        ("joint S, Renou prefactors, T = Σ_b P(b) T_b", "b1", "P(b)-weighted-joint"),
    ):
        total, vals = _T_values(tab, fifth=fifth, weighting=w)
        out[label] = {"T": repr(total), "T_b": {k: repr(v) for k, v in vals.items()}}
    t_renou = _T_values(tab, "b1", "plain-sum-joint")[0]
    t_b2 = _T_values(tab, "b2", "plain-sum-joint")[0]
    t_lit = _T_values(tab, "b2", "P(b)-weighted-joint")[0]
    ok = (t_renou == Alg(0, 6)) and (t_b2 == Alg(0, 5)) and (t_lit == Alg(0, ex.Fr(5, 4)))
    return CertResult(ok, "T = 6√2 only with the prefactor (-1)^{b1} on (S_25 + S_26) and with either "
                      "(joint correlators, plain sum over b) or (conditional correlators, P(b) weights); "
                      "with (-1)^{b2} the outcomes b = 01, 10 give 4√2·P(b) and T = 5√2; "
                      "joint correlators with an additional P(b) weight give 5√2/4" if ok else f"unexpected values: {out}",
                      {"readings": out,
                       "consequence": "the paper's explicit evaluation is for b = 00, where all prefactors are +1, "
                                      "so its numbers are unaffected; the statement 'T_b = 6√2 for all b' needs "
                                      "the Renou form"})


def cert_RQ14():
    """Eq. (118): Alice-Charlie state after Bob's outcome 00 in the real model."""
    _, _, Pi = _settings()
    e4, _ = ex.flag_vectors(4)
    state = ex.kronv(ex.bell("phi+"), ex.bell("phi+"), e4).reshape([2] * 8)
    I2_, J2_ = ex.flag_IJ(2)
    post = ex.apply(state, _T_real(Pi["00"], I2_, J2_), [1, 2, 5, 6])
    # reduced operator on (A, C, A', C'): trace out B1, B2, B1', B2'
    import numpy as np
    t = np.transpose(post, [0, 3, 4, 7, 1, 2, 5, 6]).reshape(16, 16)
    rho = ex.matmul(t, ex.dagger(t))                                   # unnormalised, trace = P(00)
    tr = ZERO
    for i in range(16):
        tr = tr + rho[i, i]
    claim = ex.kron(ex.proj(ex.bell("phi+")),
                    ex.scal(ex.Fr(1, 2), ex.add(ex.proj(ex.bell("phi-")), ex.proj(ex.bell("psi+")))))
    ok = (tr == Alg(ex.Fr(1, 4))) and ex.all_zero(ex.sub(ex.scal(4, rho), claim))
    I2f, _ = ex.flag_IJ(2)
    same_as_I = ex.all_zero(ex.sub(ex.add(ex.proj(ex.bell("phi-")), ex.proj(ex.bell("psi+"))), I2f))
    return CertResult(ok and same_as_I, "exact: P(00) = 1/4 and the normalised Alice-Charlie state equals "
                      "|φ+><φ+|_AC ⊗ (1/2)(|φ-><φ-| + |ψ+><ψ+|)_{A'C'}; the flag factor is I^(2)/2"
                      if ok and same_as_I else "FAILED",
                      {"trace": repr(tr), "flag factor equals I^(2)/2": same_as_I})


def cert_RQ15():
    """The canonical four-flag vector is not a product across the cut between the two sources."""
    e4, o4 = flag_e_o(4)
    e2, o2 = flag_e_o(2)
    # flags ordered A', B1', B2', C'; source 1 = (A', B1'), source 2 = (B2', C')
    M = sp.Matrix(4, 4, lambda i, j: e4[i * 4 + j])
    rank = M.rank()
    decomp = zero(e4 - (sp.kronecker_product(e2, e2) - sp.kronecker_product(o2, o2)) / sqrt2)
    # the product of the two sources' canonical vectors is in the same class (differs by a kernel vector)
    I4, _ = flag_I_J(4)
    prod_vec = sp.kronecker_product(e2, e2)
    same_class = zero(I4 * prod_vec - e4 / sqrt2)
    # dimension of the composite space: range of P on (R^2 x R^2_F) x (R^2 x R^2_F) for two qubits
    dA = dB = 2
    JA = sp.kronecker_product(sp.eye(dA), Jm)
    JB = sp.kronecker_product(sp.eye(dB), Jm)
    Ptot = (sp.eye(4 * dA * dB) - sp.kronecker_product(JA, JB)) / 2
    dim_ok = Ptot.rank() == 2 * dA * dB and (2 * dA) * (2 * dB) == 16
    ok = (rank == 2) and decomp and same_class and dim_ok
    return CertResult(ok, "exact: the composite space of two qubits has real dimension 8 = 2·dA·dB, not 16 = (2dA)(2dB); "
                      "ψ_even^(4) = (ψ_even^(2)⊗ψ_even^(2) − ψ_odd^(2)⊗ψ_odd^(2))/√2 has Schmidt rank 2 "
                      "across (A'B1')|(B2'C'); the product ψ_even^(2)⊗ψ_even^(2) projects onto ψ_even^(4)/√2"
                      if ok else "FAILED",
                      {"composite dimension 2·dA·dB = 8 (rank of P), tensor-product dimension 16": dim_ok,
                       "schmidt_rank_across_source_cut": int(rank), "decomposition": decomp,
                       "product representative projects to canonical/√2": same_class,
                       "reading": "inside the ambient tensor product R^2⊗R^2⊗R^2⊗R^2 the state used for two independent "
                                  "sources is correlated across the sources; independence holds only for classes of "
                                  "the quotient. Postulate (iv) of Renou et al. (tensor-product composition with "
                                  "product states for independent sources) is therefore not satisfied by the model"})


def cert_RQ16():
    """Dimension counts behind local tomography."""
    n, m = sp.symbols("n m", positive=True, integer=True)
    herm = lambda k: k ** 2                           # real dimension of Herm_k(C)
    sym = lambda k: k * (k + 1) / 2                   # Sym_k(R)
    sy = lambda k: k * (k + 1) / 2 + k * (k - 1) / 2  # {[[A,-B],[B,A]] : A sym, B antisym}
    c = {
        "dim SY_k = k^2 = dim Herm_k": sp.simplify(sy(n) - herm(n)) == 0,
        "complex / flag composition: dim(nm) = dim(n) dim(m)": sp.simplify(herm(n * m) - herm(n) * herm(m)) == 0,
        "real tensor composition: dim Sym_{nm} - dim Sym_n dim Sym_m = nm(n-1)(m-1)/4": sp.simplify(
            sym(n * m) - sym(n) * sym(m) - n * m * (n - 1) * (m - 1) / 4) == 0,
    }
    ok = all(c.values())
    return CertResult(ok, "symbolic in n, m: the flag composition is locally tomographic on SY (same count as "
                      "complex QT); the real tensor product on Sym has nm(n−1)(m−1)/4 extra parameters, > 0 for n, m ≥ 2"
                      if ok else "FAILED", {"checks": c})


def cert_RQ18():
    """Observable <-> generator link carried by J (Stone link in the real representation)."""
    d = sp.Symbol("d", positive=True, integer=True)
    H1, H2 = sp.MatrixSymbol("H1", d, d), sp.MatrixSymbol("H2", d, d)
    Zd, Id = sp.ZeroMatrix(d, d), sp.Identity(d)
    Jd = sp.BlockMatrix([[Zd, -Id], [Id, Zd]])
    TH = sp.BlockMatrix([[H1, -H2], [H2, H1]])
    # T(-iH): -iH = H2 - i H1
    TmiH = sp.BlockMatrix([[H2, H1], [-H1, H2]])
    lhs = sp.block_collapse(-1 * Jd * TH)
    ok1 = all(sp.expand((lhs.blocks[i, j] - TmiH.blocks[i, j]).doit()) in (Zd, 0) or
              getattr(sp.expand((lhs.blocks[i, j] - TmiH.blocks[i, j]).doit()), "is_ZeroMatrix", False)
              for i in range(2) for j in range(2))
    # explicit check for d = 2 that the generator is antisymmetric when H is Hermitian
    h1 = sp.Matrix([[sp.Symbol("a", real=True), sp.Symbol("b", real=True)], [sp.Symbol("b", real=True), sp.Symbol("c", real=True)]])
    h2 = sp.Matrix([[0, sp.Symbol("e", real=True)], [-sp.Symbol("e", real=True), 0]])
    H = h1 + sp.I * h2
    G = -sp.kronecker_product(sp.eye(2), Jm) * Tmap(H)
    ok2 = zero(G + G.T) and zero(Tmap(H) - Tmap(H).T)
    ok = bool(ok1 and ok2)
    return CertResult(ok, "T(−iH) = −Jd T(H) (d symbolic); for Hermitian H the generator −Jd T(H) is antisymmetric "
                      "and the observable T(H) symmetric (d = 2 explicit)" if ok else "FAILED",
                      {"general d": bool(ok1), "d = 2 explicit": bool(ok2),
                       "reading": "generator = −J × observable: the complex structure is present as the real operator J; "
                                  "the model realises ax-complex over the reals instead of dropping it"})


# ----------------------------------------------------------------------------
# the paper as a network delta
# ----------------------------------------------------------------------------

def build() -> Paper:
    G = "GEN_GPT_Level v2.6"
    nodes = [
        Node("m-quantum", "M", "model", "Complex quantum theory (nonclassicality network)",
             "States: unit vectors / density operators on C^d; effects: POVM elements; composition: tensor product over C.",
             "existing", f"{G}:m-quantum"),
        Node("m-realqm", "M", "model", "Real-amplitude QM with real tensor composites (nonclassicality network)",
             "Postulates (i_R), (ii), (iii), (iv) of Renou et al.: real Hilbert spaces, projective measurements, Born "
             "rule, composite space H_S ⊗ H_T over R; independent sources prepare product states.",
             "existing", f"{G}:m-realqm"),
        Node("ax-complex", "M", "axiom", "Complex structure (nonclassicality network)",
             "A real-linear operator J with J² = −1 that commutes with every observable and every transformation; "
             "observables and generators are related by multiplication with J.",
             "existing", f"{G}:ax-complex"),
        Node("ax-loctom", "M", "axiom", "Local tomography (nonclassicality network)",
             "Composite states are fixed by the statistics of local measurements: dim(AB) = dim(A)·dim(B) for the "
             "real linear spans of the state spaces.", "existing", f"{G}:ax-loctom"),
        Node("ax-tensorR", "M", "axiom", "Postulate (iv): Kronecker composition (Renou et al.)",
             "H_ST = H_S ⊗ H_T (tensor product over the field of the theory); local operators act as A ⊗ 1; "
             "independent preparations are tensor products.", "split", f"{G}:m-realqm (part of its definition)"),
        Node("ax-P4", "M", "axiom", "Postulate (P4): local action (Barrios Hita et al.)",
             "There are embeddings ξ (independent preparation) and η^i (local operation) with "
             "η^1(A)ξ(ψ1,ψ2) = ξ(Aψ1,ψ2) and η^2(B)ξ(ψ1,ψ2) = ξ(ψ1,Bψ2)  (Eq. (75)).", "new"),
        Node("f-real", "M", "frame", "Realification maps S, T, R (real-number QM)",
             "S(ψ) = Re ψ ⊗|0> + Im ψ ⊗|1>;  T(A) = Re A ⊗ 1 + Im A ⊗ J;  "
             "R(Ψ) = Re Ψ ⊗ ψ_even^(N) + Im Ψ ⊗ ψ_odd^(N);  T on N flags uses I^(N), J^(N).", "new"),
        Node("m-realflag", "M", "model", "Real-number QM with the flag tensor product ⊗_F",
             "Postulates (P1)–(P3) over R and (P4): states are classes in R^{2dA}⊗R^{2dB} / ker; canonical "
             "representatives lie in the range of P = (1 − J_A⊗J_B)/2; observables are T(A) (commute with J).", "new"),
        Node("s-C", "S", "hilbert", "Complex state space C^d (complex quantum theory)",
             "Unit vectors ψ ∈ C^d up to phase; density operators ρ ≥ 0, tr ρ = 1.", "existing", f"{G}:m-quantum (states)"),
        Node("s-Rflag", "S", "hilbert", "Real state space R^d ⊗ R²_F (real-number QM)",
             "Vectors S(ψ) ∈ R^{2d}; the phase orbit {(1⊗R(α))S(ψ)} is one physical state; density operator T(ρ)/2.", "new"),
        Node("s-canon", "S", "hilbert", "Canonical flag subspace (real-number QM, N parties)",
             "span{ψ_even^(N), ψ_odd^(N)} ⊂ (R²)^{⊗N}: the subspace on which all local J_k coincide.", "new"),
        Node("s-indep", "S", "cluster", "States of two independent sources (network scenario)",
             "Renou et al.: Σ_λ P(λ) σ^λ_{AB1} ⊗ σ^λ_{B2C} with real σ. Flag model: R(Ψ_{AB1} ⊗ Ψ_{B2C}).", "new"),
        Node("o-born", "O", "direct", "Outcome probabilities P(a,b,c|x,z) (network scenario)",
             "Born rule (iii)/(P3) for the three-party entanglement-swapping experiment.", "new"),
        Node("w-T", "O", "witness", "Renou functional T (network Bell functional)",
             "S^b_xz = Σ_ac ac P(a,b,c|x,z);  T_b = (−1)^{b2}(S_11+S_12) + (−1)^{b1}(S_21−S_22) + (−1)^{b2}(S_13+S_14) "
             "− (−1)^{b1+b2}(S_33−S_34) + (−1)^{b1}(S_25+S_26) − (−1)^{b1+b2}(S_35−S_36);  T = Σ_b T_b.", "new",
             refs=["Renou et al., Nature 600, 625 (2021), arXiv:2101.10873"]),
        Node("e-net", "O", "effect", "Network correlations with T > 7.6605 (network scenario)",
             "Statistics of the entanglement-swapping experiment whose T exceeds the bound for real QM with "
             "postulate (iv).", "new", f"{G}: target of edge D6 (currently e-bell)"),
        Node("t-distinguish", "O", "task", "Experimental discrimination of a real-number theory from complex QT",
             "Existence of an experiment whose statistics differ between the two theories.", "new"),
    ]

    E = Edge
    edges = [
        E("RQ1", ["ax-complex"], "f-real", "defines",
          "T: M_d(C) → M_2d(R) is an injective unital real-algebra homomorphism with T(A†) = T(A)^T, and its image "
          "is the commutant of Jd = 1⊗J.", "Eqs. (4)–(5); Props. 2, 6, 7", "exact", cert_RQ1,
          method="block-matrix algebra with d×d matrix symbols, d symbolic"),
        E("RQ2", ["s-C", "f-real"], "s-Rflag", "represents",
          "S is real-linear and bijective C^d → R^2d with T(A)S(ψ) = S(Aψ), S(iψ) = Jd S(ψ), "
          "S(φ)^T S(ψ) = Re<φ|ψ>, S(φ)^T Jd S(ψ) = −Im<φ|ψ>, S(ψ)^T T(A) S(ψ) = Re<ψ|A|ψ>.",
          "Eqs. (1), (2), (6), (67)–(69)", "exact", cert_RQ2, method="symbolic real components"),
        E("RQ3", ["s-C", "f-real"], "s-Rflag", "represents",
          "T1(ρ) = T(ρ)/2 has unit trace, tr[T1(ρ)T(A)] = Re tr(ρA), and A ≥ 0 ⇒ T(A) ≥ 0.",
          "Eqs. (84)–(85)", "exact", cert_RQ3, uses=["RQ1"], method="symbolic 2×2 matrices"),
        E("RQ4", ["f-real"], "s-canon", "defines",
          "P = (1 − J⊗J)/2 is the orthogonal projector onto span{ψ_even^(2), ψ_odd^(2)}; its kernel is spanned by "
          "|00>+|11>, |01>−|10>; on its range J⊗1 = 1⊗J.", "Eq. (8), Fig. 2", "exact", cert_RQ4,
          method="exact 4×4 matrices"),
        E("RQ5", ["s-Rflag", "s-canon"], "s-indep", "composes",
          "S(ψ)⊗_F S(φ) = R(ψ⊗φ): the class of S(ψ)⊗S(φ) has canonical representative R(ψ⊗φ)/√2, and Eq. (34) is "
          "R(ψ⊗φ).", "Prop. 3; Eqs. (34), (38), (51)", "exact", cert_RQ5, uses=["RQ4"],
          method="symbolic vectors, projection with P"),
        E("RQ6", ["f-real"], "s-canon", "defines",
          "ψ_even^(N) + iψ_odd^(N) = 2^{−(N−1)/2}(|0>+i|1>)^{⊗N}; J_k ψ_even = ψ_odd and J_k ψ_odd = −ψ_even for every "
          "flag k; the subspace on which all J_k agree is two-dimensional.", "Eqs. (44)–(46)", "exact", cert_RQ6,
          method="integer arithmetic; rank computation"),
        E("RQ7", ["s-canon"], "f-real", "defines",
          "I^(N) is a projector, (J^(N))² = −I^(N); I^(N+M) = (I^(N)⊗I^(M) − J^(N)⊗J^(M))/2, "
          "J^(N+M) = (I^(N)⊗J^(M) + J^(N)⊗I^(M))/2; partial traces of I^(N), J^(N) are I^(N−M), J^(N−M).",
          "Eqs. (57), (59), (60), (91)", "exact", cert_RQ7, uses=["RQ6"], method="exact rational matrices"),
        E("RQ8", ["f-real", "s-indep"], "ax-P4", "satisfies",
          "(T(A)⊗1)R(Ψ) = R((A⊗1)Ψ) and (1⊗T(B))R(Ψ) = R((1⊗B)Ψ) for all A, B and all Ψ ∈ C^dA⊗C^dB.",
          "Eq. (75), Prop. 11", "exact", cert_RQ8, uses=["RQ5"], method="real bases of operators and vectors"),
        E("RQ9", ["f-real", "s-canon"], "m-realflag", "defines",
          "T(A)⊗T(B) commutes with P and P(T(A)⊗T(B)) = Re(A⊗B)⊗I^(2) + Im(A⊗B)⊗J^(2) "
          "= ½[T(A)⊗T(B) − T(iA)⊗T(iB)].", "Eqs. (55)–(60); Hoffreumon–Woods (B.34)–(B.37)", "exact", cert_RQ9,
          uses=["RQ4", "RQ7"], method="real basis of operator pairs",
          refs=["Hoffreumon, Woods, arXiv:2504.02808v2"]),
        E("RQ10", ["m-realflag", "s-indep"], "o-born", "predicts",
          "R(Φ)^T [T(A)⊗T(B)] R(Ψ) = Re<Φ|A⊗B|Ψ>; hence all bipartite Born probabilities coincide with those of "
          "complex QT, entangled states included.", "Eqs. (6), (68), (85)", "exact", cert_RQ10, uses=["RQ8"],
          method="real bases, polarisation"),
        E("RQ11", ["m-quantum", "s-indep"], "w-T", "predicts",
          "Complex QT with |φ+>_{AB1}|φ+>_{B2C}, A = (Z, X, Y), C = ((X±Z), (Y±Z), (X±Y))/√2 and Bob's Bell "
          "measurement gives P(b) = 1/4 and T = 6√2.", "Eqs. (108)–(112)", "exact", cert_RQ11,
          method="exact arithmetic in Q(√2, i)"),
        E("RQ12", ["m-realflag", "s-indep"], "w-T", "predicts",
          "The real model with state |φ+>|φ+>|ψ_even^(4)> and operators T(Π^A)⊗T(Π^B)⊗T(Π^C) gives the same "
          "probabilities P(a,b,c|x,z) as complex QT for all outcomes and settings, hence T = 6√2.",
          "Eqs. (114)–(124)", "exact", cert_RQ12, uses=["RQ6", "RQ7"], method="exact arithmetic in Q(√2), all four b"),
        E("RQ13", ["w-T"], "w-T", "defines",
          "The value 6√2 is obtained with the functional of Renou et al.; the form printed in the arXiv text "
          "(Eqs. (104)–(106), as extracted) differs in one sign prefactor and in the weighting.",
          "Eqs. (104)–(106) vs Renou et al. Supplementary", "exact", cert_RQ13, uses=["RQ11"],
          method="evaluation of four readings of the definition"),
        E("RQ14", ["m-realflag", "s-indep"], "s-canon", "predicts",
          "After Bob's outcome 00 the real Alice–Charlie state is |φ+><φ+|_AC ⊗ ½(|φ−><φ−| + |ψ+><ψ+|)_{A'C'}.",
          "Eq. (118)", "exact", cert_RQ14, uses=["RQ7"], method="exact partial trace"),
        E("RQ15", ["s-canon", "ax-tensorR"], "s-indep", "violates",
          "The composite space has real dimension 2·dA·dB, not (2dA)(2dB), and the canonical state of two independent "
          "sources, ψ_even^(4) on flags (A'B1')(B2'C'), has Schmidt rank 2 across the source cut: the model does not "
          "satisfy postulate (iv) with product states for independent sources.",
          "main text (the tensor extension fails); Remark 5, Eq. (49); Sec. H", "exact", cert_RQ15, uses=["RQ6"], method="exact rank"),
        E("RQ16", ["m-realflag"], "ax-loctom", "satisfies",
          "dim SY_n = n² = dim Herm_n and (nm)² = n²m²: the flag composition is locally tomographic; the real tensor "
          "product on symmetric matrices is not (excess nm(n−1)(m−1)/4).", "— (count behind edges F5, GN6)",
          "exact", cert_RQ16, method="symbolic dimension count"),
        E("RQ17", ["m-realqm", "ax-tensorR", "s-indep"], "e-net", "forbids",
          "Real QM with postulate (iv) and independent real sources obeys T ≤ 7.6605.",
          "Ref. [12] (Renou et al.): cited in the introduction; bound 7.6605 quoted in Sec. H", "import",
          note="Bound from a semidefinite relaxation (NPA-type hierarchy); Renou et al. state that its tightness is open. "
               "Not re-derived here.", refs=["Renou et al., Nature 600, 625 (2021)"]),
        E("RQ18", ["f-real", "m-realflag"], "ax-complex", "satisfies",
          "T(−iH) = −Jd T(H): the generator of the orthogonal group T(e^{−iHt}) is −Jd times the observable T(H).",
          "Props. 6, 7 (+ edge GN7 of the network)", "exact", cert_RQ18, uses=["RQ1"], method="block-matrix algebra"),
        E("RQ19", ["m-realflag", "m-quantum"], "t-distinguish", "equiv",
          "The real model and complex QT are isomorphic as theories (states, effects, composition, probabilities), so "
          "no experiment discriminates them.", "abstract; closing paragraph of the main text", "compose",
          uses=["RQ1", "RQ2", "RQ3", "RQ5", "RQ6", "RQ7", "RQ8", "RQ9", "RQ10"],
          method="RQ1–RQ3 (single systems), RQ5–RQ9 (composition and local action) and RQ10 (Born rule on "
                 "composites) give a bijection of states and observables that preserves every probability"),
        E("RQ20", ["m-realflag", "m-realqm", "e-net"], "t-distinguish", "consistent",
          "RQ12 (T = 6√2 in the flag model) does not contradict RQ17 (T ≤ 7.6605): the premise 'postulate (iv)' of "
          "RQ17 fails for the flag model (RQ15).", "closing paragraph of the main text; Sec. H, last sentence", "logic",
          uses=["RQ12", "RQ15", "RQ17"],
          rule={"type": "scope_separation", "nogo": "RQ17", "possibility": "RQ12", "premise": "ax-tensorR",
                "evidence": "RQ15"},
          method="kernel rule: scope separation"),
        E("RQ21", ["m-realflag"], "t-distinguish", "claims",
          "'The use of complex numbers is a matter of convenience.'", "abstract", "interpretive",
          note="RQ18 shows that the model contains the complex structure as the real operator J and RQ19 that it is "
               "complex QT in real coordinates. Whether that makes complex numbers 'a convenience' depends on what "
               "one counts as the theory; no edge decides it."),
    ]

    claims = [
        Claim("B-C1", "A real-number formulation with a modified composition rule reproduces the predictions of "
              "complex quantum mechanics, for single and composite systems.", "abstract; Eqs. (6), (75), (85)",
              ["RQ19"]),
        Claim("B-C2", "The entanglement-swapping experiment of Renou et al. is reproduced by the real model: T = 6√2.",
              "Eqs. (114)–(124)", ["RQ12", "RQ11"]),
        Claim("B-C3", "This is compatible with the no-go theorem of Renou et al. because the tensor-product "
              "postulate is replaced.", "closing paragraph of the main text; Sec. H", ["RQ20"]),
        Claim("B-C4", "Real-valued quantum mechanics cannot be falsified, and the use of complex numbers is a matter "
              "of convenience.", "abstract", ["RQ19", "RQ21"], kind="interpretive"),
    ]

    delta = [
        {"op": "SPLIT", "target": "m-realqm", "into": ["m-realqm (with ax-tensorR)", "ax-tensorR"],
         "why": "the composition postulate is the premise that the 2025–26 papers change; it must be a node of its own "
                "so that edges D6 and F5 can name it"},
        {"op": "ADD", "node": "f-real", "layer": "M.frame",
         "why": "realification is a change of representation, not a model"},
        {"op": "GLUE", "node": "m-realflag", "with": "m-quantum",
         "why": "RQ19: same states, effects, composition and probabilities; if model nodes are identified as GPTs up "
                "to linear isomorphism (the layer is described as 'concrete GPTs'), this is one node with two representations"},
        {"op": "ADD", "node": "e-net", "layer": "O.effect",
         "why": "edge D6 currently targets e-bell; the theorem of Renou et al. concerns the network functional T, "
                "not Bell nonlocality"},
        {"op": "RETARGET", "edge": "D6", "from": "m-realqm → e-bell", "to": "m-realqm ∧ ax-tensorR ∧ s-indep → e-net",
         "why": "states the premises under which the no-go holds (RQ17) and survives RQ12"},
        {"op": "SCOPE", "edge": "GN7", "note": "'In real QM the generator is not an observable without superselection' "
         "— the flag model is exactly the superselection case: observables commute with J (RQ1, RQ18)"},
        {"op": "REWRITE", "node": "ax-complex", "note": "definition in terms of a complex structure J rather than of "
         "the number field, since RQ18 realises it over R"},
    ]

    findings = [
        {"level": "note", "title": "Sign and weighting in the restated functional",
         "text": "In the arXiv text (Eqs. (104)–(106) of the PDF, (S96)–(S98) in the HTML rendering of v2; both read "
                 "by an automatic extractor) the prefactor of (S_25+S_26) is (−1)^{b2} and T is Σ_b P(b)T_b with "
                 "joint-probability correlators. Renou et al. have (−1)^{b1} and T = Σ_b T_b. Only the latter gives "
                 "6√2 for every b (RQ13); the printed form gives 5√2/4. The paper's own evaluation uses b = 00 with "
                 "conditional correlators ±1/√2, where the difference vanishes, so its results are unaffected. The "
                 "journal's Supplemental Material was not checked."},
        {"level": "note", "title": "Index in Eq. (123)",
         "text": "The list of correlators contains S^00_44 where the functional uses S^00_34 (as extracted)."},
        {"level": "structure", "title": "What the equivalence is",
         "text": "RQ4–RQ9 show that ⊗_F is the tensor product over C written in real coordinates, and RQ15 that the "
                 "state of two independent sources is correlated across the sources inside the ambient real tensor "
                 "product. The no-go edge of Renou et al. keeps all its premises; the new model does not satisfy one of them."},
        {"level": "structure", "title": "Two papers, one projector",
         "text": "The combination rule of Hoffreumon and Woods (arXiv:2504.02808, Eqs. (B.34)–(B.37)) and the flag "
                 "product are the same compression by P = (1 − J⊗J)/2 (RQ9): two routes into the same target node."},
    ]

    return Paper(
        key="realqm",
        citation="P. Barrios Hita, A. Trushechkin, H. Kampermann, M. Epping, D. Bruß, "
                 "Quantum Mechanics Based on Real Numbers: A Consistent Description, "
                 "Phys. Rev. Lett. 136, 240202 (2026)",
        ids={"doi": "10.1103/4k13-sdjh", "arxiv": "2503.17307"},
        branch="GPT / nonclassicality branch (GEN_GPT_Level v2.6)",
        summary="Replaces the tensor-product postulate of real quantum theory by a 'local action' postulate realised "
                "as a quotient of the real tensor product, and shows that the resulting real-number theory reproduces "
                "complex quantum mechanics, including the network experiment that separates the two under the "
                "tensor-product postulate.",
        nodes=nodes, edges=edges, claims=claims, delta=delta, findings=findings, year=2026,
        phases=[["restructure", "the composition postulate is split off the real-QM model node"],
                ["reduce", "the new real-number model is identified with complex quantum theory"],
                ["falsify", "the no-go route of Renou et al. is kept and given its premises explicitly"]],
        sources=[
            {"title": "Barrios Hita et al., PRL 136, 240202 (2026)", "url": "https://journals.aps.org/prl/abstract/10.1103/4k13-sdjh"},
            {"title": "arXiv:2503.17307", "url": "https://export.arxiv.org/pdf/2503.17307"},
            {"title": "Renou et al., arXiv:2101.10873", "url": "https://arxiv.org/abs/2101.10873v2"},
            {"title": "Hoffreumon, Woods, arXiv:2504.02808", "url": "https://arxiv.org/abs/2504.02808v2"},
        ],
    )
