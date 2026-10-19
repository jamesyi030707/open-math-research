#!/usr/bin/env python3
"""Exact, standard-library audit of fixed E Walsh/autocorrelation restrictions.
No solver, third-party package, remote write, or full feasibility search.
"""
from collections import Counter
from functools import reduce
from itertools import combinations
from pathlib import Path
from random import Random
import hashlib, json, time


def fwht(a):
    a=list(a); step=1
    while step<len(a):
        for start in range(0,len(a),2*step):
            for j in range(start,start+step):
                u,v=a[j],a[j+step]; a[j],a[j+step]=u+v,u-v
        step*=2
    return a


def codewords():
    # Independent coefficient-array convolution, not imported generator code.
    exponents=[0,2,3,5,6,12,14,16,18,19,20,22,24,26,27,29,33,34,37,40,43,44,46,48,49,50,53]
    assert sum(1<<e for e in exponents)==0x2759262d5d506d
    words=[]
    for m in range(1024):
        bits=[0]*64
        for j in range(10):
            if (m>>j)&1:
                for e in exponents: bits[e+j]^=1
        bits[63]=sum(bits[:63])%2
        words.append(sum(b<<i for i,b in enumerate(bits)))
    return set(words)


def extend(basis,span,candidates):
    for w in sorted(candidates):
        if w not in span:
            basis.append(w); span.update([w^v for v in span])
    return basis,span


def anf_degree(bits):
    coeff=list(bits)
    for j in range(6):
        for x in range(64):
            if x&(1<<j): coeff[x]^=coeff[x^(1<<j)]
    return max((x.bit_count() for x,c in enumerate(coeff) if c),default=-1)


def autocor(signs,a):
    return sum(signs[x]*signs[x^a] for x in range(64))


