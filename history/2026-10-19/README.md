# Research record · 2026-10-19

## Result
The fixed extended BCH [64,10,28] extension problem now has seven necessary aggregate distance histograms, reduced from 25. An algebraic fourth-moment/design argument excludes 18 histograms. It neither constructs an extension nor proves that none exists.

- [Full proof and exact checker](independent/README.md)
- [Selected actual exchanges](EXCHANGES.md)
- [Sources and limited novelty check](SOURCES.md)
- [Limitations and archival caveat](LIMITATIONS.md)

The first Claude exchange completed. The second supplied a script and log verifying the intermediate 13-histogram restriction before the free usage limit interrupted final prose. The stronger seven-histogram deduction is independently developed AI-assisted work. No new solver was installed or run; the existing full OPB remains unresolved.

## Reproduce
Run `python3 independent/check_structural_moments.py` using only Python's standard library. The generated JSON records all 63 derivative ranks, two agreeing constructions of 1,008 blocks, all 64 point degrees and 2,016 pair degrees, and four implementation controls. The proof is algebraic; those four samples do not replace it.

Historical Claude files are retained unchanged in `claude/`; they are supporting discussion records, not the authoritative proof checker. No third-party source PDFs are redistributed.
