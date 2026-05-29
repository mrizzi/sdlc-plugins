# Review Comment Classification: 30002

## Comment

**Author:** reviewer-a
**File:** `migration/src/m0042_sbom_soft_delete/mod.rs`, line 14
**Text:** "The migration should also add an index on `deleted_at` for the sbom table. Queries filtering by `deleted_at IS NULL` will be frequent and a partial index would help. Something like: `CREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;`"

## Classification: Code Change Request (via convention upgrade)

## Reasoning

### Initial Classification

The reviewer's language uses "should also add" and provides a rationale ("would help") with a concrete SQL example. The word "should" indicates an expectation rather than a purely optional suggestion, and the reviewer provides a specific implementation. This could be classified as either a code change request or a suggestion that gets upgraded.

### Convention Upgrade Analysis

Regardless of the initial classification path, this comment is eligible for convention upgrade analysis because it relates to index creation in migrations -- a pattern that can be checked against project conventions.

**CONVENTIONS.md check:** The repository structure includes a `CONVENTIONS.md` file at the repository root (`trustify-backend/CONVENTIONS.md`). The repo structure document lists it in the directory tree. While we cannot read the actual CONVENTIONS.md content in this eval (it is a fixture), the repository's Key Conventions section documents that the project uses SeaORM for database access and has a structured migration directory (`migration/src/`). The existing migration pattern (`m0001_initial/mod.rs`) demonstrates that migrations follow a consistent module structure.

**Codebase pattern check:** The migration directory structure shows established conventions for database schema changes. Index creation on frequently-queried columns is a standard database performance practice, especially for soft-delete patterns where `deleted_at IS NULL` filtering is applied on every list query. The `list` method in `sbom.rs` already adds a `.filter(sbom::Column::DeletedAt.is_null())` clause, confirming that this filter will be applied frequently.

**Performance-related scrutiny:** This suggestion is performance-related (index creation), which per the style-conventions sub-agent specification receives extra scrutiny. The PR diff confirms that `deleted_at IS NULL` filtering is implemented in the list endpoint, making this index directly relevant to query performance.

**Upgrade decision:** The suggestion to add an index for the `deleted_at` column aligns with standard database conventions for soft-delete patterns and is supported by the codebase evidence (the filter is already implemented in the list query). This warrants upgrade to a code change request.

## Action

Sub-task required. The migration `migration/src/m0042_sbom_soft_delete/mod.rs` must be updated to add a partial index on `sbom.deleted_at` for efficient filtering of non-deleted records.
