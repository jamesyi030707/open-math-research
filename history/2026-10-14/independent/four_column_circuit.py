#!/usr/bin/env python3
"""Exact three-minimum-word-circuit obstruction for the552 uncovered quadruples.
Fixed scope: three-word circuits of the archived code and size4 deletion sets.
No size5 search, replacement-column search, or heuristic. Standard library only.
"""
import collections
import hashlib
import itertools
import json
import pathlib
import resource
import time

resource.setrlimit(resource.RLIMIT_CPU,(60,60))


def main():
    cpu=time.process_time()
    raw=pathlib.Path('generator_matrix.txt').read_bytes()
    rows=raw.decode().splitlines()
    assert len(rows)==11 and all(len(row)==64 and set(row)<={'0','1'} for row in rows)
    generator=[sum(int(bit)<<j for j,bit in enumerate(row)) for row in rows]
    words=[]
    for message in range(2048):
        word=0
        for i,row in enumerate(generator):
            if (message>>i)&1:
                word^=row
        words.append(word)
    assert len(set(words))==2048 and min(w.bit_count() for w in words[1:])==26
    minimum=[m for m in range(1,2048) if words[m].bit_count()==26]
    assert len(minimum)==234
    pool=set(minimum)
    circuits=[]
    pairs_examined=0
    for a,b in itertools.combinations(minimum,2):
        pairs_examined+=1
        c=a^b
        if b<c and c in pool:
            assert words[a]^words[b]^words[c]==0
            circuits.append((a,b,c))
    uncovered=json.loads(pathlib.Path('coverage_extension_uncovered_sets.json').read_text())['4']
    assert len(uncovered)==552 and len({tuple(d) for d in uncovered})==552
    witnesses=[]
    unresolved=[]
    attempts=0
    for deletion in uncovered:
        mask=sum(1<<(j-1) for j in deletion)
        assert len(deletion)==4 and all(1<=j<=64 for j in deletion)
        assert all(words[m]&mask!=mask for m in minimum)
        witness=None
        for circuit in circuits:
            attempts+=1
            deleted=[(words[m]&mask).bit_count() for m in circuit]
            total=sum(deleted)
            if total>=6:
                assert total in (6,8)
                witness={'deleted_coordinates_1based':deletion,'message_integers':list(circuit),
                    'codeword_hex':[f'{words[m]:016x}' for m in circuit],
                    'old_weights':[26,26,26], 'deleted_weights':deleted,
                    'deleted_weight_total':total,'maximum_new_column_total':8,
                    'maximum_new_weight_sum':78-total+8,'required_new_weight_sum':81,
                    'minimum_unchanged_weight':22}
                assert witness['maximum_new_weight_sum']<81
                break
        if witness:
            witnesses.append(witness)
        else:
            unresolved.append(deletion)
    result={'matrix_sha256':hashlib.sha256(raw).hexdigest(),
        'scope':'Only the552 minimum-support-uncovered size4 sets; three weight26 word circuits; no search beyond4.',
        'minimum_word_count':234,'minimum_message_pairs_examined':pairs_examined,
        'distinct_three_word_circuits':len(circuits),'uncovered_quadruples_input':len(uncovered),
        'quadruples_excluded_by_circuit':len(witnesses),'unresolved_quadruples':unresolved,
        'circuit_candidate_tests':attempts,
        'witness_deleted_total_histogram':dict(sorted(collections.Counter(w['deleted_weight_total'] for w in witnesses).items())),
        'witnesses':witnesses,
        'support_coverage_threshold_unchanged':4,
        'combined_conclusion':('All replacements of at most4 columns of this archived generator fail to reach distance27.' if not unresolved else 'Some four-column locations remain unresolved by these certificates.'),
        'global_limit':'Does not settle existence of a binary linear [64,11,27] code.'}
    pathlib.Path('four_column_circuit_results.json').write_text(json.dumps(result,indent=2)+'\n')
    log=[f'PASS: archived baseline has2048 distinct words and234 weight26 words.',
        f'Examined{pairs_examined} minimum-message pairs; found{len(circuits)} distinct three-word circuits.',
        f'Uncovered quadruples:552; excluded by circuit:{len(witnesses)}; unresolved:{len(unresolved)}.',
        f'Deleted-total histogram:{result["witness_deleted_total_histogram"]}.',
        f'Circuit candidate tests:{attempts}.',
        result['combined_conclusion'],
        'Support-only minimum uncovered subset size remains exactly4.',
        'Nonzero caveat: every changed weight26 word retains at least22 unchanged ones.',
        'No size5 search or new-column search performed.',
        f'CPU seconds:{time.process_time()-cpu:.6f}.']
    pathlib.Path('four_column_circuit.log').write_text('\n'.join(log)+'\n')
    print('\n'.join(log))


if __name__=='__main__':
    main()
