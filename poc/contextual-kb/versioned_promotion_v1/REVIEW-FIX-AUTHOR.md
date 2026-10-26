# Author response to promotion review1

Accept bothP2findings. Added isolated recovery import regression: copying only
allowlisted Python files then running Python -I -S importing the versioned
compiler failed (bundle-red.txt). Added kbcompiler/structured_source.py to runtime
allowlist and foundation pins; regression now passes. No runtime code changed.

Added coordinated recovery instructions restoring accepted commit/snapshot code,
authored inputs/catalog/manifests and schema1 DB together. rollback_check.py copies
all712pre-promotion source files and DB into an isolated temporary checkout. It
validates every snapshot hash, imports the old composition, lints original sources,
checks schema1/93facts and reproduces12public-query rankings with old code+DB.
coordinated-rollback.json/log records success. It never restores over installed DB.

Full final maintenance passed176source tests,149runtime tests and95doctorpins.
Six supported stable MCP calls and two v7rejections passed before these
recovery-only changes; runtime code/DB identical afterward. Both native model seeds
passed parameter preservation. All86unchanged prior runtimepins remain exact;
only authorized DB/launcher/server changed. Current95pins pass. final-preservation
records actual Python/SQLiteversions and counts.

Documentation now qualifies byte reproducibility to provisioned Python3.13 /
SQLite3.53.1. Reviewer found systemSQLite3.53.3 emits different bytes; do not claim
cross-toolchain byte identity. Logical table preservation and native/runtime
results remain unchanged. No commits/push yet; source/model/private archive
exclusions will be verified before staging. No coverage beyondexact6.3.12.
