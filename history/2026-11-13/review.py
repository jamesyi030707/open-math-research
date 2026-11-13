"""Separately written integer review of two labeled W non-extension certificates.
Python standard library; no solver, target-matrix enumeration, or external files.
"""
import json
from collections import Counter
B = (0x17e7146801,0x6293dc808,0xf714c2017,0x35dfc802d,0xb1f3485c,0x63e6a0ae,0x65be14f,0x196fc233,0x3e690ce6,0xcb73897)
COLUMNS = (
 (40,9,10,11,12,13,14,15,48,17,18,19,20,21,22,23,56,25,26,27,28,29,30,31,32,0,0),
 (8,41,42,43,44,45,46,47,16,49,50,51,52,53,54,55,24,57,58,59,60,61,62,63,32,32,32))
T=(6,15,20,28,39,46,53,61)
COEFF=((-1,-1,1,1,-1,-1,1,1),(-1,-1,1,1,1,1,-1,-1))
def need(v,msg):
 if not v: raise RuntimeError(msg)
def word(rows,u):
 result=0
 for row in rows:
  if u&1: result ^= row
  u >>= 1
 return result
def rows_from_columns(cols):
 return [sum(((v>>bit)&1)<<j for j,v in enumerate(cols)) for bit in range(6)]
def W(t): return ((t%32)<<4) ^ (1008 if t>=32 else 0)
def check(cols,coeff):
 rows=rows_from_columns(cols)
 signed=[0]*27
 for t,c in zip(T,coeff):
  bits=word(rows,t)
  for j in range(27): signed[j] += c*(1-2*((bits>>j)&1))
 return signed == [8 if j==12 else 0 for j in range(27)] and sum(coeff)==0
out=[]
for cols,coeff in zip(COLUMNS,COEFF):
 rows=rows_from_columns(cols)
 code=[word(rows,t) for t in range(64)]
 need(len(set(code))==64,'rank six')
 weights=[v.bit_count() for v in code]
 need(all(weights[t] in (12,16) for t in range(64) if t not in (0,32)),'W windows')
 need(weights[32] in (4,24),'h weight')
 need(all(word(B,2^W(t)).bit_count()==14 for t in T),'forced residual weight')
 need(check(cols,coeff),'integer certificate')
 bad=list(coeff);bad[0]*=-1
 need(not check(cols,bad),'damaged certificate must fail')
 # For actual outside offsets, directly check the weighted character sum
 # equals 8 times its isolated coordinate. These are real affine models,
 # not attempted full residual lifts.
 for offset in (0,1,1<<12,(1<<27)-1,0x5555555):
  left=sum(c*(27-2*(offset^code[t]).bit_count()) for t,c in zip(T,coeff))
  right=8*(1-2*((offset>>12)&1))
  need(left==right,'real affine offset identity')
 out.append({'h_weight':weights[32],'rank':6,'weight_distribution':dict(sorted(Counter(weights).items())),
             'messages':[2^W(t) for t in T],'coefficients':coeff,'isolated_column_1based':13,
             'certificate_passed':True,'damaged_certificate_rejected':True,'affine_offset_controls':5})
# Independently correct and check the small control printed in the reply.
small=(4,2,7,1,3)
w=[sum((u&v).bit_count()%2 for v in small) for u in range(8)]
need(w==[0,3,3,2,2,3,3,4],'reply control vector')
need(sum(w[u] for u in (0,2,4,6))==8,'base sum')
need(sum(w[u] for u in (1,3,5,7))==12,'coset sum')
w[3]=4;need(sum(w[u] for u in (1,3,5,7))==14,'negative control')
print(json.dumps({'status':'PASS','scope':'Only the two specified labeled W restrictions; no q28/full branch exclusion',
                  'controls':out,'reply_control_corrected':True},indent=2))
