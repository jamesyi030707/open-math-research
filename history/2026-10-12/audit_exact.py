#!/usr/bin/env python3
"""Independent exact audit. No generator imports; no large J scans.
H is certified by integer power inequalities at H,H+1. Forward brute force,
reverse with both prunes, and supplied C are compared. J92 anchor tails and
certificate entries only are checked, not the full J92 domain.
"""
import json, subprocess, time, hashlib
from pathlib import Path
P=Path(__file__).resolve().parent

def step(x): return (3*x+1)//2 if x&1 else x//2

def params(J):
    Q=[0]; H=[0]
    for j in range(1,J+1):
        q=0
        while 3**(q+1)<1<<j:q+=1
        Q.append(q)
        if not q: H.append(0);continue
        def yes(h):return (3*h+1)**q >= (1<<j)*h**q
        a,b=0,1
        while yes(b):a,b=b,b*2
        while b-a>1:
            m=(a+b)//2
            if yes(m):a=m
            else:b=m
        assert yes(a) and not yes(a+1)
        H.append(a)
    return Q,H

def reverse(J,H,Q,prune=True):
    hits=[];cands=[];seen=set();nodes=0;cut1=0;cut2=0;maxv=0
    for root in range(3,H+1,2):
        a=[root];odd=[0]
        for _ in range(J):odd.append(odd[-1]+(a[-1]&1));a.append(step(a[-1]))
        caps=[0]
        for x in a[1:]:caps.append(max(caps[-1],x))
        ohi=Q[J]-1
        stack=[(root,0,0)]
        while stack:
            n,d,o=stack.pop();nodes+=1;maxv=max(maxv,n)
            assert n not in seen,('duplicate candidate node',n,root,d)
            seen.add(n)
            if n<=caps[J-d]:
                cands.append(n)
                for t in range(1,J-d+1):
                    if n<=a[t] and o+odd[t]<=Q[d+t]:hits.append((n,d+t,o+odd[t]))
            if d==J-1:continue
            preds=[(2*n,o)]
            if n%3==2 and (2*n-1)//3>H:preds.append(((2*n-1)//3,o+1))
            for v,no in preds:
                dd=d+1
                if prune:
                    if no>ohi:cut1+=1;continue
                    r=min(J-1-dd,ohi-no)
                    if (v+1)*2**r > (caps[J-dd]+1)*3**r:cut2+=1;continue
                stack.append((v,dd,no))
    return sorted(hits),dict(nodes=nodes,candidates=len(cands),cut_P1=cut1,cut_P2=cut2,max_node=maxv)

def brute(J,H):
    X=2
    for root in range(3,H+1,2):
        x=root;X=max(X,x)
        for _ in range(J):x=step(x);X=max(X,x)
    hits=[]
    for n in range(3,X+1):
        x=n;q=0
        for j in range(1,J+1):
            q+=x&1;x=step(x)
            if 3**q<1<<j and x>=n:hits.append((n,j,q))
    return X,hits

def main():
    start=time.monotonic(); log=[]
    compile_result=subprocess.run(['cc','-O2','-Wall','-Wextra','-o',str(P/'audit_inverse'),str(P/'inverse_orbit.c')],capture_output=True,text=True,check=True)
    log.append('Compiler stderr: '+compile_result.stderr)
    cert=json.loads((P/'baseline_paradox_cert_J92.json').read_text()); results=[]
    for J in [1,2,5,8,12,20,27,35,46]:
        Q,hs=params(J);H=max(hs);X,expected=brute(J,H)
        got,metrics=reverse(J,H,Q)
        assert got==expected
        assert expected==[tuple(h) for h in cert['hits'] if h[1]<=J]
        if J<=20:
            raw,rawmetrics=reverse(J,H,Q,False)
            assert raw==got
            metrics['unpruned_nodes']=rawmetrics['nodes']
        qfile=P/f'audit_qmax_J{J}.txt';qfile.write_text('\n'.join(map(str,Q[1:]))+'\n')
        out=P/f'audit_hits_J{J}.txt'
        c=subprocess.run([str(P/'audit_inverse'),str(J),str(H),str(qfile),'10000000','30',str(out)],capture_output=True,text=True,check=True)
        log.append(c.stdout)
        cg=sorted(tuple(map(int,line.split())) for line in out.read_text().splitlines())
        assert cg==got
        assert f'nodes={metrics["nodes"]} ' in c.stdout
        assert f'leaf_tests={metrics["candidates"]} ' in c.stdout
        results.append(dict(J=J,Hmax=H,X=X,hits=len(got),C_equal=True,forward_equal=True,baseline_subset_equal=True,**metrics))
    Q,H=params(92)
    assert Q[1:]==cert['qmax'] and H[1:]==cert['H'] and max(H)==cert['Hmax']
    max_tail=0
    for root in range(3,max(H)+1,2):
        x=root
        for _ in range(92):x=step(x);max_tail=max(max_tail,x)
    assert max_tail==cert['X']
    assert len(set(tuple(h) for h in cert['hits']))==len(cert['hits'])
    for n,j,q in cert['hits']:
        x=n;actualq=0;anchor=None
        for d in range(j):
            if anchor is None and x%2 and 3<=x<=max(H):anchor=(x,d)
            actualq+=x&1;x=step(x)
        assert anchor is not None and actualq==q and 3**q<1<<j and x>=n
    summary={'cases':results,'J92_certificate_entry_checks':len(cert['hits']),'J92_unique_starts':len(set(h[0] for h in cert['hits'])),'J92_anchor_max_tail':max_tail,'J92_full_scan_performed':False,'elapsed_s':time.monotonic()-start,'source_sha256':hashlib.sha256((P/'inverse_orbit.c').read_bytes()).hexdigest()}
    (P/'audit_results.json').write_text(json.dumps(summary,indent=2)+'\n');(P/'audit_run.log').write_text('\n'.join(log));print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
