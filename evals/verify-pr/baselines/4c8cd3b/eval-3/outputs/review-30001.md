# Review Comment Classification: 30001

**Reviewer**: reviewer-a
**File**: `modules/fundamental/src/sbom/service/sbom.rs`, line 60
**Date**: 2026-04-20T14:32:00Z

## Comment Text

> The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.

## Classification: Code Change Request

**Reasoning**: The reviewer explicitly requests a specific code modification: wrapping the three UPDATE statements in a single database transaction. The language is directive ("should run", "Wrap the three operations") and the reviewer provides the exact code pattern to follow (`self.db.transaction(|txn| { ... })`). This is not a suggestion or question -- it is a concrete request to change the implementation to prevent data inconsistency. The concern is technically valid: the `soft_delete` method currently executes three independent UPDATE queries against `sbom`, `sbom_package`, and `sbom_advisory`. If any intermediate update fails after a previous one succeeds, the database is left in an inconsistent partially-deleted state where some related records have `deleted_at` set and others do not.

**Action**: Create sub-task (subtask-30001.md)
