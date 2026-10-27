#!/usr/bin/env python3
"""Fourier/subspace constraints on a(u)=sum_v m_v [u.v=1] (m_v>=0 integer column multiplicities, N columns, zero column allowed).
 m_v = 2^-n sum_u (N-2a(u)) (-1)^{u.v};  for any subspace S (dim d): sum_{u in S} a(u) = 2^(d-1) (N - M_S), M_S = sum_{v in S^perp} m_v in [0,N].
Toy (V=F_2^3, N=6): same value histogram, different label compatibility.  Also checks: a quadratic function sums to 0 mod 2 over any 3-dim subspace."""
import itertools, random
n = 3; N = 6; pc = lambda x: bin(x).count("1"); par = lambda x: pc(x) & 1
def labeling(m): return [sum(m[v] for v in range(8) if par(u & v)) for u in range(8)]
def inverse(a):
    out = []
    for v in range(8):
        s = sum((N - 2 * a[u]) * (-1) ** par(u & v) for u in range(8))
        out.append(s / 8)
    return out
def subspaces():
    seen = set()
    for r in range(0, 4):
        for gens in itertools.combinations(range(1, 8), r):
            S = {0}
            for g in gens: S |= {s ^ g for s in S}
            seen.add(frozenset(S))
    return seen
subs = subspaces(); print("subspaces of F_2^3:", len(subs))
real = {}
for m in itertools.product(range(N + 1), repeat=8):
    if sum(m) == N: real[tuple(labeling(m))] = m
print("realizable labelings (N=6):", len(real))
ok_id = all(sum(a[u] for u in S) * 2 == len(S) * (N - sum(m[v] for v in range(8) if all(par(u & v) == 0 for u in S))) for a, m in real.items() for S in subs)
print("subspace identity sum_S a = |S|(N-M_S)/2 holds for every realizable labeling and subspace:", ok_id)
base = next(a for a in real if len(set(a[1:])) >= 3 and a[0] == 0)
hist = sorted(base[1:]); print("base labeling a =", list(base), "columns m =", real[base], "| nonzero-value histogram:", hist)
good = bad = 0; example = None
for perm in set(itertools.permutations(base[1:])):
    a2 = (0,) + perm
    if a2 in real: good += 1
    else:
        bad += 1
        if example is None: example = a2
inv = inverse(example)
print(f"distinct relabelings with identical histogram: realizable {good}, NOT realizable {bad}")
print("example relabeling a' =", list(example), "| inverse m_v =", inv, "-> fails (negative/non-integer)")
for S in sorted(subs, key=lambda s: (len(s), sorted(s))):
    if len(S) in (2, 4):
        tot = sum(example[u] for u in S); need = len(S) // 2
        if tot % need or not (0 <= tot / need <= 2 * N / 1) or (N - tot / need) < 0:
            print(f"   violated subspace S={sorted(S)}: sum a' = {tot}, must equal {len(S)//2}*(N-M_S) with integer 0<=M_S<=N"); break
# quadratic functions have even sum over every 3-dim subspace (so the d=3 cut is implied once q_A=q_B is quadratic)
random.seed(1); okq = True
for _ in range(2000):
    nv = 9; lin = random.getrandbits(nv); quad = [(i, j) for i in range(nv) for j in range(i + 1, nv) if random.getrandbits(1)]
    q = lambda u: (par(u & lin) + sum(((u >> i) & 1) & ((u >> j) & 1) for i, j in quad)) % 2
    b = random.sample(range(1, 512), 3)
    if len({b[0], b[1], b[0] ^ b[1], b[2]}) < 4 or b[2] in (b[0] ^ b[1],): continue
    S = {0}
    for g in b: S |= {s ^ g for s in S}
    okq &= sum(q(u) for u in S) % 2 == 0
print("random quadratics on F_2^9: sum over random 3-dim subspaces is even:", okq)
 
