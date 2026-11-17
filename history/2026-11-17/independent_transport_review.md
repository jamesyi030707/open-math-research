# Independent audit of W translations and transport

## Actual residual automorphisms

In the column coordinates (z,x,e) of the stabilizer audit, all 32 maps

F_t(z,x,e)=(z+K_t(x)+f(t)e, x+te, e),

where K_t(x)=f(x+t)+f(x)+f(t), are linear, invertible and preserve the full 37-column set. The independent program verifies linearity of each derivative, the 37-column permutation, distinctness of all 32 permutations, and all 32*1024 residual message weights. No appeal to arbitrary GL(5,2) is made.

On W messages the transpose is g_t(s+epsilon*h)=s+(epsilon+s dot t)h. It fixes h but normally sends S to a different complement. This is consistent with the S,h stabilizer being trivial.

## Transport implementation

The independent implementation reconstructs the six 27-bit A rows from each of the 277 original column multisets. It replaces row i<5 by row_i+t_i*row_h, keeps row_h unchanged, then reconstructs and sorts all 27 six-bit column labels. This is a separate row-operation implementation of the main column formula. All 8864 origin/translation pairs are included, without sampling.

After deduplication there are 8408 restrictions, distributed by the number q of weight-12 nonzero S messages as follows: q16:2046, q20:4914, q24:1447, q28:1. The q24 restrictions have 859 distinct E sets. The canonical E has all 277 original restrictions; no other E is asserted fully classified or excluded by this count.

Transport preserves nonextendability: composing a hypothetical full lift with the inverse residual automorphism would produce an extension of the original forbidden W restriction. This relies on the November 16 completeness/exclusion certificate and does not independently rerun it. It proves these particular 8408 W restrictions nonextendable, not all orientations or all q branches. The q28 entry is already covered by the earlier full q28 result and is not a new branch exclusion.

`independent_transport.py` uses only the original h.json and the fixed B matrix, not main-program output. Ordinary and optimized runs agree after omitting CPU timing. The pattern digest is over sorted unique tuples, each rendered as comma-separated decimal labels followed by a newline; its SHA256 is stored in independent_transport.json.
