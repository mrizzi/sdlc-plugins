# Review Comment Classification: 30001

## Comment

**Author:** reviewer-a
**File:** `modules/fundamental/src/sbom/service/sbom.rs`, line 60
**Content:** The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.

## Classification: code change request

## Reasoning

The reviewer explicitly asks for a concrete code modification: wrapping three UPDATE statements in a database transaction. The language is directive ("should run", "Wrap the three operations"), identifies a specific correctness problem (inconsistent state on partial failure), and provides the exact fix pattern to apply (`self.db.transaction(|txn| { ... })`). This is not a suggestion of an alternative approach or a style preference -- it identifies a real data integrity risk and requests a specific code change to address it.

## Action

Sub-task created to address this feedback. The soft_delete method must wrap the three `update_many` calls (sbom, sbom_package, sbom_advisory) in a single database transaction to ensure atomicity.
