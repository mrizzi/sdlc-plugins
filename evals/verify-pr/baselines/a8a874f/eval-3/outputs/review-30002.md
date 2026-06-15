# Review Comment Classification: 30002

## Comment

**Author:** reviewer-a
**File:** migration/src/m0042_sbom_soft_delete/mod.rs (line 14)
**Text:** "The migration should also add an index on `deleted_at` for the sbom table. Queries filtering by `deleted_at IS NULL` will be frequent and a partial index would help. Something like: `CREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;`"

## Classification: Suggestion

## Reasoning

### Language Analysis

The reviewer uses suggestive language rather than directive language:
- "should also add" -- while "should" can be directive in some contexts, "should also" suggests an additional improvement beyond the core requirement, not a mandatory fix
- "would help" -- conditional language indicating a beneficial but optional enhancement
- "Something like:" -- presents the SQL as an illustrative example rather than a required implementation

This contrasts with comment 30001 where the reviewer used imperative "Wrap the three operations" and "use `txn`" -- clear directives. Here, the tone is advisory: the reviewer is proposing a performance optimization that would be beneficial but is not framing it as a required change.

### Convention Upgrade Eligibility Evaluation

To determine whether this suggestion should be upgraded to a code change request, the following convention checks were performed:

1. **CONVENTIONS.md check:** The target repository (trustify-backend) has a CONVENTIONS.md file. However, based on the repository structure and key conventions documented in repo-backend.md, the conventions cover framework choices (Axum, SeaORM), module patterns (model/service/endpoints), error handling, endpoint registration, response types, query helpers, testing, and caching. There is no documented convention requiring indexes on soft-delete columns, on nullable timestamp columns, or on migration files in general.

2. **Codebase pattern check:** The PR diff and repository structure show only one migration file (m0001_initial and the new m0042_sbom_soft_delete). There is insufficient evidence of an established codebase pattern of adding indexes in migration files. The repository structure does not demonstrate a consistent practice of adding partial indexes alongside column additions.

3. **Performance-related scrutiny:** While adding an index on `deleted_at` is a reasonable performance optimization for queries filtering by `deleted_at IS NULL`, this is general database best practice knowledge, not a project-specific convention. The upgrade decision must be based on concrete CONVENTIONS.md documentation or demonstrated codebase patterns, not general industry best practices.

### Conclusion

No convention upgrade is warranted. The suggestion does not match any documented convention in the project, and there is no established codebase pattern of adding indexes in migration files that would justify upgrading this to a code change request. The suggestion remains classified as a **suggestion** -- a valid performance optimization that the PR author may choose to adopt but is not required by project conventions.

## Action

No sub-task created. The suggestion is not backed by a documented project convention or established codebase pattern.
