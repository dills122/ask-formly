# Public API/configuration source checklist

Source verification is complete. All additions exist only in the isolated candidate; the positive qualification gate failed, so none is installed.

| Candidate fact | Pinned evidence | Disposition |
| --- | --- | --- |
| `public-api-configuration/wrapper-nesting-order` | K41 | Verified; isolated candidate only |
| `public-api-configuration/defaults-order-before-wrapper-fallback` | K150, K151 | Verified; isolated candidate only |
| `public-api-configuration/duplicate-type-registration` | K150, K152 | Verified; isolated candidate only |
| `public-api-configuration/duplicate-wrapper-registration` | K150 | Verified; isolated candidate only |
| `public-api-configuration/duplicate-validator-registration` | K150 | Verified; isolated candidate only |
| `public-api-configuration/preset-partial-overrides` | K44, K151, K153 | Verified; isolated candidate only |
| `public-field-api/field-get-tree-lookup` | K05, K140 | Verified; isolated candidate only |
| `public-field-api/field-get-path-boundaries` | K140, K39 | Verified; isolated candidate only |
| `public-field-api/key-id-name-roles` | K01, K05, K37 | Verified; isolated candidate only |
| `public-field-api/css-host-targets` | K01, K41, K141 | Verified; isolated candidate only |
| `public-field-api/array-control-type` | K02, K142 | Verified; isolated candidate only |
| `public-field-api/options-build-default` | K01, K06 | Verified; isolated candidate only |

Already-covered scalar/group type contracts and expression operations were reused, not duplicated. Numeric-key traversal totality, universal DOM/CSS behavior, arbitrary control preservation, hot replacement and recursive preset guarantees remain excluded or unqualified. See the complete per-topic [API decisions](api/source-decisions.json) and [configuration decisions](configuration/source-decisions.json).

Remaining test gaps: accessor forwarding relationships (API-09), updateInitialValue optional model argument (API-12), wrapper suppression-option boundary (CONFIG-08), missing named preset behavior (CONFIG-12). These require a separately frozen follow-up, not edits to this completed run.
