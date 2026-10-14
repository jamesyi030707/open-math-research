# Exact support-coverage extension: sizes 3 and 4

This experiment concerns only the archived 11×64 generator matrix. Its SHA-256 is 568e3c2281e1e7cf79d4879e5fac2b031aeb700b78f6b62581f780b3717a39f8.

The scope was fixed before execution: enumerate every coordinate subset of size 3 and size 4; record exact support multiplicities, zero counts, and the lexicographically first uncovered set; do not test size 5 or beyond and do not search replacement columns. Each program has a 60-second CPU limit and uses only Python's standard library.

## Results

- Size 3: all 41,664 subsets covered; 0 uncovered. Minimum coverage multiplicity 6; maximum 22.
- Size 4: 635,376 subsets tested; 634,824 covered; 552 uncovered. Minimum multiplicity 0; maximum 15.
- Lexicographically first uncovered quadruple, using 1-based coordinates: {1,4,32,35}.
- Consequently, the smallest coordinate subset contained in no minimum-word support has size exactly 4. Denote that minimum size by r_min; then r_min = 4.

All 234 minimum words have weight 26. For each coordinate j, a 234-bit integer records which minimum words contain j. Intersecting the incidence masks for a subset S identifies exactly the minimum words whose support contains S. The number of set bits is the exact coverage multiplicity. The program enumerates every subset once in lexicographic order and checks the expected binomial count.

A second program verifies the result in a different direction: for each of the 234 minimum supports, it increments the count of every contained triple and quadruple. The entire multiplicity histograms agree. It separately validates the incidence masks and the zero-coordinate certificate for all 234 minimum words at the first uncovered quadruple. It also records all 552 uncovered quadruples for possible later use; no search on their replacement values was performed.

## Implication for column replacements

Replacing a set S of r generator columns changes the weight of a minimum word c by

w(new c) = 26 − weight(c on S) + weight(new c on S).

If S is contained in the support of c, then weight(c on S) = r and weight(new c on S) ≤ r. Therefore w(new c) ≤ 26 for all possible replacement columns. For r ≤ 4, the witness remains nonzero because its unchanged coordinates already have weight at least 22.

Since every triple is covered, every replacement of at most three generator columns fails to raise the minimum distance above 26. This is a uniform certificate, not an enumeration of replacement values.

For 634,824 quadruples, the same support argument excludes every four-column replacement. The remaining 552 quadruples are exactly where this particular necessary obstruction does not apply. In particular, {1,4,32,35} is an uncovered set, not a successful replacement or evidence that a replacement exists. Other minimum words, higher-weight words, linear constraints on the new columns, and rank requirements may still prohibit an improvement.

No existence or nonexistence conclusion for a general binary linear [64,11,27] code follows from this coverage result.

## Reproduce

```sh
python3 coverage_extension.py
python3 coverage_extension_check.py
sha256sum -c coverage_extension_SHA256SUMS
```

The extension generator writes its own result and timing files. The checker writes the independent check log and all uncovered sets. Timing fields vary on rerun, so the archive's manifest describes the delivered run; refresh hashes after regenerating timed logs.

Files with the coverage_extension prefix are separate from the original construction artifacts.
