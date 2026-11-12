# Kernel-zero restriction: opposite h-labels consume repeated-column pairs

2026-11-12. A necessary-condition result for one fixed residual, not a new target code or a whole-branch exclusion.

## Input and prior state

The prior day's fixed-residual kernel-one closure is not rerun or reused as a kernel-zero obstruction. Its double-even rigidity prerequisite is independently recomputed: the 160 minimum residual messages evaluate all 55 linear and quadratic monomials with rank 55 over F2.

The unchanged residual input is pinned by SHA-256 `276170e9235104e8d671f4ce27eda47c25a0aee6b4dad310afae65c261f33d80`. Its ten rows are in inputs/residual_candidate.json. Sources and attribution remain those of the repository's archived input; no third-party database mirror is included.

The primary parameter entry https://www.codetables.de/BKLC/BKLC.php?k=11&n=64&q=2 was opened on this run and returned “Crawled: today”: lower bound 26, upper bound 27. The lower construction is cyclic [65,13,25], extension, then shortening. The upper chain truncates to [63,11], citing Jaffe 1996. This is a current reading of the table, not a comprehensive novelty review or evidence of a source revision today.

## Correct windows without hA=0

Use the normalized even subcode D=[A|B], with A length 27 and B the fixed length-37 residual. The rank-55 certificate forces D doubly even. Each nonzero message u therefore satisfies

    27-wt(uB) <= wt(uA) <= wt(uB),
    wt(uA) = -wt(uB) (mod 4).

The checker lists all individual windows. In particular residual weights 14,16,22 yield respectively {14}, {12,16}, {6,10,14,18,22}. A residual pair (14,22) does NOT force both corresponding left weights to 14 in the kernel-zero branch.

Let h=1008, the unique residual weight-32 message, and S={s<<4: s in F2^5}. We directly verify wt(sB)=wt((s+h)B)=16 for all nonzero s in S. Thus both left weights belong to {12,16}. In kernel zero,

    r=wt(hA) in {4,8,12,16,20,24}.

We do not set hA=0 and do not import yesterday's hyperplane periods.

## Count opposite h-labels

A column restricted to W=S+<h> is a pair (v,e), where v in F2^5 and e in F2. Write m[v,e] for its multiplicity, m[v]=m[v,0]+m[v,1], and define

    L = sum(v!=0) m[v],
    z = m[0,1],
    P = sum(v!=0) m[v,0] m[v,1].

P counts pairs of columns with the same nonzero S-label but opposite h-bits. Let q and q' count weights 12 among nonzero s in S and among h+s with s nonzero, respectively.

The restriction to S, unchanged from its direct weight supports, gives

    L=31-q/4,
    M=sum m[v]^2=992-14q-L^2,
    q in {16,20,24,28}.

Character sums, including zero columns and repeated columns, give the affine first moment

    q' = q+r/4-8z.

For completeness set a[v]=m[v,0]-m[v,1]. The two squared-weight sums over all 32 values of s are

    base = 8(L^2+M) = 7936-112q,
    shifted = 8((L+2z)^2+sum a[v]^2) = r^2+7936-112q'.

Since M-sum a[v]^2=4P, subtraction yields the exact identity

    P = r(28-r)/32 + z(L+z-28).

Every opposite-h pair is among the repeated-S-label pairs, so

    0 <= P <= sum binom(m[v],2) = (M-L)/2,
    0 <= z <= 27-L,  0 <= q' <=31.

All inequalities are necessary, not sufficient. Enumerating the at most 4*6*4 small integer cases is not a target-matrix search.

## Consequences and a parity refinement

- q=28: L=M=24 and the repeated-pair budget is zero. Hence r is only 4 or 24, not 8,12,16,20.
- q=24: L=25, M=31, pair budget 3. Hence r cannot be 12 or 16; r=4,8,20,24 remain at this level.
- q=16 and q=20: no r value is eliminated by these tests alone. There are conditional restrictions on z, listed exactly in result.json.

A further small refinement uses genuine linearity. All weights on W are divisible by four, hence A|W is self-orthogonal. The XOR of the h-selected nonzero S-labels is zero; the XOR of all nonzero S-labels is also zero because A|S is even. Thus the unselected ones likewise XOR to zero. A multiset of exactly one nonzero label cannot have zero XOR. Therefore

    r-z != 1, and L-(r-z) != 1.

For q=28 this discards (r,z)=(4,3),(24,1), leaving exactly (4,1),(24,3). We do not claim this classifies all W restrictions.

## Controls, nonredundancy, and limits

Two explicit length-27 rank-six column matrices, recorded in result.json, realize q=28 with (r,z)=(4,1) and (24,3). To construct them take S-labels 8..31 plus three zeros and the line {8,16,24}. For r=4 assign h=1 on the line and one zero column; for r=24 assign h=1 on its complement and all three zero columns. Exhaustive enumeration of their 64 messages verifies the required W windows and the identities. Their distributions are respectively 1+49x^12+13x^16+x^4 and 1+38x^12+24x^16+x^24. These are genuine local restrictions, NOT rank-ten left matrices or full residual lifts.

The formal tuple q=28,r=12,z=0,q'=31 obeys the individual W weight supports and the affine first moment, and its base S restriction is realizable. But it demands P=6 while q=28 permits P=0. This precisely demonstrates strengthening of those stated supports and first moments; no claim is made that the tuple passes every possible weight-enumerator condition or any old kernel-one seven-count model. In a full common-column model the moment identity is a consequence, not an independent constraint.

Additionally all four-column multisets in dimensions 1,2,3, including repetitions and zero columns, test the general squared-moment-difference identity on 4,241 genuine linear-column configurations. Explicit exceptions, not Python assertions, retain checks under -O.

Run `timeout 60s python -I -B check.py > result.json` and repeat with `-O`. Both runs passed in about 0.06 CPU seconds and all fields except elapsed CPU agree. No solver, large matrix search, or global nonexistence claim is part of these artifacts.

Stop this bounded step here. A meaningful next target is a compatibility condition involving W and at least one of the remaining ten residual cosets, checked against these genuine W controls. Merely reproducing the moment identity or searching complete matrices without a new certificate goal is not a continuation. Kernel zero, other residuals, and global [64,11,27] existence remain unresolved.
