"""Reproduce stored results; reject deliberately altered output certificates."""
import subprocess,json,copy
from pathlib import Path
R=Path(__file__).resolve().parent

def normalized(d):
 d=copy.deepcopy(d); d.pop('cpu_seconds',None);return d

def check(actual,expected):
 if normalized(actual)!=normalized(expected):raise ValueError('certificate mismatch')
reports={}
for name,stored in [('multiplicity','result'),('independent_audit','independent_result')]:
 expected=json.loads((R/(stored+'.json')).read_text())
 for flags in ([],['-O']):
  actual=json.loads(subprocess.check_output(['python',*flags,str(R/(name+'.py'))],timeout=60))
  check(actual,expected)
 reports[name]=normalized(actual)
for a,b in [('local_markings','canonical_patterns'),('translations_checked','translation_moment_checks'),('uniform_q24_exclusions','E_count'),('overlap_with_nov17_explicit_q24_set','overlap_with_Nov17_explicit_set')]:
 if reports['multiplicity'][a]!=reports['independent_audit'][b]:raise ValueError('independent mismatch')
check(json.loads((R/'independent_optimized.json').read_text()),reports['independent_audit'])
bad=copy.deepcopy(reports['multiplicity']);bad['uniform_q24_exclusions']+=1
try:check(bad,reports['multiplicity'])
except ValueError:rejected=True
else:raise ValueError('tampered count accepted')
print(json.dumps({'passed':True,'normal_optimized_and_stored_agree':True,'independent_core_counts_agree':True,'altered_output_count_rejected':rejected,'note':'tamper check tests output certificate comparison, not a replacement for mathematical proof','uniform_covered':69440,'overlap':7,'additional_to_nov17_set':69433},indent=2))
