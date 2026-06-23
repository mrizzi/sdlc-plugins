## Review Comment 30002 — Classification

**Comment ID:** 30002
**Author:** reviewer-a
**File:** migration/src/m0042_sbom_soft_delete/mod.rs
**Line:** 14
**Content:** The migration should also add an index on `deleted_at` for the sbom table. Queries filtering by `deleted_at IS NULL` will be frequent and a partial index would help. Something like: `CREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;`

### Classification: suggestion

### Reasoning

The reviewer proposes adding a partial index on the `deleted_at` column to improve query performance. While the language uses "should," the rationale is performance optimization ("would help"), not a correctness requirement. The migration works correctly without the index — queries filtering by `deleted_at IS NULL` will function properly, just potentially slower at scale.

To determine whether this suggestion should be upgraded to a code change request, the Convention Upgrade check was performed:

1. **CONVENTIONS.md check:** CONVENTIONS.md content for the trustify-backend repository is not available. No documented convention about adding indexes for new columns or migration patterns could be verified.
2. **Codebase pattern check:** Without access to the full repository codebase, no demonstrated pattern of adding indexes alongside new columns in migrations could be verified.
3. **General best practice exclusion:** Adding partial indexes is a recognized database optimization best practice, but the upgrade decision requires evidence from the specific project's conventions or demonstrated codebase patterns, not general industry knowledge.

Since no project-specific convention or codebase pattern supports this suggestion, it remains classified as a suggestion. No sub-task created.

### Action

No sub-task created.
