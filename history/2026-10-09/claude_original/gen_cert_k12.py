#!/usr/bin/env python3
"""Generate cert_k12.json.  Uses: DFS over parity words, lifting for residues, recursion for (s,b).
The checker (check_cert_k12.py) does NOT import this file and re-derives everything by direct simulation of T."""
import json
K = 12

def T(n):
    return n // 2 if n % 2 == 0 else (3 * n + 1) // 2

def residue_of_word(word):
    """unique r mod 2^len(word) whose first len(word) branches equal `word` (one lift works at each level:
    the two lifts r, r+2^i give T^i parities that differ because the 2^i-shift changes (3^s n+b)/2^i by 3^s, odd)."""
    r = 0
    for i, p in enumerate(word):
        ok = []
        for c in (0, 1):
            rr = r + (c << i)
            x = rr
            for _ in range(i):
                x = T(x)
            if (x & 1) == p:
                ok.append(rr)
        assert len(ok) == 1, (word, i, ok)
        r = ok[0]
    return r

def sb_of_word(word):
    s = b = 0
    for j, p in enumerate(word):     # step index j (0-based): odd step -> b = 3b + 2^j
        if p:
            b = 3 * b + (1 << j); s += 1
    return s, b

prefixes, open_words = [], []
def rec(word, s):
    j = len(word)
    if j >= 1 and (1 << j) > 3 ** s:      # first j with D_j>0  (D_j=2^j-3^s)
        prefixes.append(word); return
    if j == K:
        open_words.append(word); return
    for bit in (0, 1):
        rec(word + [bit], s + bit)
rec([], 0)

cert = {"k": K, "prefixes": [], "open": []}
for w in prefixes:
    j = len(w); r = residue_of_word(w); s, b = sb_of_word(w)
    D = (1 << j) - 3 ** s
    nmin = r if r >= 2 else r + (1 << j)          # least n>1 in the class
    cert["prefixes"].append({"len": j, "res": r, "s": s, "b": b, "D": D, "nmin": nmin})
cert["open"] = sorted(residue_of_word(w) for w in open_words)
json.dump(cert, open("cert_k12.json", "w"), indent=0)
print("prefix words:", len(prefixes), " open words:", len(open_words))
