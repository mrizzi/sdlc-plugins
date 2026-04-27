# Review Comment Classification: 30001

**Reviewer**: reviewer-a
**File**: `modules/fundamental/src/sbom/service/sbom.rs`, line 60
**Date**: 2026-04-20T14:32:00Z

## Comment Text

> The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.

## Classification: Code Change Request

**Reasoning**: The reviewer explicitly requests a concrete code modification -- wrapping the three UPDATE statements in the `soft_delete` method inside a single database transaction. The language is directive ("should run", "Wrap the three operations") and the reviewer specifies the exact code pattern to use (`self.db.transaction(|txn| { ... })`). This is not a suggestion or question; it is a direct request to change the implementation to prevent data inconsistency.

The concern is technically valid: the current `soft_delete` method executes three independent `update_many` calls against the `sbom`, `sbom_package`, and `sbom_advisory` tables sequentially without transactional wrapping. If the second or third UPDATE fails after the first succeeds, the database would be left in an inconsistent partially-deleted state where some related records have `deleted_at` set and others do not. Transaction wrapping is the standard approach for ensuring atomicity of multi-table mutations.

**Action**: Create sub-task (subtask-30001.md)
