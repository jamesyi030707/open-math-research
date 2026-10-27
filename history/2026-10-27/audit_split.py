import json
from collections import Counter
from fractions import Fraction
# Fixed category witness from published 2026-10-26 certificate.
categories=[(14,22,14,160),(16,24,16,80),(16,16,16,31),(18,18,10,140),(18,18,14,16),(18,18,18,4),(20,20,8,8),(20,20,12,6),(20,20,16,64),(20,20,20,2)]
joint=Counter({(0,0):1,(0,32):1})
for r,s,a,count in categories:
    joint[a,r]+=count
    joint[a,s]+=count
assert sum(joint.values())==1024
# Coefficients of (1+x)^(n-w)(1-x)^w through repeated multiplication,
# no combinatorial/Krawtchouk implementation reused.
def polynomial(n,w):
    p=[1]
    for factor in [1]*(n-w)+[-1]*w:
        q=[0]*(len(p)+1)
        for i,c in enumerate(p): q[i]+=c; q[i+1]+=factor*c
        p=q
    return p
out=[[0]*38 for i in range(28)]
for (a,r),count in joint.items():
    l=polynomial(27,a); rr=polynomial(37,r)
    for i in range(28):
        for j in range(38): out[i][j]+=count*l[i]*rr[j]
assert all(v%1024==0 for row in out for v in row)
out=[[v//1024 for v in row] for row in out]
negative=[{'left':i,'right':j,'coefficient':v} for i,row in enumerate(out) for j,v in enumerate(row) if v<0]
ordinary=Counter()
for row_index,row in enumerate(out):
    for col_index,val in enumerate(row): ordinary[row_index+col_index]+=val
assert all(v>=0 for v in ordinary.values())
assert sum(sum(row) for row in out)==2**54
assert out[0][0]==1
assert out[1][2]==-16 and out[3][1]==-1 and len(negative)==8
result={'method':'Direct repeated multiplication of signed linear polynomial factors; exact integer normalization 1024.','joint':{f'{a},{r}':v for (a,r),v in sorted(joint.items())},'checked_coefficients':1064,'negative_coefficients':negative,'dual_joint':out,'ordinary_diagonal_sums_nonnegative':True,'total':sum(sum(row) for row in out),'scope':'Rejects only this fixed joint/category enumerator; no branch-wide or distance-bound exclusion.'}
print(json.dumps(result,indent=2))
