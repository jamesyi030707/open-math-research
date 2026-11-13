# The minimum-word sections are bent graphs, not affine flats

This is an independent geometric check of the fixed residual used in the November 12 archive. It provides a correct small compatibility representation, not a new exclusion or target-code construction.

Use six-bit coordinates `s+32e` for the message `(s<<4) XOR (e*1008)` in W. For each t in `{2,3,5,6,8,9,10,11,12,14}`, exactly sixteen messages in `t+W` have residual weight 14. The exhaustive 1024-word check shows that each corresponding set H_t has affine-span dimension five, not four. Thus the kernel-one constant-hyperplane argument must not be applied directly to these sets in W. No claim is made that an earlier published note applied it incorrectly.

The projection of H_t onto S is an affine hyperplane. Parameterize it as

    s = o + x_0 b_0 + x_1 b_1 + x_2 b_2 + x_3 b_3,
    e = g(x),    x in F2^4.

For all ten sections, g is a quadratic Boolean function whose sixteen Walsh coefficients are all +4 or -4. The program records every origin, basis, truth-table ANF and Walsh spectrum. For t=2 one can take

    o=0, (b_0,b_1,b_2,b_3)=(1,6,8,18),
    g=x_0 x_1 + x_1 x_2 + x_2 x_3.

For example, 0,1,6 belong to H_2 but 1 XOR 6 = 7 does not, immediately disproving linearity when H_2 contains zero. Its polar form has rank four; the computed Walsh spectrum gives a second check of the bent property.

## Exact signed-count compatibility

Consider arbitrary actual left columns with W-labels `(v,e)`, and let the outside message t have coordinate bits y_j. Set `lambda(v)_i=v·b_i`. For e in {0,1}, collect the signed counts

    c_e(lambda) = sum_{j: e_j=e, lambda(v_j)=lambda}
                     (-1)^(y_j + v_j·o).

Let M_e(lambda) be the corresponding ordinary column multiplicity. Then

    |c_e(lambda)| <= M_e(lambda),
    c_e(lambda) = M_e(lambda) mod 2.

These statements include repeated columns and zero labels. Let `G(z)=sum_x (-1)^(g(x)+z·x)` and `K[z,lambda]=G(z+lambda)/4`, a sixteen-by-sixteen matrix with entries ±1. Orthogonality gives `K K^T=16 I`.

The sixteen required equations `wt(tA + (s,e)A)=14` are equivalent, by the four-dimensional Walsh transform, to the sixteen integer equations

    4 c_0(z) + sum_lambda K[z,lambda] c_1(lambda) = -4 [z=0].

Indeed the character sum of the 27 left coordinates is `27-2*14=-1` on H_t. The e=0 column characters transform to sixteen times a delta; the e=1 characters transform to the shifted bent spectrum. Hence the displayed formula follows by summing columns. Conversely, invertibility of the Walsh transform proves sufficiency for these sixteen equalities only, not for all residual windows.

Equivalently,

    c_1 = -(1/4) K^T (c_0+delta_0),
    sum_lambda c_1(lambda)^2 = sum_lambda (c_0(lambda)+[lambda=0])^2.

The common W-column multiplicities must permit such signed counts for all ten sections, with signs induced by the same linear extension, not ten unrelated choices. Treating this as ten independent feasibility tests is only a relaxation. No feasibility or infeasibility determination for general multiplicities is made here.

This representation is exact but redundant with the complete common-column model. Its value is to make the next small compatibility calculation correct and auditable, rather than to claim a new independent inequality or prove that kernel zero is impossible.

## Verification boundary

`check_geometry.py` reconstructs the fixed residual from ten pinned generating row values, checks all section geometries and all ten bent spectra, and tests the Fourier transform formula on each of the 64 possible single-column W-characters for every section (640 cases). Linearity then covers arbitrary signed multisets, including repeated and zero columns. A true affine four-flat is accepted as a contrasting positive control, and a genuine 27-column affine model with fourteen constant-one zero-label columns has weight fourteen throughout that flat.

Both normal and optimized Python runs pass in about 0.03 CPU seconds and agree after removing only `cpu_seconds`. Explicit exceptions remain active under `-O`. These finite checks are not an external peer review or a proof-assistant certification. No target-matrix search was performed.
