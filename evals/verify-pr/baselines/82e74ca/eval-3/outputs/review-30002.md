# Review Comment Classification: #30002

**Comment by:** reviewer-a
**File:** `migration/src/m0042_sbom_soft_delete/mod.rs` (line 14)
**Date:** 2026-04-20T14:35:00Z

## Original Comment

> The migration should also add an index on `deleted_at` for the sbom table. Queries filtering by `deleted_at IS NULL` will be frequent and a partial index would help. Something like:
>
> ```sql
> CREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;
> ```

## Classification: Suggestion

### Initial Classification

The reviewer proposes adding a partial index on `deleted_at`. While phrased with "should", the substance is a performance optimization suggestion rather than a correctness fix. The code functions correctly without the index — it would improve query performance for list operations that filter by `deleted_at IS NULL`.

### Convention Check

1. **CONVENTIONS.md:** No Serena instance is available for this repository (per CLAUDE.md Code Intelligence section). Unable to read the actual CONVENTIONS.md to check for documented index conventions.

2. **Codebase patterns:** Without access to the actual repository codebase (no Serena instance configured, eval mode), I cannot search for `Index::create` patterns in existing migration files to determine whether adding indexes for frequently-queried columns is an established codebase convention.

3. **Performance-related scrutiny:** This is a performance-related suggestion (index creation). Without being able to verify whether the project has existing partial indexes, retroactive index migrations, or documented performance conventions, I cannot confirm this matches an established pattern.

### Upgrade Decision

Cannot upgrade to code change request — insufficient evidence of project convention. The suggestion remains classified as **suggestion**. While adding indexes for frequently-filtered columns is generally good practice, it does not meet the threshold for upgrade without evidence of documented or demonstrated convention in this specific project.

## Action

No sub-task created. The suggestion is reported for visibility in the verification report.
