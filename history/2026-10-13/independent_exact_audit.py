#!/usr/bin/env python3
"""Independent Python integer DP/checker. No imports from Claude's code.
Budget: 60s overall, 1M DFS visits (J46 only); J92 path checks, no full DFS.
"""
from pathlib import Path
import json, hashlib, time, resource
P=Path(__file__).resolve().parent
start=time.monotonic()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def T(x):return (3*x+1)//2 if x%2 else x//2
def rows(name):return [tuple(map(int,l.split())) for l in (P/name).read_text().splitlines()]
def thresholds(a,J,H,q):
    values=[a];odds=[0]
    for _ in range(J):
        odds.append(odds[-1]+values[-1]%2);values.append(T(values[-1]))
    # Head product implies a*2^d <= n*(3+1/(H+1))^o.
    A=H+1;B=3*A+1;ap=[A**o for o in range(68)];bp=[B**o for o in range(68)]
    th=[[0]*68 for _ in range(J)]
    for d in range(J-1,-1,-1):
        leaf=[0]*67
        for t in range(1,J-d+1):
            hi=min(66,q[d+t]-odds[t])
            if hi<0:continue
            left=a<<d; right=values[t]
            if left*ap[hi]>right*bp[hi]:continue
            low=0;high=hi
            while low<high:
                mid=(low+high)//2
                if left*ap[mid]<=right*bp[mid]:high=mid
                else:low=mid+1
            for o in range(low,hi+1):leaf[o]=max(leaf[o],values[t]+1)
        for o in range(67):
            if d==J-1:th[d][o]=leaf[o]
            else:th[d][o]=max(leaf[o],th[d+1][o]*(4 if d==0 else 7)//(7 if d==0 else 13),3*th[d+1][o+1]//2)
    return values,odds,th
report={"method":"independent arbitrary-integer Python DP; J46 enumeration, J92 hit/path verification; no C execution"}
for J in [46,92]:
    cert=json.loads((P/f'paradox_cert_J{J}.json').read_text());H=cert['Hmax'];q=[0]
    for j in range(1,J+1):
        x=0
        while 3**(x+1)<2**j:x+=1
        q.append(x)
    assert q[1:]==cert['qmax']
    expected=set(map(tuple,cert['hits']))
    supplied=rows(f'theta_hits_m1_J{J}'+('_B' if J==92 else '')+'.txt')
    assert len(supplied)==len(set(supplied)) and set(supplied)==expected
    paths={}
    for n,j,odd_count in expected:
        orbit=[n];oq=[0]
        for _ in range(j):oq.append(oq[-1]+orbit[-1]%2);orbit.append(T(orbit[-1]))
        assert oq[-1]==odd_count and 3**odd_count<2**j and orbit[-1]>=n
        k=next(i for i,x in enumerate(orbit[:-1]) if x%2 and 3<=x<=H)
        a=orbit[k]
        for d in range(k+1):paths.setdefault(a,set()).add((d,oq[k]-oq[k-d],orbit[k-d]+1))
    got=[];candidates=[];node_count=0;essential_count=0;path_checks=0
    anchors=range(3,H+1,2) if J==46 else sorted(paths)
    for a in anchors:
        if time.monotonic()-start>60:raise RuntimeError('60s audit cap')
        v,odd,th=thresholds(a,J,H,q)
        for d,o,w in paths.get(a,[]):assert w<=th[d][o];path_checks+=1
        if J!=46:continue
        pm=[0]
        for x in v[1:]:pm.append(max(pm[-1],x))
        def visit(x,d,o):
            global node_count,essential_count
            node_count+=1
            if node_count>1000000:raise RuntimeError('DFS audit cap')
            found=False
            if x<=pm[J-d]:
                candidates.append(x)
                for t in range(1,J-d+1):
                    if x<=v[t] and o+odd[t]<=q[d+t]:got.append((x,d+t,o+odd[t]));found=True
            if d+1<J:
                children=[(2*x,o)]
                if x%3==2 and (2*x-1)//3>H:children.append(((2*x-1)//3,o+1))
                for child,co in children:
                    if co<=66 and child+1<=th[d+1][co]:found=visit(child,d+1,co) or found
            essential_count+=found
            return found
        if a+1<=th[0][0]:visit(a,0,0)
    result=dict(hit_triples=len(expected),distinct_starts=len({x[0] for x in expected}),hit_file_equals_baseline=True,all_hits_exactly_recomputed=True,exact_threshold_path_checks=path_checks)
    if J==46:
        assert set(got)==expected and len(got)==len(expected)
        assert candidates==[x[0] for x in rows('theta_cand_m1_J46.txt')]
        assert got==supplied
        assert node_count==199100 and essential_count==555
        result.update(exact_DFS_nodes=node_count,exact_candidates=len(candidates),essential_nodes=essential_count,ordered_hit_and_candidate_files_equal=True)
        (P/'independent_J46_hits.txt').write_text(''.join('%d %d %d\n'%r for r in got))
    report[f'J{J}']=result
old={x[0] for x in rows('theta_cand_m0_J72_B.txt')};new={x[0] for x in rows('theta_cand_m1_J72_B.txt')}
removed=sorted(old-new);assert new<=old
for n in removed:
    x=n;o=0
    for j in range(1,73):
        o+=x%2;x=T(x)
        assert not (3**o<2**j and x>=n)
report['J72_removed_candidates']=dict(values=removed,each_directly_verified_not_a_hit_through_J72=True)
report['source_sha256']=sha(P/'inverse_orbit_theta_claude_original.c')
report['runtime_s']=time.monotonic()-start
report['maxrss_kb']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
report['limits']='Original C cutoff still uses uncertified floating-point margin. Independent exact J46 completed. J92 traversal not rerun; its output and every known hit path verified. No novelty/global Collatz claim.'
(P/'independent_audit_results.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
