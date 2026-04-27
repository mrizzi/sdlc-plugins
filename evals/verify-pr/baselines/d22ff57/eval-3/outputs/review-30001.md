# Review Comment Classification: 30001

## Comment

> The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.

**File:** `modules/fundamental/src/sbom/service/sbom.rs`
**Line:** 60
**Reviewer:** reviewer-a

## Classification: code change request

## Reasoning

The reviewer explicitly requests a code modification: wrapping three UPDATE statements in a database transaction. The language is directive -- "should run", "Wrap the three operations" -- and identifies a concrete correctness issue (inconsistent state on partial failure). This is not a suggestion or optional improvement; it addresses a data integrity bug where a failure partway through the cascade updates would leave the database in an inconsistent state with some related rows marked deleted and others not.

This is a clear **code change request** requiring a sub-task.
