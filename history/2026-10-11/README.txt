Collatz finite-certificate correction and audit — 2026-10-11

Read 研究核查结论.txt for the Chinese findings, limits, and status.

claude_original/ contains the eight unchanged files actually shared by Claude today.
reference/ contains clearly labeled prior-run dependencies. These are NOT new results.
The new J92 JSON changes only descriptive metadata; its mathematical data equal the previous certificate.

Quick independent audit (Python 3 standard library only; no interval rescan):
  python3 audit_candidate_output_j92.py claude_original/paradox_cert_J92.json --selftest
The audit compares against reference/paradox_cert_J92_previous.json and recomputes each listed trajectory and the finite bound.

The original Claude generator needs the unchanged previous reference/paradox_scan.c. It does not implement the proposed inverse-orbit search. Regenerating its certificate performs the existing full interval scan; this is unnecessary for reviewing today's correction. The original Claude checker requires NumPy. Its --static-only option rechecks only q/H/X and intentionally skips trajectory scans.

Do not treat a known-set comparison as an independent new proof that an unimplemented traversal is complete. No inverse-search prototype or benchmark was completed today. The broad C overflow guarantee and generic small-J empty-set behavior still require the fixes described in the audit.