# Review Comment Classification: 30002

**Comment ID:** 30002
**Reviewer:** reviewer-a
**File:** `migration/src/m0042_sbom_soft_delete/mod.rs` (line 14)
**Classification:** code change request

## Comment Text

> The migration should also add an index on `deleted_at` for the sbom table. Queries filtering by `deleted_at IS NULL` will be frequent and a partial index would help. Something like:
>
> ```sql
> CREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;
> ```

## Classification Reasoning

The reviewer requests a code modification: adding a partial index on the `deleted_at` column in the migration. The language is directive ("should also add an index") and provides a concrete SQL example. The concern is performance-related (query efficiency for frequent `deleted_at IS NULL` filtering) and directly relates to the implementation's operational correctness.

This is a **code change request** because:
1. The reviewer asks for a specific code addition (partial index in the migration)
2. The concern is performance/operational correctness (frequent queries will lack index support)
3. The language is imperative ("should also add"), not optional
4. A concrete implementation example is provided

**Action:** Sub-task created to address this feedback.
