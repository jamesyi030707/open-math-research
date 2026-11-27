# When is a branching certificate portable?

Fix the 14 archived weight-14 equations of section `a=3`, omitting labels 25 and 60. Use the original orientations: catalogue entry 115 is the source of the archived 35-node tree and entry 0 is the preselected comparison. The latter is not a new exclusion or a surviving full lift.

Write the left coefficients as a 14 × 27 matrix with entries ±1. A reindexing of the bits permutes columns; replacing `x_j` by `1-x_j` negates its column and adjusts the right-hand side. Such a signed column permutation preserves the Gram matrix of the rows. Even allowing arbitrary signed row permutations can only reorder the absolute off-diagonal entries, so their histogram is a necessary test before attempting to move the proof.

The 91 unordered pairs have absolute dot products 3 and 5 in both cases, but the multiplicities are **54 and 37** for entry 115 and **77 and 14** for entry 0. No such signed row/coordinate relabeling takes the original fourteen rows of 115 to those of 0. This does not rule out row combinations, transport of only some consequences, a different pair of sections, or a separate certificate for entry 0.

The genuine section `a=2` has a positive control (entry 115, mask 10844010) checked in all 16 actual weight-14 rows. As a separate synthetic transport test, reversing the positions and complementing three bits preserves the histogram, and the transported contradiction replays with 35 nodes, 18 leaves and depth 6. The reversal is not claimed to be a residual-code automorphism. Duplicate labels remain separate positions.

[Check](check.py) · [Result](result.json). From the root: `python3 history/2026-11-27/check.py`. The checker reconstructs both sections from the residual generator, pins both input blobs, and computes the profiles by dot products and Hamming distances. The original and relabeled proofs use the [archived replay checker](../2026-11-26/verify.py); no new tree or broad catalogue search was done. No new Claude exchange. The [bound](https://www.codetables.de/BKLC/BKLC.php?k=11&n=64&q=2) remains 26–27.
