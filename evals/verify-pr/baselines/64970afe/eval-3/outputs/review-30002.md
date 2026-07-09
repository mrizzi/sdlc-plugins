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

## Classification: suggestion

## Reasoning

The reviewer uses suggestive language rather than directive language:

1. "should also add" -- while "should" can be directive, "also" softens it to an additive recommendation beyond the core scope
2. "would help" -- conditional/suggestive phrasing indicating this is a nice-to-have, not a requirement
3. "Something like:" -- explicitly frames the code example as one possible approach, not the required implementation

This contrasts with comment 30001, where the reviewer uses imperative language ("Wrap the three operations") and identifies a concrete correctness defect. Comment 30002 describes a performance optimization that would be beneficial but is not a correctness issue -- the code functions correctly without the index, just with potentially slower list queries as data grows.

### Convention Upgrade Evaluation

The comment was evaluated for convention upgrade eligibility -- whether a documented or demonstrated project convention would warrant upgrading this suggestion to a code change request.

**CONVENTIONS.md check**: The repository structure (repo-backend.md) indicates a `CONVENTIONS.md` file exists at the root. However, the fixture data does not include the contents of `CONVENTIONS.md`, so no specific convention about index creation in migrations can be verified.

**Codebase pattern check**: The fixture data provides only the repository directory tree and key conventions summary. The key conventions listed in repo-backend.md cover framework choices (Axum, SeaORM), module patterns, error handling, endpoint registration, response types, query helpers, testing, and caching. None of these documented conventions address index creation requirements in migration files.

**Conclusion**: No documented project convention in the available fixture data supports upgrading this suggestion to a code change request. While adding an index on a frequently-filtered column is generally good practice, the convention upgrade requires evidence from the specific project's documented conventions or demonstrated patterns -- not general database best practices. The suggestion remains classified as a suggestion.

## Action

No sub-task created. Suggestions are informational feedback that do not require tracked work unless upgraded via convention evidence.
