# Fixed-code OPB encoding and independent audit

Date: 2026-10-18.

## Result and scope

Both downloaded full-code OPB files pass an independent, coefficient-by-coefficient audit. The original file has 59 Boolean variables and 1025 source constraints (1024 inequalities and one equality). The compact file has 57 Boolean variables with the same 1024 distance inequalities and one shifted parity equality. Expanding either equality yields 1026 inequalities.

The separately implemented generator here produces both formulations with the equality expanded from the outset. No solver was installed or run. Feasibility of the full 64-coordinate problem is **not determined**. These files establish an exact encoding for this fixed code, with positive and negative controls; they establish neither global nonexistence nor novelty.

## Exact mathematical specification

Coordinates are numbered 0 through 63, with coordinate 0 the least-significant bit. Put

    g = 0x2759262d5d506d.

For j = 0,...,9, the jth basis word is g shifted left by j, followed by an even-parity extension in coordinate 63. All ten unextended shifts have weight 27 and degree at most 62. The resulting code E has 1024 words and weight enumerator

    1 + 448 z^28 + 126 z^32 + 448 z^36 + z^64.

Thus its parameters are [64,10,28], every word is even, and the all-ones word is present. In increasing message-mask order, the all-ones word has mask 939 (0x3ab).

### Gauge fixing

The 10-by-10 projection matrix onto coordinates 0,...,9 is triangular with diagonal g_0 = 1. The independent audit also enumerates all 1024 projections and verifies they are distinct. Every ambient word f therefore has a unique e_0 in E agreeing with f on these ten coordinates.

Replacing f by f + e_0 makes the first ten coordinates zero. Translation by e_0 permutes E, so it preserves the entire multiset of distances from f to E. It also preserves parity because E is even. Consequently this gauge loses no coset and changes neither relevant condition.

### Distance inequalities

Use x1,...,x54 for f_10,...,f_63. For each e in E,

    wt(f + e) = wt(e) + sum_{i=10}^{63} (1 - 2 e_i) f_i.

In particular, the fixed coordinates contribute to the constant wt(e); they must not be dropped from that constant. The desired condition wt(f + e) >= 27 is exactly

    sum_{i=10}^{63} (1 - 2 e_i) f_i >= 27 - wt(e).

There are exactly 1024 such inequalities, each with 54 coefficients in {+1,-1}. The row for e=0 implies sum(f) >= 27. The row for e=all-ones implies sum(f) <= 37.

### Original 59-variable parity encoding

Use five Boolean variables x55,...,x59 for t_0,...,t_4, with

    t = t_0 + 2 t_1 + 4 t_2 + 8 t_3 + 16 t_4,
    sum(f) - 2 t = 1.

The equality is written as one inequality in each direction in the locally generated OPB. Among all free-word weights 0,...,54, an odd weight has exactly one t=(weight-1)/2 in 0,...,26, and an even weight has none. With the two extreme distance rows, the allowed weights are 27,29,31,33,35,37 and t ranges from 13 to 18.

### Compact 57-variable parity encoding

Use three Boolean variables x55,...,x57 for u_0,u_1,u_2, with

    u = u_0 + 2 u_1 + 4 u_2,
    sum(f) - 2 u = 27.

Together with 27 <= sum(f) <= 37, this admits exactly

    (sum(f),u) = (27,0),(29,1),(31,2),(33,3),(35,4),(37,5).

Values u=6,7 would require weights 39,41 and are excluded by the all-ones row. The exact correspondence to the original encoding is t=u+13. This compact parity encoding is equivalent only in conjunction with the existing weight bounds; by itself it also accepts weights 39 and 41.

All OPB variables are Boolean by the OPB semantics. The model is pure feasibility and has no objective.

## Independence and validation

`generate_fixed_opb.py` uses shifted integer basis words and XOR to generate E. `audit_fixed_opb.py` does not import the generator or read its manifest. It reconstructs E from an independently transcribed list of polynomial exponents using coefficient-array convolution over GF(2), then parses the actual OPB text.

The audit checks:

