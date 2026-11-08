import json,time
import numpy as np
from scipy.optimize import milp,Bounds,LinearConstraint
from affine_split import make_table

F=np.array([[1,0,0,0,0,0,0,0],[4,64,-16,0,4,-4,-6,-6],[0,0,0,0,4,0,0,0],[6,0,0,8,-4,2,0,2],[-4,0,16,-16,0,-4,0,-4],[0,0,0,0,0,0,2,1],[0,0,0,0,0,2,0,1],[0,0,0,0,0,0,0,1]],dtype=object)
T=make_table()
rows=[]
for row in T.values():
    out=np.array(row,dtype=object)@F
    assert all(v%1024==0 for v in out)
    rows.append([int(v//1024) for v in out])
D=[[0,1,0,0,0,0,0,0],[80,-1,0,0,0,0,0,0],[0,0,1,0,0,0,0,0],[31,0,-1,0,0,0,0,0],[0,0,0,1,0,0,0,0],[0,0,0,0,1,0,0,0],[160,0,0,-1,-1,0,0,0],[0,0,0,0,0,1,0,0],[0,0,0,0,0,0,1,0],[0,0,0,0,0,0,0,1],[80,0,0,0,0,-1,-1,-1]]
rows += [[int(v) for v in np.array(r,dtype=object)@F] for r in D]
arr=np.array(rows,float); scale=np.maximum(1,np.max(abs(arr[:,1:]),axis=1))
results=[]
for q in [16,20,24,28]:
    lb=np.full(7,-np.inf);ub=np.full(7,np.inf);lb[3]=ub[3]=q//4
    t=time.monotonic()
    res=milp(np.zeros(7), integrality=np.ones(7), bounds=Bounds(lb,ub),constraints=LinearConstraint(arr[:,1:]/scale[:,None],-arr[:,0]/scale,np.inf),options={'time_limit':10,'mip_rel_gap':0.0})
    r={'q':q,'status':res.message,'seconds':time.monotonic()-t}
    if res.x is not None:
        u=[round(v) for v in res.x];x=[int(v) for v in F@np.array([1]+u,dtype=object)]
        slacks=[row[0]+sum(a*b for a,b in zip(row[1:],u)) for row in rows]
        assert min(slacks)>=0 and x[2]==q
        numer=[sum(a*b for a,b in zip(row,x)) for row in T.values()]
        assert all(v>=0 and v%1024==0 for v in numer)
        r.update(u=u,x=x[1:],exact_min_slack=min(slacks),zero_slacks=slacks.count(0),checked_rows=len(slacks))
    results.append(r)
print(json.dumps(results,indent=2))
