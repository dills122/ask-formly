# Annotation guide v2 clarifications

Read with v1. These general rules resolve initial annotator differences. Preserve
v1 raw files. Re-annotate all 24 independently without reading the other labels.

- A reference span is the minimal referring token/demonstrative phrase: `its`,
  `it`, `that setting`, `that wrapper`, `this`. Do not include a possessive's noun.
  Explicit demonstratives like `this configuration` are references; relative
  descriptions such as `supplied values` are not automatically reference labels.
- Use a single contiguous request-cue span when the interrogative and action
  are adjacent. Split only across intervening target/setup text. Shared question
  prefixes apply to coordinated asks even when printed once.
- Version/adapter scope belongs in versions/ui_adapters, not duplicated in
  conditions. A `For <target>` topical phrase is not also a condition. A setup
  assumption (`With ...`, `When ...`, `Given ...`) is a condition. Context such as
  `in the model` remains part of the target when it distinguishes the value.
- A requested operation on a target counts as an aspect. A comparison across
  adapters has the behavior being compared as target; adapters are scope. In
  `Can X stop Y from being removed?`, target is Y; X is the operating condition.
  `stop ... from being removed` is a negative constraint expressing prevention.
- A coordinated prohibited outcome is attached to its own aspect, not copied
  onto the positive aspect unless wording explicitly constrains that aspect.
- Include each explicitly supplied custom-name occurrence, even inside a generic
  API expression. A quoted registration name is both custom_identifier and literal.
  All relevant such occurrences also belong in the aspect identifiers list.
- For same-anchor aspects, preserve two records and the different operation cues.
  Do not change targets to actions merely to create distinct anchors.

These rules constrain annotation representation only, not Formly behavior.
