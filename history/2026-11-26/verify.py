"""Replay fixed binary weight-14 contradictions with Python 3 (standard library)."""
import copy
import hashlib
import itertools
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
BLOB = "6c2f005c33236b54ed1850f78b7700fcb44b7237"

def need(condition, reason):
    if not condition:
        raise ValueError(reason)

def swap(c):
    return (c & ~5) | ((c & 1) << 2) | ((c & 4) >> 2)

def combination(rows, signs):
    return tuple(sum(c*s for c, s in zip(col, signs)) for col in zip(*rows))

def feasible_one(coeff, target):
    # After complementing variables with negative coefficients, use unsigned subset sums.
    shift = sum(min(0, c) for c in coeff)
    target -= shift
    if target < 0:
        return False
    bits = 1
    for c in coeff:
        bits |= bits << abs(c)
    return ((bits >> target) & 1) == 1

def replay(node, partial, derived):
    def possible(eq, assigned):
        f, rhs = eq[:-1], eq[-1]
        low = high = 0
        for j, c in enumerate(f):
            if j in assigned:
                low += c * assigned[j]
                high += c * assigned[j]
            elif c < 0:
                low += c
            else:
                high += c
        return low <= rhs <= high

    partial = partial.copy()
    for j, v, reason in node["steps"]:
        need(type(j) is int and 0 <= j < 27 and j not in partial, "bad forced index")
        need(type(v) is int and v in (0, 1), "bad forced bit")
        need(type(reason) is int and 0 <= reason < len(derived), "bad reason")
        need(not possible(derived[reason], {**partial, j: 1-v}), "unproved forced bit")
        partial[j] = v
    if "row" in node:
        need(set(node) == {"steps", "row"}, "bad leaf fields")
        i = node["row"]
        need(type(i) is int and 0 <= i < len(derived), "bad leaf reason")
        need(not possible(derived[i], partial), "unproved leaf")
        return 1, 1, 0
    need(set(node) == {"steps", "j", "children"}, "bad branch fields")
    j = node["j"]
    need(type(j) is int and 0 <= j < 27 and j not in partial, "bad split")
    children = node["children"]
    need(len(children) == 2, "missing child")
    a, b = [replay(ch, {**partial, j: v}, derived) for v, ch in enumerate(children)]
    return 1+a[0]+b[0], a[1]+b[1], 1+max(a[2], b[2])

def main():
    raw = (HERE.parent / "2026-11-15" / "h.json").read_bytes()
    header = f"blob {len(raw)}".encode() + bytes([0])
    need(hashlib.sha1(header + raw).hexdigest() == BLOB, "unexpected catalogue")
    catalogue = json.loads(raw)["solutions"]
    data = json.loads((HERE / "trees.json").read_text())
    labels = data["row_labels"]
    need(labels == [0,4,5,10,11,15,18,19,23,33,46,54,56,61], "unexpected original row set")
    expected = {(115, False), (115, True), (139, False), (139, True)}
    for case in data["cases"]:
        index, swapped = case["index"], case["swapped"]
        need(type(swapped) is bool and (index, swapped) in expected, "unexpected case")
        expected.remove((index, swapped))
        cols = catalogue[index]["columns"]
        if swapped:
            cols = [swap(c) for c in cols]
        rows = []
        for t in labels:
            f = tuple(1 - 2*((t & c).bit_count() % 2) for c in cols)
            need(len(f) == 27 and (sum(f)+1) % 2 == 0, "bad row shape")
            rows.append(f + ((sum(f)+1)//2,))
        ys = case["combinations"]
        need(len(ys) == len(set(map(tuple, ys))) == (14 if index == 115 else 16), "unexpected combinations")
        need(all(len(y) == len(labels) and y[0] == 1 and all(type(s) is int and s in (-1,1) for s in y) for y in ys), "bad combination")
        derived = [combination(rows, y) for y in ys]
        tree = case["tree"]
        stats = replay(tree, {}, derived)
        need(stats == ((35,18,6) if index == 115 else (79,40,6)), "unexpected tree statistics")
        need((case["nodes"], case["depth"]) == (stats[0], stats[2]), "header mismatch")
        bad = copy.deepcopy(tree)
        leaf = bad
        while "children" in leaf:
            leaf = leaf["children"][0]
        leaf["row"] = len(derived)
        try:
            replay(bad, {}, derived)
        except ValueError as e:
            need(str(e) == "bad leaf reason", "negative control rejected for wrong reason")
        else:
            raise ValueError("negative control accepted")
        tested = 0
        for tail in itertools.product((-1,1), repeat=13):
            c = combination(rows, (1,)+tail)
            need(feasible_one(c[:-1], c[-1]), "a single all-sign equation was infeasible")
            tested += 1
        print(index, "swapped" if swapped else "original", "nodes/leaves/depth", stats, "used rows", len(ys), "single sums feasible", tested)
    need(not expected, "missing cases")

if __name__ == "__main__":
    main()
