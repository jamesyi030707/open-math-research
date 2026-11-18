# A uniform translated multiplicity obstruction

## Scope and dependencies

Fix exactly the residual B recorded in [November 17](../2026-11-17/transport.py), the normalized doubly-even lift and kernel dimension zero. This is not a claim about all residual codes or about existence of a binary [64,11,27] code. We use the previously certified full q=28 exclusion ([November 14](../2026-11-14/CLASSIFICATION.md)) and the actual B automorphisms proved on November 17. The latter act on the six-dimensional W restriction's column labels by `(v,e) -> (v+et,e)`, for all t in F2^5. This is a genuine transport of a putative full lift, not just local relabeling.

## Proposition

Let a(v), b(v) be the multiplicities of W columns (v,0),(v,1) among the 27 A columns. Every extendable W restriction satisfies

**a(0) + max_v b(v) <= 2.**

Proof. Under translation t, the zero-S column multiplicity is m0(t)=a(0)+b(t). All 31 nonzero S words have A weight 12 or 16; let q(t) count weight 12. Double-counting ones gives

`12q(t)+16(31-q(t)) = 16(27-m0(t))`, hence `q(t)=16+4m0(t)`.

Since 0<=q(t)<=31, the nonnegative integer m0(t) is at most 3. If a(0)+max b exceeds 2, some actual translated lift has m0=3, q=28. This contradicts the previously certified exclusion of the entire fixed-B, kernel-zero q28 branch. QED.

This is a new uniform consequence of earlier certificates, not a new distance bound. The one-moment identity alone does not exclude q28: the external-section certificate is essential.

## Consequence for q24

The [complete local h-classification](../2026-11-15/H_CLASSIFICATION.md) has 277 markings for each E. For canonical E={1,2,3,4,8,16,28}, exactly one violates the bound: r=4,z=0. Its a(0)=2 and b is the indicator of {28,29,30,31}. Each of those four translations enters q28. The other 276 markings have score exactly 2, so this filter alone does not exclude them.

For arbitrary valid E, its two complementary circuit spans have dimensions 2 and 3. There are 155 choices for the 2-space, 64 complementary 3-spaces, and 7 four-circuits in each 3-space. Thus there are 69,440 E sets. Each has exactly one r=4,z=0 marking. A GL(5,2) change of local S labels fixes label zero and permutes the other labels, preserving a(0) and max b. Consequently the same proved necessary inequality excludes that marking at every E. **No assertion that GL(5,2) preserves B is needed or made.** The inequality is applied independently at each label configuration, using only actual translations there.

Hence this rule covers 69,440 q24 W restrictions, counted up to A-column order, with message labels retained. Seven are already in November 17's stored explicit transport set. There are 69,433 additional patterns relative to that particular set, not a claim of mathematical novelty or of new patterns relative to every earlier argument. The local candidate count after this filter alone is 69,440*276=19,165,440; these are not claimed extendable, and other earlier certificates exclude some of them (all 277 at the original canonical E).

## Exact verification

`multiplicity.py` checks all 277*32=8,864 translated local restrictions and the moment identity, identifies the unique marking, and computes overlap with the stored previous finite set. `result.json` is its deterministic output. No assertion statements or floating point are used. Normal and `python -O` outputs agree. Independent review and code are stored alongside this proof.

The proof chain reuses November 14 and 17 certified results; today's code does not re-run their complete exclusions. No full 19-million-pattern search is performed.
