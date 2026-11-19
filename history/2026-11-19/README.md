# 2026-11-19: actual translation-orbit slice counting

[研究手记](../../notes/codes-translation-orbit-slice.md) · [精确证明](PROOF.md) · [真实交流摘录与更正](DIALOGUE.md)

- `orbits.py` / `result.json`: stabilizers, slice sizes, direct-image comparison, 8,400 key checks.
- `independent.py` / `independent_result.json`: separately written direct-image audit, including actual S weights, r/z invariance on the slice and key idempotence.
- Both scripts read the complete earlier `../2026-11-15/h.json`; default paths work from any working directory. Alternatively supply its path as the first argument.
- Run each with `python` and `python -O`; deterministic outputs agree exactly with their JSON files. Each measured run took under two seconds; reproduction budget is 60 seconds per process.
- `validation.json` records performed checks; `SHA256SUMS.txt` hashes this dated archive, excluding itself.

The input Git blob SHA was checked against the remote published input: `6c2f005c33236b54ed1850f78b7700fcb44b7237`.

There are 10,915,968 true translation orbits meeting the precisely defined local q24 slice X after the November 18 multiplicity filter, BEFORE subtracting older external exclusions. This is no new exclusion or improvement of d26–27. No ten-million-representative enumeration was run. The 69,440-E classification and actual B translation group are reused from November 15–18 with their original scope. Claude did not independently verify the supplied finite counts.

One real question/answer completed; free quota then exhausted and work stopped there. Final-answer excerpts only; no private conversation metadata, account information or thinking-panel content.
