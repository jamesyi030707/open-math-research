#!/usr/bin/env python3
"""
Independent checker for cert_k12.json  (map T(n)=n/2 even, (3n+1)/2 odd; sigma(n)=min{j>=1: T^j(n)<n}).

Independence: this file imports NOTHING from gen_cert_k12.py or collatz_classes.py and never uses the recursion
(s,b)->(s+1,3b+2^j).  Everything is re-derived from DIRECT SIMULATION of T:
   word(n)   = parities of n, T(n), ..., T^{j-1}(n)
   s_j       = number of odd entries among the first j
   b_j       = 2^j * T^j(n) - 3^{s_j} * n      (integer; must be the same for every lift of a residue class)
   D_j       = 2^j - 3^{s_j}
What is checked (k = 12):
  C1  every residue r mod 4096: word of 12 steps, s_j, b_j identical on 4 lifts (affine exactness, parity consistency)
  C2  from scratch partition: first j with D_j>0 (j*) or none; compare EXACTLY with the certificate
        prefixes  {(len, res)}  and the open list
  C3  each certificate prefix: s,b,D recomputed by simulation on 5 lifts and equal to the certificate fields;
        D>0; no earlier j has D_j>0; nmin = least n>1 in the class; b < D*nmin (strict, integers); T^len(nmin) < nmin
  C4  prefix cylinders pairwise disjoint (prefix-freeness), expansion to residues mod 4096 is an exact partition
        of Z/4096 together with the open list; sizes; weighted coverage sum 2^-len == 1935/2048
  C5  every covered residue mod 4096: its least n>1 exceeds the threshold b/D at j* (strict integer test)
  C6  every open residue: D_j<0 and b_j>=0 for ALL j<=12 (so T^j(n)>n for every n>=1 in the class)
  C7  direct scan n=2..N: first strict-descent time within 12 steps == j*(n mod 4096) if covered, else none
  --selftest : mutate the certificate in 9 ways and require the checker to REJECT each mutation.
"""
import copy, hashlib, json, sys
from collections import Counter
from fractions import Fraction

K = 12
M = 1 << K
CLAIMED = dict(prefixes=57, covered=3870, open=226, weight=Fraction(1935, 2048))

def T(n):
    return n // 2 if n % 2 == 0 else (3 * n + 1) // 2

def trace(n, j):
    """returns (word, seq) with word[i] = parity of T^i(n), seq[i] = T^i(n), i=0..j"""
    word, seq, x = [], [n], n
    for _ in range(j):
        word.append(x & 1); x = T(x); seq.append(x)
    return word, seq

def class_data(res, e, j, lifts):
    """derive (word, s_j, b_j) for residue res mod 2^e by simulating j steps on several lifts; None on inconsistency"""
    out = set()
    for t in lifts:
        n0 = res + (1 << e) * t
        word, seq = trace(n0, j)
        s = sum(word)
        out.add((tuple(word), s, (1 << j) * seq[j] - 3 ** s * n0))
    return out.pop() if len(out) == 1 else None

