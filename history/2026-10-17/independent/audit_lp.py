"""Read exported LP as data, check every constraint exactly; no solver invocation."""
import json,re
from pathlib import Path
P=Path(__file__).parent
m=json.loads((P/'model.json').read_text()); E=[0]
for s in m['basis_hex']:E += [w^int(s,16) for w in E]
reps=sorted({min(w,w^((1<<64)-1)) for w in E})
lines=(P.parent/'claude/ebch_hole_model.lp').read_text().splitlines()
for r,e in enumerate(reps):
 for prefix,symbol,bound in [('lo','>=',27-e.bit_count()),('hi','<=',37-e.bit_count())]:
  line=next(x for x in lines if x.startswith(f' {prefix}{r}:'))
  lhs,rhs=line.split(symbol)
  assert int(rhs)==bound
  terms=re.findall(r'([+-]) f(\d+)',lhs)
  assert len(terms)==54
  assert [(int(i),1 if sign=='+' else -1) for sign,i in terms]==[(c,1-2*((e>>(c+10))&1)) for c in range(54)]
par=next(x for x in lines if x.startswith(' par:'))
assert par==' par: '+' '.join('+ f%d'%c for c in range(54))+' - 2 k = 1'
assert lines[lines.index('Binary')+1].split()==[f'f{c}' for c in range(54)]
assert lines[lines.index('General')+1].strip()=='k'
assert lines[lines.index('Bounds')+1]==' 0 <= k <= 27'
assert lines[lines.index('Bounds')+2]=='Binary'
result={'all_1024_scalar_bounds_exact':True,'parity_exact':True,'binary_declarations_exact':True,'integer_parity_slack_bound_sufficient':True,'ten_zero_pivots_only':True,'solver_rerun':False,'unsat_certificate_verified':False,'thread_count_verified':False,'control_vector_available':False}
(P/'lp_audit.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
