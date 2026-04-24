# Review Comment Classification: 30001

**Reviewer**: reviewer-a
**File**: `modules/fundamental/src/sbom/service/sbom.rs`, line 60
**Date**: 2026-04-20T14:32:00Z

## Comment Text

> The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.

## Classification: Code Change Request

**Reasoning**: The reviewer explicitly requests a specific code modification: wrapping the three UPDATE statements inside a database transaction. The language is directive ("should run", "Wrap the three operations"), and the reviewer provides an exact code pattern to follow (`self.db.transaction(|txn| { ... })`). This is not a suggestion or question -- it is a concrete request to change the implementation to prevent data inconsistency. The concern is valid: if any of the three sequential UPDATE operations fails after a previous one succeeds, the database will be left in an inconsistent state where some related records are marked as deleted and others are not.

**Action**: Create sub-task (subtask-30001.md)
