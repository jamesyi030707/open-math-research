# Five forced hyperplanes exclude the fixed residual's kernel-one branch

Date: 2026-11-11. Research result for the fixed residual and stated branch.

## Result and scope

For the exact archived binary length-37 residual matrix B, there is no distance-27 lift whose normalized even subcode has a one-dimensional kernel under projection onto its left 27 coordinates. In particular, the previously remaining q=16 and q=20 cases are excluded. The proof also independently excludes q=24 and q=28, without using their earlier classification arguments.

The conclusion is strictly limited to this fixed residual and this projection-kernel branch. It does not exclude the kernel-zero branch, other residual codes, or all binary [64,11,27] codes. It gives no new code, global parameter bound, novelty claim, external peer-review claim, or proof-kernel-certified theorem.

The new ingredient is a parity consequence of exact constancy on an affine hyperplane. The hyperplanes occur in different message cosets, but all cosets share the same restricted-column multiplicities. Five independent hyperplane normals therefore constrain one common parity function. No classification of q=20 restrictions is needed.

## Fixed data and inherited normalization

The previous q=24 result and fixed residual are archived at repository commit 3229383ae26e6c445adf62f70545553fcc5d2055, dated 2026-11-10. The distinctions in ERRATA between exact finite checks, global statements and external review remain in force.

The unchanged input is history/2026-11-10/inputs/residual_candidate.json at that commit:

- Git blob: 8f76beaa5994563a2980ea9cb87412640d6560b4.
- SHA-256: 276170e9235104e8d671f4ce27eda47c25a0aee6b4dad310afae65c261f33d80.
- The ten generating rows, encoded as 37-bit integers, are 0x17e7146801, 0x6293dc808, 0xf714c2017, 0x35dfc802d, 0xb1f3485c, 0x63e6a0ae, 0x65be14f, 0x196fc233, 0x3e690ce6, 0xcb73897.

As in the archived residual-lift setup, write the target generator as the row (1^27,0^37) together with the ten rows [A|B] of its even subcode D. B has rank ten and is even. Every nonzero ten-bit message u must satisfy

    27 - wt(uB) <= wt(uA) <= wt(uB).

The checker's complete enumeration of B gives distribution

    1 + 160 x^14 + 142 x^16 + 320 x^18 + 160 x^20
      + 160 x^22 + 80 x^24 + x^32.

The unique message with residual weight at least 27 is h=1008. Thus, in the kernel-one branch, ker(A)=span(h), and hA=0.

For completeness, the inherited double-evenness condition is checked from its finite certificate. Since D is even, Q(u)=wt(uD)/2 modulo 2 is a polynomial of degree at most two, with zero constant term, in the ten message bits. Its 55 possible monomials consist of ten degree-one and 45 degree-two monomials. At each of the 160 residual weight-14 messages, the lift inequalities and evenness force wt(uA)=14, so wt(uD)=28 and Q(u)=0. The 160-by-55 evaluation matrix has rank 55 over F2. Hence Q is identically zero, and

    wt(uA) = -wt(uB) modulo 4.

This reasoning requires the normalized even-subcode representation; it is not asserted for arbitrary left matrices.

## The five-dimensional restriction and its moments

Let S=span(16,32,64,128,256), identified with F2^5 by s -> s<<4. The checker verifies that for every nonzero s,

    wt((s<<4)B) = wt(((s<<4) XOR h)B) = 16.

Consequently its left weights are 12 or 16. Let q be the number of weight-12 nonzero messages. For every nonzero five-bit column label v let m_v be the multiplicity of that label in the restriction of A to S; let

    L = sum_(v != 0) m_v

be the number of columns nonzero on S. Each nonzero label is one on 16 of the 32 messages. The first moment gives

    16L = 12q + 16(31-q), so L = 31-q/4.

Since q is an integer from 0 to 31, L is an integer, and L<=27, the only possibilities are q in {16,20,24,28}.

Writing chi_v(s)=(-1)^(v dot s), the restriction's weight function is

    w_0(s) = L/2 - (1/2) sum_(v != 0) m_v chi_v(s).

Character orthogonality gives

    sum_s w_0(s)^2 = 8 (L^2 + sum_(v != 0) m_v^2).

On the other hand this sum is 144q+256(31-q). Therefore

    sum_(v != 0) m_v^2 = 992 - 14q - L^2.

The resulting exact pairs (L, sum m_v^2) are (27,39), (26,36), (25,31), and (24,24), respectively. Repeated columns are fully included in this identity.

## Actual residual messages force ten constant hyperplanes

Because hA=0, use representatives u=t XOR (s<<4), with 0<=t<16 and 0<=s<32. The residual inequalities for u and u+h, together with both mod-four conditions, give a left-weight window at each representative.

The following triples (t,n,c) have the exact window {14} when n dot s=c and {10,14,18} on the other half:

    (2,22,0), (3,26,0), (5,8,0), (6,13,1), (8,10,1),
    (9,19,1), (10,14,0), (11,28,0), (12,29,0), (14,23,0).

The checker recomputes these windows from all residual words. In particular, it does not assume that the displayed table is correct merely because it appeared in the previous archive.

