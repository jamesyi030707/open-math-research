# Bounded inverse-orbit enumeration of paradoxical sequences: construction, invariants, pilot, negative benchmark

T(n)=n/2 (even), (3n+1)/2 (odd); a_s = T^s(n). A **hit** is (n,j) with n>=3, 1<=j<=J, q<=qmax(j) (i.e. 3^q<2^j), a_j>=n, where q = #odd among a_0..a_{j-1}
(Rozier–Terracol "paradoxical", Def. 1.1). The 593 triples / 550 starts found for J=92 are a **reproduction** of their Theorem 1.3 data; nothing here is claimed new,
and nothing here proves Collatz or CST.

## 1. Construction (all steps proved below; no heuristic cut)
* H(j) = floor(R(j,qmax(j))), R(j,q)=1/(2^{j/q}-3) REAL; Hmax(J)=max_{j<=J} H(j) (certificate field `Hmax`).
* Anchor of a hit: x0=a_{s0}, s0 = first index s in [0,j-1] with a_s odd and 3<=a_s<=Hmax. Tail: a_j = T^t(x0), t=j-s0 in [1,J-s0].
* Reverse edges: preds(v) = {2v} U {(2v-1)/3 : v = 2 mod 3}. The odd pred is odd; as a HEAD term it must be > Hmax.
* Tree T(x0): root x0 (depth 0); child 2v; child (2v-1)/3 when v=2 (mod 3) and (2v-1)/3 > Hmax. Depth <= J-1. Leaf test at node v (depth d, o = #odd-pred edges on its path):
  (v, d+t) is a hit  <=>  v <= T^t(x0)  and  o + sodd[x0][t] <= qmax[d+t],   sodd[x0][t] = #odd among T^0(x0..)..T^{t-1}(x0).

## 2. Lemmas (finite-depth invariant before any pruning)
* **L1 (identity)** a_j = n (3^q/2^j) prod_k (1+1/(3 m_k)), m_k = odd terms among a_0..a_{j-1}  [(3m+1)/2 = (3m/2)(1+1/(3m))].
* **L2 (anchor exists, s0<=j-1)** hit => prod >= 2^j/3^q; AM–GM: prod <= (1+1/(3h))^q, h the REAL harmonic mean => h <= R(j,q). The smallest odd value m_o is an INTEGER with
  m_o <= h <= R(j,q) <= R(j,qmax(j)) (R grows with q), so m_o <= floor(R)=H(j)<=Hmax. m_o=1 is impossible (orbit would end in {1,2}, a_j<=2<n). So an odd term in [3,Hmax] exists at some index i<=j-1, hence s0<=i<=j-1<=J-1.
* **L3 (head invariant)** every ODD head term a_s (s<s0) is > Hmax: it is not in [3,Hmax] by minimality of s0, and not 1 (else a_j<=2<n).
* **L4 (membership, uniqueness)** the head a_{s0},a_{s0-1},...,a_0 is a root-to-node path of T(x0): a_s even => a_s=2a_{s+1}; a_s odd => a_s=(2a_{s+1}-1)/3 with a_{s+1}=2 mod 3, odd and > Hmax by L3. T is a function, so n has one orbit, hence one (anchor, depth): no duplicates.
* **L5 (exact leaf test)** the path is the true orbit, so q_{d+t}(v)=o+sodd[x0][t] and a_{d+t}=T^t(x0); the displayed equivalence is exact (j>s0 for every hit by L2).
  Hence: if the enumeration finishes without hitting a cap, its output is exactly P(<=J) (all n, no bound X used).
* **L6 (sound prunings of INTERMEDIATE nodes).** Let w=v+1>=4 (nodes are >=3). Reverse E-edge: w'=2w-1>=(3/2)w. Reverse O-edge: w'=(2/3)w EXACTLY ((2v-1)/3+1=(2v+2)/3).
  P1: o <= ohi[d] := max over s0>=d, 1<=t<=J-s0 of (qmax[s0+t]-sodd[x0][t])  (a hit needs q<=qmax[j]; the final o is >= current o).
  P2: for any descendant leaf: w_leaf >= w (2/3)^{o'}, o' = #remaining O-edges <= min(J-1-d, ohi[d]-o). A leaf can be a hit start only if n <= cap_d := max_{1<=t<=J-d} T^t(x0). So prune iff w (2/3)^{o'max} > cap_d+1 (integer test w*2^{o'} > (cap+1)*3^{o'}).
  These bounds are DEPTH-DEPENDENT (intermediate nodes may be far above X); no cut at the start bound X; no use of "earlier descent" (a node whose orbit already fell below n is never discarded).
* Overflow guards in `inverse_orbit.c`: abort (status 3) if w>=2^64, o'>60 or cap>=2^30 (then w<<o' < 2^124 and (cap+1)3^{o'} < 2^125 fit unsigned __int128). Never triggered.

## 3. Pilot (declared caps: node 3e8 [stage 3: 2.5e9], wall 90 s [stage 3: 60 s], memory O(J); caps hit => INCOMPLETE, proves nothing)
Baseline certificates (paradox_gen.py + independent numpy checker) per J; J=92 baseline = existing certificate, not rescanned. "steps": baseline = (X-2)*J T-applications; inverse = reverse nodes.
| J | X | baseline steps | inverse nodes | nodes/steps | unique candidates (leaf tests) | inv. wall | status | equals baseline |
|---|---|---|---|---|---|---|---|---|
| 46 | 6,560 | 301,668 | 344,109 | 1.14 | 1,233 | 0.005 s | COMPLETE | yes (286) |
| 65 | 125,252 | 8,141,250 | 18,292,922 | 2.2 | 3,762 | 0.26 s | COMPLETE | yes (532) |
| 72 | 125,252 | 9,018,000 | 53,492,331 | 5.9 | 3,961 | 0.86 s | COMPLETE | yes (532) |
| 80 | 125,252 | 10,020,000 | 178,885,090 | 17.9 | 4,166 | 2.46 s | COMPLETE | yes (588) |
| 86 | 125,252 | 10,771,500 | 300,000,001 (cap) | – | – | 4.0 s | **INCOMPLETE (node cap)**, 476 of 588 triples found | subset only |
| 92 | 125,252 | 11,523,000 | 1,095,960,493 | 95.1 | 4,358 | 14.2 s | COMPLETE | yes (593; 550 distinct starts) |
Baseline C scan at J=65..86: 0.03–0.04 s (J=92 baseline wall time not re-measured). Max RSS ~15 MB throughout. Growth of nodes per +1 in J (Hmax=1192 regime): ~1.163.
Stage-1 J=92 projection (6.2e11) was wrong because it mixed Hmax regimes (146->386); the stage-2 same-regime projection (1.09e9) was accurate (observed 1.096e9). Stages 2 and 3 are amendments declared before running; the J=86 cap exhaustion and the J=92 run (separate caps) are both reported.

## 4. Conclusion of the experiment (negative benchmark, mathematically positive)
* Mathematical completeness: proved (L1–L6); finite runs with status COMPLETE reproduce the baseline exactly through J=80 and J=92.
* Candidate domain: only 3.5% of [3,X] (4,358 of 125,250 at J=92) ever needs the exact test — the "small-odd-hit" invariant really shrinks the set of starts.
* Cost: the sound reverse enumeration visits ~95x more nodes than the forward scan has steps at J=92 (~14 s vs ~0.04 s), growing ~1.16^J; the baseline scan only grows with X(J)*J. So **the inverse approach does not outperform the baseline in this regime**; it would need a stronger sound intermediate bound (not found here).
* Not claimed: anything beyond J=92; any CST/Collatz statement; novelty.

## 5. Overlap with the literature (sources actually read)
* Rozier–Terracol, arXiv:2502.00948v4 (13 Apr 2026): Definition 1.1 (paradoxical), CST equivalents C1–C3, Theorem 1.3 (593 sequences with first term <=4614; none known up to 2.8e19). My v4 fetch was truncated before Section 5, so v4's Theorem 5.3 text was not read by me; the v5 PDF I read earlier states the j<=301993 scope. Their scope (all j up to 301993, n up to 2.8e19) is far stronger than this J<=92 reproduction.
* Angeltveit, arXiv:2602.10466v1 (11 Feb 2026): an algorithm to VERIFY convergence for all n<2^N by recursive addition of bits plus four sieves (Descent, mod-9 Preimage, Path-Merging, Odd-Even-Even). Its preimage lemma uses the same reverse edge n=T((2n-1)/3) (n=2 mod 3), but to EXCLUDE starts that merge with smaller ones; its Descent Sieve discards a class once it has descended — which would be unsound for our target (paradoxical returns happen after descent). No code of his was run here.
* arXiv:2605.13886 is withdrawn (v2); its comment says the results duplicate Rozier–Terracol v4. It is not used as a result anywhere.

## 6. Files (hashes in inverse_orbit_hashes.txt)
inverse_orbit.c (enumerator), inverse_orbit_pilot.py / inverse_orbit_stage2.py / inverse_orbit_stage3_J92.py (drivers), inverse_pilot*_results.json, *_log.txt, inv_hits_J*.txt, paradox_cert_J*.json.
