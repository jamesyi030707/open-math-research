# Fixed BCH code: a seven-histogram necessary condition

Date: 2026-10-19. All computations use Python's standard library. No solver was installed or run. The 57-variable OPB remains unresolved.

## Main result

For this fixed extended BCH code E = [64,10,28], an odd-weight vector at distance at least 27 would have an aggregate distance histogram among only these seven possibilities:

| Number at distances 27 and 37 (each) | Number at 29 and 35 (each) | Number at 31 and 33 (each) |
|---:|---:|---:|
|224|288|0|
|240|240|32|
|256|192|64|
|272|144|96|
|288|96|128|
|304|48|160|
|320|0|192|

This reduces the earlier 25 necessary aggregate histograms to seven. It does not establish that any survivor is realizable, exclude all survivors, solve the full model, prove global nonexistence of a binary [64,11,27] code, or assert novelty.

## Fixed-code coordinates and quadratic structure

The polynomial is g = 0x2759262d5d506d. The ten shifted generators, each extended by an even-parity coordinate, generate E. The 128 codewords of weights 0, 32, and 64 form an RM(1,6) subcode. An all-ones word and six further RM basis words label the 64 coordinates by all x in F_2^6.

Choose three words q1,q2,q3 extending that RM basis to E. Write Q(x) = (q1(x),q2(x),q3(x)). The supplied audit constructs this labeling and basis independently from polynomial exponents, verifies degree exactly two for each qi, and checks all seven nonzero components q_lambda = lambda dot Q have Walsh magnitudes eight. Thus every nonzero component is bent. These are properties of E itself and do not assume a desired f exists.

For a nonzero shift a, define the linear polar map

    L_a(x) = Q(x) + Q(x+a) + Q(0) + Q(a).

It has rank three. Indeed, a nonzero left-kernel vector lambda would make the derivative of the bent quadratic q_lambda in direction a constant. Its nonzero-shift autocorrelation would then be plus or minus 64, whereas a bent function has zero nonzero-shift autocorrelation. The contradiction proves rank three. Also L_a(a)=0. Each fiber therefore has eight points, grouped into four unordered pairs {x,x+a}.

The script checks linearity and rank three for all 63 nonzero a, not merely selected shifts.

## One spectrum: four possible magnitude histograms

For an odd-weight vector f, let

    W_lambda(u) = sum_x (-1)^[f(x) + q_lambda(x) + u dot x].

The full-code distance condition is equivalent to all 512 magnitudes |W_lambda(u)| being at most ten. Odd weight makes each coefficient congruent to two modulo four, so the only magnitudes are 2, 6, and 10.

For one spectrum, let (a,b,c) count these three magnitudes. Parseval gives

    a+b+c=64,
    a+9b+25c=1024,
    a=2c-56, b=120-3c, 28 <= c <= 40.

Its fourth moment is

    M4 = 16a + 1296b + 10000c = 154624 + 6144c.

For h=f+q_lambda define A_h(v)=sum_x (-1)^[h(x)+h(x+v)]. At a nonzero shift, the 64 points form 32 pairs. If m pairs have unequal h values, then A_h(v)=64-4m. Because wt(h) is odd, m is odd. Hence A_h(v) is congruent to four modulo eight, and A_h(v)^2 is congruent to 16 modulo 128.

The identity M4=64 sum_v A_h(v)^2 and A_h(0)=64 give

    sum_(v != 0) A_h(v)^2 = 96c-1680.

Comparing with 63*16 modulo 128 yields c divisible by four. Therefore each individual spectrum has (a,b,c) equal to

    (0,36,28), (8,24,32), (16,12,36), or (24,0,40).

By themselves these four possibilities still permit all 25 previous aggregate histograms.

## Cross-spectrum parity: an intermediate modulus eight

For one nonzero shift v and each z in F_2^3, put

    S_z = sum_(x in L_v^(-1)(z)) (-1)^[f(x)+f(x+v)].

Each fiber has four unordered pairs, so S_z is divisible by four. Moreover sum_z S_z / 4 = A_f(v)/4 is odd. Parseval over F_2^3, allowing irrelevant component-wise constant signs, yields

    sum_lambda A_(f+q_lambda)(v)^2 = 8 sum_z S_z^2 = 128 (mod 256).

Summing over 63 shifts shows that C=sum_lambda c_lambda is divisible by eight. This alone reduces 25 histograms to 13. The design argument below is stronger.

## Weight-four dual supports form a 2-(64,4,3) design

Let B consist of unordered four-element subsets {x,y,z,w} satisfying

    x+y+z+w=0,
    Q(x)+Q(y)+Q(z)+Q(w)=0.

These are exactly the weight-four supports orthogonal to E. For a fixed pair {x,y}, put v=x+y. The other pair {z,w} in such a block must lie in the same L_v fiber, with z+w=v. There are exactly three other pairs in that eight-point fiber. Thus every unordered point pair lies in exactly three blocks.

Consequently there are 1008 blocks and each point belongs to 63 blocks:

    |B| = 3 * binom(64,2) / binom(4,2) = 1008,
    r = 3 * 63 / 3 = 63.

The script constructs the blocks two different ways, from derivative fibers and directly from triples. The sets agree. All 64 point degrees and all 2016 pair degrees are checked exactly.

## Odd intersections force C divisible by sixteen

Let F be the support of f, with odd weight w, and let V count blocks B for which |B intersect F| is odd. For k=0,1,2,3,4,

    1_(k odd) = k - 2 binom(k,2)  (mod 4).

Using the design degrees gives

    V = 63w - 6 binom(w,2)
      = 66w - 3w^2
      = 3 (mod 4),

because w is odd.

To connect V to the spectra, expand the sum of all eight fourth moments and sum the characters indexed by (lambda,u). The surviving ordered quadruples have both coordinate sum and Q-value sum zero. The tuples with repeated coordinates contribute

    64 + 6 binom(64,2) = 12160.

Each distinct-coordinate block has 24 orderings and contributes its sign (-1)^|B intersect F|. With T=1008-2V,

    sum_lambda M4_lambda
      = 512 * (12160 + 24T)
      = 6225920 + 12288T
      = 18612224 - 24576V.

If all spectra obey the target bound, the same quantity is

    8*154624 + 6144C.

Equating these expressions gives

    C = 2828 - 4V.

Since V is congruent to three modulo four, C is divisible by sixteen.

The previous parameterization was

    (x,y,z) = (224+4t, 288-12t, 8t), 0 <= t <= 24,

where x=C counts magnitude ten, y counts magnitude six, and z counts magnitude two among the 512 Walsh coefficients. Therefore t must be divisible by four, giving exactly the seven rows listed above. Each Walsh coefficient corresponds to a complementary pair of codewords, explaining the distance-histogram interpretation.

## Validation and scope

Run from this folder:

    python3 check_structural_moments.py

The report is written to structural_moments_report.json. It records exhaustive fixed-code checks, the seven surviving histograms, and four odd-vector identity controls: one unit vector, the archived RM witness, its gauge-normalized version, and one deterministic pseudorandom vector. These controls do not satisfy the full target bound; they test unrestricted moment and design identities. The formal expression 2828-4V is a true magnitude-ten count only when the target bound holds.

The main derivation is an algebraic proof with exact verification of the fixed code's structural premises. The sample controls are implementation checks, not the basis of a universal claim.
