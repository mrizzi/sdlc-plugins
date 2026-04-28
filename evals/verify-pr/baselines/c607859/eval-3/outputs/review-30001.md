# Review Comment Classification: 30001

**Comment ID:** 30001
**Author:** reviewer-a
**File:** `modules/fundamental/src/sbom/service/sbom.rs` (line 60)
**Classification:** code change request

## Comment Text

> The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.

## Classification Reasoning

This is a **code change request**. The reviewer explicitly directs a code modification using imperative language ("should run", "Wrap the three operations"). The comment identifies a concrete correctness bug -- the three UPDATE statements in `soft_delete` are not wrapped in a transaction, which can lead to inconsistent state if a partial failure occurs (e.g., `sbom_package` updated but `sbom_advisory` update fails). The reviewer provides a specific fix: use `self.db.transaction(|txn| { ... })` and replace `self.db` with `txn` in each exec call.

This requires a sub-task to implement the fix.
