#!/usr/bin/env python3
"""Exact replacement for log2l/ceil(L-1e-6) in build_theta.  A=H+1 (Hmax+1), B=3A+1.
Head odd terms are >= A, so each head factor is <= 1+1/(3A); n = x0*2^d/(3^o * P_head) >= x0*2^d/(B/A)^o ; a hit needs n <= V[t]
=>  x0 * 2^d * A^o <= V[t] * B^o   (integers; monotone in o because B > A).   Domain: x0>=3 odd, 0<=d<=J-1, V>=1, H>=5."""
def olo(x0, d, V, H):
    assert H >= 5
    A = H + 1; B = 3 * A + 1; pa = pb = 1; o = 0
    while (x0 << d) * pa > V * pb: o += 1; pa *= A; pb *= B
    return o
def hit_window(x0, d, o, V, Q, qm, H):          # exact window used for leaf(d,o): o+Q<=qmax[d+t] and the integer inequality
    A = H + 1; B = 3 * A + 1
    return o + Q <= qm and (x0 << d) * A ** o <= V * B ** o
if __name__ == "__main__":
    import json, math
    for J in (46, 58):
        c = json.load(open(f"paradox_cert_J{J}.json")); H = c["Hmax"]; qm = [None] + c["qmax"]
        pairs = fl_gt = fl_lt = 0
        for a in range(3, H + 1, 2):
            V = [a]; Q = [0]; x = a
            for t in range(1, J + 1):
                Q.append(Q[-1] + (x & 1)); x = (3 * x + 1) // 2 if x & 1 else x // 2; V.append(x)
            lg = math.log2(3 * (1 + 1 / (3 * (H + 1))))
            for d in range(J):
                for t in range(1, J - d + 1):
                    ex = olo(a, d, V[t], H); fl = max(0, math.ceil((d + math.log2(a / V[t])) / lg - 1e-6)); pairs += 1
                    fl_gt += fl > ex; fl_lt += fl < ex
        print(f"J={J}: (anchor,d,t) triples {pairs}; float olo > exact (would be UNSOUND): {fl_gt}; float olo < exact (sound, weaker): {fl_lt}")
