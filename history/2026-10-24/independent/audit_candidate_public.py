"""Independently enumerate the published residual candidate; standard library only.

Usage: python audit_candidate_public.py [residual_candidate.json]
The source/shortening provenance is documented in the accompanying note.
This checks the derived basis, not all binary [37,10,14] codes.
"""
import json
from pathlib import Path
from collections import Counter
import sys
path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).with_name('residual_candidate.json')
data = json.loads(path.read_text())
rows = [int(x, 16) for x in data['basis_hex']]
assert len(rows) == 10 and all(0 <= x < 1 << 37 for x in rows)
words = {0}
for row in rows:
    words |= {x ^ row for x in tuple(words)}
hist = Counter(x.bit_count() for x in words)
expected = {0:1, 14:160, 16:142, 18:320, 20:160, 22:160, 24:80, 32:1}
assert len(words) == 1024 and hist == expected
assert hist == {int(k):v for k,v in data['weight_distribution'].items()}
heavy = sorted(x for x in words if x.bit_count() >= 27)
assert heavy == [0xffffffff]
print(json.dumps({'word_count':len(words), 'dimension':10, 'minimum_distance':14,
                  'weight_distribution':dict(sorted(hist.items())),
                  'heavy_words_hex':[hex(x) for x in heavy]}, indent=2))
