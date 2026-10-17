"""Integer specification and independent checks, no feasibility claim."""
import json, hashlib
from pathlib import Path
P=Path(__file__).parent
g=0x2759262d5d506d
basis=[(g<<j)|(((g<<j).bit_count()%2)<<63) for j in range(10)]
E=[0]
for b in basis: E += [c^b for c in E]
assert len(set(E))==1024
coords=[];x=1
for j in range(63):
 coords.append(x);x<<=1
 if x&64:x^=67
coords.append(0)
Q=[0x172e5cb972e5cb97,0x65cb972e5cb972e5,0x3972e5cb972e5cb9]
reps=[0]
for q in Q:reps += [c^q for c in reps]
forms=[];words=[]
for q in reps:
 for a in range(64):
  w=q ^ sum(((a&x).bit_count()%2)<<j for j,x in enumerate(coords))
  words.append(w)
  forms.append([1-2*((w>>j)&1) for j in range(64)])
assert len(set(words))==512
assert set(words)|{w^((1<<64)-1) for w in words}==set(E)
# A binary f meets sum_j A_ij*f_j in [(sum A_i-10)/2,(sum A_i+10)/2].
# All endpoints integral. Parity encoded sum f_j - 2*t = 1, t in 0..31.
# Complement symmetry permits f_63=0: adding all-ones preserves odd parity/distances.
checks=[]
for f in [1,7,0x13579bdf2468ace1,0x123456789abcdef0]:
 d=min((f^e).bit_count() for e in E)
 maxW=max(abs(sum(s*(1-2*((f>>j)&1)) for j,s in enumerate(row))) for row in forms)
 assert d==(64-maxW)//2
 checks.append({'f':f'{f:016x}','distance':d,'max_abs_Walsh':maxW})
obj={'basis_hex':[f'{b:016x}' for b in basis],'forms':forms,'parity':'sum(f)-2*t=1; t integer 0..31','safe_symmetry':'f[63]=0 by all-ones addition'}
(P/'model.json').write_text(json.dumps(obj,separators=(',',':'))+'\n')
(P/'checks.json').write_text(json.dumps({'parent_words':1024,'forms':512,'exact_interface_checks':checks,'solve_performed':False},indent=2)+'\n')
print(json.dumps(checks))
