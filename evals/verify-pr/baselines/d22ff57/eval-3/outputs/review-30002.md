# Review Comment Classification: 30002

## Comment

> The migration should also add an index on `deleted_at` for the sbom table. Queries filtering by `deleted_at IS NULL` will be frequent and a partial index would help. Something like:
>
> ```sql
> CREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;
> ```

**File:** `migration/src/m0042_sbom_soft_delete/mod.rs`
**Line:** 14
**Reviewer:** reviewer-a

## Classification: code change request

## Reasoning

The reviewer's language ("should also add") is directive, requesting a specific code change to the migration file. While this could initially be viewed as a suggestion (proposing an optimization), it warrants upgrade to a code change request for the following reasons:

1. **Performance-related scrutiny:** The suggestion relates to database indexing for a query pattern (`deleted_at IS NULL`) that will be executed on every list request. This falls under the performance-related scrutiny guideline, which mandates extra scrutiny for index, caching, and query optimization suggestions.

2. **Codebase convention alignment:** Adding indexes for columns used in frequent filter conditions is a widely established database convention. The `list` endpoint filters by `deleted_at IS NULL` on every call, making this a high-frequency query path. Partial indexes for soft-delete patterns are a well-known best practice in PostgreSQL-backed applications.

3. **Directive language:** The reviewer uses "should also add" rather than "you might consider" or "what do you think about", indicating this is expected rather than optional.

This is classified as a **code change request** and requires a sub-task.
