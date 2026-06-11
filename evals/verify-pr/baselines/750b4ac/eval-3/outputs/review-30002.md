## Review Comment 30002 -- Classification: suggestion

**Comment:** "The migration should also add an index on `deleted_at` for the sbom table. Queries filtering by `deleted_at IS NULL` will be frequent and a partial index would help. Something like: `CREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;`"

**File:** migration/src/m0042_sbom_soft_delete/mod.rs, line 14

**Classification reasoning:**

The reviewer proposes adding an index as a performance optimization. The language uses suggestive phrasing:
- "should also add" -- advisory tone, not a directive requirement
- "would help" -- conditional language indicating this is a recommendation, not a mandate

**Convention upgrade eligibility evaluation:**

Per Step 4c and the Style/Conventions sub-agent's Check 1 (Convention Upgrade), suggestions are evaluated for potential upgrade to code change request if they match a documented or demonstrated project convention.

1. **CONVENTIONS.md check:** The repository structure shows a `CONVENTIONS.md` file exists at the repository root. However, the repo's Key Conventions section (from repo-backend.md) documents conventions for framework usage (Axum, SeaORM), module patterns, error handling, endpoint registration, response types, query helpers, testing, and caching. There is no documented convention requiring indexes on soft-delete columns or requiring partial indexes for nullable timestamp columns in migrations.

2. **Codebase pattern check:** The PR diff contains only one migration file (`m0042_sbom_soft_delete/mod.rs`). There is no evidence within the PR diff of other migrations using `Index::create` or creating indexes for foreign key or filter columns. Without access to the full codebase to count occurrences (and given the eval context), there is no demonstrated codebase pattern of adding indexes alongside column additions in migrations.

3. **Performance-related scrutiny:** Per Check 1c, performance-related suggestions (indexes, caching, query optimization) receive extra scrutiny. However, extra scrutiny does not mean automatic upgrade -- it means more carefully checking for convention backing. No performance-related conventions are documented in the available project conventions.

**Upgrade decision:** The suggestion is NOT upgraded because:
- No matching convention exists in CONVENTIONS.md for index creation on soft-delete or nullable columns
- No demonstrated codebase pattern of adding indexes in migration files was found
- General database best practices ("indexes improve query performance") are explicitly insufficient for upgrade per the Style/Conventions sub-agent instructions: "Do NOT upgrade based on general industry best practices"
- The upgrade evidence must cite a concrete CONVENTIONS.md section or a counted codebase pattern; neither is available

The comment remains classified as **suggestion**. No sub-task created.
