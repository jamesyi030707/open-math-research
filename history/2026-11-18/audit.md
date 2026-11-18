# Independent audit: zero-column obstruction from real translations

## Verdict and scope

The proposed implication is correct for the fixed residual B, normalized doubly-even lift and kernel-zero W restrictions used in the November 14–17 proofs. It excludes one r=4,z=0 restriction for every one of the 69,440 labelled q=24 S orientations. This is a new uniform corollary of the previously proved q=28 exclusion and the actual residual translations, not a new global bound or an independent re-proof of the q=28 theorem. No entire new q branch or entire new E family of 277 restrictions is excluded.

## Derivation

Let a(v), b(v) be the multiplicities of W columns (v,0), (v,1). The November 17 verified residual automorphism with parameter t sends these columns to (v+et,e), hence its zero-S multiplicity is m0(t)=a(0)+b(t). All 31 nonzero S messages in the transported restriction still have left weight 12 or 16: the message action replaces s by s+(s dot t)h, and both choices obey those local windows.

If q(t) counts weight-12 S messages, summing their weights gives

12q(t)+16(31-q(t))=16(27-m0(t)),

because each nonzero S column contributes 16 and a zero column contributes zero. Thus q(t)=16+4m0(t). Since q(t)<=31 and m0(t) is a nonnegative integer, m0(t)<=3. If a(0)+max_v b(v)>2, some actual residual translation therefore has m0=3 and q=28. An extension of the original restriction would transport to an extension in the already excluded complete q=28 branch. Consequently every extendable restriction satisfies a(0)+max_v b(v)<=2.

The maximum includes v=0. This matters for a correct invariant, although the unique q24 violating pattern below has b(0)=0.

## Local classification versus residual symmetry

An arbitrary GL(5,2) relabelling of the S labels fixes zero and permutes the b(v) values. Therefore a(0)+max b is unchanged. GL(5,2) is used only to classify the local patterns and transfer the invariant's value, not to transport a full lift while holding B fixed. Once a locally relabelled pattern is placed at any actual E, its obstruction is established afresh by one of the 32 genuine residual translations. This avoids the invalid assumption that arbitrary local GL transformations are B automorphisms.

Among the existing 277 canonical patterns exactly one violates the inequality: r=4,z=0, a(0)=2 and max b=1. Its three double nonzero labels are each split, and the fourth h-selected label is their XOR. This characterization is intrinsic and gives exactly one pattern per E. The r=4,z=0 pattern has four distinct h-selected labels; translation by any one of them produces three zero-S columns and hence q=28.

## Independent counting and computational checks

`independent_audit.py` reads only the prior canonical h.json and November 17 explicit transport set. It checks the moment identity for all 277*32 transports. It independently enumerates E as a three-point line plus a four-circuit in a complementary three-space: 155 lines, 64 complements per line and 7 four-circuits per complement. The resulting 69,440 E sets are distinct. For every E it reconstructs column multiplicities by character inversion, builds the unique r=4,z=0 pattern, directly checks all 62 nontrivial s and s+h windows, and verifies the obstruction value. The 69,440 complete W-column multisets are distinct.

This audit reuses the certified residual translations and complete q28 exclusion rather than rerunning their full proofs. All checks use explicit exceptions, not assertions.

## Novelty accounting

Seven of these 69,440 patterns already occur in the November 17 explicit set of 8,408 excluded restrictions. Thus 69,440 is the total scope of the new uniform rule, while 69,433 are additional to that particular previously enumerated set. This count is not a claim of novelty against all existing literature. The previous canonical exclusion covers the original r=4,z=0 pattern among those seven.
