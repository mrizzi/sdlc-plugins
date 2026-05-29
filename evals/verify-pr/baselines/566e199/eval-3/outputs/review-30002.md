# Review Comment Classification: 30002

## Comment

**Author:** reviewer-a
**File:** `migration/src/m0042_sbom_soft_delete/mod.rs`, line 14
**Text:** "The migration should also add an index on `deleted_at` for the sbom table. Queries filtering by `deleted_at IS NULL` will be frequent and a partial index would help. Something like: `CREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;`"

## Classification: suggestion

## Reasoning

The reviewer uses suggestive language: "should also add", "would help", "Something like". The phrase "should also" proposes an addition beyond the current scope rather than identifying a defect in existing code. "Would help" frames the recommendation as beneficial but not strictly required. "Something like" further signals this is a proposed approach, not a mandated change.

### Convention upgrade eligibility check

To determine whether this suggestion should be upgraded to a code change request, I checked for documented or demonstrated conventions:

1. **CONVENTIONS.md check:** The repo-backend has a CONVENTIONS.md file, but based on the repository structure and key conventions listed (Framework: Axum/SeaORM, Module pattern, Error handling, Endpoint registration, Response types, Query helpers, Testing, Caching), there is no documented convention requiring indexes on soft-delete columns or on foreign key columns in migrations.

2. **Codebase pattern check:** The PR diff only includes one migration file (`m0042_sbom_soft_delete/mod.rs`). The repository structure shows only `m0001_initial/mod.rs` as another migration. Without evidence of a consistent pattern of adding indexes in migration files across the codebase, there is no demonstrated convention to cite.

Since no documented convention in CONVENTIONS.md and no demonstrated codebase pattern (counted occurrences) support this practice as an established project convention, the suggestion is NOT upgraded. General database best practices ("indexes are good for frequently filtered columns") are not sufficient grounds for upgrade per the convention upgrade rules.

## Sub-task required: No
