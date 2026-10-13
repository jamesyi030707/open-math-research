#!/usr/bin/env python3
"""Compare paradox_cert_J92.json with Table 1, Appendix B and Section 5 statements of Rozier-Terracol arXiv:2502.00948v5
(values typed from the fetched text; any mismatch is printed).  This is a REPRODUCTION check."""
import json, sys
from collections import defaultdict
def T(n): return n // 2 if n % 2 == 0 else (3 * n + 1) // 2
c = json.load(open(sys.argv[1] if len(sys.argv) > 1 else "paradox_cert_J92.json"))
hits = sorted(tuple(h) for h in c["hits"])
# Table 1: (j,q) -> (N, Nodd, nmin, nmax, dmin, dmax)
EXP = {(8,5):(5,0,7,25,1,2), (27,17):(50,12,164,885,1,26), (46,29):(231,56,91,4611,1,188), (54,34):(2,0,432,864,1,2),
       (65,41):(244,62,73,4547,7,292), (73,46):(56,18,487,4614,1,63), (92,58):(5,0,3567,4551,65,125)}
g = defaultdict(list)
for n, j, q in hits:
    x = n
    for _ in range(j): x = T(x)
    g[(j, q)].append((n, x))
ok = True
print("(j,q)   N  Nodd   nmin-nmax     d-range   | expected from Table 1")
for k in sorted(g):
    L = g[k]; N = len(L); nodd = sum(1 for n, x in L if n % 2 and x % 2)
    nmin = min(n for n, _ in L); nmax = max(n for n, _ in L); ds = [x - n for n, x in L]
    got = (N, nodd, nmin, nmax, min(ds), max(ds)); e = EXP.get(k)
    flag = "OK " if got == e else "MISMATCH"
    if got != e: ok = False
    print(f"{str(k):8s}{N:3d} {nodd:4d}  {nmin:5d}-{nmax:5d}  {min(ds):3d}-{max(ds):3d}   | {e} {flag}")
if set(g) != set(EXP): ok = False; print("pair sets differ:", set(g) ^ set(EXP))
print("total hits:", len(hits), "(Theorem 1.3: 593)")
distinct = len({n for n, j, q in hits}); print("distinct starting integers:", distinct, "(paper: 550)")
even_even = sum(1 for n, j, q in hits if n % 2 == 0 and (lambda x: x % 2 == 0)(__import__('functools').reduce(lambda a, _: T(a), range(j), n)))
print("sequences starting and ending at even integers:", even_even, "(paper: 138)")
near = sorted((j, n) for n, j, q in hits if __import__('functools').reduce(lambda a, _: T(a), range(j), n) - n == 1)
EXPN = [(8,7),(8,9),(8,19),(8,25),(27,166),(27,250),(27,333),(27,376),(46,91),(46,121),(46,243),(46,667),(46,889),(54,432),
        (73,487),(73,649),(73,865),(73,1153),(73,2307),(73,3643)]
print("near-cycles T^j(n)=n+1 among hits:", len(near), "(paper: 20)", "; list equals Appendix B minus (3,3):", near == sorted(EXPN))
def orbit(n, j):
    o = [n]
    for _ in range(j): o.append(T(o[-1]))
    return o
contains = all((11 in orbit(n, j)) if j == 8 else (103 in orbit(n, j)) for n, j, q in hits)
print("every sequence contains 11 (j=8) or 103 (j>8):", contains, "(paper claim)")
t859 = sorted((j, orbit(859, j)[-1]) for n, j, q in hits if n == 859)
print("n=859:", t859, "(paper: 46->890, 65->911, 73->866)")
a = [(j, orbit(859, j)[-1]) for j in (46, 65, 73)]; ok = ok and (t859 == sorted(a) and a == [(46, 890), (65, 911), (73, 866)])
ok = ok and len(hits) == 593 and distinct == 550 and even_even == 138 and len(near) == 20 and near == sorted(EXPN) and contains
print("ALL COMPARISONS MATCH" if ok else "SOME COMPARISON DIFFERS")
