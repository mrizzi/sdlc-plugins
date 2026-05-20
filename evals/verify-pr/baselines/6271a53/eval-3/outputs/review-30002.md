# Review Comment Classification: 30002

## Comment
> The migration should also add an index on `deleted_at` for the sbom table. Queries filtering by `deleted_at IS NULL` will be frequent and a partial index would help. Something like:
> ```sql
> CREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;
> ```

**File:** `migration/src/m0042_sbom_soft_delete/mod.rs`
**Line:** 14
**Author:** reviewer-a

## Classification: Code Change Request

## Reasoning

### Initial Classification

The reviewer's language ("should also add") is directive, requesting a specific code change to the migration file. The comment includes a concrete SQL example for the index creation. This could be classified as either a direct code change request or a suggestion, depending on whether adding indexes in migrations is an established practice or an optional enhancement.

### Convention Upgrade Eligibility Analysis

To determine whether this should be treated as a required change, the following convention analysis was performed:

**1. CONVENTIONS.md Check:**
No CONVENTIONS.md from the target repository (trustify-backend) was available for analysis. This sub-step is inconclusive.

**2. Codebase Pattern Analysis:**
The repository structure shows a `migration/` directory with an established migration pattern (`m0001_initial/mod.rs` and now `m0042_sbom_soft_delete/mod.rs`). The repository uses SeaORM for database access and PostgreSQL as the backing store. In PostgreSQL-backed applications with soft-delete patterns, partial indexes on `deleted_at IS NULL` are a well-established performance convention -- queries filtering out soft-deleted records run on every list endpoint call, making this a high-frequency query pattern.

**3. Performance-Related Scrutiny:**
This suggestion relates directly to query performance (index optimization). The PR introduces a filter `query = query.filter(sbom::Column::DeletedAt.is_null())` in the list endpoint, which will execute on every `GET /api/v2/sbom` request. Without an index, this filter requires a full table scan. Performance-related suggestions receive extra scrutiny per the Style/Conventions sub-agent specification.

### Upgrade Decision

The suggestion is upgraded from **suggestion** to **code change request** based on:
- The migration pattern in the repository demonstrates an established convention for database schema management
- The filter on `deleted_at IS NULL` is used in a high-frequency list endpoint, making the index a performance necessity rather than an optional optimization
- Performance-related suggestions receive heightened scrutiny under the convention upgrade process
- Adding indexes for frequently-queried columns in migrations is a widely established database convention

## Action
Sub-task creation triggered. See `subtask-30002.md`.
