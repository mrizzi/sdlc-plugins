# Review Comment Classification: Comment 30001

## Comment

> The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.

**Author:** reviewer-a
**File:** `modules/fundamental/src/sbom/service/sbom.rs`
**Line:** 60

## Classification: code change request

## Reasoning

The reviewer explicitly instructs a specific code modification: wrapping the three UPDATE statements in `self.db.transaction(|txn| { ... })` and changing `self.db` to `txn` for each `.exec()` call. This is not a suggestion or an optional alternative -- the reviewer identifies a concrete correctness issue (inconsistent state if a middle operation fails without transaction wrapping) and prescribes the exact fix. The language is directive ("should run", "Wrap the three operations"), not advisory.

This meets the criteria for **code change request**: the reviewer asks for a code modification to fix a data integrity bug.

## Sub-task required: Yes

A sub-task will be created to wrap the `soft_delete` method's three UPDATE operations in a single database transaction to ensure atomicity.
