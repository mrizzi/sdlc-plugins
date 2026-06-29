# Review Comment Classification: 30002

**Reviewer**: reviewer-a
**File**: `migration/src/m0042_sbom_soft_delete/mod.rs`, line 14
**Date**: 2026-04-20T14:35:00Z

## Comment Text

> The migration should also add an index on `deleted_at` for the sbom table. Queries filtering by `deleted_at IS NULL` will be frequent and a partial index would help. Something like:
>
> ```sql
> CREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;
> ```

## Classification: Suggestion

**Reasoning**: The reviewer uses suggestive, non-directive language throughout. Key phrases include "should also add" (additive suggestion, not a correction), "would help" (conditional benefit, not a requirement), and "Something like" (proposing one possible approach rather than dictating a specific fix). The comment proposes a performance optimization -- adding a partial index -- but frames it as an enhancement that would be beneficial, not as a mandatory change to fix a defect.

Unlike comment 30001, which identifies a correctness bug (inconsistent state on partial failure) and uses imperative language ("Wrap the three operations"), comment 30002 identifies a potential future performance concern and presents a possible solution. The index would improve query performance as data grows, but its absence does not cause incorrect behavior, data corruption, or API errors.

### Convention Upgrade Evaluation

The suggestion was evaluated for upgrade to a code change request based on whether it matches a documented or demonstrated project convention.

**Convention evidence examined**:
- The repository structure (repo-backend.md) shows a `CONVENTIONS.md` file exists in the repository root, but its content is not available in the fixture data.
- The "Key Conventions" section in repo-backend.md documents conventions for framework choice (Axum, SeaORM), module structure (`model/ + service/ + endpoints/`), error handling (`Result<T, AppError>` with `.context()`), endpoint registration patterns, response types, query helpers, testing patterns, and caching middleware. None of these conventions mention database indexing requirements for migrations.
- No existing migration files are provided in the fixture data that could demonstrate a pattern of always including indexes alongside new columns.

**Conclusion**: There is no documented convention or demonstrated codebase pattern in the available fixture data that requires migrations adding filterable columns to also include indexes. Without such convention evidence, the suggestion cannot be upgraded. The comment remains classified as a suggestion.

**Action**: No sub-task created. Suggestions without convention backing do not warrant follow-up tasks.
