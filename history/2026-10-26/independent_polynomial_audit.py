"""Independent exact audit using polynomial multiplication, not Krawtchouk sums.
Run beside enumerator_witness.json. This audits formal distributions, not a code.
"""
import json
from pathlib import Path

def main():
    data = json.loads(Path(__file__).with_name('enumerator_witness.json').read_text())
    for code, length, size in [('A', 27, 512), ('D', 64, 1024), ('C', 64, 2048)]:
        result = [0] * (length + 1)
        for weight, count in data[code].items():
            weight = int(weight)
            polynomial = [1]
            for sign in [-1] * weight + [1] * (length - weight):
                product = [0] * (len(polynomial) + 1)
                for i, value in enumerate(polynomial):
                    product[i] += value
                    product[i + 1] += sign * value
                polynomial = product
            for i, value in enumerate(polynomial):
                result[i] += count * value
        assert all(value >= 0 and value % size == 0 for value in result)
        assert [value // size for value in result] == data['dual_' + code]
        assert sum(result) // size == 2**length // size
    for i in range(65):
        assert data['dual_D'][i] == data['dual_C'][i] + data['dual_C'][64-i]
        assert data['dual_D'][i] >= data['dual_C'][i] >= data['D'].get(str(i), 0)
        assert data['dual_D'][i] >= data['C'].get(str(i), 0)
    print('PASS: 158 exact transform coefficients and stated nested identities; no realizability claim.')

if __name__ == '__main__':
    main()
