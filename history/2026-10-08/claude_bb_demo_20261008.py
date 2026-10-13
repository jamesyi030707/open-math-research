#!/usr/bin/env python3
"""
Finite demonstration of the single-trajectory adversary argument (BB').

Model (deterministic oracle algorithms): an algorithm alg(orc) may only call orc.query(i) (i in N, answer Bool)
and returns ('inl', n)  [claims alpha(n)=True]  or  ('inr',)  [claims alpha is all-False].
Good(alpha, ('inl', n))  :<=>  alpha(n) = True
Good(alpha, ('inr',))    :<=>  alpha(n) = False for all n

Sequences used are monotone step sequences Seq(t): alpha(i) = (t is not None and i >= t); Seq(None) = all False.
(Monotone, because judges for P_C(n)=isOfHLevel(n+2) C are monotone in n.)

Adversary: run alg on Seq(None), record the finite set S of queried positions (may be empty, may repeat,
may be adaptive).  If output is ('inl',n): wrong on Seq(None).  If ('inr',): let N = max(S) (N=-1 if S empty),
and run alg on Seq(N+1).  Locality (the trace on Seq(N+1) equals the trace on Seq(None)) forces the same
output ('inr',), which is wrong because alpha(N+1)=True.

THIS IS A FINITE SANITY CHECK of the argument on test classes, NOT a proof for all algorithms.
The proof is the 5-line paper argument; the checker verifies its two ingredients (trace equality, outputs) on examples.
Not covered: randomized algorithms, white-box access, extra oracles (e.g. the jump), non-halting (semi-decision) runs.
"""
import itertools, random, sys

class Seq:
    def __init__(self, t): self.t = t                      # first True position or None
    def __call__(self, i): return self.t is not None and i >= self.t
    def good(self, out):
        if out[0] == 'inl': return self(out[1])
        return self.t is None

class Oracle:
    def __init__(self, seq): self._seq = seq; self.trace = []
    def query(self, i):
        a = self._seq(i); self.trace.append((i, a)); return a

def run(alg, seq):
    o = Oracle(seq); out = alg(o); return out, o.trace

def adversary(alg):
    """returns (verdict, details). verdict in {'wrong_on_all_False','wrong_on_tail','LOCALITY_VIOLATED'}"""
    out0, tr0 = run(alg, Seq(None))
    if out0[0] == 'inl':
        return 'wrong_on_all_False', None
    S = {i for i, _ in tr0}
    N = max(S) if S else -1
    seq1 = Seq(N + 1)
    out1, tr1 = run(alg, seq1)
    if tr1 != tr0 or out1 != out0:
        return 'LOCALITY_VIOLATED', (tr0, tr1, out0, out1)
    assert not seq1.good(out1)
    return 'wrong_on_tail', N + 1

# ---------- (A) hand-written test algorithms ----------
def alg_const_inr(o): return ('inr',)
def alg_const_inl(o): return ('inl', 5)
def alg_scan(K):
    def a(o):
        for i in range(K):
            if o.query(i): return ('inl', i)
        return ('inr',)
    return a
def alg_repeat(o):                                  # repeated queries of one position
    for _ in range(10): o.query(3)
    return ('inr',)
def alg_adaptive_jump(o):                           # position depends on earlier answers; large jumps
    p = 1
    for _ in range(12):
        a = o.query(p); p = p * 7 + (1 if a else 2)
    return ('inr',)
def alg_guess_unqueried(o):                         # output witness not in the queried set
    o.query(0); return ('inl', 123456)
def alg_nonuniform_time(o):                         # running time depends on the answer to the first query
    if o.query(0):
        for i in range(1, 10**5): o.query(i)
        return ('inr',)
    for i in range(1, 50): o.query(i)
    return ('inr',)
def alg_peek(o):                                    # CHEAT: reads the hidden sequence (white box) -> not in the model
    return ('inr',) if o._seq.t is None else ('inl', o._seq.t)

# ---------- (B) exhaustive small decision trees ----------
def trees(depth, positions, outs):
    if depth == 0:
        yield from (('leaf', o) for o in outs); return
    sub = list(trees(depth - 1, positions, outs))
    yield from (('leaf', o) for o in outs)
    for i in positions:
        for t0 in sub:
            for t1 in sub:
                yield ('q', i, t0, t1)
def tree_alg(t):
    def a(o):
        node = t
        while node[0] == 'q':
            node = node[3] if o.query(node[1]) else node[2]
        return node[1]
    return a

# ---------- (C) random adaptive algorithms (history-hash policies, bounded steps) ----------
def random_alg(seed, max_steps=30):
    def a(o):
        hist = ()
        for _ in range(max_steps):
            r = random.Random(f"{seed}|{hist}")
            if r.random() < 0.15:
                return ('inl', r.choice([0, 1, 2, 10, 10**6])) if r.random() < 0.3 else ('inr',)
            pos = r.choice([0, 1, 2, 3, 7, 50, 1000, 10**6, 10**9])
            hist += (o.query(pos),)
        return ('inr',)
    return a

def main():
    print("== (A) hand-written algorithms ==")
    tests = [('const_inr', alg_const_inr), ('const_inl5', alg_const_inl), ('scan10', alg_scan(10)),
             ('scan1000', alg_scan(1000)), ('repeat', alg_repeat), ('adaptive_jump', alg_adaptive_jump),
             ('guess_unqueried', alg_guess_unqueried), ('nonuniform_time', alg_nonuniform_time),
             ('PEEK(cheat)', alg_peek)]
    for name, a in tests:
        print(f"  {name:16s} -> {adversary(a)[0]}")
    print("== (A') control: a promise removes the obstruction ==")
    B = 40
    ok = all(Seq(t).good(run(alg_scan(B + 1), Seq(t))[0]) for t in [None] + list(range(0, B + 1)))
    print(f"  scan({B+1}) is correct on all Seq(t), t=None or t<={B}: {ok}")
    print("== (B) exhaustive: all decision trees of depth<=2, positions {0,1,2,3}, outputs inr or inl 0..3 ==")
    outs = [('inr',)] + [('inl', n) for n in range(4)]
    cnt = {'wrong_on_all_False': 0, 'wrong_on_tail': 0, 'LOCALITY_VIOLATED': 0}; total = 0
    for t in trees(2, [0, 1, 2, 3], outs):
        total += 1; cnt[adversary(tree_alg(t))[0]] += 1
    print(f"  trees: {total}; {cnt}; trees correct on both inputs: 0 (every tree lands in one of the two wrong-classes)")
    assert cnt['LOCALITY_VIOLATED'] == 0 and total == sum(cnt.values())
    print("== (C) 20000 random adaptive algorithms (bounded steps, repeated/large/adaptive queries) ==")
    cnt = {'wrong_on_all_False': 0, 'wrong_on_tail': 0, 'LOCALITY_VIOLATED': 0}
    for s in range(20000):
        cnt[adversary(random_alg(s))[0]] += 1
    print(f"  {cnt}")
    assert cnt['LOCALITY_VIOLATED'] == 0

if __name__ == "__main__":
    main()
