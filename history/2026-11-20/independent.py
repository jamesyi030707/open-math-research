"""Independent seven-sign enumeration and local-control verification."""
import itertools,json
B=[0x17e7146801,0x6293dc808,0xf714c2017,0x35dfc802d,0xb1f3485c,0x63e6a0ae,0x65be14f,0x196fc233,0x3e690ce6,0xcb73897]
C=[37,6,7,9,10,11,13,14,15,17,18,19,21,22,23,25,58,27,28,29,29,30,30,31,63,0,32]
def require(ok):
 if not ok:raise ValueError('audit failed')
def cw(u):
 x=0
 for i,b in enumerate(B):
  if u>>i&1:x^=b
 return x
def W(t):return ((t&31)<<4)^(1008 if t&32 else 0)
def chi(t,c):return 1-2*((t&c).bit_count()%2)
H=[t for t in range(64) if cw(2^W(t)).bit_count()==14]
raw=[[sum(chi(t,v)*chi(t,c) for t in H) for c in C] for v in (0,1)]
rhs=[-sum(chi(t,v) for t in H) for v in (0,1)]
require(all(x%4==0 for row in raw for x in row) and all(x%4==0 for x in rhs))
rows=[[x//4 for x in row] for row in raw];target=tuple(x//4 for x in rhs)
active=[j for j in range(27) if rows[0][j] or rows[1][j]]
points={tuple(sum(row[j]*s for j,s in zip(active,signs)) for row in rows) for signs in itertools.product((-1,1),repeat=len(active))}
local=[]
for t in range(1,64):
 b=cw(W(t)).bit_count();a=sum((t&c).bit_count()%2 for c in C)
 local.append(27-b<=a<=b and (a+b)%4==0)
q=sum(sum((t&c).bit_count()%2 for c in C)==12 for t in range(1,32))
scalar=[target[i] in {p[i] for p in points} for i in (0,1)]
require(all(local) and q==24 and len(active)==7 and len(points)==47)
require(all(scalar) and target not in points)
print(json.dumps({'index_zero_based':1,'H':H,'local_windows_passed':sum(local),'q':q,'r':sum(c>>5 for c in C),'z':C.count(32),'active_indices':active,'scaled_rows':[[row[j] for j in active] for row in rows],'target':target,'sign_assignments':2**len(active),'reachable_pairs':len(points),'scalar_feasible':scalar,'joint_feasible':target in points,'first_coordinate_when_second_zero':sorted(x for x,y in points if y==0)},indent=2))
