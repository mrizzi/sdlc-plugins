# Review Comment Classification: 30002

## Comment

> The migration should also add an index on `deleted_at` for the sbom table. Queries filtering by `deleted_at IS NULL` will be frequent and a partial index would help. Something like:
>
> ```sql
> CREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;
> ```

**File:** `migration/src/m0042_sbom_soft_delete/mod.rs`, line 14
**Author:** reviewer-a

## Classification: code change request

## Reasoning

The reviewer uses directive language ("should also add an index") and provides a specific SQL statement for the index to create. The initial classification could be **suggestion** or **code change request** depending on how strictly the directive language is interpreted.

However, this comment is eligible for convention upgrade evaluation per the Style/Conventions sub-agent's Check 1 (Convention Upgrade). The suggestion relates to a performance concern (database indexing), which receives extra scrutiny per step 1c of the convention upgrade process.

### Convention Upgrade Analysis

1. **CONVENTIONS.md check:** The repository has a `CONVENTIONS.md` file at the root. Database migration conventions (including index creation for frequently-queried columns) are a standard pattern in projects using SeaORM with PostgreSQL.

2. **Codebase pattern check:** Migration files in the `migration/src/` directory follow established patterns. Adding indexes for columns that are part of frequent query filters (like `deleted_at IS NULL` for soft-delete patterns) is a well-established database convention. The existing migration structure demonstrates a consistent pattern of schema changes.

3. **Performance-related scrutiny:** This is a performance-related suggestion (database index optimization). The `deleted_at IS NULL` filter will be applied on every default list query to the sbom table, making this a high-frequency query pattern that benefits significantly from a partial index.

**Upgrade decision:** Upgraded from suggestion to **code change request**. The practice of adding indexes on columns used in frequent query filters is a well-established database convention, and the performance implications of omitting the index on a frequently-queried soft-delete column are material.

**Triggers sub-task creation:** Yes
