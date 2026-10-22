#!/usr/bin/env python3
"""Independent exact 64-point two-translate audit; no Boolean-function search.
Standard library only. Previous quadratic mask convention is reused, not re-enumerated.
"""
from itertools import combinations
from collections import Counter
import json, time

PAIRS=list(combinations(range(6),2))
def parity(x): return x.bit_count()&1
def quad(mask):
    return [sum(((x>>i)&1)*((x>>j)&1) for k,(i,j) in enumerate(PAIRS) if mask>>k&1)%2 for x in range(64)]
def walsh(bits):
    return [sum((-1 if bits[x]^parity(a&x) else 1) for x in range(64)) for a in range(64)]
def radical(mask):
    rows=[0]*6
    for k,(i,j) in enumerate(PAIRS):
        if mask>>k&1: rows[i]^=1<<j;rows[j]^=1<<i
    return [x for x in range(64) if all(parity(x&r)==0 for r in rows)]
def xor(a,b): return [x^y for x,y in zip(a,b)]
def margins_realizable(rows,cols):
    # Exhaustive per-row subsets for a 4x4 matrix; <=6^4 choices.
    def dfs(i,remaining):
        if i==4: return not any(remaining)
        for inds in combinations(range(4),rows[i]):
            new=list(remaining)
            for j in inds: new[j]-=1
            if all(0<=v<=3-i for v in new) and dfs(i+1,new): return True
        return False
    return dfs(0,list(cols))
def gale_ryser(rows,cols):
    rows=sorted(rows,reverse=True)
    return sum(rows)==sum(cols) and all(sum(rows[:k])<=sum(min(k,c) for c in cols) for k in range(1,5))

def main():
    start=time.process_time()
    hmask=513; qmask=19053
    h,q=quad(hmask),quad(qmask)
    hs=[h,xor(h,q)]
    radicals=[radical(hmask),radical(hmask^qmask)]
    assert radicals==[[0,16,32,48],[0,28,35,63]]
    assert radical(qmask)==[0]
    Wq_involution=walsh(q)
    assert set(map(abs,Wq_involution))=={8}
    # The circulant Walsh-convolution operator squares to identity.
    assert all(sum(Wq_involution[b]*Wq_involution[a^b] for b in range(64))==(4096 if a==0 else 0) for a in range(64))
    assert set(radicals[0])&set(radicals[1])=={0}
    rs=sorted({r^s for r in radicals[0] for s in radicals[1]})
    reps=[]; covered=set()
    for x in range(64):
        if x not in covered: reps.append(x);covered.update(x^v for v in rs)
    assert len(reps)==4
    controls=[('zero',[0]*64),('delta0',[int(x==0) for x in range(64)]),
              ('previous_radius15',[h[x]^(((x>>4)&1)*((x>>5)&1))^int(x==48) for x in range(64)]),
              ('cubic_odd',[((x&1)*((x>>1)&1)*((x>>2)&1))^int(x==17) for x in range(64)])]
    results=[]
    for name,f in controls:
        W0=walsh(f); W1=walsh(xor(f,q)); Wq=walsh(q)
        # Product/convolution identity, all 64 frequency coordinates.
        assert all(64*W1[a]==sum(W0[b]*Wq[a^b] for b in range(64)) for a in range(64))
        # Twisted affine-support projection, denominator 64 on the left.
        t=[1-2*(f[x]^h[x]) for x in range(64)]
        for i,(hi,R,W) in enumerate(zip(hs,radicals,[W0,W1])):
            Wh=walsh(hi);support=[a for a in range(64) if Wh[a]]
            assert len(support)==16
            for x in range(64):
                lhs=(1-2*hi[x])*sum(W[a]*(-1 if parity(a&x) else 1) for a in support)
                rhs=16*sum(t[x^r] for r in R)
                assert lhs==rhs
        # One grid per R+T coset, genuine common error bits, no sign ambiguity.
        for c in reps:
            grid=[[f[c^r^s]^h[c^r^s] for s in radicals[1]] for r in radicals[0]]
            rows=list(map(sum,grid)); cols=[sum(grid[i][j] for i in range(4)) for j in range(4)]
            assert gale_ryser(rows,cols) and margins_realizable(rows,cols)
        results.append({'name':name,'weight':sum(f),'distance_from_h':sum(xor(f,h)),
                        'max_abs_W0':max(map(abs,W0)),'max_abs_Wq':max(map(abs,W1))})
    # Local margin controls only: these are NOT spectra satisfying target constraints.
    margin_controls=[([4,4,0,0],[4,2,2,0],False),([4,4,0,0],[2,2,2,2],True),([3,2,1,0],[3,2,1,0],True)]
    for rows,cols,expected in margin_controls:
        assert gale_ryser(rows,cols)==margins_realizable(rows,cols)==expected
    # Independently check every translated spectrum of yesterday's explicit control.
    basis=[19053,24003,9757]; masks=[0]
    for m in basis: masks += [v^m for v in masks]
    old=controls[2][1]
    maxima=[max(map(abs,walsh(xor(old,quad(m))))) for m in masks]
    assert maxima[0]==10 and any(m>10 for m in maxima[1:])
    out={'status':'PASS','date':'2026-10-22','source_commit':'36760bd352596dfa5fb4865f8dee3dd0d70441c0',
         'reused_quadratic_basis_masks':basis,'hmask':hmask,'qmask':qmask,'radicals':radicals,
         'grid_component_representatives':reps,'controls':results,'convolution_coordinates_checked':256,'involution_shift_coordinates_checked':64,
         'signed_projection_coordinates_checked':512,'genuine_grids_checked':16,
         'local_margin_controls':[{'rows':r,'cols':c,'realizable':e} for r,c,e in margin_controls],
         'previous_radius15_eight_spectrum_maxima':maxima,
         'scope':'Exact identities and tiny controls only. No new exclusion of the seven aggregate profiles, no fixed-E feasibility decision, no global nonexistence or novelty claim.',
         'cpu_seconds':round(time.process_time()-start,4)}
    print(json.dumps(out,indent=2))
if __name__=='__main__':main()
