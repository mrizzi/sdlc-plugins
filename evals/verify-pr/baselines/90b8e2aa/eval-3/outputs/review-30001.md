# Review Comment Classification: 30001

## Comment

> The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.

**Author:** reviewer-a
**File:** `modules/fundamental/src/sbom/service/sbom.rs`, line 60
**Review ID:** 20001

## Classification: code change request

## Reasoning

The reviewer explicitly instructs a specific code modification: wrap the three UPDATE statements in a database transaction using `self.db.transaction(|txn| { ... })`. The language is imperative ("should run", "Wrap the three operations"), not suggestive or optional. The reviewer identifies a concrete correctness issue (inconsistent state if a middle operation fails) and prescribes the exact fix with API-level detail (`self.db.transaction(|txn| { ... })`).

This is a direct code change request because:
1. It identifies a concrete defect (lack of transactional atomicity leading to potential data inconsistency)
2. It prescribes a specific code change (wrap in transaction, use `txn` instead of `self.db`)
3. The language is imperative, not conditional or exploratory

## Action

Sub-task will be created to address this feedback.
