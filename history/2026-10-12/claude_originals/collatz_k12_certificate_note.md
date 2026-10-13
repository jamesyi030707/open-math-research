# Collatz, shortcut map T: k = 12 finite certificate (note)

T(n) = n/2 (even), (3n+1)/2 (odd). σ(n) = min{ j ≥ 1 : T^j(n) < n } for n > 1.
**Nothing here proves the Collatz conjecture.** Lemma D (σ finite for all n>1 ⇔ Collatz) is not used.
No novelty is claimed; these are textbook-style (Terras-type) class decompositions.

## 0. Corrections recorded
- **A (retracted claim).** "The first L branches of w = (3^m−1)/2^{v₂(3^m−1)} depend only on m mod 2^(L−1)" is **false**: m = 2 and m = 6 (congruent mod 4) give w = 1 and 91, W₃ = 101 vs 110 (already W₂ = 10 vs 11). The error: for even m, v = v₂(3^m−1) depends on e = v₂(m).
- **A (corrected, sufficient, not claimed minimal).** Lemma O: 3^(2^k) ≡ 1 (mod 2^(k+2)) for k ≥ 1 (induction). Lemma V: v₂(3^m−1) = 1 (m odd), 2+e (m even, e = v₂(m)). Then
  - m odd, L ≥ 2: W_L depends only on m mod 2^(L−1) (w mod 2^L ← 3^m mod 2^(L+1)); L = 1: W₁ = (1).
  - m even: W_L depends only on (e, m mod 2^(e+L)) (w mod 2^L ← 3^m mod 2^(e+L+2); e fixes v).
  - unnormalised x = 3^m−1 is a different object: its first L branches depend on 3^m mod 2^L, i.e. m mod 2^(L−2) (L ≥ 3), and word(x) = 0^v · word(w).
- **B.** Slope 3^s/2^j < 1 (D > 0) alone does not give descent at a given n: T^j(n) < n ⇔ b < (2^j − 3^s)·n (strict). Boundary: n = 1, word (1,0), s = 1, b = 1, D = 1: 1 < 1 is false, T²(1) = 1. Also n = 2 at j = 2 (descent happened earlier at j = 1).
- **Earlier wording.** The real threshold is b/D (max 319/13 ≈ 24.538 at k = 12); ⌊b/D⌋ = 24 is derived; the least integer start satisfying the strict inequality is 25.

## 1. General (any k) statements, paper proofs
- **G1** (Theorem A) The first k branches of n depend only on n mod 2^k. Proof: T^j(n) = (3^s n + b)/2^j with s, b fixed by the first j branches; parity of T^j(n) is determined by 3^s n + b mod 2^(j+1).
- **G2** Words ↔ classes: exactly one class mod 2^j for each word of length j (lifting r → r or r+2^i: the two lifts change (3^s n+b)/2^i by 3^s, odd, so exactly one matches the next parity).
- **G3** (affine lemma) T^j(n) < n ⇔ b < D·n, D = 2^j − 3^s ≠ 0 for j ≥ 1. D < 0 ⇒ T^j(n) > n for all n ≥ 1 (b ≥ 0). D > 0 ⇒ descent ⇔ n > b/D (a real inequality; equality n = b/D means T^j(n) = n).
- **G4** Stopping words (first j with D_j > 0 along the word) form a prefix-free set; so their cylinders (classes mod 2^len) are pairwise disjoint (a common member's word would have both as prefixes).
- **G5** Weighted coverage Σ 2^(−len) over stopping words of length ≤ k equals (number of covered residues mod 2^k)/2^k = 1 − c(k)/2^k, with c(k) = number of words of length k with D_j < 0 for all j ≤ k.
- **G6 (corrected; supersedes the earlier "iff threshold condition" wording)** For a class r mod 2^k put theta_r := min{ b_j/D_j : 1<=j<=k, D_j>0 } (infinity if no such j). Exact class criterion: for n = r (mod 2^k), sigma(n) <= k  <=>  n > theta_r (real inequality). The classification "sigma(n)<=k <=> n lies in a covered class, for all n>1" holds <=> every covered class has least n>1 greater than theta_r (open classes never descend, so "=>" is automatic). The FIRST-threshold condition (least n>1 > b_{j*}/D_{j*}) is SUFFICIENT (it gives sigma(n)=j* exactly and theta_r <= b_{j*}/D_{j*}); its NECESSITY is NOT claimed: an n could fail at j* and still descend later within k steps. Remark: a failure of the first-threshold condition at some cylinder is exactly an n>1 with t(n) > tau(n), i.e. a counterexample to Terras' CST conjecture (Rozier-Terracol, formulation C1); no such n is known below 2.8e19. See collatz_formal_corrections.md.

## 2. k = 12 exhaustive facts (checker output, `check_log_k12.txt`)
- 57 stopping words, lengths {1:1, 2:1, 4:1, 5:2, 7:3, 8:7, 10:12, 12:30}; weight 1/2+1/4+1/16+2/32+3/128+7/256+12/1024+30/4096 = **1935/2048**; refined to mod 4096: **3870** classes covered, **226** open.
- Every open class has D_j < 0 and b_j ≥ 0 for all j ≤ 12, so T^j(n) > n for all n ≥ 1 in it.
- Every certified class: least n > 1 exceeds b/D (max b/D = 319/13; 3072 residues mod 4096 have integer b/D).
- **Theorem (k = 12, finite certificate).** For every n > 1: σ(n) ≤ 12 ⇔ n mod 4096 lies in one of the 3870 certified classes, and then σ(n) equals the class's j*. Proof = G1–G6 + the finite checks above.
- Direct scan 2 ≤ n ≤ 200000 agrees (distribution of σ: 1:100000, 2:49999, 4:12500, 5:12500, 7:4689, 8:5468, 10:2341, 12:1466, >12: 11036). This is a finite sanity check, not part of the proof.

## 3. What was run
- `gen_cert_k12.py` → `cert_k12.json` ("generated", **not** "verified").
- `check_cert_k12.py` (imports nothing from the generator; derives words, s, b, D by direct simulation; checks C1–C7; `--selftest` rejects all 9 mutated certificates) → `check_log_k12.txt`: **ALL CHECKS PASSED** (finite facts only).
- `periodicity_w_check.py` → `periodicity_w_log.txt`; `affine_boundary_examples.py` → `affine_boundary_log.txt`.

## 4. Not done / not claimed
- No claim for k > 12; each k needs its own threshold check.
- Part A moduli are sufficient, not shown minimal; the finite groupings in the log only test statements proved on paper.
- `collatz_tables.py` in the outputs directory was not created by me and is neither run nor cited.
- Independence of checker from generator is logical (different derivation: simulation vs. recursion), but both are by the same author in the same language; an outside reimplementation would be stronger.
