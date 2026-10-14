# Binary [64,11,26] reproduction and exact local obstructions

Date: 2026-10-14.

## Scope and source

This archive independently reproduces the mathematical construction in [Markus Grassl's Code Tables](https://www.codetables.de/BKLC/BKLC.php?k=11&n=64&q=2): generate a binary cyclic [65,13,25] code from the displayed degree-52 polynomial, append an overall parity coordinate, and shorten at coordinates 65 and 66. The page was checked on 2026-10-14 and reports lower bound 26 and upper bound 27 for binary linear [64,11] codes. Its displayed construction date is 2001-01-30.

All Python code here is independently authored. No MAGMA program, database source, or external package is used. The polynomial and construction are mathematical data credited to the source above. This is reproduction of a known lower bound, not a new [64,11,26] construction. The local obstructions below are conclusions about this particular reproduced code; no priority claim is made.

## Reproduce

From this directory, run:

```sh
python3 verify_code64.py
python3 check_certificates.py
sha256sum -c SHA256SUMS
```

The first program rewrites its generated artifacts and refreshes the manifest. Its timing log varies with the machine. The second program reads the matrix and certificates independently and does not import the first program. No installation, network access, solver, randomness, or heuristic search is needed.

## Verified baseline

Coordinates are numbered from 1. Coordinate j is the coefficient of x^(j−1); the appended parity coordinate is 66. The shortening constraints require both coordinates 65 and 66 to be zero before deletion.

The first implementation uses polynomial integers, parity extension, Gaussian elimination over GF(2), and a nullspace basis of the two shortening constraints. The constraints have rank 2, leaving dimension 11. The resulting 11×64 generator matrix has rank 11. Exact enumeration checks all 2,048 words, including all 2,047 nonzero words.

A second implementation uses literal coordinate arrays and convolution, enumerates all 8,192 original messages, appends parity, filters on both shortening constraints, and deletes those coordinates. It agrees on the complete shortened codeword set. It also verifies the parent distances 25 and 26.

The full weight distribution is:

| Weight | Count |
|---:|---:|
| 0 | 1 |
| 26 | 234 |
| 28 | 259 |
| 30 | 420 |
| 32 | 396 |
| 34 | 186 |
| 36 | 261 |
| 38 | 216 |
| 40 | 75 |

The counts sum to 2,048. All 234 messages attaining weight 26 are listed in `minimum_messages.tsv`. Message integer bit i selects generator row i+1; displayed bit strings run from low to high index. Hexadecimal codewords have bit j−1 at coordinate j.

## Exact exclusion: replacing one or two generator columns

Let a message m generate a minimum word c of weight 26. Replacing a set S of old generator columns changes its weight by

w(new c) = 26 − weight(c on S) + weight(new c on S).

If c is 1 at every coordinate of S, its new weight is at most 26 for every replacement. Since at most two coordinates change, this witness remains nonzero; thus it is a valid upper bound on the modified code's distance, even if the modified generator loses rank.

Every one of the 64 individual coordinates has such a minimum-word witness. Therefore all 64×2^11 = 131,072 single-column choices are ruled out, including zero columns. This is exact symbolic pruning: zero old columns survive, so no individual new-column tests are needed.

Every one of the 2,016 unordered coordinate pairs also has a minimum-word witness containing both coordinates. Therefore all 2,016×2^22 = 8,455,716,864 ordered replacement-column assignments across those pairs are ruled out. The program does not enumerate billions of candidates: it supplies one certificate per old pair, valid for all 2^22 new pairs. This is a complete exclusion of the one- and two-column replacement neighborhoods of the displayed generator.

`obstruction_certificate.json` provides all 64 single-coordinate witnesses and all 2,016 pair witnesses. The independent checker verifies each witness directly against the supplied matrix.

## Exact algebraic obstruction: hyperplanes and one-bit extension

Three minimum-message integers are 11, 32, and 43. Their XOR is zero. Their corresponding three codewords all have weight 26 and also XOR to zero.

A linear functional h cannot equal 1 on all three messages: applying h to their zero sum would give 0 = 1+1+1 = 1 in GF(2). Thus the system m·h = 1 for all minimum messages is inconsistent. The full coefficient system has rank 11; adding the all-one right-hand side raises the rank to 12. The triple is a small, independently checkable inconsistency certificate.

Consequences for this code C:

1. Every dimension-10 subcode of C contains a weight-26 word. Such a subcode is the kernel of a nonzero functional, and at least one of the three certified words lies in that kernel.
2. Every binary linear dimension-11 code D with dim(C∩D) ≥ 10 has minimum distance at most 26, because the intersection contains such a weight-26 word. Therefore an improving dimension-11 code must intersect this C in dimension at most 9.
3. No linear one-coordinate extension of C can have distance at least 27, because some weight-26 word receives appended bit 0. This claim concerns extensions to length 65, not all codes of that length.

The independent checker also checks all 2,048 possible linear functionals against the triple.

## Limits

These results do not prove the global nonexistence of a binary linear [64,11,27] code. They do not search other equivalence classes, exclude all larger modifications, or improve the verified table bounds 26–27. The pair-support certificate is specific to coordinate replacements; the intersection-dimension obstruction is a distinct algebraic statement. Neither should be promoted to a universal upper bound of 26.

## Files

- `verify_code64.py`: original construction, two implementation paths, and certificate generation
- `check_certificates.py`: independent matrix and certificate checker
- `generator_matrix.txt`: 11 rows of 64 binary coordinates
- `weight_distribution.tsv`: full distribution, including zero
- `minimum_messages.tsv`: all 234 minimum messages and codewords
- `results.json`: structured baseline and experiment summary
- `obstruction_certificate.json`: coordinate, pair, and odd-XOR certificates
- `verification.log`: construction assertion outcomes and run timing
- `certificate_checker.log`: independent checker outcomes
- `SHA256SUMS`: relative-path SHA-256 manifest

## Exact coverage extension (sizes 3 and 4)

A subsequent preregistered exact calculation on this same matrix covers all 41,664 triples (minimum multiplicity 6), excluding every three-column replacement. Among 635,376 quadruples, exactly 552 are uncovered; the first is {1,4,32,35} in 1-based coordinates. Hence the smallest minimum-support-uncovered subset has size exactly 4. This does not establish a successful four-column replacement. See `coverage_extension_proof.md`, the separate scripts, full histograms, and independent check log. The original construction, matrix, certificates, and logs are preserved.

## Four-column circuit refinement

Every one of the 552 support-uncovered quadruples is also excluded by an explicit three-minimum-word circuit. Across three words with XOR zero, four replacement coordinates contribute at most 8 total ones. Each supplied circuit loses at least 6 old ones, so the new total weight is at most 80, below the 81 needed to make all three weights at least 27. Each changed word remains nonzero with at least 22 unchanged ones. Combined with support coverage, this excludes all replacements of at most four generator columns. The support-only threshold remains exactly 4. See `four_column_circuit_proof.md`, all 552 certificates, and the independent checker. No size-5 work was performed.
