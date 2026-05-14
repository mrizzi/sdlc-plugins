# Review Comment Classification: 30001

## Comment

**Author:** reviewer-a
**File:** `modules/fundamental/src/sbom/service/sbom.rs` (line 60)
**Date:** 2026-04-20T14:32:00Z

> The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.

## Classification: code change request

## Reasoning

The reviewer uses imperative language ("should run", "Wrap the three operations") and identifies a concrete code defect: the three UPDATE statements in `soft_delete` execute independently without transactional guarantees. If any intermediate operation fails, the database will be left in an inconsistent state where some related records are marked as deleted and others are not.

This is not a suggestion or optional improvement -- it describes a correctness bug where partial failure leads to data inconsistency. The reviewer prescribes a specific code change: wrapping the operations in `self.db.transaction(|txn| { ... })` and using the transaction handle for each exec call.

This clearly meets the "code change request" classification: the reviewer asks for a code modification to fix incorrect behavior.

## Action

Sub-task creation required. The three UPDATE statements in `soft_delete` must be wrapped in a database transaction to ensure atomicity.
