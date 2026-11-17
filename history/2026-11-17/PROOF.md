# Exact stabilizer of the fixed S

Let b(u)=wt(uB), B the explicit rank-ten 10×37 binary matrix in `stabilizer.py`, S={s<<4:0≤s<32}, h=1008. We classify **all invertible message maps g with b(gu)=b(u), g(S)=S and g(h)=h**. We do not classify automorphisms moving S. In fact h is the unique weight-32 message, so the last condition is automatic for weight-preserving maps.

## Column coordinates

Write a column as (z,x,η), where z is its low four bits, x bits four through eight, and η=〈h,column〉. This is an invertible coordinate system. Direct extraction gives

C={(f(x),x,1): x∈F₂⁵} ∪ {(z,0,0): z∈Z},

where Z={1,4,7,13,15} is a five-point circuit spanning F₂⁴ and f(0)=0. All 37 columns are distinct/nonzero. Each of the 15 scalar functions q_a(x)=〈a,f(x)〉, a≠0, is quadratic with polar rank four and a unique nonzero radical vector r_a. The program verifies quadraticity through the affine first-derivative identity on all x,v.

The radical table in a=1,...,15 order is

7,22,26,21,8,13,27,10,19,14,28,29,30,23,31.

These vectors span F₂⁵. (For example the radical vectors at a=1,2,3,4,6 form a basis.)

## Why only 120 cases remain

The column action gᵀ has η'=η because g fixes h. Since g preserves S, x'=Lx with L invertible; neither z nor η may appear in x'. Its remaining block is z'=Dz+Kx+cη, with D invertible. Preserving the five η=0 columns forces D(Z)=Z. A five-point circuit allows exactly 5!=120 such D. Preserving the unique graph point with x=0 forces c=0.

Thus it suffices to find L,K such that

f(Lx)=D f(x)+Kx   for every x.

Taking polars gives

P_a(Lx,Ly)=P_(Dᵀa)(x,y),

hence **L r_(Dᵀa)=r_a** for every nonzero a. For any fixed D the source radicals still span F₂⁵, so these equations determine at most one L. The program solves five independent equations, checks the other ten, then checks the entire graph identity. K is uniquely determined by the five standard basis values. This proves completeness without traversing GL(5,2), and without supposing any subgroup generators are complete.

## Outcome and implication

Of 120 possible D, only the identity has a consistent linear radical correspondence. It passes the graph identity with L=I and K=0. Thus the above stabilizer is exactly the identity. The full returned coordinate permutation and induced S action are the identity; the canonical E orbit has size one.

This proves that the November 16 canonical-orientation exclusion cannot be enlarged by a nontrivial **fixed-S** symmetry of this B. It does not prove the full automorphism group of B is trivial; maps moving S have deliberately not been classified. It does not eliminate any additional q24 orientation, any q16/q20 branch, another residual code, or the global [64,11,27] problem.

For transport: if a lift A existed at an image orientation, precompose A by the corresponding invertible message map (and permute the B coordinates as certified). All distance windows and the previously justified doubly-even premise transport. This would contradict the original full-family exclusion. Here there is no nonidentity map in the specified stabilizer to use.

## Moving S inside W: 32 genuine translations

Keeping W=S+〈h〉 but allowing S to move changes the block constraint to x'=Lx+tη. The same polar-radical equations still determine L because translation does not change the polar of a quadratic function. Consequently D=L=I, while every t∈F₂⁵ is allowed:

x'=x+tη,
z'=z+K_t(x)+f(t)η,
η'=η,

where K_t(x)=f(x+t)+f(x)+f(t) is linear (f(0)=0). Each map sends the graph point indexed x to the graph point indexed x+t, and fixes the five special columns. These 32 maps form the complete W-stabilizer under the stated conditions. Their message restrictions are

g_t(s+εh)=s+(ε+〈s,t〉)h.

Thus an A column labelled (v,e) on W becomes (v+et,e). `transport.py` checks all 32 actual column permutations of B and transports all 277 excluded restrictions. Sorting the 27 actual W-column labels quotients only coordinate permutations, not message labels. Every distinct output includes one source index and t as a reproducible transport witness.

The 8,864 source/translation pairs produce 8,408 distinct excluded W restrictions:

| Number q of S messages of A-weight 12 | Excluded restrictions |
|---|---:|
|16|2,046|
|20|4,914|
|24|1,447|
|28|1|

The q24 outputs occupy 859 distinct E label sets. Only the original E has all 277 h restrictions excluded by this transport family; the other 858 E sets have only partial coverage (756 sets with 1, 24 with 2, 72 with 4, 6 with 13). The q28 output falls within the already excluded q28 branch, so it must not be presented as a new branch result.

No new expensive external-coset search is run: this reuses the November 16 verified obstruction through explicitly verified automorphisms. It does not eliminate any entire new q branch or all 69,440 q24 E orientations. Future work should group full W restrictions under this 32-element action and seek structural obstructions on the remaining orbits; enumerating 19 million labels mechanically remains outside the stated budget.