def run_checks(cert, N, verbose=True):
    F = []
    def fail(msg): F.append(msg)
    def ok(name, detail=""):
        if verbose: print(f"[PASS] {name} {detail}")

    # ---------- structure ----------
    try:
        prefixes = cert["prefixes"]; opens = cert["open"]; assert cert["k"] == K
        for p in prefixes:
            assert all(isinstance(p[f], int) for f in ("len", "res", "s", "b", "D", "nmin"))
            assert 1 <= p["len"] <= K and 0 <= p["res"] < (1 << p["len"])
        assert all(isinstance(r, int) and 0 <= r < M for r in opens)
    except Exception as ex:
        return [f"STRUCTURE: {ex!r}"]
    if len({(p["len"], p["res"]) for p in prefixes}) != len(prefixes): fail("duplicate prefixes")
    if len(set(opens)) != len(opens): fail("duplicate open residues")

    # ---------- C1 + C2 + C6: from-scratch partition ----------
    jstar = {}                                  # r -> (j*, s, b, D) or None
    c1_bad = 0; open_bad = 0
    for r in range(M):
        lifts = [r + M * t for t in range(1, 5)]
        trs = [trace(n0, K) for n0 in lifts]
        if any(tr[0] != trs[0][0] for tr in trs): c1_bad += 1; fail(f"C1 parity word differs across lifts r={r}")
        word = trs[0][0]
        s = 0; first = None
        for j in range(1, K + 1):
            s += word[j - 1]
            bs = {(1 << j) * tr[1][j] - 3 ** s * n0 for tr, n0 in zip(trs, lifts)}
            if len(bs) != 1: c1_bad += 1; fail(f"C1 remainder b_j not constant r={r} j={j}"); continue
            b = bs.pop(); D = (1 << j) - 3 ** s
            if b < 0: c1_bad += 1; fail(f"C1 negative remainder r={r} j={j}")
            if D == 0: c1_bad += 1; fail(f"C1 D=0 r={r} j={j}")
            if D > 0 and first is None: first = (j, s, b, D)
        jstar[r] = first
        if first is None:                       # C6: D_j<0 for all j (first is None) and b_j>=0 was checked above
            pass
    if c1_bad == 0: ok("C1 affine exactness & parity consistency", f"(4096 residues x 4 lifts x 12 steps)")
    exp_open = sorted(r for r in range(M) if jstar[r] is None)
    exp_prefix = {(jstar[r][0], r % (1 << jstar[r][0])) for r in range(M) if jstar[r] is not None}
    got_prefix = {(p["len"], p["res"]) for p in prefixes}
    if exp_prefix != got_prefix: fail(f"C2 prefix set differs: only-in-cert={sorted(got_prefix-exp_prefix)[:5]} only-derived={sorted(exp_prefix-got_prefix)[:5]}")
    else: ok("C2 prefix set equals from-scratch derivation", f"({len(got_prefix)} prefixes)")
    if exp_open != sorted(opens): fail(f"C2 open set differs (cert {len(opens)} vs derived {len(exp_open)})")
    else: ok("C2 open list equals from-scratch derivation", f"({len(opens)} residues)")
    open_set = set(exp_open)
    bad = 0
    for r in exp_open:                          # C6 explicit: D_j<0, b_j>=0, and T^j(n)>n on lifts
        for t in range(1, 5):
            n0 = r + M * t; word, seq = trace(n0, K); s = 0
            for j in range(1, K + 1):
                s += word[j - 1]
                if not ((1 << j) - 3 ** s < 0 and (1 << j) * seq[j] - 3 ** s * n0 >= 0 and seq[j] > n0): bad += 1
    if bad: fail(f"C6 open classes: {bad} violations")
    else: ok("C6 open classes: D_j<0, b_j>=0, T^j(n)>n for all j<=12", f"({len(exp_open)} classes)")

    # ---------- C3: each certificate prefix ----------
    c3_bad = 0
    for p in prefixes:
        e, r = p["len"], p["res"]
        data = class_data(r, e, e, range(1, 6))
        if data is None: c3_bad += 1; fail(f"C3 inconsistent lifts for {(e, r)}"); continue
        word, s, b = data; D = (1 << e) - 3 ** s
        if (s, b, D) != (p["s"], p["b"], p["D"]): c3_bad += 1; fail(f"C3 cert fields differ for {(e, r)}: derived {(s, b, D)}"); continue
        if D <= 0: c3_bad += 1; fail(f"C3 D<=0 for {(e, r)}"); continue
        cs = 0
        for i in range(1, e):                   # no earlier descent possibility
            cs += word[i - 1]
            if (1 << i) >= 3 ** cs: c3_bad += 1; fail(f"C3 earlier D_i>0 at i={i} for {(e, r)}")
        nmin = r if r >= 2 else r + (1 << e)
        if p["nmin"] != nmin: c3_bad += 1; fail(f"C3 nmin differs for {(e, r)}")
        if not b < D * nmin: c3_bad += 1; fail(f"C3 threshold not exceeded for {(e, r)}: b={b} D={D} nmin={nmin}")
        x = nmin
        for _ in range(e): x = T(x)
        if not x < nmin: c3_bad += 1; fail(f"C3 no strict descent at nmin for {(e, r)}")
    if c3_bad == 0: ok("C3 per-prefix fields, minimality, strict threshold b < D*nmin, direct descent at nmin", f"({len(prefixes)} prefixes)")

    # ---------- C4: disjointness, exact partition, weighted coverage ----------
    ov = 0
    for a in prefixes:
        for c in prefixes:
            if a is not c and a["len"] <= c["len"] and c["res"] % (1 << a["len"]) == a["res"]: ov += 1
    if ov: fail(f"C4 {ov} overlapping prefix pairs")
    else: ok("C4 prefix cylinders pairwise disjoint (prefix-free)")
    cover = Counter()
    for p in prefixes:
        for t in range(1 << (K - p["len"])): cover[p["res"] + (t << p["len"])] += 1
    multi = [r for r, c in cover.items() if c > 1]
    if multi: fail(f"C4 residues covered twice: {multi[:5]}")
    if set(cover) & set(opens): fail("C4 open list intersects covered residues")
    if set(cover) | set(opens) != set(range(M)): fail("C4 covered ∪ open != Z/4096")
    if len(cover) + len(opens) != M: fail("C4 sizes do not add to 4096")
    w = sum((Fraction(1, 1 << p["len"]) for p in prefixes), Fraction(0))
    if w != Fraction(len(cover), M): fail(f"C4 weight {w} != covered/4096 = {Fraction(len(cover), M)}")
    if verbose: ok("C4 exact partition of Z/4096", f"covered={len(cover)} open={len(opens)} weight={w}  lens={dict(sorted(Counter(p['len'] for p in prefixes).items()))}")
    claimed_ok = (len(prefixes) == CLAIMED["prefixes"] and len(cover) == CLAIMED["covered"]
                  and len(opens) == CLAIMED["open"] and w == CLAIMED["weight"])
    if not claimed_ok: fail(f"CLAIMED numbers (57, 3870, 226, 1935/2048) not reproduced: got {(len(prefixes), len(cover), len(opens), w)}")
    else: ok("claimed numbers reproduced: 57 prefixes, 3870 covered, 226 open, weight 1935/2048")

    # ---------- C5: threshold at mod-4096 level ----------
    bad = 0; maxratio = Fraction(0); eq = 0
    for r in range(M):
        if jstar[r] is None: continue
        j, s, b, D = jstar[r]
        n4096 = r if r >= 2 else r + M
        if not (D > 0 and b < D * n4096): bad += 1; fail(f"C5 threshold not exceeded r={r}")
        maxratio = max(maxratio, Fraction(b, D)); eq += (b % D == 0)
    if bad == 0: ok("C5 every covered residue mod 4096: least n>1 > threshold b/D (strict)", f"max b/D = {maxratio} ≈ {float(maxratio):.4f}; classes with integer b/D: {eq}")

    # ---------- C7: direct scan ----------
    mism = 0; cnt = Counter()
    for n in range(2, N + 1):
        x = n; first = None
        for j in range(1, K + 1):
            x = T(x)
            if x < n: first = j; break
        e = jstar[n % M]; exp = e[0] if e else None
        cnt[first] += 1
        if first != exp: mism += 1; fail(f"C7 n={n}: direct first descent {first}, certificate {exp}")
    if mism == 0: ok(f"C7 direct scan 2<=n<={N}: first strict descent within 12 steps == certified j* (or none)", f"(distribution {dict(sorted(cnt.items(), key=lambda kv: (kv[0] is None, kv[0] or 0)))})")
    return F

