#!/usr/bin/env python3
"""Separate FWHT and direct-column audit; standard library, no target search."""
import itertools,json
from fractions import Fraction
from pathlib import Path

def fwht(values):
    a=list(values);h=1
    while h<len(a):
        for i in range(0,len(a),2*h):
            for j in range(i,i+h):
                x,y=a[j],a[j+h];a[j],a[j+h]=x+y,x-y
        h*=2
    return a

def inverse(w,n):return [Fraction(x,len(w)) for x in fwht([n-2*x for x in w])]
def weights(cols,k):
    return tuple(sum(bin(u&v).count('1')%2 for v in cols) for u in range(2**k))
def main():
    data=json.loads(Path(__file__).with_name('message_columns_result.json').read_text())
    c=data['control'];a=weights(c['left_columns'],4);b=weights(c['right_columns'],4)
    bad=tuple(c['relabelled_weights'])
    assert sorted(zip(a,b))==sorted(zip(bad,b))
    assert list(map(str,inverse(bad,8)))==c['relabelled_column_multiplicities']
    assert inverse(a,8)==[c['left_columns'].count(v) for v in range(16)]
    actual={weights(cols,2) for cols in itertools.product(range(4),repeat=3)}
    accepted=set()
    for t in itertools.product(range(4),repeat=3):
        w=(0,)+t
        if all(x>=0 and x.denominator==1 for x in inverse(w,3)):accepted.add(w)
    assert actual==accepted and len(actual)==20
    wrong=[0,4,2,2,0,2,2,2];got=list(map(str,inverse(wrong,6)))
    assert got==['5/2','3/2','1/2','3/2','-1/2','1/2','-1/2','1/2']
    print(json.dumps({'status':'pass','independent_method':'butterfly Walsh transform and direct column enumeration','small_realizable_functions':len(actual),'claude_final_example_multiplicities':got,'scope':'No target labelling or target existence decision.'},indent=2))
if __name__=='__main__':main()
