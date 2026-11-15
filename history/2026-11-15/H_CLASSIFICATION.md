# Independent q=24 h-marking verification

Scope: a normalized fixed-residual kernel-zero restriction to W=S+<h>. This is a local classification, not an external-compatibility or full-lift result.

## Old S classification and normalization

The q=24 S classification is already present in the November 10 history and is not a new result here. Let E be the seven nonzero S messages whose left weights are 16. Exact character inversion gives m(v)=(3-sum_{s in E}(-1)^(s.v))/4 for v!=0. Nonnegative integral multiplicities imply XOR(E)=0 and rank(E)=5. The two-dimensional dependency space of the seven columns contains all-ones; its other dependency splits E into disjoint circuits of sizes 3 and 4, since columns are nonzero and distinct. These circuit spans are complementary. Thus all S restrictions are GL(5,2)-equivalent as local restrictions. This does not assert that this GL action is a symmetry of the fixed residual.

Use canonical E={1,2,3,4,8,16,28}. There are 19 singleton labels, three double labels {29,30,31}, nine absent nonzero labels and two zero-S columns.

## Finite h-marking problem

For each nonzero v let b(v) be the number of copies bearing h-bit 1, so 0<=b(v)<=m(v). Let z in {0,1,2} count selected zero-S columns and r=sum b(v)+z. The permitted r are 4,8,12,16,20,24. The November 12 exact identity gives

P=sum_v b(v)(m(v)-b(v))=r(28-r)/32+z(z-3), 0<=P<=3.

Since every multiplicity is at most 2, P is simply the number of split double labels. A necessary self-orthogonality condition is XOR of selected labels (with multiplicity) equal zero. The exact local conditions, beyond r, are

wt((h+s)A)=r+wt(sA)-2 sum_{s.v=1} b(v) in {12,16} (s!=0).

These conditions are sufficient for this local W restriction only. They make all its weights positive and divisible by four, hence its rank is six.

## Two elementary eliminations

The moment table allowed (r,z)=(4,2) and (24,1), both requiring P=1. The first selects exactly two nonzero S columns; their XOR must vanish, so they have the same label. Both copies of that label are then selected, giving P=0, contradiction. The second leaves exactly two nonzero S columns unselected. The XOR of all S columns is zero, so those two labels must likewise coincide and again P=0. Thus both tuples are impossible independently of enumeration.

For (r,z)=(4,0), P=3 means all three double labels are split. One singleton remains selected; XOR forces it to be 29 xor 30 xor 31=28. This produces exactly one h marking and directly passes all local windows.

## Independent exhaustive enumeration

check_h.py enumerates selected or unselected nonzero multisets, choosing whichever is smaller; this differs from enumerating masks on a 27-position column list. It enumerates all three double-label multiplicities in {0,1,2}, selects the remaining singleton subset, checks the exact P and XOR conditions, then evaluates all 31 shifted weights and independently all 64 local message weights. No assertions are used, so -O retains checks.

10,861 multisets after the P filter give exactly 277 local h markings:

| r | z | count |
|---|---|---|
|4|0|1|
|4|1|18|
|8|1|96|
|8|2|24|
|20|1|24|
|20|2|96|
|24|2|18|

Counts are modulo permutation of equal S columns, not modulo message-space automorphisms. The whole original-coordinate S class has 69,440 restrictions and therefore 69,440*277=19,234,880 W restrictions up to column order. Using one canonical S restriction to establish the h count is valid; using it to infer that every differently labelled restriction fails outside W is not valid without transporting the external constraints.

Normal and optimized JSON agree after removing cpu_seconds. All recorded controls are true local restrictions, not target codes. No external section was tested by this script and no global or entire q=24 exclusion follows.
