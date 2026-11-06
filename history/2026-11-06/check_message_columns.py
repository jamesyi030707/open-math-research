#!/usr/bin/env python3
"""Exact bounded message-level control; standard library only. No target search."""
import json,time,collections,itertools,math
from fractions import Fraction
from pathlib import Path

def weights(columns,k):
    return [sum((u&v).bit_count()%2 for v in columns) for u in range(1<<k)]

def invert(a,n):
    N=len(a)
    return [Fraction(sum((n-2*a[u])*(-1 if (u&v).bit_count()%2 else 1) for u in range(N)),N) for v in range(N)]

def kw(n,w,j):
    return sum((-1)**s*math.comb(w,s)*math.comb(n-w,j-s) for s in range(max(0,j-(n-w)),min(w,j)+1))

def split(a,b):return collections.Counter(zip(a,b))

def main():
    start=time.process_time()
    k=4;left=[1,1,2,2,4,4,8,8];right=list(range(1,16))
    a=weights(left,k);b=weights(right,k);bad=a.copy();bad[1],bad[7]=bad[7],bad[1]
    assert a==[0,2,2,4,2,4,4,6,2,4,4,6,4,6,6,8]
    assert split(a,b)==split(bad,b)
    assert all((x-y)%4==0 for x,y in zip(a,bad))
    good_m=invert(a,8);bad_m=invert(bad,8)
    assert good_m==[Fraction(collections.Counter(left)[v]) for v in range(16)]
    assert [(v,int(m)) for v,m in enumerate(bad_m) if m<0]==[(10,-1),(12,-1)]
    # Check the entire unchanged split MacWilliams transform exactly.
    primal=split(a,b)
    dual={}
    for i in range(9):
        for j in range(16):
            value=Fraction(sum(count*kw(8,x,i)*kw(15,y,j) for (x,y),count in primal.items()),16)
            assert value.denominator==1 and value>=0
            dual[i,j]=int(value)
    assert sum(dual.values())==2**19
    # Independent direct dual enumeration: first left coordinate of each duplicate
    # pair is a pivot, all other 19 coordinates free. Solve syndrome with pivots.
    cols=left+right;pivots=[0,2,4,6];free=[j for j in range(23) if j not in pivots]
    direct=collections.Counter();word=0;syn=0;prev=0
    for z in range(1<<19):
        gray=z^(z>>1)
        if z:
            d=gray^prev;t=d.bit_length()-1;j=free[t];word^=1<<j;syn^=cols[j]
        fixed=word
        for i,j in enumerate(pivots):
            if (syn>>i)&1:fixed|=1<<j
        direct[(fixed&255).bit_count(),(fixed>>8).bit_count()]+=1
        prev=gray
    assert all(direct[p]==c for p,c in dual.items())
    # Exact reconstruction test for every labelled function on F2^2 with n=3:
    # iff inverse nonnegative integral. Enumerate all 64 functions and all 64
    # ordered lists of three generator columns, including zero/repeated columns.
    genuine={tuple(weights(c,2)) for c in itertools.product(range(4),repeat=3)}
    accepted=set()
    for t in itertools.product(range(4),repeat=3):
        w=(0,)+t;m=invert(w,3)
        if all(x>=0 and x.denominator==1 for x in m):accepted.add(w)
    assert accepted==genuine
    out={'status':'pass','scope':'Message-labelled column-realizability control only; no target-code exclusion or construction.',
         'control':{'k':k,'left_columns':left,'right_columns':right,'left_weights':a,'relabelled_weights':bad,
          'split_histogram':[[x,y,c] for (x,y),c in sorted(primal.items())],
          'split_dual_cells_checked':len(dual),'direct_dual_words_checked':2**19,
          'same_weights_modulo_4':True,'relabelled_column_multiplicities':[str(x) for x in bad_m],
          'negative_columns':[[10,-1],[12,-1]],'fractional_columns':[]},
         'exhaustive_small_control':{'labelled_functions':64,'ordered_column_lists':64,'realizable_distinct_weight_functions':len(genuine),'mismatches':0},
         'cpu_seconds':time.process_time()-start}
    Path(__file__).with_name('message_columns_result.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
if __name__=='__main__':main()
