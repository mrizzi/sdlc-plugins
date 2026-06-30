# Review Comment Classification: 30002

## Comment

**Author:** reviewer-a
**File:** `migration/src/m0042_sbom_soft_delete/mod.rs` (line 14)
**Text:** The migration should also add an index on `deleted_at` for the sbom table. Queries filtering by `deleted_at IS NULL` will be frequent and a partial index would help. Something like:
```sql
CREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;
```

## Classification: SUGGESTION

## Reasoning

The reviewer uses suggestive language: "should also add" and "would help." This proposes an improvement (adding a database index) that is not required for functional correctness of the feature. The soft-delete endpoint works correctly without the index; the index is a performance optimization.

### Convention Upgrade Eligibility

Convention upgrade was evaluated and rejected for the following reasons:

1. **CONVENTIONS.md check:** The target repository's CONVENTIONS.md documents conventions for Framework (Axum, SeaORM), Module pattern, Error handling, Endpoint registration, Response types, Query helpers, Testing, and Caching. It does NOT contain any section on index creation patterns, migration-specific conventions, or database performance conventions. There is no documented convention that requires adding indexes on new columns in migrations.

2. **Codebase pattern check:** The PR diff contains exactly one migration file (`m0042_sbom_soft_delete/mod.rs`), which is the new migration being added. There are no other migration files visible in the PR diff, so there is no way to count instances of `Index::create` or similar index-creation patterns to establish a codebase convention. Zero occurrences of index creation patterns were found in the available diff.

3. **Performance-related scrutiny:** Per the Style/Conventions sub-agent guidelines, performance-related suggestions (indexes, caching, query optimization) receive extra scrutiny. The PR diff and available CONVENTIONS.md content contain no dedicated performance-related patterns such as retroactive index migrations, caching layers, or documented performance conventions.

4. **General best practices are insufficient:** While adding indexes on frequently-filtered columns is a general database best practice, the convention upgrade mechanism requires evidence from the specific project -- either a CONVENTIONS.md section or a counted codebase pattern. General industry knowledge ("indexes are a database best practice") does not qualify as project-specific convention evidence.

Since no documented or demonstrated project convention supports this suggestion, it remains classified as SUGGESTION. No sub-task is created.
