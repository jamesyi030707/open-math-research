"""Independent exact check of the local kernel-zero conditions; not a full lift."""
from pathlib import Path
from fractions import Fraction
from collections import Counter
import hashlib,json,time
start=time.process_time()
def need(x,why):
    if not x: raise ValueError(why)
raw=(Path(__file__).parent/'inputs/residual_candidate.json').read_bytes()
need(hashlib.sha256(raw).hexdigest()=='276170e9235104e8d671f4ce27eda47c25a0aee6b4dad310afae65c261f33d80','residual pin')
rows=[int(x,16) for x in json.loads(raw)['basis_hex']]
def enumerate_words(rows):
    words=[0]
    for row in rows: words += [x^row for x in words]
    return words
words=enumerate_words(rows); h=1008; S=[16*i for i in range(32)]
need(len(set(words))==1024,'residual rank')
need(h not in S and len(set(S+[s^h for s in S]))==64,'direct sum')
need(words[h].bit_count()==32,'heavy message')
need(all(words[s].bit_count()==words[s^h].bit_count()==16 for s in S[1:]),'residual W weights')
cases=[]
for q in (16,20,24,28):
    L=31-q//4; M=992-14*q-L*L; upper=Fraction(M-L,2)
    before=[]; after=[]
    for r in range(4,25,4):
        for z in range(28-L):
            qp=q+r//4-8*z
            P=Fraction(r*(28-r),32)+z*(L+z-28)
            if P.denominator!=1 or not (0<=P<=upper and 0<=qp<=31 and 0<=r-z<=L): continue
            record={'r':r,'z':z,'qprime':qp,'P':int(P)}
            before.append(record)
            if r-z!=1 and L-r+z!=1: after.append(record)
            # Independent character-square-sum identity, including s=0 and h.
            base=27**2+q*3**2+(31-q)*5**2
            shifted=(27-2*r)**2+qp*3**2+(31-qp)*5**2
            need(base-shifted==128*(P+z*(27-L-z)),'character identity')
    cases.append({'q':q,'L':L,'M':M,'before_xor':before,'after_xor':after})
need({v['r'] for v in cases[2]['before_xor']}=={4,8,20,24},'q24')
need({(v['r'],v['z']) for v in cases[3]['after_xor']}=={(4,1),(24,3)},'q28')
need(all({v['r'] for v in c['after_xor']}=={4,8,12,16,20,24} for c in cases[:2]),'q16 q20')
controls=[]
for complement in (False,True):
    special={8,16,24}
    cols=[v+32*int((v in special)!=complement) for v in range(8,32)]
    cols += [32,32,32] if complement else [32,0,0]
    Arows=[sum(((c>>j)&1)<<i for i,c in enumerate(cols)) for j in range(6)]
    aw=enumerate_words(Arows); wt=[w.bit_count() for w in aw]
    need(len(set(aw))==64 and len(cols)==27,'control rank and length')
    need(set(wt[1:32]+wt[33:])=={12,16},'control windows')
    r=wt[32]; q=wt[1:32].count(12); qp=wt[33:].count(12)
    counts=Counter(cols); m=Counter(c%32 for c in cols if c%32)
    L=sum(m.values()); M=sum(x*x for x in m.values()); z=counts[32]
    P=sum(counts[v]*counts[v+32] for v in range(1,32))
    need(q==28 and r in (4,24),'control parameters')
    need(qp==q+r//4-8*z,'control first moment')
    need(P==Fraction(r*(28-r),32)+z*(L+z-28) and P<=(M-L)//2,'control second moment')
    need(all(w%4==0 for w in wt),'control double even')
    for bit in (0,1):
        acc=0
        for c in cols:
            if c//32==bit: acc ^= c%32
        need(acc==0,'control selected label XOR')
    controls.append({'r':r,'z':z,'qprime':qp,'rank':6,'L':L,'M':M,'P':P,'weights':dict(Counter(wt))})
print(json.dumps({'status':'PASS','scope':'local W restrictions only, not rank10 A or target code','cases':cases,'controls':controls,'cpu_seconds':time.process_time()-start},indent=2))