- 1024 distinct codewords, the exact weight enumerator, evenness, and 1024 distinct information-set projections.
- Every distance row, all 55,296 distance coefficients, and every right-hand side.
- Every auxiliary coefficient, both directions of parity, all declared variables, and the constraint count.
- The distance identity and its truth value on 58,368 row/vector pairs. The zero vector and all 54 unit vectors identify each entire affine distance expression; two dense vectors are additional controls.
- All 55 x 32 = 1760 original parity assignments, or all 55 x 8 = 440 compact parity assignments, including the zero/all-ones weight bounds.
- The gauge's full distance multiset on 67 selected ambient vectors, in addition to the general algebraic argument and exhaustive projection check.
- Two exhaustive 8-bit toy models: threshold 1 is feasible (128 ambient odd solutions, 8 gauge representatives); threshold 3 is infeasible (0 solutions). This is an extended [8,4,4] Hamming-code control, not a search on the 64-bit problem.
- Rejection of twelve tampered encodings: wrong threshold, coefficient sign, variable, duplicated row, auxiliary weight, parity sign, header, terminator, duplicate term, missing distance row, missing reverse parity, and missing row with a revised header.
- Acceptance of reordered constraints and either orientation of a single parity equality in external mode.

This is implementation independence from the supplied generators and verifiers, not a claim of independent human authorship. The parser deliberately accepts a restricted, fully consumed OPB subset: signed integer coefficients, Boolean x variables, `>=`, and optional `=` in external mode. It rejects duplicate terms, complemented literals, objectives, and other unsupported syntax instead of silently interpreting them.

## RM-only control

`audit_rm_control.py` separately audits the downloaded 69-variable RM-only instance using the independent polynomial reconstruction and parser. The 128 words of weights 0,32,64 form a dimension-seven subspace. Closure is checked on all 16,384 pairs. A basis consisting of the all-ones word and six further words yields all 64 distinct six-bit coordinate labels; this verifies that the subcode is RM(1,6), up to coordinate relabeling.

The explicit planted word is

    q1 = 0x172e5cb972e5cb97, wt(q1)=36, q1 in E,
    f  = 0x172e5cb972e5cb96 = q1 XOR delta_0, wt(f)=35.

The independent calculations give d(f,RM(1,6))=27 and d(f,E)=1. With t=17 it satisfies every parsed RM-only OPB constraint. After valid E-gauge normalization, f becomes 0x9d6498b57541b400, of weight 27, and violates exactly one full-code distance row. Therefore the RM-only success cannot be taken as a full-code solution.

## Files and rerun commands

All commands use Python 3's standard library only. Run them from this directory:

```sh
python generate_fixed_opb.py
python audit_fixed_opb.py fixed_E_odd_d27.opb --report audit_report.json

python generate_fixed_opb.py --compact
python audit_fixed_opb.py fixed_E_odd_d27_compact57.opb --compact --report audit_compact57_report.json

python audit_fixed_opb.py ../claude/ebch_hole.opb --external --report external_claude_audit_report.json
python audit_fixed_opb.py ../claude/ebch_hole_u3.opb --external --compact --report external_claude_compact57_report.json
python audit_rm_control.py ../claude/ebch_hole_rm_control.opb --report external_rm_control_report.json
```

The scripts do not write to the downloaded OPB files. The two independent OPB files are reproducibly generated by the commands above rather than duplicated in the archive. Their manifests and all five audit reports are retained; redundant stdout captures are omitted. Script compilation also passed with `python -m py_compile`.

## SHA-256 evidence

| Artifact | SHA-256 |
|---|---|
| Downloaded original `../claude/ebch_hole.opb` | `7eb3692251403d3fb66b064cf84001cee8193e7948189b30f7059841f26936d6` |
| Downloaded compact `../claude/ebch_hole_u3.opb` | `3a6a7bb159e0ebd51a86b07c2e283d17a6179c3ecbc978011d59db750f097dac` |
| Downloaded RM control `../claude/ebch_hole_rm_control.opb` | `c0cdbf0fd21939b1aa21446bd944402fe48ced638b9eaf2d642357fc99b5d5d5` |
| Local original `fixed_E_odd_d27.opb` | `2895cec073c374cc72c4ba62a07174dcabb1472bb307ed0f0c17b8e524340087` |
| Local compact `fixed_E_odd_d27_compact57.opb` | `a431ee1d4d3b2c990bb795dd649b0d7ccabc2955648b63d178bd0da4d0a1f495` |

Different hashes are expected: local files expand equality into two inequalities and have their own comments and spacing. The semantic multiset audit establishes the stated equivalence.
