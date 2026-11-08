# Independent audit

## Four formal points

All four points in `intersection_result.json`, for q = 16, 20, 24, 28, pass an independently implemented exact integer transform. The checker parses only the literal GROUPS assignment from `affine_split.py` with Python AST. It does not import or execute that file or call its Krawtchouk or table routines. Instead it multiplies the factors of (1-X)^w(1+X)^(n-w).

For each point it verifies 1,064 integral nonnegative normalized split coefficients, the 11 count-domain bounds, source total 1,024, dual total 2^54, all 65 ordinary-weight diagonals, and exact inverse transformation. Minimum slack is zero for all four; zero counts are 25, 29, 29, 29, agreeing with the supplied results. These are feasible formal enumerators under the checked conditions, not realized codes.

## Repeated-column calculation

Write m_v for multiplicity of a nonzero column v in the restriction to S = F2^5; N is the number of its nonzero columns. The first moment gives 16N = 12q + 16(31-q), so N = 31-q/4. The second moment is

sum_s wt(s)^2 = 8(N^2 + N + 2 sum_v binom(m_v,2)).

Indeed, a single nonzero coordinate is 1 on 16 messages, two equal columns are simultaneously 1 on 16 messages, and two distinct nonzero columns are simultaneously 1 on 8 messages. The specified spectrum gives sum_s wt(s)^2 = 144q + 256(31-q). Consequently

sum_v binom(m_v,2) = (992 - 14q - N^2 - N)/2.

For q = 16, 20, 24, 28 the respective effective lengths are 27, 26, 25, 24 and repeated-column pair counts are 6, 5, 3, 0.

## q = 28 classification

There are 24 distinct nonzero columns, so their complement D in the 31 nonzero vectors of F2^5 has size seven. The full simplex has weight 16 at every nonzero message, so evaluation on D has weight 4 for 28 messages and zero for three nonzero messages. Including the zero message, its evaluation kernel has size four; thus D spans a three-dimensional subspace U. Since U has exactly seven nonzero elements and D consists of seven distinct nonzero elements, D = U minus {0}.

Thus the restriction is, up to row transformations and coordinate permutations, the 24-column complement of a three-dimensional subspace, together with three zero columns when the ambient block has length 27. This classification is exact.

## Extension identities, not an exclusion

For completeness, the derived identities are recorded, with no further extension search. For an extension coset t+S, let e_v be its value at the column indexed by v outside U and let z be its weight on the three zero columns. Define

F_t(s) = sum_(v outside U) (-1)^(e_v + s dot v).

Then wt(t+s) = 12+z-F_t(s)/2. Character orthogonality gives sum_s F_t(s)=0 and sum_s F_t(s)^2=32*24. Therefore the 32 coset weights have sum 384+32z and sum_s (wt(t+s)-12-z)^2 = 192.

Let A = U-perp, a two-dimensional subspace of S. For every a, sum_(s in a+A) F_t(s)=0, because none of the active columns belongs to U. Thus each of the eight four-element blocks a+A has weight sum 48+4z.

If S extends inside a nine-dimensional message space T, restriction to the three zero coordinates induces a linear map T/S -> F2^3. Its kernel has dimension at least one. In particular at least one nonzero quotient coset has z=0. More precisely if this map has rank r, the multiset of its zero-coordinate patterns contains each member of a rank-r binary length-three code exactly 2^(4-r) times. These necessary identities do not by themselves rule out any target code.

`audit_subspace_extensions.py` samples 1,024 deterministic sign assignments and all four values of z as a check of the formulas. The proof above, not those samples, establishes the identities for arbitrary assignments.
