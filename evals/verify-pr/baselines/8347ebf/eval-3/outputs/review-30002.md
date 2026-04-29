# Review Comment Classification: 30002

## Comment
**Author:** reviewer-a
**File:** `migration/src/m0042_sbom_soft_delete/mod.rs` (line 14)
**Text:** "The migration should also add an index on `deleted_at` for the sbom table. Queries filtering by `deleted_at IS NULL` will be frequent and a partial index would help. Something like: `CREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;`"

## Classification: code change request

## Reasoning
The reviewer requests a specific code addition: adding a partial index on the `deleted_at` column in the migration. The language is directive ("should also add") and the reviewer provides the exact SQL for the index. The reasoning is concrete -- queries filtering by `deleted_at IS NULL` will be frequent in the list endpoint, and without an index these queries will perform full table scans. This is a performance-impacting change that the reviewer is requiring, not merely suggesting as an optional alternative. The reviewer provides specific implementation guidance (the SQL statement), indicating they expect this to be implemented.
