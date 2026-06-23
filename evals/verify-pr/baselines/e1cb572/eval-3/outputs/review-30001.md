# Review Comment Classification: 30001

## Comment

**Author:** reviewer-a
**File:** `modules/fundamental/src/sbom/service/sbom.rs` (line 60)
**Text:** "The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call."

## Classification: code change request

## Reasoning

The reviewer uses directive language: "should run", "Wrap the three operations". This is not a suggestion or optional improvement -- it identifies a concrete correctness bug (partial failure leaving inconsistent state) and prescribes a specific code change (wrapping three UPDATE statements in a database transaction). The reviewer explains the defect scenario (sbom_advisory update failing after sbom_package succeeds leads to inconsistent state) and provides the exact fix (use `self.db.transaction(|txn| { ... })`).

This meets the definition of a code change request: the reviewer asks for a code modification to fix a correctness issue. A sub-task will be created to address this feedback.
