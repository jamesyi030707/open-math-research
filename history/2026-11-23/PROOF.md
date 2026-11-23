# A genuine gap between all character pairs and one full section

Keep fixed the explicit binary residual B, the kernel-zero branch and the established doubly-even normalization. Use the same rank-six W embedding as on November 22. From the November 15 catalogue take the first index for each surviving multiplicity shape, in zero-based order: 1, 19, 115, 139, 163, 259. Use each original marking and the same fixed low-bit swap (0,2), preserving column order and bit 5. This was a twelve-control test, not a scan of orientations. Each passes the 63 local distance windows and congruences, has q=24, and passes the November 18 multiplicity rule. A local relabeling does not change the fixed B and is not assumed to act on B.

For one of the ten tested external cosets a, let H_a consist of the sixteen labels t for which the residual weight is 14. The A-side weight must be 14: the distance window permits 13 or 14 and the normalization requires the combined weight to be divisible by four. The corresponding offset-sign system is Σ_j χ_t(c_j) ε_j=−1 for t∈H_a, with χ_t(v)=(-1)^{〈t,v〉} and each ε_j=±1. If F_a(u)=Σ_{t∈H_a} χ_t(u), the projected system is Σ_j F_a(u XOR c_j) ε_j=−F_a(u). The 64 projected equations together are equivalent to the sixteen equations, since the 64×64 character matrix is invertible and unselected rows have residual zero.

## Two short filters

For distinct u,v and s=±1 write D(c)=F_a(u XOR c)+s F_a(v XOR c), T=−D(0), and g=gcd_j |D(c_j)|. For g>0, any sign solution requires T≡Σ_j D(c_j) mod 2g, since ε_j−1 is even. For g=0 the target must be zero. The singleton test is its special case with zero target and exactly one nonzero column coefficient; positions, not distinct labels, are counted.

Across the 4,032 choices (u<v,s) in each of the ten actual minimum-word sections, both filters hit only four of twelve controls: indices 1 and 259, each in both orientations. The congruence catches more combinations but no additional controls in this panel. The new swapped 259 case is exhausted by a=2, u=33, v=38, s=−1: only zero-based column 14 remains, with equation 16 ε_14=0. For a non-singleton congruence on the same control set (u,v,s)=(32,47,−1). Its five coefficients (−16,+16,−16,+16,+16), at zero-based positions (8,11,18,25,26), sum to 16, whereas T=0 and 2g=32.

## Exact stronger test on the eight filter misses

For all eight remaining cases and each of a=2,3, every one of the 2,016 unordered pairs among **all 64 character directions** can meet its two targets with a common sign vector. That vector may vary by pair. This statement is stronger than checking pair sums or differences separately. It is proved by exact pair-sum bitsets: after dividing coefficients by 4, encode each pair (x,y) as 512x+y. Each y-coordinate of a reachable signed sum has absolute value at most 108 and the target at most 4, so equality in the encoded value for a reachable point and the target cannot disguise a nonzero y-difference. Subset-shift accumulation gives exact reachability of the encoded target.

Yet the raw full-section counts are:

| Source index | Shape (r,z) | a=2 original / swapped | a=3 original / swapped |
|---|---|---|---|
| 19 | (8,1) | 128 / 48 | 0 / 0 |
| 115 | (8,2) | 64 / 16 | 0 / 0 |
| 139 | (20,1) | 64 / 16 | 0 / 0 |
| 163 | (20,2) | 128 / 48 | 0 / 0 |

Counts here are of raw 27-bit offsets satisfying all sixteen minimum-word equations of that section, without any quotient, and not of lifts or offsets satisfying additional words. Exact meet-in-the-middle splits the 27 columns 13+14, forms the sixteen actual mismatch counts from each half, and tests complementary weight-count vectors summing to 14 in each coordinate. Every right component is at most 14. The packed implementation uses five bits per component, so no carries or borrows affect its target comparisons, and counts all left-half multiplicities. The independent implementation uses explicit tuples without such packing, and provides positive offset masks for a=2. The a=3 section is H_3=(0,4,5,10,11,15,18,19,23,25,33,46,54,56,60,61). Failure on these sixteen necessary equalities precludes extension at that marking, without needing a search of all other weight inequalities.

## Prior coverage and limits

The four swapped cases just rejected at a=3 plus swapped 259 have distinct (r,z) and are not in the November 17 8,408-member explicit transport set or the full November 22 orbit set (480 members, including November 21's six orbits). Their q24 representatives pass the November 18 multiplicity test. Within a true translation orbit r is fixed, and z is fixed on its q24 slice; thus these are five distinct orbits. Direct re-enumeration gives respectively 8,1,20,1,3 q24 members for swapped indices 19,115,139,163,259. We report five concrete representative exclusions relative to the named earlier coverage, not a historical novelty or a branch-wide assertion. The canonical failures were already covered. This is an exact boundary of the pairwise test on the stated controls, not a new global distance bound.
