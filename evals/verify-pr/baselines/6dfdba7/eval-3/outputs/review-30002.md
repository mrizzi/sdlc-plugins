# Review Comment 30002 — Classification

**Comment by:** reviewer-a
**File:** `migration/src/m0042_sbom_soft_delete/mod.rs` (line 14)
**Content:** The migration should also add an index on `deleted_at` for the sbom table, specifically a partial index for `WHERE deleted_at IS NULL` queries.

## Classification: suggestion

## Reasoning

The reviewer proposes adding a partial index on the `deleted_at` column to optimize queries that filter by `deleted_at IS NULL`. This is framed as a performance optimization suggestion ("would help"), not a mandatory correctness fix.

**Initial classification:** suggestion

**Convention check (suggestion upgrade evaluation):**

1. **CONVENTIONS.md check:** The repository has a `CONVENTIONS.md` file at the root, but we cannot access its contents in this context to verify whether it documents index creation patterns for migration files.

2. **Codebase pattern check:** Without access to the actual codebase, we cannot count occurrences of `Index::create` or similar index creation patterns in existing migration files (e.g., `migration/src/m0001_initial/mod.rs` and other migrations) to determine if FK/filter column indexing is a consistent convention.

3. **Performance-related scrutiny:** This is a performance-related suggestion (index creation). The suggestion is reasonable — queries filtering `WHERE deleted_at IS NULL` will run on every list request — but without evidence of an established project convention for index creation in migrations, we cannot upgrade this to a code change request.

**Upgrade decision:** Cannot confirm match with documented or demonstrated convention. Classification remains **suggestion**.

**Final classification:** suggestion

**Action:** No sub-task created. The suggestion is noted in the verification report for the reviewer's consideration.
