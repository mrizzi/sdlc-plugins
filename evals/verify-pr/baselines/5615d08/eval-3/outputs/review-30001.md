# Review Comment Classification: 30001

**Comment ID:** 30001
**Reviewer:** reviewer-a
**File:** modules/fundamental/src/sbom/service/sbom.rs
**Line:** 60
**Classification:** code change request

## Comment Text

> The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.

## Classification Reasoning

This is a **code change request**. The reviewer explicitly requests a specific code modification: wrapping the three UPDATE statements in the `soft_delete` method inside a database transaction. The language is directive ("should run", "Wrap the three operations"), the reviewer specifies the exact code change needed (`self.db.transaction(|txn| { ... })`), and the issue is a correctness concern -- without a transaction, a partial failure could leave the database in an inconsistent state where `sbom_package` rows are marked deleted but `sbom_advisory` rows are not (or vice versa). This is not a suggestion or optional improvement; it is a required fix to prevent data integrity issues.
