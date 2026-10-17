"""Optional bounded MILP runner. Solver infeasibility is NOT a proof certificate.
Run model_check.py first. Uses scipy >=1.9, NumPy, HiGHS.
This runner is supplied for reproduction; its execution is not asserted.
"""
import json,resource,time
from pathlib import Path
import numpy as np
import scipy
from scipy.optimize import milp,Bounds,LinearConstraint
P=Path(__file__).parent
model=json.loads((P/'model.json').read_text())
A=np.array(model['forms'],dtype=np.int64)
M=np.zeros((513,65),dtype=np.float64);M[:512,:64]=A
M[512,:64]=1;M[512,64]=-2
lo=np.r_[(A.sum(axis=1)-10)//2,1]
hi=np.r_[(A.sum(axis=1)+10)//2,1]
lb=np.zeros(65);ub=np.r_[np.ones(64),31];ub[63]=0
resource.setrlimit(resource.RLIMIT_CPU,(120,120))
t=time.process_time()
r=milp(np.zeros(65),integrality=np.ones(65),bounds=Bounds(lb,ub),constraints=LinearConstraint(M,lo,hi),options={'time_limit':115,'disp':True,'threads':1})
out={'scipy':scipy.__version__,'status':int(r.status),'message':r.message,'cpu_seconds':time.process_time()-t,'proof_certificate':False}
if r.x is not None:
 x=np.rint(r.x).astype(np.int64)
 assert np.max(np.abs(r.x-x))<1e-5
 assert np.all(M@x>=lo) and np.all(M@x<=hi)
 f=sum(int(x[j])<<j for j in range(64));E=[0]
 for b in model['basis_hex']:E += [e^int(b,16) for e in E]
 d=min((f^e).bit_count() for e in E)
 assert f.bit_count()%2==1 and d>=27
 out.update(candidate=f'{f:016x}',exact_distance=d)
(P/'solver_result.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out))
