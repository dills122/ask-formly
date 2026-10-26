# Material choice-controls promotion

Promotes the reviewed 111-fact / 24-document candidate as foundation12 and model-free-discovery-4. See PLAN.md, RESULTS.md, CHECKLIST.md and the final review when complete. Runtime implementations and models remain unchanged. Evaluation stays sealed.

The promotion helper revalidates the old baseline, qualification and exact candidate bytes before changing five targets under the existing guarded transaction. It is historical and intentionally refuses to rerun against an already promoted DB. Recovery snapshots are private under test-output/install-1/before; ordinary exceptions roll back, but this is not crash-atomic across all files. Do not publish the DB, backups, model assets or raw settings/transport output.

Existing MCP processes must be restarted through their client UI to load the new pins. This task does not edit client configuration. The stable launcher remains the supported entry point.
