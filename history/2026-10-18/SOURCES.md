# Primary sources checked 2026-10-18

- [Grassl: binary linear codes [64,11]](https://www.codetables.de/BKLC/BKLC.php?k=11&n=64&q=2): current entry still gives 26 ≤ d ≤ 27. It is a table-status check, not an exhaustive literature exclusion.
- Meidl, Polujan and Pott, *Linear codes and incidence structures of bent functions and their generalizations*, [arXiv:2012.06866v2](https://arxiv.org/html/2012.06866v2), final 2023 version, §5.1 and Question 5.18. The maximal-output bent-function case remains posed there; the stated bound gives rho(E)<28 in this six-variable case, not rho(E)≤26. The exact BCH-to-bent-code correspondence was checked in the previous archive.
- [VeriPB official project](https://veripb.org/): describes proof logging, independent checking, current Rust implementation and CakePB elaboration. Listing a supported solver is not evidence that this notebook ran it or that its installed output format is compatible.
- [VeriPB current proof format overview](https://gitlab.com/MIAOresearch/software/VeriPB/blob/HEAD/proof_format_overview.md): current version 3.0 syntax. Old examples using version 1.1/2.0 must not be assumed compatible.
- [RoundingSat upstream](https://gitlab.com/MIAOresearch/software/roundingsat/-/blob/master/README.md): candidate proof-producing pseudo-Boolean solver. A solver/checker pair must pass an actual small satisfiable/unsatisfiable test before relying on it.

Only links and short summaries are redistributed. Existing repository attribution and licensing apply.
