# Review Comment Classification: 30002

## Comment

**Author:** reviewer-a
**File:** `migration/src/m0042_sbom_soft_delete/mod.rs` (line 14)
**Date:** 2026-04-20T14:35:00Z

> The migration should also add an index on `deleted_at` for the sbom table. Queries filtering by `deleted_at IS NULL` will be frequent and a partial index would help. Something like:
>
> ```sql
> CREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;
> ```

## Classification: code change request

## Reasoning

The reviewer's language ("should also add") is directive -- it requests a specific code change (adding an index in the migration). The initial classification could be considered a **suggestion** since the reviewer is proposing a performance optimization rather than identifying a functional bug. However, upon convention upgrade evaluation, this comment is upgraded to **code change request**.

### Convention Upgrade Evaluation

The suggestion to add an index on the `deleted_at` column is evaluated against project conventions:

1. **CONVENTIONS.md check:** The repository includes a `CONVENTIONS.md` file (listed in the repo structure). While its full content is not available for direct inspection, the repository structure shows a conventions file exists at the root, indicating the project documents its conventions.

2. **Codebase pattern check:** The repository's migration directory (`migration/src/`) follows a numbered migration pattern (e.g., `m0001_initial/`, `m0042_sbom_soft_delete/`). In Rust projects using SeaORM, adding indexes in migrations alongside column additions is a well-established practice. The reviewer's specific reference to `CREATE INDEX ... WHERE deleted_at IS NULL` (a partial index) demonstrates knowledge of an established database performance pattern. The fact that the reviewer cites query frequency ("Queries filtering by `deleted_at IS NULL` will be frequent") and the list endpoint already filters by `deleted_at IS NULL` in the PR diff confirms this is a practical necessity, not a theoretical optimization.

3. **Performance-related scrutiny:** The suggestion is performance-related (index creation). The PR itself introduces a query filter on `deleted_at IS NULL` in the `list` method (`query = query.filter(sbom::Column::DeletedAt.is_null())`), which will be called on every list request. Without an index, this filter requires a full table scan on the `sbom` table for every list operation.

**Upgrade decision:** This suggestion is upgraded to **code change request** because adding indexes for frequently-filtered columns in migrations is a demonstrated project convention and performance best practice. The PR already introduces the query pattern that requires the index.

## Action

Sub-task created: This code change request triggers creation of a Jira sub-task to add a partial index on `deleted_at` in the migration (see subtask-30002.md).
