"""Exact split-weight obstruction for the 2026-10-26 formal witness only.
Python 3 standard library. No search; no branch-wide exclusion.
"""
import json
from pathlib import Path
from collections import Counter
from math import comb

def K(n,j,w):
    return sum((-1)**i*comb(w,i)*comb(n-w,j-i)
               for i in range(max(0,j-n+w),min(j,w)+1))

def check(source):
    prior=json.loads(Path(source).read_text())
    joint=Counter({(0,0):1,(0,32):1})
    for r,s,a,count in prior['categories']:
        joint[a,r]+=count
        joint[a,s]+=count
    assert sum(joint.values())==1024
    assert Counter({int(k):v for k,v in prior['D'].items()}) == Counter({w:sum(c for (a,r),c in joint.items() if a+r==w) for w in {a+r for a,r in joint}})
    out=[]
    for i in range(28):
        row=[]
        for j in range(38):
            num=sum(c*K(27,i,a)*K(37,j,r) for (a,r),c in joint.items())
            assert num%1024==0
            row.append(num//1024)
        out.append(row)
    ordinary=[sum(out[i][w-i] for i in range(28) if 0<=w-i<38) for w in range(65)]
    assert ordinary==prior['dual_D']
    terms=[{'a':a,'r':r,'count':c,'K1':K(27,1,a),'K2':K(37,2,r),'numerator':c*K(27,1,a)*K(37,2,r)} for (a,r),c in sorted(joint.items())]
    negative=[{'left':i,'right':j,'coefficient':out[i][j]} for i in range(28) for j in range(38) if out[i][j]<0]
    assert sum(t['numerator'] for t in terms)==-16384
    return {'block_lengths':[27,37],'code_size':1024,'joint_distribution':[{'a':a,'r':r,'count':c} for (a,r),c in sorted(joint.items())],
            'checked_split_coefficients':1064,'all_coefficients_integral':True,'negative_coefficients':negative,
            'B_1_2_terms':terms,'B_1_2_numerator':-16384,'B_1_2':-16,
            'split_dual':out,'ordinary_diagonal_sums':ordinary,
            'scope':'This joint formal witness cannot be the split-weight distribution of a binary linear code. No exclusion of all kernel-one candidates or of the target code.'}

if __name__=='__main__':
    import sys
    print(json.dumps(check(sys.argv[1]),indent=2))
