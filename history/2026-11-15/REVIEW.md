# Independent q24 local enumeration

This is a local classification audit, not a lift-existence result.

The S restriction is classified in the existing November 10 argument independently of the h-kernel assumption. In canonical message coordinates its seven weight-16 messages are H={1,2,3,4,8,16,28}. Character inversion gives each nonzero label multiplicity m_v=(k_v-2)/2 with k_v the number of H characters evaluating to one. There are 19 single labels, three double labels, and two zero columns; the code has length 27 and dimension 5.

The earlier November 12 pair-budget restriction leaves h weights r=4,8,20,24. The independent local.py explicitly enumerates every coordinate subset of size r (via complements for r>13), rejects nonzero XOR of selected S labels, and tests each of 31 shifted nonzero S messages for weight 12 or 16. No other pruning is used. Equal coordinate permutations are identified by the 32-entry vector of h-selected label multiplicities. The resulting 277 vectors are complete for this fixed S labelling, not just samples:

- r4: (z,q',count)=(0,25,1),(1,17,18).
- r8: (1,18,96),(2,10,24).
- r20: (1,21,24),(2,13,96).
- r24: (2,14,18).

The stability group of H is GL(2,2) times the permutation group on its four complementary heavy vectors, of order 6*24=144. The triple is the unique zero-sum triple in H, so any stabilizer preserves the two summand subspaces. Every permutation of the four complementary vectors extends uniquely to an invertible map on their 3-space, because any three are independent and all four sum to zero. Thus these 144 maps give the full stabilizer, not a guessed subgroup. The column action is the transpose of the message action; the inverse-transpose gives the same set because this is a group.

orbits.py explicitly partitions all 277 vectors into nine disjoint orbits with sizes:
r4: 1,18; r8:24,72,24; r20:24,72,24; r24:18.

There are |GL(5,2)|/144=69440 distinct S labellings. Equivalently choose 155 two-dimensional P, 64 complementary V, and seven affine planes in V not containing zero. The number of W restrictions before external compatibility is therefore 69440*277=19234880, modulo coordinate permutations but retaining fixed message labels. Neither the 144 local maps nor arbitrary GL5 maps are asserted to preserve the external residual B. No external search is performed.

Both scripts use explicit ValueError checks rather than asserts. local.py ordinary and -O agree after omitting cpu_seconds; about 3 CPU seconds each. orbits.py ordinary and -O agree byte-for-byte. The retained full vectors permit independent recounting. Rank 6 of W follows already because h has weight 4,8,20 or24 whereas every nonzero S word has weight12 or16.

The Grassl source was actually opened on November 15: lower26 upper27, https://www.codetables.de/BKLC/BKLC.php?q=2&n=64&k=11. This is current reading of a table, not a new source revision or exhaustive novelty search.
