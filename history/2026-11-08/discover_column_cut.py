#!/usr/bin/env python3
"""Optional <=60-second numerical proposal search; exact checker is the proof.

Requires already-installed NumPy/SciPy. Does not install software or publish.
Solver-selected tuples may vary by version. Only exact nonnegative row slacks
are accepted as formal points. Solver infeasible/optimal statuses are not proof.
"""
from pathlib import Path
import csv
import json
import os
import time

os.environ.setdefault('OMP_NUM_THREADS','1')
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
os.environ.setdefault('MKL_NUM_THREADS','1')
import numpy as np
import scipy
from scipy.optimize import Bounds, LinearConstraint, milp

HERE=Path(__file__).resolve().parent
keys=['constant']+list('abcdefg')
rows=[[int(r[k]) for k in keys]
      for filename in ['domain_inequalities.csv','integer_coefficients.csv']
      for r in csv.DictReader((HERE/'inputs'/filename).open())]

def run(label,objective,extra,lower_d,upper_d):
    system=rows+extra
    A=np.asarray([r[1:] for r in system],dtype=float)
    constants=np.asarray([r[0] for r in system],dtype=float)
    scale=np.maximum(1,np.max(np.abs(A),axis=1))
    low=np.full(7,-np.inf); high=np.full(7,np.inf)
    low[3]=lower_d; high[3]=upper_d
    start=time.monotonic()
    result=milp(np.asarray(objective,dtype=float),integrality=np.ones(7),
                bounds=Bounds(low,high),
                constraints=LinearConstraint(A/scale[:,None],-constants/scale,np.inf),
                options={'time_limit':5,'mip_rel_gap':0.0})
    out={'label':label,'solver_status':int(result.status),
         'elapsed_seconds':time.monotonic()-start,
         'status_is_not_proof':True,'exact_accepted':False}
    if result.x is not None:
        u=[round(float(x)) for x in result.x]
        values=[r[0]+sum(c*v for c,v in zip(r[1:],u)) for r in system]
        if min(values)>=0 and lower_d<=u[3]<=upper_d:
            out.update(exact_accepted=True,point=u,minimum_integer_slack=min(values),
                       new_cut_slack=2*u[0]+u[3]-u[1]-2)
    return out

results=[run('formal_q_'+str(4*d),[0]*7,[],d,d) for d in range(4,8)]
results.append(run('seek_violation_even_with_zero_column_inclusion',
                   [2,-1,0,1,0,0,0],[[2,-1,0,0,1,0,0,0]],4,7))
print(json.dumps({'scipy_version':scipy.__version__,
                  'max_solver_calls':5,'seconds_per_call':5,
                  'results':results},indent=2))
