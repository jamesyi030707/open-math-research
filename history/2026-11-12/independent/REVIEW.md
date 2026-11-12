# Independent local kernel-zero audit

The executable `review.py` and its normal and optimized-mode output accompany this audit. Both runs passed. Checks use explicit exceptions, not Python `assert`, and exact rational arithmetic.

## Algebra checked separately

Let q and q′ count the weight-12 messages among the 31 nonzero messages of S and their h-translates. Write m_v=m_v,0+m_v,1 for v nonzero, L=Σm_v, M=Σm_v², and z=m_0,1. The first moment gives q′=q+r/4−8z. For the character sum F=27−2w, the base sum of squares is 27²+9q+25(31−q); the translated sum is (27−2r)²+9q′+25(31−q′). Their difference equals 128[P+z(27−L−z)], by character orthogonality. Substitution yields

    P = r(28−r)/32 + z(L+z−28).

For each label, m_v,0 m_v,1 ≤ binom(m_v,2). Summing gives P≤(M−L)/2. This is a general algebraic argument; the finite parameter loop additionally checks the displayed character-square equality for every surviving tuple.

Double-evenness on W implies orthogonality of hA to S A. Consequently the XOR of the nonzero S labels selected by h is zero. The total label XOR is also zero since S A is even, so the unselected label XOR is zero. Neither group can contain exactly one nonzero label. This uses hA nonzero, not hA=0.

## Executed checks

- Independently enumerate all 1024 words from the pinned residual rows; verify rank 10, h weight 32, S⊕<h> dimension 6, and weight 16 for each of its 62 other nonzero messages.
- Enumerate the finite q,r,z domain with exact fractions. Before the XOR condition, q=28 permits only r=4,24 and q=24 excludes r=12,16; q=16,20 retain all six r values. After XOR, q=28 retains exactly (r,z)=(4,1),(24,3).
- Construct the two local controls by explicit column design, transpose into six generating rows, then enumerate all 64 words by iterative XOR. Both have rank 6 and the required local windows, moments and label XORs.
- The r=4 control has weights {0:1,4:1,12:49,16:13}; the r=24 control has {0:1,12:38,16:24,24:1}. Both have L=M=24 and P=0.

## Limits and provenance

The residual JSON is reused unchanged from the archived input; SHA-256 is pinned inside the checker. This audit reuses the already established double-even-rigidity premise rather than re-proving its rank-55 certificate. The general double-even implication is proved above; the actual two controls are additionally checked to be double-even.

The controls realize only a six-dimensional W restriction. They are neither a full rank-10 left matrix nor a [64,11,27] code. The finite filter is a necessary condition, not an existence test or entire-branch exclusion. No literature priority or global nonexistence claim follows. The algebra was independently derived, but this is not external peer review.

Run from any directory with Python 3:

    python review.py
    python -O review.py
