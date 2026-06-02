# Review Comment Classification: 30002

## Comment
**Author:** reviewer-a
**File:** `migration/src/m0042_sbom_soft_delete/mod.rs`, line 14
**Body:** The migration should also add an index on `deleted_at` for the sbom table. Queries filtering by `deleted_at IS NULL` will be frequent and a partial index would help. Something like:
```sql
CREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;
```

## Classification: code change request

## Reasoning
The reviewer requests a specific code modification: adding a partial index on the `deleted_at` column in the migration file. While the word "should" could indicate a suggestion, the reviewer provides a concrete SQL statement for the index and explains the performance rationale (frequent queries filtering by `deleted_at IS NULL`). The reviewer is requesting an addition to the migration, not proposing an optional alternative approach. This is a code change request because the reviewer states what "should" be done and provides the exact implementation, indicating an expectation that this change will be made.
