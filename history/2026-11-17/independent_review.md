# Independent audit: the stabilizer of S and h

The claimed group order 1 is correct for this scope: invertible message maps preserving the weight function of the fixed B, fixing h=1008, and preserving S={s<<4}. It is not the full automorphism group of B or the stabilizer of W=S+<h>.

## Completeness of the block form

Write a B column as (z,x,e), where z consists of its low four bits, x of bits 4..8, and e=h dot column. This is an invertible change of ten column coordinates. The 37 columns consist of 32 points (f(x),x,1), one for each x in F2^5, and five points (z,0,0), with z in Z={1,4,7,13,15}.

Fixing h forces e'=e. Preserving S forces x'=Lx, with L invertible. The most general invertible column action is therefore

(z,x,e) -> (Dz+Kx+ce,Lx,e),

where D is invertible. Preservation of the five e=0 columns requires D(Z)=Z. These five points form a spanning circuit, and every permutation uniquely determines an invertible D: there are exactly 120 possibilities. The e=1 column with x=0 is (0,0,1), because f(0)=0; its image must itself have x=0 and hence z=0. Thus the potentially missing term c is forced to zero, not simply assumed absent.

## Recovering L from radicals

Each scalar function q_a(x)=a dot f(x), a!=0, is quadratic, and its polar form has a one-dimensional radical with unique nonzero vector r_a. This is verified from all 32 truth-table values. Their fifteen radical vectors span F2^5. The required identity f(Lx)=Df(x)+Kx implies

L(r_(D^t a))=r_a.

Consequently each D determines at most one L. The independent implementation uses XOR closure of all fifteen required correspondences, not the main implementation's selected-basis inversion. Exactly one of the 120 correspondences is a well-defined invertible linear map: D=L=identity. The full graph identity then forces K=0. Thus identity is the only candidate and it really preserves the columns.

## Verification

`independent_stabilizer.py` does not import the main implementation. It independently builds the polar truth tables, verifies their bilinearity and radical dimensions, derives candidates by XOR closure, checks full graph/column preservation, recovers a coordinate permutation, and tests all 1024 message weights for the accepted candidate. Its output is `independent_stabilizer.json`. Ordinary and `python -O` outputs agree after discarding CPU timing. All checks raise errors explicitly; none depend on `assert`.

The result does not permit arbitrary GL(5,2) transport of the canonical exclusion and adds no new excluded S orientation. In particular, preserving W alone would allow x'=Lx+t e and is a different group problem.
