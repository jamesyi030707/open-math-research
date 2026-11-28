"""Two-step residual and weight-28 profiles; run with Python 3.10+."""
from collections import Counter, defaultdict
from itertools import combinations, product
import json

# The fixed 37-coordinate residual from the October 24 archive.
B = (0x17e7146801, 0x6293dc808, 0xf714c2017, 0x35dfc802d, 0xb1f3485c,
     0x63e6a0ae, 0x65be14f, 0x196fc233, 0x3e690ce6, 0xcb73897)
ANCHOR = 2  # Lock a single weight-14 word, not a scan over possible anchors.

def require(ok, message):
    if not ok:
        raise ValueError(message)

def encode(rows, u):
    w = 0
    for i, row in enumerate(rows):
        if (u >> i) & 1:
            w ^= row
    return w

def rank(rows):
    pivots = {}
    for row in rows:
        while row:
            k = row.bit_length() - 1
            if k not in pivots:
                pivots[k] = row
                break
            row ^= pivots[k]
    return len(pivots)

def weight(w):
    return w.bit_count()

def split_check(t, r):
    bits = [(1 << a)-1 for a in (*t, r)]
    z = sum(b << s for b,s in zip(bits, (0,14,28,42)))
    x = (1 << 28)-1
    y = ((1 << 14)-1) | (((1 << 14)-1) << 28)
    words = [encode((x,y,z), u) for u in range(8)]
    require(len(set(words)) == 8, "toy rank")
    return tuple(sorted(weight(w) for w in words[4:]))

def profiles(r):
    found = set()
    for t in product(range(15), repeat=3):
        closed = tuple(sorted(r + sum(14-t[j] if j in mask else t[j]
                                      for j in range(3))
                              for mask in ((),(0,1),(0,2),(1,2))))
        require(closed == split_check(t, r), "formula / explicit codeword mismatch")
        if all(w >= 28 and w % 4 == 0 for w in closed):
            found.add((tuple(sorted(t)), closed))
    return sorted(found)

def main():
    words = [encode(B,u) for u in range(1 << 10)]
    spec = {0:1,14:160,16:142,18:320,20:160,22:160,24:80,32:1}
    require(len(set(words)) == 1024 and all(w.bit_length() <= 37 for w in words)
            and Counter(map(weight, words)) == spec, "fixed residual")
    mons = [(i,) for i in range(10)] + list(combinations(range(10),2))
    eval_rows = [sum(int(all((u >> i) & 1 for i in m)) << k
                     for k,m in enumerate(mons))
                 for u,w in enumerate(words) if weight(w) == 14]
    require(rank(eval_rows) == 55, "quadratic-rigidity prerequisite")
    anchor = words[ANCHOR]
    require(weight(anchor) == 14, "anchor")
    fibres = defaultdict(list)
    for u,w in enumerate(words):
        fibres[w & ~anchor].append(u)
    require(len(fibres) == 512 and all(len(f) == 2 and f[0]^f[1] == ANCHOR
                                      for f in fibres.values()), "quotient fibres")
    spectrum = Counter(map(weight, fibres))
    require(min(w for w in spectrum if w) == 7, "quotient distance")
    low = {r: Counter(tuple(sorted(weight(words[u]) for u in f))
                      for w,f in fibres.items() if weight(w) == r) for r in (7,8,9)}
    require(low[7] == {(14,14):18} and low[8] == {(14,16):33}
            and low[9] == {(14,18):48,(16,16):6}, "low-weight preimages")
    minimum = [w for w in fibres if weight(w) == 7]
    pair_hist = Counter(weight(a^b) for a,b in combinations(minimum,2))
    edges = Counter()
    for a,b in combinations(minimum,2):
        if weight(a^b) != 8:
            continue
        wa,wb = words[fibres[a][0]],words[fibres[b][0]]
        require(weight(wa & anchor) == weight(wb & anchor) == 7, "seven-subsets")
        inter = weight(wa & wb & anchor)
        require(weight((wa^wb)&anchor) == 14-2*inter, "intersection check")
        edges[inter] += 1
    require(pair_hist == {8:42,10:70,12:37,14:4} and edges == {3:34,4:8}, "pair profiles")
    p7,p8 = profiles(7),profiles(8)
    require(p7 == [((7,7,7),(28,28,28,28))]
            and p8 == [((6,6,8),(28,28,28,32)),((8,8,8),(28,28,28,32))], "weight profiles")
    require(split_check((4,8,8),8) == (24,28,32,32), "negative toy")
    print(json.dumps({
        "anchor_message":ANCHOR,
        "anchor_word_hex":hex(anchor),
        "quadratic_evaluation_rank":55,
        "quotient_length_dimension_distance":[23,9,7],
        "quotient_weight_distribution":dict(sorted(spectrum.items())),
        "low_quotient_preimage_weights":{
            r:{",".join(map(str,k)):v for k,v in sorted(c.items())}
            for r,c in low.items()},
        "weight7_unordered_pair_sum_weights":dict(sorted(pair_hist.items())),
        "weight7_pairs_summing_to_weight8_fixed_block_intersections":dict(sorted(edges.items())),
        "weight7_block_and_fibre_profiles":p7,
        "weight8_block_and_fibre_profiles":p8,
        "forced_weight28_words_in_weight7_or_8_fibres":18*4+33*3,
        "new_exclusion":False
    }, indent=2))

if __name__ == "__main__":
    main()
