#!/usr/bin/env python3
"""Independent exact checker. No reducer/verifier imports; standard library only."""
import csv, hashlib, itertools, json
from pathlib import Path
root = Path(__file__).resolve().parent
p = root.parent / '2026-10-29' / 'affine_coefficients.csv'
c = json.loads((root / 'certificate.json').read_text())
sha = hashlib.sha256(p.read_bytes()).hexdigest()
assert sha == c['input_sha256'] == 'c49805f554e88c468d92d1835fb19f47480295a95eb32f5c18e53db05277323c'
cols = ['p','q','y10','y14','z8','z12','z16','constant']
assert c['columns'] == cols
assert (c['original_modulus'],c['common_divisor'],c['modulus']) == (1024,16,64)
rows = list(csv.DictReader(p.open()))
assert len(rows) == 1064
raw = [[int(r[k]) for k in cols] for r in rows]
assert all(int(r['denominator']) == 1024 for r in rows)
assert all(a % 16 == 0 for r in raw for a in r)
A = [[a // 16 % 64 for a in r] for r in raw]
B = c['basis']
expected = [[1,1,2,1,3,2,1,52],[0,8,8,4,0,0,0,32],
 [0,8,8,0,0,56,56,16],[0,16,0,0,32,0,32,0],
 [0,0,0,0,0,32,32,0],[0,0,0,0,32,0,32,0]]
assert B == expected
assert len(c['basis_from_input_sparse']) == 6
assert len(c['input_from_basis']) == 1064
# Verify every coordinate in each witness direction, including affine constant.
for i,w in enumerate(c['basis_from_input_sparse']):
    assert all(len(t) == 2 and 0 <= t[0] < 1064 for t in w)
    for j in range(8):
        assert (sum(k*A[r][j] for r,k in w) - B[i][j]) % 64 == 0, ('forward',i,j)
for i,w in enumerate(c['input_from_basis']):
    assert len(w) == 6
    for j in range(8):
        assert (sum(w[k]*B[k][j] for k in range(6))-A[i][j]) % 64 == 0, ('reverse',i,j)
# Each simplified relation S_i z == 0 mod m_i has B_i == (64/m_i) S_i mod64.
# For integer z this identity is an exact equivalence, not a probabilistic test.
S = [[1,1,2,1,3,2,1,-12],[0,2,2,1,0,0,0,-8],
 [0,1,1,0,0,-1,-1,-6],[0,1,0,0,2,0,2,0],
 [0,0,0,0,0,1,1,0],[0,0,0,0,1,0,1,0]]
mods = [64,16,8,4,2,2]
for b,s,m in zip(B,S,mods):
    assert all((v-(64//m)*w)%64 == 0 for v,w in zip(b,s))
# Claude toy example: exact multiplication plus exhaustive residue bijection.
def mm(A,B): return [[sum(a*b for a,b in zip(r,col)) for col in zip(*B)] for r in A]
def mv(A,x): return tuple(sum(a*b for a,b in zip(r,x)) for r in A)
M = [[2,4],[0,8],[2,12]]
U = [[1,0,0],[0,1,0],[-1,-1,1]]
V = [[1,-2],[0,1]]
Vi = [[1,2],[0,1]]
b = (6,8,14)
assert mm(U,mm(M,V)) == [[2,0],[0,8],[0,0]]
assert mv(U,b) == b[:2]+(0,)
assert mm(V,Vi) == mm(Vi,V) == [[1,0],[0,1]]
solx = {x for x in itertools.product(range(16),repeat=2) if all((a-bb)%16==0 for a,bb in zip(mv(M,x),b))}
soly = {y for y in itertools.product(range(16),repeat=2) if y[0]%8==3 and y[1]%2==1}
assert len(solx) == len(soly) == 16
assert {tuple(t%16 for t in mv(V,y)) for y in soly} == solx
x = (1,9)
y = mv(Vi,x)
assert x in solx and y == (19,9) and mv(V,y) == x
assert mv(V,(3,9)) == (-15,9)
assert tuple(t%16 for t in mv(V,(3,9))) == x
result = dict(status='PASS',input_sha256=sha,rows=1064,columns=8,
 forward_scalar_checks=48,reverse_scalar_checks=8512,simplified_relations=6,
 toy_residue_count=16,toy_integer_y=y,toy_canonical_y_image=(-15,9),
 scope='Congruence equivalence for the supplied CSV only; no source derivation, positivity, or code-existence claim.')
print(json.dumps(result,indent=2))
