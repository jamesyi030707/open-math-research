# BCH [64,10,28] and the maximal-output bent-function code

Checked 2026-10-17. This is a focused source/mapping check, not an exhaustive literature survey or a covering-radius computation.

## Result

The supplied extended BCH code is exactly the code C_F for the (6,3)-function F(y)=y^36 from GF(64) to GF(8), in the coordinate order alpha^0,...,alpha^62,0. The applicable published results imply covering radius at most 27. They do not exclude an odd coset of minimum 27. No primary theorem establishing that exclusion was found in this focused search.

## Exact mapping (direct derivation, independently checked)

Use GF(64)=F_2[alpha]/(alpha^6+alpha+1). Since 36*8 is congruent to 36 modulo 63, y^36 lies in GF(8). In fact,

F(y)=y^36=(y^9)^4=N_GF(64)/GF(8)(y)^4.

Thus F is output-linearly equivalent to the relative norm y^9. Choosing a basis gamma_1,gamma_2,gamma_3 of GF(8), and the trace-dual output coordinate basis, its coordinate functions are q_j(y)=Tr_GF(8)/F_2(gamma_j y^36). The paper's generator matrix (1.1), with rows 1, x, F(x), gives

C_F = { (c + Tr_GF(64)/F_2(a y) + Tr_GF(8)/F_2(gamma y^36))_y : c in F_2, a in GF(64), gamma in GF(8) }.

The norm is perfect nonlinear: for t nonzero, substitute y=t z in (y+t)^9+y^9 to obtain t^9(z^8+z+1). The relative trace z^8+z maps GF(64) onto GF(8), with each fiber of size 8. Fourth-power Frobenius preserves this property. Hence F is (6,3)-bent.

On the 63 nonzero coordinates the trace polynomial exponents are {0,1,2,4,8,16,32,9,18,36}. Their negatives modulo 63 are exactly {0,27,31,45,47,54,55,59,61,62}. All other Fourier positions vanish. The supplied degree-53 polynomial g=0x2759262d5d506d has exactly these ten nonroots. Therefore its dimension-10 cyclic code is the trace-evaluation code. The sum of the 64 evaluations is zero (each positive exponent has a zero field power sum, as does the constant term in characteristic two), so evaluation at y=0 is precisely the parity extension.

The companion script independently checks the field arithmetic, all 63 root positions, the map into GF(8), both dimension-10 row spaces and their exact equality. Its output is saved as literature_mapping.output.json. It does not perform a coset search.

## Applicable published sources and exact scope

1. Wilfried Meidl, Alexandr A. Polujan, Alexander Pott, *Linear codes and incidence structures of bent functions and their generalizations*, Discrete Mathematics 346(1), 113157 (2023), author version v2 dated 10 May 2023. https://arxiv.org/html/2012.06866v2

   Equation (1.1) defines C_F. Remark 5.2 invokes Nyberg's nonextendability bound for m=n/2; the paragraph immediately before Example 5.17 explicitly concludes that its covering radius is strictly below 2^(n-1)-2^(n/2-1). At (n,m)=(6,3), this means rho(C_F)<28, hence rho(C_F)<=27. Theorem 5.7 has the printed hypothesis m<=n/2-1 and must not be cited as directly applying to (6,3).

   Question 5.18 remains in v2 and asks about maximal-output bent functions: “What is the covering radius of C_F? Does it depend on F?” This is evidence of the general question's status in that paper, not proof that the particular BCH instance is unresolved in all later literature.

2. Jian Liu, Lusheng Chen, *On Nonlinearity of S-Boxes and Their Related Binary Codes*, Chinese Journal of Electronics 25(1), 167-173 (2016), DOI 10.1049/cje.2016.01.025. https://cje.ejournal.org.cn/article/pdf/preview/10.1049/cje.2016.01.025.pdf

   Theorem 4(i), journal p.170 (PDF page 4), states that for even n the maximum cardinality of a linear supercode of RM(1,n) with minimum distance 2^(n-1)-2^(n/2-1) is 2^(3n/2+1). For n=6, the maximum is 1024. Consequently a linear [64,11,28] supercode containing RM(1,6) is impossible. This theorem concerns distance 28; it does not rule out distance 27.

## Consequences that are safe to use

Because the code contains RM(1,6), every vector has distance at most 28. If any vector had distance 28 from C_F, adjoining it would produce a dimension-11 supercode of minimum distance 28, contradicting the cited bound. Thus rho<=27.

All codewords are even, so every even coset has even minimum, necessarily at most 26. The only remaining possibility above 26 is an odd coset of minimum exactly 27. Excluding that case requires another theorem or an exact verified argument/computation. If an independently checked minimum-26 coset is already available, the radius is reduced to the alternatives 26 or 27; the source check by itself does not establish the lower bound 26.

The field representation and the exact generator have been verified, but this note supplies no new proof of rho<=26 and makes no claim of complete literature coverage.
