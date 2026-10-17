# Verification boundaries

1. HiGHS status 2 is preserved as a reported solver outcome, not an exact nonexistence proof. Model validity and solver soundness are separate questions.
2. All exported LP coefficients, bounds, parity, variable types, and the ten-coordinate gauge passed an independent integer audit. The source and LP use the same documented formulas. No extra f63=0 gauge is imposed in the exported Claude model.
3. The source does not explicitly force one HiGHS thread, and has no hard CPU guard. The log's59.6 CPU seconds is below the requested budget, but does not certify the complete runtime environment or worker count.
4. The positive-control log reports distances27 and19 but does not save the returned vector. Its exact vector-level result was not independently checked. The general existence of an RM(1,6) distance27 control follows by flipping one point of a bent function.
5. A supplied independent optional runner is syntax-checked only. Its status must not be confused with the downloaded run. The new exact checks do not repeat the solver.
6. The literature establishes rho(E)≤27, not rho(E)≤26. The cited general open question dates to2023; the focused current search is not a proof that every special case remains unstudied.
7. Any future certified exclusion applies to this fixed E only, not every [64,11,27] binary linear code.
