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

**Reasoning**: The reviewer uses suggestive language throughout the comment. Key phrases:

- "should also add" -- uses "should" in an advisory sense combined with "also", implying this is an addition the reviewer thinks would be beneficial, not a directive correction of existing code.
- "would help" -- conditional/suggestive phrasing indicating the reviewer believes this is a good idea rather than a required change.
- "Something like" -- explicitly frames the SQL example as an approximation or proposal, not a specific required implementation.

These language markers distinguish this from a code change request, where the reviewer uses imperative/directive language to demand a specific modification. Here, the reviewer is proposing an optimization that they believe is beneficial but is not framing it as a blocking requirement.

### Convention Upgrade Evaluation

The suggestion describes adding a partial index on a column used in frequent WHERE clauses, which is a common database performance practice. To upgrade a suggestion to a code change request, the suggestion must match a documented or demonstrated project convention.

**Convention check**: The repository structure in repo-backend.md lists a `CONVENTIONS.md` file in the repository root, but the fixture data does not include the contents of this file. Without access to the actual CONVENTIONS.md content, there is no way to verify whether "adding indexes on filter columns in the same migration" is a documented project convention. A convention upgrade requires evidence from the project's own documentation or demonstrated patterns -- general database best practices alone are insufficient.

**Conclusion**: The suggestion is NOT eligible for convention upgrade because:
1. The CONVENTIONS.md contents are not available in the fixture data to verify a matching convention.
2. No other migration files are provided to demonstrate a pattern of index creation alongside column additions.
3. General industry best practices (adding indexes on frequently-filtered columns) do not substitute for project-specific convention documentation.

The suggestion remains classified as a suggestion. It is a reasonable performance optimization recommendation, but without convention backing it does not warrant a sub-task.

**Action**: No sub-task created. This is a suggestion without convention backing.
