# Publication status — judged 5/12; remediation in progress

The approved additive evidence release was published to the existing
Hugging Face Space `DineshAI/m4TAzup6Yc` at revision
`887693a544629b31b7c6dc141fa321a9fcdb5948`.

The remote tree was redownloaded at that exact revision and verified:

- 17/17 judged baseline paths remain present;
- 16/16 protected non-navigation files are byte-identical;
- 76/76 approved text paths match the SHA-256 upload manifest;
- the complete Space tree contains 92 paths.

The live judge evaluated that exact revision on 2026-07-24 and assigned
**5/12**: Claims 1–5 were `toy` and Claim 6 was `inconclusive`. The repeated
criticism was that the d=8 section described results but showed no executable
code or raw output.

The root cause is now reproduced: `trackio logbook read
DineshAI/m4TAzup6Yc` serializes the plain-Markdown rigorous subtree as
`No cells`, so the judge received the preserved 1D baseline cell. The current
unpublished child adds an additive Trackio-cell subtree with the formal d=8
source, raw rate/tail tables, independent checker source and output, and
negative controls. No score increase is claimed.
