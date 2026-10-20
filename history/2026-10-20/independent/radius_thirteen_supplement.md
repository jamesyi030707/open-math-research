# Excluding distance thirteen: signed-fiber integrality

Date: 2026-10-20. This supplements, and strengthens, the quadratic-neighborhood lemma. AI-assisted analysis; originality has not been established.

## Strengthened conclusion

For the same fixed parent E, every odd f with |W_(f+q)|<=10 for all q in Q satisfies **d(f,RM(2,6)) >= 15**.

The preceding proof excludes all distances below thirteen. If d(f,g)=13 for a quadratic g, choose a non-bent h=g+q. Ranks zero and two already require distances at least 27 and 23. Thus only rank four needs consideration.

## Restricted spectrum at equality

Write u=f+q. Let S be the sixteen-element Walsh support of h and epsilon=W_h/16 on S. The exact identity from the basic lemma gives

sum_(a in S) epsilon(a) W_u(a) = 256-8*13 = 152.

Each W_u(a) is congruent to two modulo four: u has odd weight because q has even weight. Hence every aligned value epsilon(a)W_u(a) is at most ten and congruent to two modulo four. Sixteen maxima would sum to 160. The total deficit eight can therefore have exactly two forms:

1. One aligned value two, with the other fifteen equal to ten.
2. Two aligned values six, with the other fourteen equal to ten.

Negative aligned entries cannot occur here, since each would incur deficit at least twelve.

## Signed-fiber integrality

Let R be the two-dimensional radical of h's alternating bilinear form. Its Walsh support is an affine coset S=a0+R-perp. Define the restricted inverse transform

P_u(x) = (1/64) sum_(a in S) W_u(a) (-1)^(a dot x).

Character orthogonality gives

P_u(x) = (1/4) sum_(z in R) (-1)^(a0 dot z) s_u(x+z).

Thus every P_u(x) belongs to {-1,-1/2,0,1/2,1}. The signs matter when S is affine rather than linear, but do not change this integrality restriction.

For case 1, with the exceptional coefficient at a, Walsh inversion for h gives

P_u(x) = (5/8)s_h(x) - (1/8)epsilon(a)(-1)^(a dot x).

Its possible values are ±1/2 and ±3/4. Avoiding ±3/4 everywhere would require epsilon(a)(-1)^(a dot x)=s_h(x) everywhere, making h affine. This contradicts its rank four. Therefore this case is impossible. More precisely, the correlation is epsilon(a)W_h(a)=16, so the signs disagree on exactly 24 positions, and all 24 yield illegal values.

For case 2, at distinct a,b, the expression is

P_u(x) = (5/8)s_h(x) - (1/16)[epsilon(a)(-1)^(a dot x)+epsilon(b)(-1)^(b dot x)].

The two signed characters cancel at exactly 32 positions because a differs from b. At those positions P_u(x)=±5/8, again impossible.

Both cases contradict a necessary property of every Boolean u. Distance thirteen is therefore excluded. All distances from odd f to quadratic functions are odd, so the next possible distance is fifteen.

## Independent finite check

`python check_radius_thirteen.py` checks the canonical rank-four quadratic h=x0*x1+x2*x3. It enumerates all sixteen single-defect and 120 double-defect restricted spectra with exact integers, applies the inverse Walsh transform, and verifies that each fails signed-fiber integrality. The first case fails at exactly 24 positions; the second at least 32. Its output is `radius_thirteen_report.json`.

This representative computation is supplementary. The argument above applies to every rank-four quadratic, including affine terms, without relying on numerical sampling or assuming a linear Walsh support. The exhaustive non-bent-translate check for the actual parent remains the finite component supplied by `check_quadratic_neighborhood.py`.

The result removes structured construction neighborhoods, not any of the seven remaining aggregate weight profiles. It neither constructs a [64,11,27] code nor proves that none exists.
