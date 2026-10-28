"""Small genuine-code controls for the binary split MacWilliams transform.
Standard library only. No target-code search; left block is low-order bits.
"""
from collections import Counter
from fractions import Fraction
from math import comb
import json

def span(rows):
    words = {0}
    for row in rows:
        words |= {v ^ row for v in list(words)}
    return words

def joint(words, n, left):
    mask = (1 << left) - 1
    return Counter(((x & mask).bit_count(), (x >> left).bit_count()) for x in words)

def K(n, j, w):
    return sum((-1)**t * comb(w,t) * comb(n-w,j-t)
               for t in range(max(0,j-(n-w)), min(j,w)+1))

def transform(J,n,left,size):
    return {(i,j): Fraction(sum(c*K(left,i,a)*K(n-left,j,b) for (a,b),c in J.items()),size)
            for i in range(left+1) for j in range(n-left+1)}

def merge(J,n):
    return [sum(c for (a,b),c in J.items() if a+b==w) for w in range(n+1)]

def encode(J):
    return [[i,j,int(v)] for (i,j),v in sorted(J.items()) if v]

def control(n,left,rows):
    C=span(rows)
    assert len(C)==2**len(rows)
    dual={v for v in range(1<<n) if all((v&r).bit_count()%2==0 for r in rows)}
    J=joint(C,n,left); direct=joint(dual,n,left)
    trans=transform(J,n,left,len(C))
    assert all(v.denominator==1 and v>=0 for v in trans.values())
    assert all(trans[k]==direct[k] for k in trans)
    assert sum(trans.values())==len(dual)==2**n//len(C)
    back=transform(trans,n,left,len(dual))
    assert all(back[k]==J[k] for k in back)
    ordinary=[Fraction(sum(c*K(n,w,a+b) for (a,b),c in J.items()),len(C)) for w in range(n+1)]
    assert ordinary==merge(trans,n)==[sum(v.bit_count()==w for v in dual) for w in range(n+1)]
    changed=rows[:];changed[0]^=changed[1]
    assert span(changed)==C
    swapped={(b,a):c for (a,b),c in J.items()}
    sw=transform(swapped,n,n-left,len(C))
    assert all(sw[j,i]==trans[i,j] for i,j in trans)
    wrong=transform(J,n,left,2*len(C))
    assert wrong[0,0]==Fraction(1,2) and wrong!=trans
    # A coordinate permutation within each block preserves joint counts.
    def swap_bits(v,i,j):
        if ((v>>i)^(v>>j))&1: v^=(1<<i)|(1<<j)
        return v
    perm={swap_bits(swap_bits(v,0,left-1),left,n-1) for v in C}
    assert joint(perm,n,left)==J
    return {'length':n,'dimension':len(rows),'left_block_low_bits':left,
            'rows_msb_first':[format(r,f'0{n}b') for r in rows],
            'code_size':len(C),'dual_size':len(dual),
            'min_distance':min(v.bit_count() for v in C if v),
            'joint':encode(J),'dual_joint':encode(direct),
            'all_split_cells_checked':len(trans),'ordinary_dual':list(map(int,ordinary)),
            'checks':['direct dual enumeration','normalization','ordinary merge','involution','basis change','block swap','within-block permutation','wrong divisor rejected']}

def main():
    source_rows=['10000111','01001011','00101101','00011110']
    # Reverse display strings so their first three coordinates become low-order bits.
    reply=control(8,3,[int(row[::-1],2) for row in source_rows])
    reply['source_rows_left_to_right']=source_rows
    reply['source_split']='First three displayed coordinates versus last five; reversed into low-bit convention.'
    cases=[reply,control(6,2,[0b001011,0b110010])]
    return {'controls':cases,'split_cells_total':sum(x['all_split_cells_checked'] for x in cases),
            'scope':'Finite controls validate these transform implementations; not a target code or proof of branch infeasibility.'}
if __name__=='__main__':print(json.dumps(main(),indent=2))
