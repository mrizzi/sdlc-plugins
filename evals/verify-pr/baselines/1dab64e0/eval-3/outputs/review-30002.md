# Review Comment Classification: 30002

## Comment

**Author:** reviewer-a
**File:** `migration/src/m0042_sbom_soft_delete/mod.rs`, line 14
**Content:** The migration should also add an index on `deleted_at` for the sbom table. Queries filtering by `deleted_at IS NULL` will be frequent and a partial index would help. Something like:

```sql
CREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;
```

## Classification: SUGGESTION

## Reasoning

The reviewer uses suggestive language: "should also add" and "would help." The phrasing proposes an optimization (a partial index for query performance) rather than identifying a correctness defect. The reviewer provides a rationale ("queries filtering by `deleted_at IS NULL` will be frequent") and an example SQL snippet, but does not frame this as a blocking requirement.

### Convention Upgrade Eligibility Evaluation

Per Step 4c and the Style/Conventions sub-agent's Check 1 (Convention Upgrade), suggestions must be evaluated for upgrade to code change request if they match a documented project convention or demonstrated codebase pattern.

**CONVENTIONS.md check:** The repository structure (repo-backend.md) lists a `CONVENTIONS.md` file at the repository root. However, the fixture data does not include the contents of CONVENTIONS.md, and no convention within the available fixture data documents an index creation requirement for migration files. There is no documented convention mandating indexes on nullable timestamp columns or soft-delete filter columns.

**Codebase pattern check:** The PR diff and available fixture data do not contain evidence of a consistent codebase pattern of adding indexes in migration files. The migration directory shows only `m0001_initial/mod.rs` alongside the new `m0042_sbom_soft_delete/mod.rs`. No other migration files are available to count `Index::create` or similar patterns.

**Performance-related scrutiny (Check 1c):** This is a performance-related suggestion (index optimization). Extra scrutiny applies, but the fixture data contains no dedicated performance-related patterns, retroactive index migrations, or documented performance conventions to support an upgrade.

**Upgrade decision:** The suggestion does NOT match any documented convention in the available CONVENTIONS.md data, and no counted codebase pattern demonstrates consistent index creation in migrations. General database best practices ("indexes improve query performance") are explicitly insufficient for upgrade per the skill definition -- upgrade evidence must cite a concrete CONVENTIONS.md section or a counted codebase pattern.

**Result:** Classification remains SUGGESTION. No upgrade applied. No sub-task created.

## Action

No sub-task created. The suggestion proposes a performance optimization that is not backed by a documented project convention or demonstrated codebase pattern in the available fixture data.
