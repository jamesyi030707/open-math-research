# Independent audit of the q = 24 obstruction

## Verdict and scope

The q = 24 exclusion is valid for the pinned length-37 residual and the branch with a one-dimensional left-projection kernel. No mathematical gap was found in the classification, four-message block identity, residual-window argument, or final linear-map contradiction.

Together with the previously established parameter restrictions and the q = 28 exclusion, the surviving parameters in this particular branch are q = 16 and q = 20. This audit does not exclude either survivor, another residual, or the zero-kernel branch, and does not resolve the global binary [64,11,27] existence problem. It is an independently written computational and mathematical check, not external peer review or proof-assistant certification.

Neither script imports or executes the candidate q24 obstruction checker. The audit reads only the pinned residual JSON. The separate classification script has no external input.

## Fixed input

The unchanged residual input is included in `inputs/residual_candidate.json`.

- Source: [pinned repository input](https://github.com/jamesyi030707/open-math-research/blob/6b256ed107ce3fd81724b03864643c1e86e4f18d/history/2026-11-08/inputs/residual_candidate.json).
- Git blob: `8f76beaa5994563a2980ea9cb87412640d6560b4`.
- SHA-256: `276170e9235104e8d671f4ce27eda47c25a0aee6b4dad310afae65c261f33d80`.

The audit expands all 37 coordinates directly and reconstructs all 1,024 residual weights. The distribution is 0:1, 14:160, 16:142, 18:320, 20:160, 22:160, 24:80, 32:1. The residual has rank ten. Its only nonzero message of weight at least 27 is h = 1008.

The 160 residual weight-14 messages independently give rank 55 for the evaluation matrix of the ten linear and 45 quadratic monomials. This verifies the inherited doubly-even rigidity certificate. The residual-pair weights on every nonzero member of S = span(16,32,64,128,256) are (16,16). The representatives t XOR (s << 4), together with their h translates, cover all 1,024 messages exactly once.

The audit derives the allowed left weights from both residual lift bounds and the modulo-four condition. For the ten labels T = {2,3,5,6,8,9,10,11,12,14}, it independently recovers the unique affine hyperplane containing the sixteen forced weights 14; the other sixteen entries allow precisely 10,14,18. The recovered normal/offset pairs agree with the claimed table, entry by entry.

## Classification covers all restrictions

Let H be the seven nonzero messages of weight 16; the other 24 nonzero messages have weight 12. Inverting the weight function gives, for every nonzero column label v,

    m_v = (k_v - 2)/2,
    k_v = #{s in H : s dot v = 1}.

Nonnegative integer column multiplicities imply k_v is 2, 4, or 6. Hence H spans five dimensions, its total XOR is zero, and each multiplicity is at most two. A triple column is impossible.

Regarding the seven distinct nonzero vectors H as a generator matrix gives an even [7,5] evaluation code. Its dual has dimension two and contains the all-ones vector. Nonzero, pairwise distinct generator columns exclude dual words of weights one and two. The other two nonzero dual words are complements; both have weight at least three, so their weights must be three and four. Thus H is the disjoint union of a zero-sum triple and a zero-sum quadruple. The triple spans a two-dimensional P, and the quadruple spans a complementary three-dimensional space. The quadruple is an affine plane not containing zero. This proves one equivalence class under GL(5,2).

As a redundant exhaustive check, `q24_independent_check.py` examines all C(31,7) = 2,629,575 seven-subsets. Exactly 69,440 have rank five and total XOR zero. Every one has exactly one zero-sum triple, and the remaining four points have rank three complementary to that triple.

The audit uses the canonical H = {1,2,3,4,12,20,28}, different from the candidate proof's coordinate choice but equivalent to it. It obtains 19 single columns, three double columns, and two zero columns. The double labels are {5,6,7}, which have rank three. Among the 25 active coordinate positions, precisely one annihilates P = {0,1,2,3}: the single label 4. The remaining 24 positions are nonzero on P. This unique-column property follows for all orientations from the classification, not just from testing the canonical example.

## Four-message blocks supply the missing restriction

For a quotient coset, let z be the weight on the two columns vanishing on S. The 24 coordinate positions nonzero on P each contribute two ones to every P-coset. The unique active column vanishing on P contributes four times its block bit b. Therefore every four-message block satisfies

    block weight sum = 48 + 4z + 4b.

The special column is nonzero on S/P, so exactly four of the eight blocks have b = 0 and four have b = 1, for either affine offset.

Now fix one of the ten residual windows and assume z = 0. If P lies in the direction of its forced-14 hyperplane, four blocks consist entirely of weights 14 and sum to 56, incompatible with either permitted block sum 48 or 52. If P is transverse, every block has two forced weights 14. A block with b = 0 must have its other two weights 10,10; a block with b = 1 must have 10,14 in either order. Four blocks of each type force exactly twelve weights 10 and twenty weights 14 in the whole coset. Their mean is 25/2, and their centered energy is exactly

    12(10 - 25/2)^2 + 20(14 - 25/2)^2 = 120.

For an actual restriction, signed character orthogonality instead gives energy 8 times the sum of squared signed multiplicities. The 19 singles each contribute one. Each doubled label contributes zero or four depending on its two signs. The only possible true energies are therefore 152,184,216,248, all greater than 120. This contradiction proves z(t) is nonzero for every t in T.

The finite audit covers all 155 two-dimensional P, all seven nonzero functionals annihilating each P, both offsets, and all ten residual windows. These 21,700 cases include 4,900 parallel cases rejected by block sums and 16,800 transverse cases whose only possible energy is 120. The implementation obtains each block's possible energies by enumerating its actual residual weight choices and then combines the blocks. It does not hard-code the conclusion that their energy is 120.

## Why the earlier moment-feasible cases are not counterexamples

The first and second moments alone allow z = 0. If r is the number of disagreeing repeated-column pairs, their centered energy is 248 - 32r. For z = 0, the residual windows admit these two formal multisets:

- r = 2: fourteen weights 10, sixteen weights 14, two weights 18; energy 184.
- r = 3: thirteen weights 10, eighteen weights 14, one weight 18; energy 152.

Both have the correct sum 400. They were correctly accepted by the preliminary moment-only check. Neither can satisfy the classified P-block identities: in the transverse case those identities force twelve weights 10 and twenty weights 14, with no weights 18; in the parallel case no assignment is possible. The new exclusion therefore adds structural information rather than contradicting the earlier calculation.

## Final quotient map

The two S-zero columns also annihilate h and induce a linear map Z from F2^4 to F2^2. Put C = {1,4,7,13,15}. Its ten pairwise XORs are precisely T. Since Z is nonzero on T, every two distinct elements of C have different images under Z. This would inject five points into the four-point space F2^2, an impossibility.

The audit also exhausts all 256 ordered pairs of four-bit coordinate functionals, including zero and repeated columns. None is nonzero on all ten labels T.

## Controls, limitations, and replay

`q24_independent_audit.py` checks a genuine rank-nine, 27-column binary control. Its sixteen affine cosets realize all four possible centered energies and satisfy every four-message block identity. It violates the complete residual lift bounds on 151 nonzero messages, so it is not a target code. The full control columns are recorded in the result JSON. This final control differs from an earlier preliminary control; the count 151 applies to the archived version here.

The scripts detect a changed residual-hyperplane offset, an omitted special-column block term, a falsely constant repeated-column moment, and use of the q28 energy 192. Explicit exceptions keep acceptance checks active with Python optimization enabled. The classification script also checks 2,048 genuine affine cosets and lists every moment-only residual-window solution.

This independent audit does not rerun the old 1,075 aggregate-formal-model inequalities; the exclusion proof does not depend on their feasibility. Any assertion about the old q24 formal survivor should retain its separate original certificate or the primary checker's exact replay. This audit does not claim a comprehensive new literature search or novelty.

Run both files from a disposable copy of this directory, preserving `inputs/`:

    timeout 60s python -I -B q24_independent_check.py > classification_replay.json
    timeout 60s python -I -B q24_independent_audit.py > obstruction_replay.json

Both use only the Python standard library, without installation, network access, numerical solvers, or target-matrix search. Only the CPU-time field is machine-dependent. Mathematical result fields should agree exactly with the included result JSON files.
