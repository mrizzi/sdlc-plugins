# Review Comment Classification: 30001

## Comment

**Author:** reviewer-a
**File:** `modules/fundamental/src/sbom/service/sbom.rs` (line 60)
**Text:** "The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call."

## Classification: code change request

## Reasoning

The reviewer explicitly asks for a code modification: wrapping three UPDATE operations in a database transaction. The language is directive ("should run ... inside a single database transaction", "Wrap the three operations in ...") and prescribes a specific technical solution (`self.db.transaction(|txn| { ... })`).

This is not a suggestion or alternative approach -- the reviewer identifies a correctness defect (potential data inconsistency if a partial failure occurs during cascade updates) and requests a concrete fix. The absence of a transaction means that if the `sbom_advisory` update fails after `sbom_package` succeeds, the database will be left in an inconsistent state where some join table rows are marked deleted and others are not.

This classifies as a **code change request** because:
1. The reviewer asks for a specific code modification (not an alternative approach)
2. It addresses a correctness/data integrity concern, not just style or performance
3. The language is imperative ("should", "Wrap")

**Action:** Sub-task will be created to address this feedback.
