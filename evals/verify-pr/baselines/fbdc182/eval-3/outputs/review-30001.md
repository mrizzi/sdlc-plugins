# Review Comment Classification: 30001

**Comment ID:** 30001
**Author:** reviewer-a
**File:** `modules/fundamental/src/sbom/service/sbom.rs` (line 60)
**Classification:** code change request

## Comment Text

> The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.

## Reasoning

The reviewer explicitly requests a code modification: wrapping the three UPDATE statements in a database transaction. This is not a suggestion of an alternative approach or a question -- it is a direct instruction to change the implementation to prevent inconsistent state. The reviewer identifies a concrete defect (partial failure leaves inconsistent data) and prescribes the exact fix (use `self.db.transaction()`). This clearly meets the definition of a code change request.

## Action

Sub-task created (see subtask-30001.md).
