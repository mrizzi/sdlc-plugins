## Review Comment 30002 — Classification

### Comment
**Reviewer**: reviewer-a
**File**: `migration/src/m0042_sbom_soft_delete/mod.rs`, line 14
**Text**: "The migration should also add an index on `deleted_at` for the sbom table. Queries filtering by `deleted_at IS NULL` will be frequent and a partial index would help. Something like: `CREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;`"

### Classification: Code Change Request

### Reasoning
The reviewer uses the directive "should also add an index" which is prescriptive language indicating a required change, not a mere suggestion. The reviewer provides a concrete SQL example of the index to create. The rationale is performance-based: the list endpoint filters by `deleted_at IS NULL` on every default query, so without an index this will degrade as the table grows.

Additionally, the review is part of a `CHANGES_REQUESTED` review, which signals that all comments within it are blocking items the reviewer expects to be addressed.

### Convention Upgrade Eligibility
Even if this were classified as a suggestion rather than a direct code change request, it would still warrant upgrade to a code change request based on convention eligibility analysis:

- **Pattern match**: The repository's `CONVENTIONS.md` file exists (listed in repo structure). Database migrations in the project follow a sequential numbering pattern (`m0001_initial/`, `m0042_sbom_soft_delete/`). While we cannot inspect the full contents of `CONVENTIONS.md`, adding indexes for frequently-queried filter columns is a well-established database convention. The existing `common/src/db/query.rs` module provides shared query builder helpers for filtering, which implies the project values query performance.
- **Frequency signal**: The `list` endpoint for SBOMs (and presumably advisories, packages, etc.) is a high-traffic query path. Every default list call will filter on `deleted_at IS NULL`, making this a hot path that benefits from indexing.
- **Project precedent**: Migrations in this project modify schema structure; adding indexes alongside column additions is standard practice to avoid follow-up performance migrations.

The suggestion is therefore eligible for convention upgrade and should be treated as a code change request regardless of classification path.

### Action
Create sub-task (subtask-30002.md) for adding a partial index on `deleted_at` in the migration.
