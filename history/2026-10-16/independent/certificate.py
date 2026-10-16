import json
from pathlib import Path
p=Path(__file__).parent
r=json.loads((p/'results.json').read_text())
D={int(j):v for j,v in r['dual_weight_enumerator'].items()}
constraints=r['constraints_j_a_b_constant_upper']
endpoint={}
for t in [0,24]:
 x,y,z=224+4*t,288-12*t,8*t
 dual={}
 for j,a,b,c,hi in constraints:
  numerator=a*x+b*y+c
  assert 0<=numerator<=hi and numerator%2048==0
  if numerator:dual[j]=numerator//2048
 endpoint[t]=dual
# Since x,y affine in t, every dual coefficient is affine in t.
# Check integrality of all slopes, hence all integer t between endpoints.
slopes={}
for j,a,b,c,hi in constraints:
 slope=(4*a-12*b)
 assert slope%2048==0
 if slope:slopes[j]=slope//2048
(p/'endpoint_dual_certificates.json').write_text(json.dumps({'t0_dual':endpoint[0],'t24_dual':endpoint[24],'integer_dual_slopes_per_t':slopes},indent=2))
(p/'REPORT.md').write_text('''# Independent exact BCH/coset verification

The binary primitive narrow-sense BCH code of length 63 with roots alpha^1 through alpha^26, where alpha is x modulo x^6+x+1, has generator polynomial encoded by 0x2759262d5d506d (bit i is the coefficient of x^i). Exact field multiplication verifies alpha has order 63. Closing the roots under binary conjugation gives generator degree 53, hence dimension 10. Enumeration of all 1,024 codewords after overall parity extension gives

W_C(z) = 1 + 448 z^28 + 126 z^32 + 448 z^36 + z^64.

Thus C is [64,10,28] and contains the all-ones vector.

## Necessary odd-coset constraints

Suppose v is odd weight and v+C has minimum weight at least 27. Complementation and even parity of C restrict the coset to weights 27,29,31,33,35,37. Set x=A27=A37, y=A29=A35, z=A31=A33. Then x+y+z=512.

Let K_j(w) be the binary length-64 Krawtchouk polynomial and D_j the dual enumerator coefficient of C. Since C union (v+C) would be a dimension-11 linear code, its dual coefficients E_j must be integers satisfying 0 <= E_j <= D_j. They obey

2048 E_j = sum_w A_w(C) K_j(w) + x[K_j(27)+K_j(37)] + y[K_j(29)+K_j(35)] + z[K_j(31)+K_j(33)].

For j=2, D_2=0 forces 3x+y=960. Hence y=960-3x and z=2x-448. Nonnegative counts force 224<=x<=320. For j=4 the equation simplifies to E_4=301+x/4, so x is divisible by 4.

All remaining constraints are satisfied by every one of the resulting 25 candidates:

(x,y,z)=(224+4t, 288-12t, 8t), integer t=0,...,24.

The endpoint dual enumerators and integral slopes are recorded in endpoint_dual_certificates.json. Every coefficient is affine in t, so exact endpoint bounds plus integral slopes certify all 25 candidates. The independent exhaustive enumeration in verify.py confirms no other nonnegative integer distributions satisfy the stated constraints.

Conclusion: these weight-enumerator and dual-enumerator constraints alone do not obstruct an odd coset of minimum weight 27. A feasible distribution is only a necessary-condition certificate; it does not construct such a coset or establish existence of a [64,11,27] code. Nothing here addresses global nonexistence.

Reproduce: python verify.py && python certificate.py. Standard Python only; no dependencies required.
''')
print('Exact endpoint and affine-slope certificate saved.')
