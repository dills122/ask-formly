# Findings

Previous API-only probes lost operation/condition context and did not improve retrieval even with goldAPIlabels. This test isolates a contextual rewrite, with fullquestions preserved and unchanged engine/resultbudget. No GLiNER training or newmodel.

Contextual queries improved pooled recall by0.5556points but lost C06required key/type mapping and missed batch3floor. C30 recovered a defaults-merging fact. These texts change multiple wording features; word ordering alone was not causally isolated. Preserving original queries does not preserve all facts after fusion and the eight-result budget. A downstream policy change would require separate scope; none made.
