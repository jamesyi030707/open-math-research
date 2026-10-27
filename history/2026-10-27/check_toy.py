"""Fixed eight-message examples only; does not rerun Claude's search/random tests."""
from fractions import Fraction
import json
N=6
m=[0,0,0,0,0,0,1,5]
a=[0,5,6,1,6,1,0,5]
b=[0,5,5,6,1,1,0,6]
assert [sum(m[v] for v in range(8) if (u&v).bit_count()%2) for u in range(8)]==a
assert sorted(a)==sorted(b)
inverse=[Fraction(sum((N-2*b[u])*(-1)**((u&v).bit_count()%2) for u in range(8)),8) for v in range(8)]
assert inverse==[0,3,Fraction(5,2),Fraction(-1,2),-2,0,Fraction(1,2),Fraction(5,2)]
assert sum(b[u] for u in [0,1,2,3])==16>2*N
print(json.dumps({'verified':'Fixed compatible and incompatible labelings share a histogram.', 'compatible':a,'columns':m,'incompatible':b,'inverse':[str(x) for x in inverse], 'subspace':[0,1,2,3],'sum':16,'upper_bound':12,'scope':'Toy only; no target exclusion or complete-search reproduction.'},indent=2))
