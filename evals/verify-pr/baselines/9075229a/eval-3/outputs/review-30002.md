# Review Comment Classification: 30002

## Comment

**Author:** reviewer-a
**File:** `migration/src/m0042_sbom_soft_delete/mod.rs`, line 14
**Text:** "The migration should also add an index on `deleted_at` for the sbom table. Queries filtering by `deleted_at IS NULL` will be frequent and a partial index would help. Something like:\n\n```sql\nCREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;\n```"

## Classification: suggestion

## Reasoning

The reviewer uses suggestive language throughout: "should also add" (proposing an additional enhancement beyond the current scope) and "would help" (indicating a benefit rather than a requirement). The comment proposes a performance optimization (a partial index) rather than identifying a correctness defect or a required code change. The reviewer is not saying the code is broken without the index; rather, they are recommending an improvement that "would help" with query performance.

### Convention Upgrade Eligibility

This suggestion was evaluated for convention upgrade per Step 4c and Check 1 of the Style/Conventions sub-agent:

1. **CONVENTIONS.md check:** The repository's `CONVENTIONS.md` was checked for documented conventions requiring index creation on new columns or in migrations. No such convention was found. There is no documented requirement that migrations adding nullable columns must also add indexes.

2. **Codebase pattern check:** The PR diff was searched for patterns demonstrating consistent index creation in migrations (e.g., `Index::create` calls in migration files). The PR diff contains only one migration file (`m0042_sbom_soft_delete/mod.rs`) and it does not include any existing index creation patterns. Without access to other migration files in the diff, there is insufficient evidence of a codebase-wide convention of adding indexes alongside new columns.

3. **Performance-related scrutiny:** While adding an index is a reasonable performance optimization, the upgrade decision requires concrete evidence from the project's own CONVENTIONS.md or demonstrated codebase patterns. General database best practices (e.g., "indexes improve query performance") are explicitly excluded as upgrade evidence per the Style/Conventions sub-agent rules. The upgrade evidence must cite a concrete CONVENTIONS.md section or a counted codebase pattern.

**Conclusion:** No convention upgrade is warranted. The suggestion remains classified as **suggestion** because (a) the reviewer's language is suggestive rather than directive, (b) no documented convention in CONVENTIONS.md backs index creation on new columns, and (c) no established codebase pattern of consistent index creation in migrations was found in the available evidence.

## Action

No sub-task created.
