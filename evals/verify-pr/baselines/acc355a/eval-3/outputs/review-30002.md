# Review Comment Classification: 30002

## Comment

**Author**: reviewer-a
**File**: `migration/src/m0042_sbom_soft_delete/mod.rs`, line 14
**Text**: The migration should also add an index on `deleted_at` for the sbom table. Queries filtering by `deleted_at IS NULL` will be frequent and a partial index would help. Something like:

```sql
CREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;
```

## Classification: CODE CHANGE REQUEST

## Reasoning

The reviewer is requesting a specific code change to the migration file -- adding a partial index on the `deleted_at` column. While the comment is phrased as a suggestion ("should also add"), it meets the criteria for a code change request because:

1. **It requests a concrete modification**: Add an index creation step to the migration.
2. **It provides exact implementation guidance**: The reviewer supplies the SQL for the partial index (`CREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL`).
3. **It addresses a performance concern**: The list endpoint filters by `deleted_at IS NULL` on every request, and without an index this becomes a sequential scan as the table grows.

### Convention Upgrade Eligibility Evaluation

Convention upgrade eligibility was evaluated. The repository's `CONVENTIONS.md` file was noted in the repo structure, and the key conventions listed in `repo-backend.md` include guidance on query helpers and shared patterns. While no explicit convention about "all filter columns must be indexed" was found in the available repo documentation, the reviewer's request is independently strong enough to classify as a code change request without needing convention-based upgrade. The comment prescribes a specific schema change with exact SQL, which goes beyond a suggestion into an actionable code change request.

Even if this were initially classified as a suggestion, it would warrant upgrade consideration because:
- Frequent query patterns on unindexed columns represent a performance risk
- The reviewer provided exact implementation details, indicating this is a firm expectation rather than an optional idea

## Action

Sub-task created: subtask-30002.md
