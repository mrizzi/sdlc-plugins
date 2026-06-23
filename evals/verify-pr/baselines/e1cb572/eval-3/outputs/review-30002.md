# Review Comment Classification: 30002

## Comment

**Author:** reviewer-a
**File:** `migration/src/m0042_sbom_soft_delete/mod.rs` (line 14)
**Text:** "The migration should also add an index on `deleted_at` for the sbom table. Queries filtering by `deleted_at IS NULL` will be frequent and a partial index would help. Something like: `CREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;`"

## Classification: suggestion

## Reasoning

The reviewer uses suggestive language: "should also add", "would help", "Something like". The phrase "should also" proposes an addition beyond the current scope rather than requesting a correction to existing code. The phrase "would help" indicates an optional performance improvement, not a required fix. The reviewer is suggesting a performance optimization (adding a partial index) that is not part of the task's acceptance criteria or implementation notes.

### Convention Upgrade Eligibility

This suggestion was evaluated for convention upgrade eligibility per the Style/Conventions sub-agent's Check 1 process:

1. **CONVENTIONS.md check:** The repository has a CONVENTIONS.md but it does not document index creation patterns for migration files. There is no section covering indexing conventions, partial index requirements, or migration best practices related to indexes. Without an explicit documented convention, this criterion is not met.

2. **Codebase pattern check:** The PR diff does not contain evidence of a consistent codebase pattern for adding indexes alongside new columns in migrations. Only one migration file is present in this PR (`m0042_sbom_soft_delete/mod.rs`), and the diff does not show other migration files that demonstrate an established index creation pattern. Without counted evidence of a consistent codebase practice (e.g., "N out of M migrations add indexes for filter columns"), this criterion is not met.

3. **Performance-related scrutiny:** While adding indexes is a general database best practice, the upgrade decision requires project-specific evidence -- either a documented convention in CONVENTIONS.md or a demonstrated codebase pattern with multiple instances. General industry best practices ("indexes are good for query performance") are explicitly excluded from upgrade criteria. The convention upgrade process requires citing a concrete CONVENTIONS.md section or a counted codebase pattern; general knowledge is not sufficient.

**Conclusion:** The suggestion does not qualify for upgrade to code change request because neither CONVENTIONS.md nor counted codebase patterns support it. It remains classified as a suggestion. No sub-task created.
