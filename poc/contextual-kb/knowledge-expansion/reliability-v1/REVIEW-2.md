# Independent correction review2of3

Verdict: **Not ready** pending one bounded literal-preservation correction.

P2: scanning single backticks toggled twice for double-backtick Markdown code spans, incorrectly allowing a capitalization rewrite inside the literal. Reviewer independently reproduced this while16 tests passed. Author accepted. Added tests for delimiter runs1–4, tilde fencing, HTML code markup and multiline indentation; five cases failed before the fix.

The final candidate deliberately declines automatic repair for any question containing backticks, tilde fences, angle-bracket markup or line breaks. It does not attempt to parse Markdown. Already-valid plans still pass through accepted normalization unchanged. Quote protection for ordinary single-line prose remains. All17 tests now pass. This conservative reduction of repair scope requires final reviewer3 verification before inference.

Reviewer found the unchanged frozen-test plan suitable and no need for architectural pivot. No source edits, hosted calls, builds or sealed evaluation access occurred during review. Final instance3 will inspect the correction and then the completed results; no fourth review starts automatically.
