# Seven remaining distance profiles

*Research note · 19 October 2026*

## Question
Can the fixed extended BCH [64,10,28] code be extended by an odd vector whose distance from every parent codeword is at least 27? This is a concrete subproblem of the binary [64,11] distance gap, currently listed as 26–27 in [Grassl's table](https://www.codetables.de/BKLC/BKLC.php?k=11&n=64&q=2). Better error-correcting codes concern reliable storage and communication; this finite restriction has no demonstrated deployment benefit by itself.

## What changed
Earlier moment constraints allowed 25 aggregate distance profiles. Looking at each of eight Walsh spectra separately gives four local patterns, but still allows all 25 global profiles. The useful step is their shared quadratic structure.

The weight-four dual supports form a 2-(64,4,3) design with 1,008 blocks. If V counts blocks meeting an odd support in an odd number of points, the design equations force V ≡ 3 modulo 4. The combined fourth-moment identity gives C = 2828 − 4V, where C counts magnitude-ten coefficients when the target distance condition holds. Thus C is divisible by 16.

Exactly seven necessary profiles remain. Each row gives counts at distances (27,37), (29,35), and (31,33), with the listed count applying to each member of its pair:

|27 and 37|29 and 35|31 and 33|
|---:|---:|---:|
|224|288|0|
|240|240|32|
|256|192|64|
|272|144|96|
|288|96|128|
|304|48|160|
|320|0|192|

## Research commentary
The reduction comes from coupling the spectra, rather than spending more computation on them independently. Eighteen candidate profiles are now excluded by a short algebraic argument. This is a useful restriction of the fixed-instance search space, although it does not establish feasibility or impossibility for the seven survivors. No claim of priority is made: the identities and design method are established theory, and the contribution recorded here is their explicit, reproducible application.

The next experiment should aim for a verifiable witness or an independently checked impossibility certificate. Further changes of notation or model format alone would not answer the remaining question.

## Discussion and evidence
The work used AI-assisted mathematical discussion. A first exchange derived four local spectrum patterns; a second delivered a check of an intermediate 13-profile restriction before a usage limit. The seven-profile result was then derived and verified independently, without inventing another exchange.

- [Actual selected discussion](../history/2026-10-19/EXCHANGES.md)
- [Complete derivation, exact checker, and results](../history/2026-10-19/independent/README.md)
- [Sources and novelty limits](../history/2026-10-19/SOURCES.md)
- [Scope and archival caveats](../history/2026-10-19/LIMITATIONS.md)
