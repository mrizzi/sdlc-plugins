# Review Comment 30002 — Classification

**Comment by:** reviewer-a
**File:** `migration/src/m0042_sbom_soft_delete/mod.rs` (line 14)
**Text:** The migration should also add an index on `deleted_at` for the sbom table. Queries filtering by `deleted_at IS NULL` will be frequent and a partial index would help. Something like: `CREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;`

## Classification: Suggestion

### Reasoning

The reviewer proposes adding a partial index on the `deleted_at` column to optimize queries that filter by `deleted_at IS NULL`. The language ("should also add", "would help") is suggestive rather than imperative. While the suggestion is technically sound -- partial indexes for soft-delete columns are a well-known database optimization -- this is a performance optimization, not a correctness issue.

### Convention Check

This is a performance-related suggestion, which warrants extra scrutiny per the verification process:

1. **CONVENTIONS.md:** The target repository (`trustify-backend`) has a `CONVENTIONS.md` file, but its contents are not available for inspection. We cannot confirm whether index creation for frequently-filtered columns is a documented convention.

2. **Codebase patterns:** Without access to the actual repository files, we cannot count occurrences of `Index::create` or similar patterns in existing migration files to determine whether FK/filter index creation is a consistent practice.

3. **Upgrade decision:** Without confirmed evidence from either CONVENTIONS.md or codebase pattern analysis, the suggestion cannot be upgraded to a code change request. It remains classified as a **suggestion**.

### Action

No sub-task created. The suggestion is valid and the PR author may choose to implement it, but it does not meet the threshold for a mandatory code change request without confirmed convention evidence.
