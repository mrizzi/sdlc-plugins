# Review Comment Classification: 30001

## Comment
**Author:** reviewer-a
**File:** `modules/fundamental/src/sbom/service/sbom.rs`, line 60
**Body:** The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.

## Classification: code change request

## Reasoning
The reviewer explicitly requests a concrete code change: wrapping the three UPDATE statements in a database transaction. This is not a suggestion of an alternative approach or a question -- it is a direct instruction to modify the `soft_delete` method to use `self.db.transaction()`. The reviewer identifies a specific correctness issue (inconsistent state on partial failure) and prescribes the exact fix (use a transaction). This is a clear code change request that requires a tracked fix.
