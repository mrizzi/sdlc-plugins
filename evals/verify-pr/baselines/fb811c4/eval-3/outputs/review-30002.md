# Review Comment Classification: 30002

## Comment

**Author:** reviewer-a
**File:** migration/src/m0042_sbom_soft_delete/mod.rs:14
**Text:** "The migration should also add an index on `deleted_at` for the sbom table. Queries filtering by `deleted_at IS NULL` will be frequent and a partial index would help. Something like: `CREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;`"

## Classification: suggestion

## Reasoning

The reviewer uses suggestive language throughout this comment:

1. **"should also"** -- the phrase "should also" is additive and suggestive, indicating this is an enhancement on top of the existing work rather than a required correction. The word "also" signals this goes beyond the scope of the current task.

2. **"would help"** -- the phrase "would help" is conditional/suggestive language indicating a potential benefit rather than a directive requirement. Compare this with comment 30001 which uses "should run" (directive) and "Wrap the three operations" (imperative).

3. **"Something like:"** -- this phrasing proposes an example approach rather than prescribing a specific fix. It leaves the exact implementation open-ended, consistent with a suggestion rather than a requirement.

The comment proposes a performance optimization (adding an index) that is a reasonable database best practice, but it does not identify a bug, correctness issue, or violation of project conventions.

## Convention Upgrade Evaluation

The suggestion was evaluated for convention upgrade eligibility per Step 6b:

- **CONVENTIONS.md check:** No CONVENTIONS.md file exists in the fixture data for the trustify-backend repository. Therefore, no documented convention about index creation on nullable filter columns could be found.

- **Codebase pattern check:** The PR diff contains only one migration file (m0042_sbom_soft_delete/mod.rs). No other migration files are present in the diff to establish a codebase pattern of index creation. Without access to the full repository (eval mode), no counted codebase pattern can be demonstrated.

- **Conclusion:** The suggestion does NOT qualify for convention upgrade. While adding an index on `deleted_at` is a reasonable database best practice, general best practices are not sufficient for upgrade -- a concrete CONVENTIONS.md section or a counted codebase pattern is required. The suggestive language classification is correct and the suggestion remains as-is.

## Action

No sub-task created. This is a valid suggestion for the PR author to consider, but it does not meet the threshold for a tracked code change request.
