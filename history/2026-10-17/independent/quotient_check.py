"""Exact systematic transversal for F_2^64 / E. No feasibility search."""
import json
from pathlib import Path
P=Path(__file__).parent
M=json.loads((P/'model.json').read_text())
rows=[int(x,16) for x in M['basis_hex']]
piv=[];r=0
for j in range(64):
 k=next((k for k in range(r,len(rows)) if (rows[k]>>j)&1),None)
 if k is None:continue
 rows[r],rows[k]=rows[k],rows[r]
 for k in range(len(rows)):
  if k!=r and (rows[k]>>j)&1: rows[k]^=rows[r]
 piv.append(j);r+=1
 if r==10:break
assert len(piv)==10
assert all(((rows[k]>>j)&1)==(k==i) for i,j in enumerate(piv) for k in range(10))
assert all(x.bit_count()%2==0 for x in rows)
E=[0]
for x in rows:E += [e^x for e in E]
def normalize(f):
 for j,row in zip(piv,rows):
  if (f>>j)&1:f^=row
 return f
checks=[]
for f in [1,7,0x13579bdf2468ace1,0x123456789abcdef0]:
 f0=normalize(f)
 assert all(not((f0>>j)&1) for j in piv)
 assert f.bit_count()%2==f0.bit_count()%2
 # A full coset check establishes distance preservation, without a search for a deep hole.
 assert {f^e for e in E}=={f0^e for e in E}
 checks.append({'input':f'{f:016x}','normal':f'{f0:016x}'})
result={'pivot_positions_zero_based':piv,'rref_rows_hex':[f'{x:016x}' for x in rows],'remaining_binary_coordinates':54,'all_cosets_have_unique_zero_pivot_representative':True,'sample_coset_checks':checks,'deep_hole_search':False}
(P/'quotient_certificate.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
