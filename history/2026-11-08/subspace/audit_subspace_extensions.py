"""Independent stdlib audit. Parses only literal GROUPS; executes no model code."""
import ast,json
from collections import defaultdict
from pathlib import Path

def polynomial(n,w):
    a=[1]
    for sign in [-1]*w+[1]*(n-w):
        b=[0]*(len(a)+1)
        for j,c in enumerate(a):
            b[j]+=c; b[j+1]+=sign*c
        a=b
    return a

module=ast.parse(Path('affine_split.py').read_text())
groups=next(ast.literal_eval(node.value) for node in module.body
    if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='GROUPS' for t in node.targets))
points=json.loads(Path('intersection_result.json').read_text())
P27=[polynomial(27,w) for w in range(28)]
P37=[polynomial(37,w) for w in range(38)]
P64=[polynomial(64,w) for w in range(65)]
results=[]
for point in points:
    p,q,y10,y14,z8,z12,z16=point['x']; v=[1]+point['x']
    source=defaultdict(int,{(0,0):1,(0,32):1})
    for r,s,a,coeff in groups:
        count=sum(c*x for c,x in zip(coeff,v))
        assert count>=0
        source[a,r]+=count; source[a,s]+=count
    assert sum(source.values())==1024 and min(source.values())>=0
    numerator=[[0]*38 for _ in range(28)]
    for (a,b),count in source.items():
        for i,lc in enumerate(P27[a]):
            for j,rc in enumerate(P37[b]):
                numerator[i][j]+=count*lc*rc
    assert all(c>=0 and c%1024==0 for row in numerator for c in row)
    dual=[[c//1024 for c in row] for row in numerator]
    assert dual[0][0]==1 and sum(map(sum,dual))==2**54
    for k in range(65):
        assert sum(numerator[i][k-i] for i in range(28) if 0<=k-i<38)==sum(count*P64[a+b][k] for (a,b),count in source.items())
    mid=[[sum(P27[i][a]*numerator[i][j] for i in range(28)) for j in range(38)] for a in range(28)]
    for a in range(28):
        for b in range(38):
            assert sum(P37[j][b]*mid[a][j] for j in range(38))==2**64*source[a,b]
    bounds=[p,80-p,q,31-q,y10,y14,160-y10-y14,z8,z12,z16,80-z8-z12-z16]
    assert min(bounds)>=0
    vals=[c for row in dual for c in row]+bounds
    results.append({'q':q,'x':point['x'],'split_rows':1064,'domain_rows':11,'minimum':min(vals),'zero_rows':vals.count(0),'integral_nonnegative':True,'inverse_transform':True,'ordinary_diagonals':65})

# Independently enumerate classified q=28 S model and sample all sign patterns
# of degree <=2 on its 24 active columns for the extension identities.
U=set(range(8)); active=[v for v in range(32) if v not in U]
weights=[sum((s&v).bit_count()%2 for v in active) for s in range(32)]
assert weights.count(12)==28 and weights.count(16)==3 and weights.count(0)==1
ann=[0,8,16,24]
for mask in range(1<<10):
    # Ten cross terms; this supplies 1024 deterministic diverse assignments.
    signs=[]
    for v in active:
        pairs=[((v>>i)&1)*((v>>j)&1) for i in range(5) for j in range(i+1,5)]
        signs.append(sum(((mask>>i)&1)*b for i,b in enumerate(pairs))%2)
    for z in range(4):
        ws=[z+sum(e^((s&v).bit_count()%2) for v,e in zip(active,signs)) for s in range(32)]
        assert sum(ws)==384+32*z
        assert sum((w-12-z)**2 for w in ws)==192
        assert all(sum(ws[a^k] for k in ann)==48+4*z for a in range(8))
summary={'formal_points':results,'S_repeated_column_pairs':[{ 'q':q,'effective_length':31-q//4,'pairs':(992-14*q-(31-q//4)**2-(31-q//4))//2} for q in [16,20,24,28]],'q28_extension_checks':4096,'scope':'Independent exact necessary-condition check only. No generator matrix, extension feasibility, target construction or exclusion established. Extension identities are proved in accompanying audit note, not inferred from samples.'}
Path('audit_subspace_extensions_result.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
