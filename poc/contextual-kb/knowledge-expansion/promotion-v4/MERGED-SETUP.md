# Remote integration qualification

The frozen70-fact promotion passed before merging remote main3607c17. That remote commit introduced project/worktree settings and version matching. This integration retains those source files and the local reviewed capitalization/service composition, combines both maintenance suites, and preserves foundation5's exact70-fact DB and models.

The foundation manifest imports only the seven changed/new remote source pins and the required semantic-version2.10.0 package declaration. The package was added to the server environment; model environments/assets were not changed. Five new pinned files bring doctor coverage to86.

Local verification passed:106source tests (104 before the two caller-command tests),114runtime regression tests,86doctor checks, plus the separate real-stdio fixture transport test. The first merged-live attempt delivered0/15 usable answers: every call was rejected before retrieval because the new potentially state-writing lookup annotation required approval under the unattended caller policy. These failures are retained. The bounded merged_run.py wrapper enables only lookup_formly and records its explicit authorization per invocation; it does not change global configuration, sandbox policy, tool annotations, runtime code, questions or grading. Its two command-boundary tests demonstrated red/green. The repaired run uses a separate merged-live-approved directory. Fresh independent review instance2of3 covers the merge and outcomes. No sealed evaluation is used.

The per-tool approval override and enabled-tools allowlist follow [official MCP configuration documentation](https://learn.chatgpt.com/docs/extend/mcp). The user authorized these tests; this is not a default blanket approval for other tools.

## Repeating an explicitly authorized smoke check

Use a new output name; never overwrite or retry a saved run implicitly:

```sh
poc/contextual-kb/mcp_v1/.venv/bin/python -B poc/contextual-kb/knowledge-expansion/promotion-v4/merged_run.py --name new-approved-run --approved-lookups
poc/contextual-kb/mcp_v1/.venv/bin/python -B poc/contextual-kb/knowledge-expansion/admission/assess_run.py --implementation extensions-v2 --root poc/contextual-kb/knowledge-expansion/promotion-v4/test-output/new-approved-run --cases poc/contextual-kb/knowledge-expansion/promotion-v4/cases.json --repeats 1 --arms candidate
```

The explicit flag records authorization for this invocation; it does not request or grant permission for unrelated tools. Ordinary interactive clients can approve the lookup when prompted. No user/global client configuration was edited.

## Completed results

The corrected lookup-only run passed15/15 usable answers, zero critical failures, across three five-question batches. The failed initial0/15 approval-blocked run remains separate. All86current manifest pins verified; relative to the frozen promotion, only the imported remote server and requirements-lock pins changed and five new remote source pins were added. Model and installedDB bytes stayed unchanged. See [independent merged review](REVIEW-MERGED.md).
