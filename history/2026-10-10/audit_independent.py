import json,pathlib,subprocess,hashlib,time
p=pathlib.Path(__file__).parent
c=json.loads((p/'claude_original/paradox_cert_J300.json').read_text())
# Pin every supplied cutoff by exact adjacent integer inequalities, not
# the generator's incremental search. Pin each bound by its two endpoints.
assert c['J']==300
for j,(q,h) in enumerate(zip(c['qmax'],c['H']),1):
 assert 3**q<2**j<=3**(q+1)
 if h:
  assert (3*h+1)**q >= 2**j*h**q
  assert (3*(h+1)+1)**q < 2**j*(h+1)**q
 else: assert q==0 or 4**q<2**j
assert len(c['qmax'])==len(c['H'])==300
assert max(c['H'])==c['Hmax']==6724
# Only finite 300-step excursions are needed for the all-n reduction.
peak=0
for m in range(3,6725,2):
 x=m
 for i in range(301):
  peak=max(peak,x)
  x=(3*x+1)//2 if x%2 else x//2
assert peak==c['X']==4076810
# Produce cutoffs independently through logarithm-free bit lengths.
cut=[sum(3**q<2**j for q in range(j+1))-1 for j in range(1,301)]
assert cut==c['qmax']
(p/'audit_qmax.txt').write_text('\n'.join(map(str,cut)))
subprocess.run(['gcc','-O2',str(p/'audit_independent.c'),'-o',str(p/'audit_independent')],check=True)
t=time.time();r=subprocess.run([str(p/'audit_independent'),str(p/'audit_qmax.txt')],capture_output=True,text=True,check=True)
(p/'audit_hits.txt').write_text(r.stdout)
got=[tuple(map(int,line.split())) for line in r.stdout.splitlines()]
expected=list(map(tuple,c['hits']))
assert len(set(expected))==len(expected)==593
assert sorted(got)==sorted(expected)
# Verify exact trajectories, CST finite consequence, and counts.
for n,j,q in got:
 x=n;s=0;tau=None;stop=None
 for k in range(1,j+1):
  s+=x%2;x=(3*x+1)//2 if x%2 else x//2
  if tau is None and 3**s<2**k:tau=k
  if stop is None and x<n:stop=k
 assert x>=n and s==q and tau==stop and stop<j
print('Exact q and H boundaries PASS; finite-excursion X bound PASS')
print(r.stderr.strip());print('All 593 certificate entries and completeness scan MATCH')
print('All listed hits have t(n)=tau(n)<j; 550 distinct starts:',len({a for a,_,_ in got})==550)
print('Wall seconds:',round(time.time()-t,3))
print('Certificate SHA256:',hashlib.sha256((p/'claude_original/paradox_cert_J300.json').read_bytes()).hexdigest())
