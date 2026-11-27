"""A finite test of signed-coordinate transport on fixed residual sections."""
from collections import Counter
from itertools import combinations
from pathlib import Path
import hashlib
import json
import runpy

HERE = Path(__file__).resolve().parent
PREV = HERE.parent / "2026-11-26"
B = (0x17e7146801, 0x6293dc808, 0xf714c2017, 0x35dfc802d, 0xb1f3485c,
     0x63e6a0ae, 0x65be14f, 0x196fc233, 0x3e690ce6, 0xcb73897)
SOURCE, CANDIDATE, POSITIVE_MASK = 115, 0, 10844010

def require(ok, msg):
    if not ok:
        raise ValueError(msg)

def content(path, blob):
    raw = path.read_bytes()
    require(hashlib.sha1(f"blob {len(raw)}".encode() + b"\0" + raw).hexdigest() == blob,
            "unexpected input")
    return json.loads(raw)

def section(a):
    answer = []
    for t in range(64):
        u = a ^ ((t & 31) << 4) ^ (1008 if t & 32 else 0)
        word = 0
        for i,b in enumerate(B):
            if (u >> i) & 1:
                word ^= b
        if word.bit_count() == 14:
            answer.append(t)
    return answer

def rows(cols, labels):
    return [[1 - 2*((t & c).bit_count() % 2) for c in cols] for t in labels]

def profile(f):
    ans = Counter()
    for u,v in combinations(f, 2):
        # Check via direct dot products and independently via Hamming distance.
        k = abs(sum(a*b for a,b in zip(u,v)))
        require(k == abs(len(u) - 2*sum(a != b for a,b in zip(u,v))), "dot/Hamming")
        ans[k] += 1
    return dict(sorted(ans.items()))

def with_rhs(f):
    return [tuple(r) + ((sum(r)+1)//2,) for r in f]

def reverse_tree(node, flips):
    def move(j):
        return 26-j
    result = {"steps": [[move(j), v ^ (j in flips), r] for j,v,r in node["steps"]]}
    if "row" in node:
        result["row"] = node["row"]
    else:
        j = node["j"]
        result["j"] = move(j)
        result["children"] = [reverse_tree(node["children"][v ^ (j in flips)], flips)
                              for v in (0,1)]
    return result

def main():
    sol = content(HERE.parent / "2026-11-15/h.json",
                  "6c2f005c33236b54ed1850f78b7700fcb44b7237")["solutions"]
    data = content(PREV / "trees.json", "620cce91a2f4687deaf60ea431975afbc34fc85a")
    labels = [t for t in section(3) if t not in (25,60)]
    require(len(section(3)) == 16 and labels == data["row_labels"], "source section")
    source_cols, candidate_cols = (sol[i]["columns"] for i in (SOURCE,CANDIDATE))
    f, g = rows(source_cols, labels), rows(candidate_cols, labels)
    before, after = profile(f), profile(g)
    require(before == {3:54,5:37} and after == {3:77,5:14}, "section signatures")
    require(before != after and sum(before.values()) == sum(after.values()) == 91,
            "transport screen did not discriminate")

    h = section(2)
    real = rows(source_cols, h)
    require(len(h) == 16 and all(
        sum(((t & c).bit_count() & 1) ^ ((POSITIVE_MASK >> j) & 1)
            for j,c in enumerate(source_cols)) == 14 for t in h), "positive witness")
    require(all(sum(r[j] * ((POSITIVE_MASK >> j) & 1) for j in range(27)) == r[-1]
                for r in with_rhs(real)), "positive equation check")

    # Synthetic transport control, not a purported residual-code automorphism.
    # X_j = Y_(26-j) except j in flips, where X_j = 1 - Y_(26-j).
    flips = {0,6,25}
    transport = [tuple(row[j] * (-1 if j in flips else 1) for j in reversed(range(27)))
                 + (row[-1] - sum(row[j] for j in flips),) for row in with_rhs(f)]
    require(profile([r[:-1] for r in transport]) == before, "true transport screen")
    old = next(c for c in data["cases"] if c["index"] == SOURCE and not c["swapped"])
    verifier = runpy.run_path(str(PREV / "verify.py"))
    combine, replay = verifier["combination"], verifier["replay"]
    original = replay(old["tree"], {}, [combine(with_rhs(f), y) for y in old["combinations"]])
    moved = replay(reverse_tree(old["tree"], flips), {},
                   [combine(transport, y) for y in old["combinations"]])
    require(original == moved == (35,18,6), "tree replay")
    print(json.dumps({
        "source": {"section":3, "index":SOURCE, "absolute_row_pairs":before},
        "candidate": {"section":3, "index":CANDIDATE, "absolute_row_pairs":after},
        "row_labels":labels, "signed_coordinate_transport":"obstructed",
        "synthetic_transported_tree_nodes_leaves_depth":moved,
        "real_positive_control":{"section":2,"index":SOURCE,"weight14_rows":16,
                                 "mask":POSITIVE_MASK}
    }, indent=2))

if __name__ == "__main__":
    main()
