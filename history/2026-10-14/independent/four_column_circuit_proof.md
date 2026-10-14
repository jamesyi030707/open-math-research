# All four-column replacements are locally excluded

This result concerns the same archived binary [64,11,26] code and generator matrix. It does not settle existence of a binary linear [64,11,27] code.

## Fixed scope and exact result

The previous support-coverage calculation covered 634,824 of the 635,376 coordinate quadruples and left exactly 552 uncovered. This refinement examined only those 552 quadruples and three-word circuits consisting entirely of minimum-weight words. It did not search replacement columns or any deletion set of size 5 or larger.

There are 234 minimum messages. Checking their 27,261 unordered pairs yielded 1,196 distinct circuits (a,b,c), where a < b < c and c = a XOR b. A circuit witness was found for every one of the 552 uncovered quadruples. The search tested 1,446 circuit–quadruple combinations before finding these witnesses.

For the selected witnesses, the total deleted weight is 6 in 489 cases and 8 in 63 cases. There are no unresolved quadruples. An independent checker validates every certificate using literal-coordinate encoding, without importing the producing script.

## Three-word circuit proof

Let x, y, z be three old codewords of weight 26 with x + y + z = 0 over GF(2). Equivalently, their three message vectors sum to zero. Let D be a set of four old coordinates. Put

T = weight(x restricted to D) + weight(y restricted to D) + weight(z restricted to D).

After replacing the four generator columns, linearity preserves x′ + y′ + z′ = 0. At any new binary coordinate, the three bits must have even parity. Thus their total is either 0 or 2. Across the four new coordinates, their combined contribution is at most 8.

Their new total weight therefore satisfies

weight(x′) + weight(y′) + weight(z′) ≤ 78 − T + 8.

Each supplied witness has T ≥ 6, so the upper bound is at most 80. For all three words to have weight at least 27, their sum would have to be at least 81. This is impossible. At least one new word has weight at most 26.

The zero-word caveat is essential and satisfied: changing four coordinates of an old weight-26 word leaves at least 22 unchanged ones. Each of x′, y′, and z′ is therefore nonzero, regardless of whether the changed generator retains rank 11. Hence the argument really bounds the modified code's minimum distance.

## Combined conclusion

- For 634,824 coordinate quadruples, a minimum word containing all four old coordinates already supplies the support obstruction.
- For the remaining 552 quadruples, the three-word circuit certificate above supplies the obstruction.
- Every coordinate triple is also covered by a minimum support, as verified previously.

Consequently, every replacement of at most four columns of the archived generator yields a code of minimum distance at most 26. This is an exact exclusion of that local modification family, not a heuristic search result.

The support-only threshold remains unchanged: the smallest coordinate set contained in no minimum support has size exactly 4. Circuit certificates are stronger constraints that exclude improvement even at those support-uncovered sets. Do not reinterpret the support threshold as a replacement distance, nor as a global coding bound.

## Files and reproduction

```sh
python3 four_column_circuit.py
python3 four_column_circuit_check.py
sha256sum -c four_column_circuit_SHA256SUMS
```

- `four_column_circuit.py`: original bounded circuit-certificate generator
- `four_column_circuit_results.json`: all 552 certificates and exact search counts
- `four_column_circuit.log`: producing-run results and timing
- `four_column_circuit_check.py`: independent checker
- `four_column_circuit_check.log`: checker results and timing
- `four_column_circuit_proof.md`: this proof and scope statement
- `four_column_circuit_SHA256SUMS`: hashes of the delivered circuit artifacts

Timing fields vary on rerun; refresh their hashes after rerunning. Both programs impose a 60-second CPU limit and require only the Python standard library.
