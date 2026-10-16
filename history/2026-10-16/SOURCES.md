# Sources and scope

Retrieved 2026-10-16 from the current accessible primary sources:

- Markus Grassl, binary [64,11] parameter table: https://www.codetables.de/BKLC/BKLC.php?k=11&n=64&q=2 . Displayed bounds 26–27. The construction entry itself is historically dated 2001-01-30. This is a table check, not exhaustive literature coverage or proof that no unpublished improvement exists.
- Markus Grassl, binary [64,10] parameter table: https://www.codetables.de/BKLC/BKLC.php?k=10&n=64&q=2 . Displayed matching bounds 28 and the known extended BCH(63,27) construction.
- Magma Handbook, BCH construction conventions: https://magma.maths.usyd.edu.au/magma/handbook/text/1978 . The omitted starting exponent defaults to 1. Our implementation uses binary cyclotomic closure of exponents 1 through 26.
- Magma Handbook, extension convention: https://magma.maths.usyd.edu.au/magma/handbook/text/1979 . Extension appends the coordinate making the total coordinate sum zero.

The finite construction below independently implements this known recipe. It does not copy or relicense Magma software or the database. Attribution to the existing construction is retained. All new scripts use Python's standard library.

Motivation: error control in digital communication and storage. Distance 27 would guarantee correction of 13 errors under worst-case unique decoding, compared with 12 for distance 26. No practical deployed improvement is claimed.

The study concerns one fixed parent, not classification of all even [64,10,28] codes. Integer-feasible weight distributions are not actual cosets. AI-assisted discussion and separately implemented checks are not external peer review or proof-assistant certification.