The first five normals 22,26,8,13,10 are linearly independent over F2. All ten normals have rank five. Only five are needed below.

## Constant-hyperplane lemma

Consider any affine binary-column weight function on F2^r. Let m_v be the multiplicity of each nonzero column label, L=sum m_v, and let z be the number of constant-one columns in the chosen affine coset. Each column restricting to v has an affine sign +1 or -1. Their signed sum is a_v, so

    w(s) = L/2 + z - (1/2) sum_(v != 0) a_v chi_v(s),
    a_v = m_v modulo 2.

Suppose w(s)=K, an integer constant, on the affine hyperplane n dot s=c, n!=0. On that hyperplane chi_(v+n)=(-1)^c chi_v. Distinct pairs {v,v+n} correspond to distinct restricted characters. The pair {0,n} is the constant character. Orthogonality on the hyperplane therefore gives

    a_v + (-1)^c a_(v+n) = 0  for v not in {0,n},
    a_n = (L + 2z - 2K)(-1)^c.

Define the artificial parity function f on the entire column-label space by

    f(0) = L modulo 2,
    f(v) = m_v modulo 2 for v!=0.

Reducing the displayed equations modulo two proves

    f(v+n)=f(v) for every v.

The definition at zero is essential: f(0) is not generally the parity of the number of zero columns. It makes the exceptional pair {0,n} obey the same translation law as every other pair. The argument permits zero columns, repeated columns, arbitrary affine offsets, and arbitrary constant K.

## Apply all five periods to the same column multiplicities

For each of the certified message cosets, the signed coefficients a_v and the number z can change. The multiplicities m_v and L cannot change, because every coset comes from the same left matrix A.

Apply the lemma with K=14 to each forced hyperplane. Thus every certified normal is a translation period of one common f. Five independent normals generate all of F2^5, so f is constant and

    m_v = L modulo 2 for every nonzero v.

There are now two cases, both impossible:

1. If L is odd, every one of the 31 nonzero labels has positive odd multiplicity. Therefore L>=31, contradicting L<=27. This excludes q=16 and q=24.

2. If L is even, every m_v is even and nonnegative. Then m_v^2>=2m_v for every v, so sum m_v^2>=2L. For q=20, the exact values would require 36>=52; for q=28 they would require 24>=48. Both are contradictions.

This covers every possible q, and proves the stated fixed kernel-one branch exclusion.

## Nonredundancy and real-code controls

The old formal points with seven counts

    q=16: (20,16,84,32,18,44,18),
    q=20: (24,20,80,32,18,44,18)

still pass all 11 count bounds and all 1,064 integral nonnegative split-transform coefficients, reconstructed directly from their joint distributions. Their November 8 incidence slacks are 0 and 1. The checker recomputes these facts by integer polynomial multiplication, not a numerical solver. Thus the new actual-column obstruction does not retract the old formal feasibility; it excludes all actual realizations of those points and of the whole fixed branch.

The constant-hyperplane lemma is also checked on every dimension-three multiset of 0 through 4 binary columns and every affine offset on each column. This is 6,401 genuine affine-column configurations and 89,614 hyperplanes, of which 8,862 are constant. For each hyperplane, the checker tests both directions of the exact signed-coefficient criterion; on every constant hyperplane, it additionally tests the parity-period implication. These are finite controls for the algebraic lemma, not a substitute for its general proof.

A real q=20 restriction with 26 active columns is explicitly supplied:

    1,3,5,7,9,11,13,14,14,15,17,19,21,22,22,23,
    25,26,26,27,28,28,29,30,30,31.

Together with one zero column, it has the exact weight distribution 1+20x^12+11x^16 and sum m_v^2=36. The script embeds it into an actual 27-column, rank-nine left matrix with kernel span(h), exercising a real local instance rather than only a formal weight list. That matrix fails 123 full residual-lift bounds. It is expressly not a target code. Its multiplicity parity has only a four-dimensional period space and cannot satisfy the five independent forced periods.

Negative controls reject a changed hyperplane offset, reject changed input bytes through the same pin checker, and detect the incorrect choice f(0)=0 on a genuine one-column constant-hyperplane instance.

## Reproduction, budget, and stopping point

Run from the artifact directory using Python 3.10 or newer and only the standard library:

    timeout 60s python -I -B check_fourier_obstruction.py > result.json
    timeout 60s python -I -O -B check_fourier_obstruction.py > result_optimized.json

The final local runs took about 0.22 and 0.21 CPU seconds. All mathematical fields agree after removing only cpu_seconds. Explicit exception checks remain active under -O. Timing is machine-dependent; the one-minute limit is per deterministic check.

No target-matrix search, numerical feasibility solve, software installation, or public write was performed. The small local q=20 control was found by a bounded constructive enumeration and then frozen as explicit columns; it is not claimed to classify q=20 restrictions. The source's large historical experiments were not rerun.

Stop this fixed kernel-one branch here except for independent review or corrections. Any investigation of the kernel-zero branch or another residual needs its own structural certificate target and budget. Global [64,11,27] existence remains unresolved by this work. No new external parameter-table or comprehensive literature verification is claimed in this report.
