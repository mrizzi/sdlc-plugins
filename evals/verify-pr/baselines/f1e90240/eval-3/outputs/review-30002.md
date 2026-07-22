# Review Comment Classification: 30002

## Comment

**Author:** reviewer-a
**File:** `migration/src/m0042_sbom_soft_delete/mod.rs`, line 14
**Content:** The migration should also add an index on `deleted_at` for the sbom table. Queries filtering by `deleted_at IS NULL` will be frequent and a partial index would help. Something like:
```sql
CREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;
```

## Classification: code change request

## Reasoning

The reviewer uses directive language ("should also add an index") and provides a concrete SQL example of the expected change. The reviewer identifies a specific performance concern (frequent `deleted_at IS NULL` queries) and prescribes the exact solution (a partial index). This is a request for a code modification, not a tentative suggestion or optional proposal. The reviewer is instructing the author to add the index as part of this migration.

No convention upgrade was applicable because CONVENTIONS.md content for the trustify-backend repository was not available for analysis. The classification was determined directly from the reviewer's directive language.

## Action

Sub-task created to address this feedback. The migration must be updated to include a partial index on the `deleted_at` column for the `sbom` table.
