# Prebuild review response
Accept all three findings. results.py now tracks discovery IDs per case, checks recovery scope and exact original request/plan, and validates all initial calls against one frozen canonical lookup list used for both arms. It returns separate immutable initial packets and completed packets; each has separate caller-answer judgments and scores. test_audit.py reproduces all findings: red failures retained in audit-red.txt, all18tests green in audit-green.txt. No knowledge/plans/criteria changed. Candidate not built or tested yet.

A second run-freeze pins databases.json after candidate build; preserved() verifies it. A red/green regression detects wiring drift. This prevents a later transport config change from silently selecting a different database.
