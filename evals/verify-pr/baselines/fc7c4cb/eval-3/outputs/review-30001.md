# Review Comment Classification: 30001

## Comment

**Author:** reviewer-a
**File:** `modules/fundamental/src/sbom/service/sbom.rs`, line 60
**Text:** "The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call."

## Classification: Code Change Request

## Reasoning

The reviewer uses imperative language throughout: "should run", "Wrap the three operations", "use `txn` instead of `self.db`". This is a direct instruction to change the code, not a suggestion or optional improvement. The reviewer identifies a concrete correctness bug (inconsistent state if a middle UPDATE fails) and prescribes a specific fix (wrap in a database transaction using `self.db.transaction()`).

This clearly meets the criteria for a **code change request**: the reviewer asks for a specific code modification to fix a data consistency issue.

## Action

Sub-task required. The `soft_delete` method in `modules/fundamental/src/sbom/service/sbom.rs` must be modified to wrap the three `update_many` calls inside a single database transaction.
