# Sources and scope

- Markus Grassl, bounds for binary linear [64,11] codes, https://www.codetables.de/BKLC/BKLC.php?k=11&n=64&q=2 . Retrieved 2026-10-15 through web research; page displayed lower26, upper27. The research index reported a four-day crawl age; this is evidence of the current accessible table, not a claim of complete literature coverage or absence of unpublished improvements. The construction entry is historically dated2001-01-30. No change of record is claimed.
- Baseline matrix reused unchanged from [previous verified construction](../2026-10-14/independent/generator_matrix.txt), itself independently reconstructed from the table's cyclic-code, parity-extension and shortening recipe. Baseline attribution remains Grassl and the references maintained there.
- Actual mathematical prompts and Claude final replies are preserved here. Displayed thinking/tool-progress summaries, interface account information and private conversation identifiers are excluded. Research commentary is newly edited mathematical analysis, not invented personal testimony.

The application motivation is error control in communications and storage. Under ordinary worst-case unique decoding, distance26 guarantees correction of12 errors, while distance27 would guarantee13. This notebook does not claim a deployed benefit for this particular low-rate code.

New owned code and notes follow the repository's MIT / CC BY4.0 policy only to the extent rights are held. No upstream database or third-party software has been copied or relicensed. No originality, peer review, global nonexistence, or formal proof-assistant certification is claimed.

- Markus Grassl, binary[64,10] parameter page, https://www.codetables.de/BKLC/BKLC.php?k=10&n=64&q=2 . Retrieved2026-10-15; research source crawled today. It lists matching bounds28 and an extended BCH(63,27) construction. This motivates a future fixed-parent experiment, not an experiment completed here.
