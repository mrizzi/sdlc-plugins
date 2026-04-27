# Review Comment Classification: #30001

**Comment by:** reviewer-a
**File:** `modules/fundamental/src/sbom/service/sbom.rs`, line 60
**Date:** 2026-04-20T14:32:00Z

## Original Comment

> The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.

## Classification: code change request

## Reasoning

The reviewer explicitly requests a code modification: wrapping three UPDATE statements in a database transaction. The language is imperative ("should run", "Wrap the three operations") and identifies a concrete correctness defect -- if one of the cascade updates fails after another succeeds, the database will be left in an inconsistent state with partially soft-deleted records. This is not a stylistic preference or optional enhancement; it addresses a data integrity bug where a partial failure leaves orphaned state.

The reviewer also provides specific implementation guidance (use `self.db.transaction(|txn| { ... })` and replace `self.db` with `txn`), making the required change unambiguous.

**Classification:** code change request -- triggers sub-task creation (subtask-30001.md).
