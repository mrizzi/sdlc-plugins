# Review Comment 30002 Classification

**Comment by:** reviewer-a
**File:** `migration/src/m0042_sbom_soft_delete/mod.rs`, line 14
**Text:** The migration should also add an index on `deleted_at` for the sbom table. Queries filtering by `deleted_at IS NULL` will be frequent and a partial index would help. Something like: `CREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;`

## Classification: Suggestion

**Reasoning:**

The reviewer proposes adding a partial index for query performance optimization. While the reviewer uses "should", the context is performance improvement rather than a correctness fix. The qualifier "would help" indicates this is a recommendation for better performance, not a requirement for correctness. The code will function correctly without the index -- queries will just be slower at scale.

This is classified as a suggestion because:
1. It proposes a performance optimization, not a correctness fix
2. The language "would help" indicates it is optional/advisory
3. The absence of the index does not cause incorrect behavior -- only suboptimal query performance
4. No CONVENTIONS.md is available for this repository to determine if index creation on filter columns is a documented convention

**Convention Upgrade Assessment:** No CONVENTIONS.md is available for the trustify-backend repository to check for documented index conventions. Without documented conventions or the ability to inspect the full codebase for migration patterns, this suggestion cannot be upgraded to a code change request based on convention evidence. However, the suggestion has strong technical merit for production readiness.
