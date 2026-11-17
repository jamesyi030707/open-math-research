"""Re-run current proofs in two modes, compare complete transported signatures."""
import subprocess,json,hashlib,gzip
from pathlib import Path
R=Path(__file__).resolve().parent
reports={}
for name in ('transvections','stabilizer','transport','independent_stabilizer','independent_transport'):
 outputs=[]
 for flags in ([],['-O']):
  r=json.loads(subprocess.check_output(['python',*flags,str(R/(name+'.py'))],timeout=60))
  r.pop('cpu_seconds',None); outputs.append(r)
 if outputs[0]!=outputs[1]:raise ValueError(name+' optimization mismatch')
 reports[name]=outputs[0]
r=reports['transport'];i=reports['independent_transport']
lines='\n'.join(','.join(map(str,c['columns'])) for c in r['transported'])+'\n'
if hashlib.sha256(lines.encode()).hexdigest()!=i['distinct_patterns_sha256']:raise ValueError('full pattern mismatch')
if reports['stabilizer']['group_order']!=1:raise ValueError('group')
print(json.dumps({'normal_optimized_agree':list(reports),'full_pattern_digest':i['distinct_patterns_sha256'],'distinct_patterns':i['distinct_restrictions'],'weight_pairs':i['verified_weight_pairs'],'passed':True},indent=2))
