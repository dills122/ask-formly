# Review clarifications — no labels or scores changed

The completed independent reviewer identified defensible relevant material outside the frozen prospective labels. Examples include R08's disabled-expression caveat, R19's legacy model/formState argument distinction, and R20's props alias/Material-property-consumption caveat. The labels are a reviewed reference set, not an exhaustive semantic relevance oracle.

Consequently, all reported recall/precision/hit counts mean agreement with the frozen labels. In particular, wide selection's74.73% selected-fact precision does NOT mean the other25.27% of selected facts are necessarily semantically irrelevant or wrong. R20 has no labeled hit, but selected partial evidence may still be useful; it is not justified to say its packet contains nothing useful. These caveats also apply to the baseline and other arms. The partial-support gaps remain, and no final-answer correctness was measured.

No gold was expanded after seeing outputs, and no score was recomputed using changed labels. The strict preregistered decision remains unchanged: wide selection fails preservation of labeled baseline facts, recall utility, consistency, and the separate R26 foundation meaning check. The narrower minimum-group metric and broader labeled-fact metric remain distinct; neither can be substituted for the other to declare a pass.

AUTHOR-EXPLANATION.md is the frozen prospective/preflight author snapshot. Its statements that live retrieval had not yet run describe that earlier checkpoint. RESULTS.md and the saved acquisition/selection artifacts describe the subsequent completed experiment. The prospective document was deliberately not rewritten after execution.

Accept these review clarifications as limits on interpretation, not a material implementation fix. No third review, new inference, query rerun, label repair, or promotion is warranted. This file supplements the frozen RESULTS.md; it does not overwrite historical evidence.