def mutations(cert):
    out = []
    c = copy.deepcopy(cert); c["prefixes"][10]["b"] += 1; out.append(("b+1", c))
    c = copy.deepcopy(cert); c["prefixes"][20]["D"] += 2; out.append(("D+2", c))
    c = copy.deepcopy(cert); del c["prefixes"][5]; out.append(("drop prefix", c))
    c = copy.deepcopy(cert); p = c["prefixes"][30]; c["prefixes"].append({**p, "len": p["len"]}); out.append(("duplicate prefix", c))
    c = copy.deepcopy(cert); p = c["prefixes"][3]
    if p["len"] < K: c["prefixes"].append({**p, "len": p["len"] + 1}); out.append(("overlapping refinement", c))
    c = copy.deepcopy(cert); c["open"].pop(0); out.append(("drop open residue", c))
    c = copy.deepcopy(cert); c["open"][0] = (c["open"][0] + 1) % M if (c["open"][0] + 1) % M not in c["open"] else (c["open"][0] + 2) % M; out.append(("shift an open residue", c))
    c = copy.deepcopy(cert); c["prefixes"][12]["nmin"] -= 1; out.append(("nmin-1", c))
    c = copy.deepcopy(cert); c["prefixes"][7]["res"] = (c["prefixes"][7]["res"] + 1) % (1 << c["prefixes"][7]["len"]); out.append(("move residue", c))
    return out

def main():
    path = "cert_k12.json"; N = 200000; selftest = False
    for a in sys.argv[1:]:
        if a == "--selftest": selftest = True
        elif a.startswith("--N="): N = int(a[4:])
        else: path = a
    raw = open(path, "rb").read()
    print(f"certificate {path}  sha256={hashlib.sha256(raw).hexdigest()}  ({len(raw)} bytes)")
    cert = json.loads(raw)
    F = run_checks(cert, N)
    if selftest:
        print("---- selftest: mutated certificates must be REJECTED ----")
        for name, c in mutations(cert):
            f = run_checks(c, 3000, verbose=False)
            print(f"  mutation '{name}': {'REJECTED' if f else 'ACCEPTED (BAD!)'}  ({len(f)} failure messages)")
            if not f: F.append(f"selftest: mutation {name} accepted")
    print("=" * 60)
    if F:
        print(f"FAIL: {len(F)} problems; first: {F[:3]}"); sys.exit(1)
    print("ALL CHECKS PASSED (k=12 certificate; finite facts only; not a Collatz proof)")

if __name__ == "__main__":
    main()