def main():
    start=time.process_time(); E=codewords(); one=(1<<64)-1
    assert len(E)==1024
    rm={w for w in E if w.bit_count() in (0,32,64)}
    assert len(rm)==128 and all(x^y in rm for x in rm for y in rm)
    rb,span=extend([one],{0,one},rm)
    assert len(rb)==7 and span==rm
    labels=[sum(((rb[j+1]>>i)&1)<<j for j in range(6)) for i in range(64)]
    assert sorted(labels)==list(range(64))
    pos=[labels.index(x) for x in range(64)]
    eb,span=extend([],set(rm),E)
    assert len(eb)==3 and span==E
    qb=[[ (w>>pos[x])&1 for x in range(64)] for w in eb]
    assert [anf_degree(q) for q in qb]==[2,2,2]
    Q=[sum(qb[j][x]<<j for j in range(3)) for x in range(64)]
    qs=[[ (b&Q[x]).bit_count()%2 for x in range(64)] for b in range(8)]
    assert all(set(map(abs,fwht([1-2*v for v in q])))=={8} for q in qs[1:])
    fibers=[]
    for a in range(1,64):
        derivative=[Q[x]^Q[x^a]^Q[0]^Q[a] for x in range(64)]
        assert all(derivative[x^y]==derivative[x]^derivative[y] for x in range(64) for y in range(64))
        assert Counter(derivative)=={z:8 for z in range(8)}
        assert derivative[a]==0
        fibers.append([[x for x in range(64) if derivative[x]==z] for z in range(8)])
    # Fixed-code weight-four dual supports, built from the derivative fibers.
    blocks=set()
    for ai,a in enumerate(range(1,64)):
        for cell in fibers[ai]:
            pairs=[(x,x^a) for x in cell if x<(x^a)]
            assert len(pairs)==4
            for p,q in combinations(pairs,2): blocks.add(tuple(sorted(p+q)))
    direct=set()
    for x,y,z in combinations(range(64),3):
        w=x^y^z
        if w>z and Q[x]^Q[y]^Q[z]^Q[w]==0: direct.add((x,y,z,w))
    assert blocks==direct and len(blocks)==1008
    assert all(len(set(B))==4 and reduce(int.__xor__,B)==0
               and reduce(int.__xor__,[Q[x] for x in B])==0 for B in blocks)
    degrees=Counter(x for B in blocks for x in B)
    pairs=Counter(p for B in blocks for p in combinations(B,2))
    assert degrees=={x:63 for x in range(64)}
    assert len(pairs)==2016 and set(pairs.values())=={3}
    # Structural derivative rank check is exhaustive over this entire fixed code.
    # The identity audit below uses fixed controls plus deterministic random f.
    rng=Random(20261019)
    samples=[1,0x172e5cb972e5cb96,0x9d6498b57541b400]
    for _ in range(1):
        w=rng.getrandbits(64)
        if w.bit_count()%2==0: w^=1
        samples.append(w)
    total_fourth_residues=set(); single_fourth_residues=set(); design_checks=[]
    for w in samples:
        f=[(w>>pos[x])&1 for x in range(64)]
        assert sum(f)%2==1
        spectral_moment=0; total_nonzero_energy=0
        autoc=[]
        for q in qs:
            signs=[1-2*(f[x]^q[x]) for x in range(64)]
            W=fwht(signs); A=[autocor(signs,a) for a in range(64)]
            assert sum(v*v for v in W)==4096
            assert all(v%4==2 for v in W)
            assert all(v%8==4 for v in A[1:])
            fourth=sum(v**4 for v in W)
            assert fourth==64*sum(v*v for v in A)
            assert fourth%8192==7168
            single_fourth_residues.add(fourth%8192)
            spectral_moment+=fourth
            total_nonzero_energy+=sum(v*v for v in A[1:]); autoc.append(A)
        assert total_nonzero_energy%256==128
        assert spectral_moment%16384==8192
        V=sum(sum(f[x] for x in B)%2 for B in blocks)
        assert V%4==3
        assert spectral_moment==6225920+12288*(1008-2*V)
        assert spectral_moment==8*154624+6144*(2828-4*V)
        assert (2828-4*V)%16==0
        design_checks.append({'f_hex':hex(w),'weight':sum(f),'odd_intersection_blocks':V,
                              'formal_fourth_moment_C':2828-4*V,
                              'note':'C is a true magnitude-10 count only if all eight spectra obey the target bound.'})
        total_fourth_residues.add(spectral_moment%16384)
        signs=[1-2*v for v in f]
        for ai,a in enumerate(range(1,64)):
            S=[sum(signs[x]*signs[x^a] for x in cell) for cell in fibers[ai]]
            assert all(v%4==0 for v in S)
            assert sum(v//4 for v in S)%2==1
            assert sum(autoc[b][a]**2 for b in range(8))==8*sum(v*v for v in S)
            assert sum(autoc[b][a]**2 for b in range(8))%256==128
    # The finite set of aggregate histograms remaining after the new congruence.
    before=[{'t':t,'x':224+4*t,'y':288-12*t,'z':8*t} for t in range(25)]
    after=[r for r in before if r['x']%16==0]
    single=[]
    for c in range(28,41):
        a,b=2*c-56,120-3*c
        fourth=16*a+1296*b+10000*c
        assert fourth==154624+6144*c
        if fourth%8192==7168: single.append({'abs2':a,'abs6':b,'abs10':c})
    assert [r['abs10'] for r in single]==[28,32,36,40]
    assert [r['t'] for r in after]==list(range(0,25,4))
    out={
      'status':'PASS', 'date_utc':'2026-10-19',
      'code_size':len(E),'rm_size':len(rm),
      'rm_basis_hex':[hex(w) for w in rb],
      'quadratic_quotient_basis_hex':[hex(w) for w in eb],
      'quadratic_degrees':[anf_degree(q) for q in qb],
      'derivative_rank_three_nonzero_shifts':63,
      'derivative_linearity_pairs_checked':63*64*64,
      'fibers_per_shift':8,'points_per_fiber':8,'unordered_pairs_per_fiber':4,
      'odd_vectors_identity_audited':len(samples),'spectra_identity_audited':len(samples)*8,
      'single_fourth_moment_mod8192':sorted(single_fourth_residues),
      'total_fourth_moment_mod16384':sorted(total_fourth_residues),
      'single_spectrum_allowed_histograms':single,
      'aggregate_histograms_before':before,
      'aggregate_histograms_after_mod16':after,
      'removed_t_values':[r['t'] for r in before if r['x']%16],
      'weight_four_dual_blocks':len(blocks),
      'independent_triple_enumeration_matches_blocks':True,
      'design_vertex_degree':63,'design_pair_degree':3,
      'design_vertex_checks':len(degrees),'design_pair_checks':len(pairs),
      'odd_vector_design_identity_checks':design_checks,
      'solver_installed':False,'solver_invoked':False,
      'full_model_status':'NOT DETERMINED',
      'claim_scope':'Necessary conditions only for this fixed E; no feasibility, global nonexistence, or novelty claim.',
      'cpu_seconds':round(time.process_time()-start,4),
    }
    path=Path(__file__).with_name('structural_moments_report.json')
    path.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))

if __name__=='__main__': main()
