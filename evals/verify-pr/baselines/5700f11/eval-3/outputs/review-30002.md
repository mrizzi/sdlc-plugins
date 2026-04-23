# Review Comment Classification: 30002

**Comment ID:** 30002
**Reviewer:** reviewer-a
**File:** `migration/src/m0042_sbom_soft_delete/mod.rs` (line 14)
**Comment:** The migration should also add an index on `deleted_at` for the sbom table. Queries filtering by `deleted_at IS NULL` will be frequent and a partial index would help. Something like: `CREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;`

## Classification: Code Change Request

## Reasoning

The reviewer uses directive language ("should also add an index") and provides a specific SQL example for a partial index. This is not framed as an optional suggestion -- the reviewer identifies a concrete performance concern: the list endpoint filters by `deleted_at IS NULL` on every default query, and without an index, these queries will degrade as the table grows.

The comment requests a specific code change to the migration file with a concrete implementation. The performance rationale is sound: the `list` endpoint applies `filter(sbom::Column::DeletedAt.is_null())` by default on every list request, making this a high-frequency query path. Adding a partial index is a well-established database practice for soft-delete patterns.

This is classified as a code change request because:
1. The language is directive ("should also add"), not suggestive ("you might consider")
2. The fix is concrete and specific (partial index with exact SQL provided)
3. It addresses a real performance concern on a high-frequency query path

## Action

Sub-task created. See `subtask-30002.md` for the full sub-task description.
