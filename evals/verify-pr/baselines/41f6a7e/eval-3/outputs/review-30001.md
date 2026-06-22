# Review Comment Classification: 30001

**Comment ID:** 30001
**Author:** reviewer-a
**File:** modules/fundamental/src/sbom/service/sbom.rs
**Line:** 60
**Classification:** code change request

## Comment Text

> The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.

## Classification Reasoning

This comment is classified as a **code change request** because the reviewer explicitly directs a specific code modification: wrapping the three UPDATE operations in a database transaction. The language is imperative ("should run", "Wrap the three operations") and identifies a concrete correctness issue — partial failure leaving the database in an inconsistent state. This is not a suggestion of an alternative approach; it identifies a bug-class defect (missing atomicity guarantee) and prescribes the fix.

The reviewer provides the exact API to use (`self.db.transaction(|txn| { ... })`), the specific scope of the change (all three UPDATE statements), and the rationale (preventing inconsistent state if a later update fails after an earlier one succeeds). This level of specificity and the correctness implications make this a required code change, not an optional suggestion.

## Action

Sub-task created to address this feedback — wrap the three `update_many` operations in `soft_delete()` inside a single database transaction.
