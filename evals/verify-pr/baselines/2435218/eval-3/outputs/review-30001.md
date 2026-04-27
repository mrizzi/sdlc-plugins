# Review Comment Classification: 30001

**Comment ID:** 30001
**Reviewer:** reviewer-a
**File:** modules/fundamental/src/sbom/service/sbom.rs
**Line:** 60
**Classification:** code change request

## Comment Text

> The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.

## Classification Reasoning

This is a **code change request**. The reviewer directly asks for a code modification: wrapping three UPDATE statements in a database transaction. The language is directive ("should run ... inside a single database transaction") and provides specific implementation guidance (use `self.db.transaction(|txn| { ... })`). The reviewer identifies a concrete correctness issue -- partial failure could leave the database in an inconsistent state where `sbom_package` rows are marked deleted but `sbom_advisory` rows are not. This is not a stylistic preference or optional improvement; it addresses a data integrity concern.

## Action

Sub-task created to address this feedback. The fix requires wrapping the three `update_many` calls in `soft_delete` inside a database transaction.
