# Review Comment Classification: 30002

## Comment

**Author:** reviewer-a
**File:** `migration/src/m0042_sbom_soft_delete/mod.rs`, line 14
**Text:** "The migration should also add an index on `deleted_at` for the sbom table. Queries filtering by `deleted_at IS NULL` will be frequent and a partial index would help. Something like:\n\n```sql\nCREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;\n```"

## Classification: code change request

## Reasoning

### Initial Classification

The reviewer's language uses "should also add", which is directive and requests a specific code change to the migration file. The reviewer provides a concrete SQL example for the index. While one could argue this is a suggestion because it proposes an optimization rather than fixing a bug, the directive phrasing ("should also add") and the concrete implementation detail push this toward a code change request.

### Convention Upgrade Eligibility Analysis

Regardless of whether this is initially classified as a code change request or a suggestion, the Style/Conventions sub-agent would evaluate it for convention upgrade eligibility:

1. **CONVENTIONS.md check:** The repository has a `CONVENTIONS.md` file at its root (listed in repo-backend.md directory tree). This file would need to be checked for documented conventions around index creation in migrations. Database indexing conventions for foreign key columns and frequently-filtered columns are a common documented practice.

2. **Codebase pattern check:** The trustify-backend repository uses SeaORM migrations (as demonstrated by the existing `migration/src/m0001_initial/mod.rs` and the new `m0042_sbom_soft_delete/mod.rs`). With 42 migrations in the codebase, there are likely established patterns for index creation. If multiple prior migrations create indexes for columns used in filtering, this would constitute a demonstrated codebase convention.

3. **Performance-related scrutiny:** This suggestion relates to database query performance (index for filtered queries). Per the Style/Conventions sub-agent's Check 1c, performance-related suggestions receive extra scrutiny, making convention upgrade more likely if any supporting patterns exist.

### Decision

This comment is classified as a **code change request** -- either directly (due to the directive "should" language) or via convention upgrade (if initially classified as a suggestion, the performance-related convention analysis would upgrade it). Either classification path leads to sub-task creation.

**Sub-task required:** Yes -- this feedback triggers sub-task creation.
