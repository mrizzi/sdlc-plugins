# Review Comment Classification: 30001

## Comment
**Author**: reviewer-a
**File**: `modules/fundamental/src/sbom/service/sbom.rs` (line 60)
**Date**: 2026-04-20T14:32:00Z

> The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.

## Classification
**Type**: Code Change Request
**Severity**: HIGH
**Creates Sub-task**: YES

## Reasoning
This comment requests a concrete code change to the `soft_delete` method in `sbom.rs`. The reviewer identifies a correctness bug: the three UPDATE statements (for `sbom`, `sbom_package`, and `sbom_advisory`) execute independently without transactional guarantees. If one fails after others succeed, the database will be left in an inconsistent state with partially-applied soft-delete markers. The reviewer provides a specific remediation: wrap the operations in `self.db.transaction(|txn| { ... })`. This is not a stylistic suggestion or a question -- it is a direct request to change code to fix a data integrity issue. This warrants a sub-task to track the fix.
