# Review Comment Classification: 30002

**Comment ID:** 30002
**Author:** reviewer-a
**File:** `migration/src/m0042_sbom_soft_delete/mod.rs` (line 14)
**Comment text:** "The migration should also add an index on `deleted_at` for the sbom table. Queries filtering by `deleted_at IS NULL` will be frequent and a partial index would help. Something like: `CREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;`"

## Classification: suggestion

## Reasoning

The reviewer proposes adding a partial index on the `deleted_at` column for performance optimization. The language uses "should" and "would help", which is suggestive rather than imperative. The reviewer is proposing an enhancement -- a performance optimization -- rather than identifying a functional defect. The current implementation is functionally correct without the index; queries will work, just potentially slower at scale. No CONVENTIONS.md is available for this repository to check whether index creation on filter columns is a documented convention. Without evidence of an established codebase convention requiring indexes on frequently-filtered columns, this remains classified as a suggestion. The Style/Conventions sub-agent would need to check for codebase patterns (e.g., whether other migrations consistently add indexes for nullable filter columns) to determine if this should be upgraded to a code change request.

**Note:** This suggestion is performance-related and receives extra scrutiny per the convention upgrade check. Without access to the full codebase to verify whether adding indexes on filter columns is an established pattern, it remains a suggestion. If the codebase showed a consistent pattern of adding partial indexes on nullable columns used in WHERE clauses, this would be upgraded to a code change request.
