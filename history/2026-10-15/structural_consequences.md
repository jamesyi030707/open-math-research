# Consequences of a blocking set of minimum-weight messages

Let G be the archived rank11 binary generator matrix and let C be its row space. The injective map m↦mG identifies message subspaces with code subspaces. Let W be the234 messages whose codewords have weight26.

## Codimension-two enumeration and the stronger spectral certificate

Every dimension9 message subspace is the kernel of a rank2 linear map. Its two-dimensional annihilator has exactly three nonzero vectors a,b,a XOR b. Selecting a<b<a XOR b gives one representative of each annihilator. Thus the number is (2047×2046)/6=698027.

The exact enumeration shows each such kernel contains at least36 members of W. More strongly, the compact character certificate proves that every dimension8 message subspace contains at least3 members of W: F(0)=234, all nonzero F(a)≥−30, and the average of F over any3-dimensional annihilator is at least(234−7×30)/8=3. Consequently any linear code C' with minimum distance at least27 satisfies dim(C∩C')≤7. This holds regardless of how C' is generated; the conclusion concerns overlap with this fixed code in its fixed coordinate positions, not all codes of the target parameters.

For a same-size matrix perturbation G'=G+E with rank(E)≤3, the left kernel {m:mE=0} has dimension at least8, and for m in that kernel mG'=mG. Injectivity of G shows that these shared words span at least8 dimensions. Therefore such a perturbation cannot produce minimum distance at least27. This excludes replacing any three generator rows and more generally all rank≤3 updates, even if they change all64 coordinates. The matrices are compared in the same coordinate representation; rank of a matrix difference is not an invariant of two independently chosen generator bases. The code-intersection statement itself is basis invariant. It is distinct from a restriction on the number of changed columns.

## Why the tempting seven-word certificate cannot exist

A3-dimensional binary subcode has7 nonzero words. At each coordinate, the coordinate functional on that subcode is either zero or takes value1 on exactly4 words. Its total nonzero-word weight is therefore divisible by4. Seven words all of weight26 would have total182, not divisible by4. Hence a3D constant-weight26 subspace is impossible. This does not rule out more general small blocking certificates.

These are elementary linear-algebra deductions conditional on the separately checked finite blocking result; they do not prove global nonexistence of a[64,11,27] code.
