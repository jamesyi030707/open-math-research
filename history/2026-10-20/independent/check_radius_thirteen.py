#!/usr/bin/env python3
"""Exact inverse-Walsh obstruction for all 136 rank-four r=13 profiles.
Representative h=x0*x1+x2*x3; generic proof in accompanying supplement.
"""
from itertools import combinations
from pathlib import Path
import json
from check_quadratic_neighborhood import fwht

def main():
 h=[((x&1)*((x>>1)&1))^(((x>>2)&1)*((x>>3)&1)) for x in range(64)]
 signs=[1-2*v for v in h]; W=fwht(signs)
 S=[a for a,v in enumerate(W) if v]
 assert len(S)==16 and {abs(W[a]) for a in S}=={16}
 eps=[v//16 for v in W]
 records=[]
 for defects in [[(a,8)] for a in S]+[[(a,4),(b,4)] for a,b in combinations(S,2)]:
  candidate=[10*e for e in eps]
  for a,delta in defects:candidate[a]-=delta*eps[a]
  assert sum(e*v for e,v in zip(eps,candidate))==152
  numerators=fwht(candidate)
  # Each inverse value is numerator/64; a signed four-point mean
  # is a half-integer, requiring numerator divisible by 32.
  bad=[x for x,v in enumerate(numerators) if v%32]
  assert bad
  if len(defects)==1:assert len(bad)==24
  else:assert len(bad)>=32
  records.append({'defects':defects,'invalid_inverse_positions':len(bad),'inverse_numerators':sorted(set(numerators))})
 out={'status':'PASS','date':'2026-10-20','single_defect_profiles':16,'double_defect_profiles':120,'profiles_passing_signed_fiber_integrality':0,'profiles':records,'scope':'Representative numerical check supplements the generic rank-four argument. No search over f and no global nonexistence claim.'}
 Path(__file__).with_name('radius_thirteen_report.json').write_text(json.dumps(out,indent=2)+'\n')
 print('PASS: all 136 possible rank-four r=13 restricted spectra violate signed fiber integrality.')
if __name__=='__main__':main()
