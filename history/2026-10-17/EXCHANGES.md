# 2026-10-17: retained research exchange

One research request and one completed reply were visible today. Selected exact excerpts below come from that reply; omitted passages are not reconstructed. The research request asked for a primary-literature check, the exact coupled odd-Walsh model, a bounded solve, and explicit separation of a solver status from a certificate. No further research message was sent after the account limit appeared.

## Claude: model and symmetry

> “Fix f = 0 on an information set I of E (coordinates 0–9, checked bijective on all 1024 words).”

> “The map f → f+e preserves distance to E, and it preserves oddness because E is even. So every coset has exactly one representative vanishing on I.”

## Claude: result and its boundary

> “HiGHS status 2, ‘infeasible’, in 59.6 CPU seconds, about half the 120 s budget. It ran as one process.”

The UI used double quotation marks around “infeasible”; typographic quotation marks have been normalized in the excerpt.

> “No independently checkable certificate was produced: HiGHS output no proof and no node counts.”

> “If true, it would mean only that no [64,11,27] code contains this particular E.”

## Preserved research artifacts

The five original downloaded source/model/log files are in [claude/](claude/). They were copied without code changes after content screening. Their model has been independently audited, but their infeasibility claim has not been certified. The positive-control log omits the actual candidate vector, so its stated distance19 to E cannot be independently reconstructed from that log alone.

## Editorial clarification

One process is not evidence of a single worker thread. The supplied SciPy options do not explicitly set a thread limit; the process CPU total is reported, but exact worker count is not established. The source also specifies a wall-time limit, not a hard CPU-time limit. No additional solver run was performed to repeat its status.

The literature search in the reply did not locate the relevant bent-function covering-radius paper. The separate source note adds that connection. It yields an upper bound27, not the desired exclusion of27.
