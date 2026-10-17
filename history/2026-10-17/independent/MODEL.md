# Exact shared-variable model and quotient interface

Let f_j be binary and A_i the 512 sign rows in model.json. Each row represents a word w_i of E modulo the all-one word. Its Walsh coefficient is sum_j A_ij(1−2f_j). The exact constraints are

    (sum_j A_ij−10)/2 ≤ sum_j A_ij f_j ≤ (sum_j A_ij+10)/2,
    sum_j f_j−2t=1,   t∈{0,…,31}.

All coefficients and bounds are integers. These are 512 two-sided constraints, equivalently 1024 scalar inequality bounds. The 512 represented words and their complements are exactly E. Thus the model is feasible exactly when an odd coset has minimum distance at least 27. The row-coverage check establishes equivalence for every vector; four small direct-distance checks only test the implementation interface.

## A safe systematic quotient

Adding any word of E preserves both the coset and odd parity, since E is even. Row reduction gives ten rows with the identity matrix in coordinates 0,…,9. Every coset therefore has exactly one representative with those ten bits zero. The remaining 54 binary coordinates describe the quotient exactly; parity leaves 2^53 possible odd representatives. No enumeration of those representatives has been performed.

The full RREF matrix is in quotient_certificate.json. Invertibility on the ten pivots proves both existence and uniqueness: subtract the rows selected by the pivot entries, then use the identity pivot block to rule out a second zero-pivot representative in the same coset.

Important: this replaces the weaker f_63=0 complement normalization. Do not impose both normalizations together without a new proof. All codeword translations have already been used by the systematic transversal; fixing an extra coordinate could exclude cosets.

## Reproduce

Run `python model_check.py`, then `python quotient_check.py` in a temporary copy of this directory. These regenerate model.json, checks.json and quotient_certificate.json. Neither searches for a feasible vector.

The optional solve_scipy.py uses the weaker complement normalization only. It was syntax-checked, not executed in this independent check. It requires SciPy/NumPy and requests one HiGHS worker with a 115-second wall budget plus a 120 CPU-second process limit. A hard CPU exit may occur before writing JSON; preserve stdout and process status when running it. Solver infeasibility is not an independent certificate. Any candidate is rechecked with exact integer distances. Floating-point MILP arithmetic is not itself an exact proof engine.
