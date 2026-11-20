# 2026-11-20: short joint-character certificate

[研究手记](../../notes/codes-joint-character-certificate.md) · [证明与范围](PROOF.md) · [真实讨论摘录](DIALOGUE.md)

- `check.py` / `result.json`: exact rational ranks and all 17,728 scalar character tests for the 277 canonical restrictions, one fixed-pair test, plus the complete 47-point certificate for control index 1.
- `independent.py` / `independent_result.json`: self-contained independent enumeration of the seven active signs (128 assignments), actual B section and all 63 local windows. This independently audits the main control, not the entire 277-wide batch.
- `validation.json`: performed checks; `SHA256SUMS.txt`: hashes of this dated archive, excluding itself.

Run `python history/2026-11-20/check.py` and `python history/2026-11-20/independent.py`; repeat using `python -O`. Both mode pairs have identical deterministic outputs. Only the standard library is needed. The batch reads the previously published `history/2026-11-15/h.json`; alternatively give its filename as the first argument. Each computation is capped at 60 seconds. No large global search.

The control and all 17 fixed-pair rejections were already excluded on November 16. Today's contribution is a short exact certificate and an explicit separation between the specified scalar tests and joint compatibility, not a new bound or claim of original discovery. The old doubly-even normalization is indispensable.

The earlier single-label q28 eight-equation certificates (November 13) were not claimed new here; this note develops a two-projection q24 control with its own actual coefficients. General use at another labeling requires recomputing those coefficients.

One actual Claude exchange completed before free quota exhaustion. The numerical two-line certificate was checked independently and was not subsequently reviewed by Claude.
