# Findings

Previous contextual-query trial recovered one relevant fact but lost a baseline key/type fact after fusion/interleave. New hypothesis: reserving six baseline slots may retain useful original evidence while allowing two additions. It cannot guarantee all relevant facts survive; gold is unavailable to the combiner.

Fixed prefix protection preserves rank, not relevance: useful tail facts remain exposed. Foundation/current/protected pooled recall: 92.07/92.55/92.07%; weakest batch: 85.71/87.14/85.71%. None consistently meets 89.25%. Candidate acquisition also limits improvement: M14/M19 required facts absent from all saved query lists. Retain foundation; do not promote this policy.
