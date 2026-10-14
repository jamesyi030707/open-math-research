#!/usr/bin/env python3
"""Small exact Collatz leaf filter reference; no orbit-tree enumeration.

Original discussion: archive history/2026-10-13/exact_pruning_proof.txt.
This newly written function does not patch or certify the historical C code.
"""
import json
import time


def first_admissible_odd_count(a, d, H, tail_value, hi):
    """Return minimum o in [0,hi] with a*2^d*(H+1)^o <= V*(3H+4)^o.

    The caller must set hi=min(d,qmax[d+t]-Q[t]) to retain the odd budget.
    A return value is only a necessary envelope, never a hit certificate.
    """
    if any(type(x) is not int for x in (a,d,H,tail_value,hi)):
        raise TypeError('integer inputs required')
    if H < 5 or not (3 <= a <= H and a % 2) or d < 0 or tail_value < 1:
        raise ValueError('require H>=5, odd 3<=a<=H, d>=0, V>=1')
    if hi < 0:
        return None
    hi = min(hi,d)
    A, B = H+1,3*(H+1)+1
    def ok(o):
        return (a << d) * A**o <= tail_value * B**o
    if not ok(hi):
        return None
    low,high = 0,hi
    while low < high:
        mid = (low+high)//2
        if ok(mid):
            high=mid
        else:
            low=mid+1
    return low


def main():
    start=time.process_time()
    tests=0
    for H in (5,6,11,20):
        for a in range(3,H+1,2):
            for d in range(13):
                for V in (1,a,2*a,19,100,1000):
                    for hi in (-1,0,d//2,d,d+2):
                        A,B=H+1,3*(H+1)+1
                        expected=next((o for o in range(min(hi,d)+1)
                            if (a << d)*A**o <= V*B**o),None)
                        assert first_admissible_odd_count(a,d,H,V,hi)==expected
                        tests+=1
    # Inspect actual prefixes before their first small odd anchor.
    head_checks=0
    for H in (5,11,20):
        for n in range(3,513):
            v=n; o=0
            for d in range(25):
                if v%2 and 3<=v<=H:
                    A,B=H+1,3*(H+1)+1
                    assert (v << d)*A**o <= n*B**o
                    assert first_admissible_odd_count(v,d,H,n,o) is not None
                    head_checks+=1
                    break
                if v%2:
                    # Once v=1, there can be no future first anchor >=3.
                    if v==1:
                        break
                    assert v>H
                    o+=1
                    v=(3*v+1)//2
                else:
                    v//=2
    invalid=0
    for args in ((3,0,4,3,0),(2,0,5,3,0),(7,0,5,3,0),(3,-1,5,3,0),(3,0,5,0,0)):
        try:
            first_admissible_odd_count(*args)
        except ValueError:
            invalid+=1
    assert invalid==5
    print(json.dumps({'binary_vs_linear_cutoff_cases':tests,
      'actual_head_necessary_inequalities':head_checks,'domain_rejections':invalid,
      'arithmetic':'Python arbitrary-precision integers',
      'scope':'small function regression only; no new full inverse traversal or historical C certification',
      'cpu_seconds':time.process_time()-start},indent=2))


if __name__=='__main__':
    main()
