# Local AI Central setup

This extraction uses the same shared-link pattern as Angular Usage Lookup. Source: /Users/dsteele/.ai-central, revision e08d63e874f39264ed36f31812476f0816b9e49e, clean at inspection. No source update is performed.

```sh
sh tools/bootstrap-ai-central.sh --dry-run
sh tools/bootstrap-ai-central.sh
```

The maintained installer detects profiles/bundles and preserves existing project files. AGENTS.md and project steering are real files. Verified shared skills/steering links are excluded by exact path in .git/info/exclude, so another checkout needs its own bootstrap. Set AI_CENTRAL_HOME to an existing source checkout if required. Do not modify shared targets.

Selected profiles: base,javascript-typescript. Selected bundles: core,node. Ten shared skills have ten compatibility links, plus one shared steering link; all 21 resolve and are locally excluded. Initial apply and repeat refresh succeeded, preserving project files.
