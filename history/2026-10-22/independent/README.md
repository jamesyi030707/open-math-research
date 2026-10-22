# Two-translate compatibility audit

Date: 2026-10-22. Source baseline: `36760bd352596dfa5fb4865f8dee3dd0d70441c0`.
This is AI-assisted, separately authored exact checking, not external peer review or proof-assistant verification. No novelty claim.

## Results and stopping boundary

1. The exact full-spectrum convolution relation is verified on four explicit 64-point functions, at all 64 frequencies each. It is already implied by using one common Boolean truth table; this is not a stronger fixed-parent obstruction.
2. For two rank-four quadratic translates whose difference is bent, the two signed support projections reduce to row and column sums of four independent binary 4-by-4 matrices. The resulting margin compatibility can reject detached projections that separately have valid fiber averages and equal totals. It does **not** strengthen the complete common-truth-table model.
3. The explicit function from October 21, `f=x0*x1+x2*x3+x4*x5+delta_48`, has eight maximum absolute Walsh coefficients `[10,10,10,10,18,18,10,18]` in the fixed quotient-mask order described below. Thus it actually passes the chosen first pair of bounds but fails three of the eight bounds. This is a small additional check, not a new candidate search or code construction.

No surviving aggregate distance profile was eliminated. Fixed-parent feasibility and the global binary [64,11,27] problem remain undecided. No 32,768-form enumeration, large function search or solver run was repeated.

## Exact conventions and proof

All functions are on F2^6; addition of function values is modulo two. For a function v, write `s_v(x)=(-1)^v(x)` and `W_v(a)=sum_x s_v(x)(-1)^(a dot x)`. The unnormalized Walsh transform squares to 64 times the identity. Multiplying signs and applying inversion gives, for any f,q,

`64 W_(f+q)(a) = sum_b W_f(b) W_q(a+b)`.

This identity uses all signed coefficients, not merely their magnitudes or histograms. If H is the Walsh matrix and D_q is the diagonal matrix of signs of q, the operator is T_q=H D_q H/64. Since H squared is 64I and D_q squared is I, T_q squared is I. For bent q its entries have magnitude 1/8. The script additionally checks its involution by all 64 convolution shifts.

Let h_i=h+q_i be rank-four quadratic functions with radicals R_i of size four, and let S_i be their Walsh supports. Define the normalized support projection

`P_i(x)=(1/64) sum_(a in S_i) W_(f+q_i)(a)(-1)^(a dot x)`.

Then the precise signed fiber identity is

`(-1)^h_i(x) P_i(x) = (1/4) sum_(r in R_i) (-1)^(f(x+r)+h(x+r))`.

Indeed, the affine support S_i consists of characters with restriction `a dot r=h_i(r)+h_i(0)` on R_i. Averaging these characters gives the signed radical projection. The quadratic identity `h_i(x+r)+h_i(x)=h_i(r)+h_i(0)` for r in R_i converts the twist into the displayed common sign function. The statement therefore includes affine supports and constants, not just homogeneous quadratics. The numerical checker below checks the specified homogeneous representatives; the algebra supplies the general affine statement.

Suppose q_i+q_j is bent, equivalently its alternating bilinear form has zero radical. A vector in R_i intersect R_j is in the radical of their sum, hence must be zero. Thus R_i+R_j has dimension four. Each of its four cosets has a unique grid parameterization `x=c+r+s`, with r in R_i and s in R_j. Put binary errors `e(x)=f(x)+h(x)`. Their four-point fiber counts are integers from zero to four. An average A gives error count `2(1-A)`.

Rows of a grid are R_j fibers, and columns are R_i fibers. Two prescribed sets of these fiber counts have a common Boolean realization on the coset if and only if they are margins of a binary 4-by-4 matrix. Sorting row counts d_1>=...>=d_4, the classical [Gale–Ryser criterion](https://doi.org/10.2140/pjm.1957.7.1073) is equality of total counts together with

`sum_(i=1..k) d_i <= sum_(j=1..4) min(k,c_j)` for k=1,2,3,4.

Equivalently, one can enumerate the at most six choices for each row of degree two, never more than 6^4 row choices. The checker uses both methods on three explicit controls. Compatibility on all four cosets is necessary and sufficient for the **two prescribed projections** to come from a shared Boolean error vector. It is not sufficient for arbitrary prescribed *full spectra* or for the remaining six translates.

## Small controls and their limited meaning

Take row counts `[4,4,0,0]` and column counts `[4,2,2,0]`. Both totals are eight; their signed averages are `[-1,-1,1,1]` and `[-1,0,0,1]`, all legal four-sign averages. But the first two rows being full force every column to contain at least two ones, contrary to the final zero column. Equivalently, k=2 gives 8>6 in Gale–Ryser. Counts `[4,4,0,0]` and `[2,2,2,2]` are a positive control.

These margin examples are **not** claimed to have full Walsh coefficients bounded by ten, satisfy the seven aggregate profiles, or share all the other previously imposed hypotheses. Therefore they show only that separate fiber integrality plus equal totals do not guarantee pairwise realizability. They do not establish a new exclusion for the actual target problem. For an already common 64-bit model every margin condition above is automatic.

## Reproduction and exact coverage

Run `python audit_pairwise.py > pairwise_report.json` using Python 3 standard library only. All mathematical output is deterministic; `cpu_seconds` is run-dependent and must be excluded when comparing reports. Do not compare regenerated report hashes as a mathematical correctness test.

The script uses direct character summation rather than importing an earlier transform implementation. It checks:

- Four explicit functions: zero, delta_0, the prior radius-15 control, and `x0*x1*x2+delta_17`.
- 256 convolution coordinates, 64 involution convolution shifts, and 512 signed projection coordinates.
- 16 genuine 4-by-4 grids, and three separate small margin controls.
- All eight translated spectra of the prior radius-15 control.

The chosen h has mask 513, representing `x0*x1+x2*x3`, and q has mask 19053. Their radicals are respectively `[0,16,32,48]` and `[0,28,35,63]`; grid coset representatives are `[0,1,4,5]`. The radical of q is zero.

Masks use lexicographic pairs `(i,j)`, 0<=i<j<6, with x0 the least significant input bit. The fixed BCH quotient basis masks `[19053,24003,9757]` are reused from the published October 20 reconstruction, not reconstructed or globally enumerated again. The eight mask order is `[0,b0,b1,b0+b1,b2,b0+b2,b1+b2,b0+b1+b2]`. Dropping affine parts changes only frequency locations/signs and not maximum absolute Walsh coefficients, so homogeneous representatives suffice for the eight-bound test.

## Sources and current parameter-table check

- [Published quadratic basis and previous proof](https://github.com/jamesyi030707/open-math-research/blob/36760bd352596dfa5fb4865f8dee3dd0d70441c0/history/2026-10-20/independent/quadratic_neighborhood_proof.md)
- [Previous explicit radius-15 control](https://github.com/jamesyi030707/open-math-research/blob/36760bd352596dfa5fb4865f8dee3dd0d70441c0/notes/codes-single-spectrum-limit.md)
- [Grassl binary [64,11] parameter entry](https://www.codetables.de/BKLC/BKLC.php?k=11&n=64&q=2): retrieval on October 22 displayed lower bound 26 and upper bound 27. The retrieval service labeled its crawl as the previous day. This is a primary-table observation, not comprehensive current-literature verification or a priority claim.
