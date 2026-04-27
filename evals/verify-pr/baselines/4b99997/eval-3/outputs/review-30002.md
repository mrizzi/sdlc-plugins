# Review Comment Classification: #30002

**Comment by:** reviewer-a
**File:** `migration/src/m0042_sbom_soft_delete/mod.rs`, line 14
**Date:** 2026-04-20T14:35:00Z

## Original Comment

> The migration should also add an index on `deleted_at` for the sbom table. Queries filtering by `deleted_at IS NULL` will be frequent and a partial index would help. Something like:
>
> ```sql
> CREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;
> ```

## Classification: code change request (upgraded from suggestion)

## Reasoning

### Initial Classification: suggestion

The reviewer proposes adding a partial index on `deleted_at` for the sbom table. The phrasing "should also add an index" and "a partial index would help" initially reads as a suggestion -- the reviewer is recommending a performance improvement rather than fixing a correctness bug.

### Convention Check: upgraded to code change request

Per the SKILL.md Step 4c convention check process, suggestions related to performance receive extra scrutiny. This comment involves:

1. **Performance-related scrutiny:** The suggestion concerns database indexing, which falls squarely into the performance category. The `list` endpoint will filter by `deleted_at IS NULL` on every call, making this a hot query path. Without an index, this becomes a full table scan as the sbom table grows.

2. **Codebase pattern analysis:** The repository follows a migration-based schema management pattern (migration directory with numbered migrations). Database indexing for frequently-queried columns is a standard practice in production backend services, and the project structure (SeaORM, PostgreSQL) supports this pattern.

3. **Practical impact:** The `list_sboms` function adds `.filter(sbom::Column::DeletedAt.is_null())` to every list query when `include_deleted` is false (the default). This means the vast majority of list queries will filter on this column, making an index operationally important.

**Upgrade decision:** The suggestion is upgraded to a code change request because it addresses a performance concern on a hot query path, aligns with standard database indexing practices for soft-delete patterns, and the reviewer provides specific implementation guidance (partial index with WHERE clause).

**Classification:** code change request (upgraded from suggestion) -- triggers sub-task creation (subtask-30002.md).
