# Binary branching certificates for four fixed weight systems

The four previously infeasible 14-equation systems have compact proofs under the binary restriction, despite having nonnegative integer solutions in the relaxation. The checker independently reconstructs each equation from the pinned catalogue, requires both children at each split, and checks every forced decision and contradiction exactly. It also checks that all 8,192 normalized all-±1 combinations are separately feasible in each instance. No new Claude exchange or code-distance result is claimed.

- [Proof and scope](PROOF.md)
- [Full four certificates](trees.json)
- [Verifier](verify.py), [recorded verification](verification.txt)

From the repository root: `python3 history/2026-11-26/verify.py`. Python 3.10+; standard library only.
