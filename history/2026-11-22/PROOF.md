# The 345 singleton-test supports of a minimum-word section

## Exact scope and notation

Keep the fixed [37,10,14] residual B and the kernel-zero doubly-even normalization from the preceding work, not an arbitrary residual. Use W(t)=((t&31)<<4) XOR (1008 if t&32 else 0), for t=0,…,63. Column labels c_j lie in F₂⁶. Bit 5 is the h-bit. The sections use actual residual weights, not a presumed symmetry under relabeling A.

At an external representative a, take H_a={t:wt((a XOR W(t))B)=14}. The A-side window is 13–14; the doubly-even sum condition forces weight 14. If the extension existed, its offset signs would satisfy Σ_j χ_t(c_j) ε_j=−1 for every t∈H_a, where χ_t(v)=(-1)^{〈t,v〉}. Write F_a(v)=Σ_{t∈H_a} χ_t(v). Multiplying by χ_t(u) and summing gives Σ_j F_a(u XOR c_j) ε_j=−F_a(u).

For distinct characters u,v and s=±1 put D(c)=F_a(u XOR c)+s F_a(v XOR c). The combined equation is Σ_j D(c_j) ε_j=−D(0). When D(0)=0 and the support contains exactly one **column position**, the equation forces a sign to be zero. Repeated labels count with their multiplicities: a support that catches one different label occurring twice is not a singleton certificate. We catalog only the nonempty supports of these zero-target two-character combinations, not all possible projection obstructions.

## Quotient proof of the support catalog

For a=2 and a=6 the independently extracted section has 16 points. Translate t by the least t0 in H_a and write F for its new transform. The transform is simply F_a(x) multiplied by χ_t0(x); reparametrizing s by χ_t0(u XOR v) preserves D's zero target and support, so the catalog is unchanged by this normalization. The exact low transform is 16 at 0 and k, and zero elsewhere (k=22 at a=2; k=13 at a=6). In the high half every absolute value is 4. The low peaks imply the normalized H_a lies in the hyperplane t·k=0, hence F(x XOR k)=F(x). On the quotient Q=F₂⁵/<k>, of size 16, let f(x)=F(32 XOR x)/4. Both spectra, the quotient property, and all 15 balanced derivatives of f are checked exactly in the scripts.

Why the derivative is balanced here: Walsh inversion in the low half of F gives one point of H_a above each low t in k-perp and none elsewhere. Thus H_a is the graph of one bit on that 4-dimensional space; F in the high half is the Walsh transform of the graph's sign function. The transform of f on the dual quotient therefore takes values ±4 by character orthogonality. The autocorrelation of f at a nonzero shift is zero, since the square of its transform is constant. Consequently, for any distinct u,v in Q, f(x XOR u)±f(x XOR v) has support on exactly eight quotient labels, with complementary supports for the two signs.

| Case | Low labels | High labels | Distinct supports |
|---|---:|---:|---:|
| Both characters low, two distinct nonzero quotient labels | 4 | 16 | 2 C(15,2) = 210 |
| Both high, two distinct quotient labels | 16 | 4 | C(16,2) = 120 |
| Both low, same nonzero quotient label, reinforcing sign | 2 | 32 | 15 |

In the first row the low support is exactly the pair of full quotient classes, which determines the unordered pair; the two signs yield complementary high parts. In the second row the high support determines the pair and the zero target fixes the sign. In the third row the low support is one nonzero class, and the high part is all 32 labels. Distinct family sizes on the two halves separate all three rows. Mixed low/high cannot give zero target, as the low magnitude is 0 or 16 and the high magnitude is 4. The remaining same-class cancellations have zero support; a distinct low pair containing the zero quotient class cannot give zero target. Each support of the first two rows admits four lifts of its unordered pair; the third admits one. Hence there are 345 distinct nonempty supports and 1,335 qualifying triples (u<v,s) per section. This is a complete count for the specified combinations and fixed sections.

## Exact finite application and stopping boundary

Take the 120 permutations of the five low bit positions of the [November 15](../2026-11-15/README.md) q24 marking indexed 1, with the high bit untouched. These are local test restrictions, not transformations of residual B. Deduplicating gives 60 column multisets. All satisfy the 63 nonzero W windows and congruences, have q=24, r=4, z=1, and pass the uniform multiplicity bound with a(0)+max b=2. Each has one q24 representative in its eight-element true translation orbit; thus there are exactly 60 distinct q24 orbits in this family.

The a=2 catalog finds a singleton position on 54 controls, and the independently recomputed a=6 catalog finds one on 54. There are 48 controls with both, six with only a=2, and six with only a=6, so their union rejects all 60. A concrete a=2 miss uses the low-bit image permutation (0,3,4,1,2), zero-based. At a=6, characters (1,4) with sign −1 leave coefficient −16 only at column position 10 (label 12), yielding −16 ε_10=0. The exact original, unshifted sections produce the published certificates.

Of the 60, six were already in the regenerated November 17 explicit transport set and six in the distinct November 21 orbit set. The remaining 48 are concrete additional q24 orbit representatives relative to those named sets and the November 18 multiplicity filter, not a net count against every earlier result. The 60 finite controls are a coordinate-permutation family of one seed; these statistics are not a sampling estimate of all q24 labels. A miss of this catalog would say nothing about extendability. No full q24 or code bound claim follows, and no larger scan was run.
