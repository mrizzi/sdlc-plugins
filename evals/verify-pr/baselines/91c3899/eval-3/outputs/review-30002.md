# Review Comment Classification: 30002

## Comment

**Author:** reviewer-a
**File:** `migration/src/m0042_sbom_soft_delete/mod.rs`, line 14
**Text:**
> The migration should also add an index on `deleted_at` for the sbom table. Queries filtering by `deleted_at IS NULL` will be frequent and a partial index would help. Something like:
>
> ```sql
> CREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;
> ```

## Classification: SUGGESTION

## Reasoning

The reviewer uses suggestive, non-directive language:

1. **"should also"** -- this is additive guidance ("also"), not a correction of an existing defect. The word "should" here is advisory rather than imperative because it introduces a new concern not present in the task requirements.
2. **"would help"** -- this is explicitly suggestive language indicating a potential improvement, not a required change. It acknowledges the change is beneficial but does not assert it is mandatory.
3. **"Something like"** -- this phrasing proposes an approach without insisting on it, leaving room for the author to decide.

The comment proposes adding a database index as a performance optimization. While adding indexes for frequently queried columns is a reasonable database practice, the reviewer's language frames this as a recommendation rather than a requirement.

### Convention Upgrade Eligibility Evaluation

To determine whether this suggestion should be upgraded to a code change request, the following convention sources were evaluated:

1. **CONVENTIONS.md:** The repo-backend.md fixture describes a repository structure with a CONVENTIONS.md file present at the root. However, the fixture data does not provide the contents of CONVENTIONS.md. The Key Conventions section in repo-backend.md documents framework choices (Axum, SeaORM), module patterns, error handling, endpoint registration, response types, query helpers, testing patterns, and caching -- but does **not** document any convention about index creation for new columns or migrations.

2. **Codebase patterns:** The fixture data includes only the PR diff and repository structure. No evidence of existing migration files creating indexes is available in the provided data. The single migration visible in the repo structure (`m0001_initial/mod.rs`) is not included in the fixture content, so no codebase pattern count can be established.

3. **Task specification:** The task description (TC-9103) does not mention index creation in its Files to Modify, Implementation Notes, or Acceptance Criteria sections.

**Conclusion:** Without documented convention evidence in CONVENTIONS.md or demonstrated codebase patterns in the fixture data, there is no basis to upgrade this suggestion to a code change request. The upgrade requires citing a concrete CONVENTIONS.md section or a counted codebase pattern -- general knowledge that "indexes are a database best practice" is not sufficient per the Style/Conventions sub-agent rules (Check 1d).

## Action

No sub-task created. The suggestion remains classified as a suggestion.
