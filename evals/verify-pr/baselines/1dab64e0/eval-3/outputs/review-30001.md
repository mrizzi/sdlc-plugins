# Review Comment Classification: 30001

## Comment

**Author:** reviewer-a
**File:** `modules/fundamental/src/sbom/service/sbom.rs`, line 60
**Content:** The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.

## Classification: CODE CHANGE REQUEST

## Reasoning

The reviewer explicitly requests a code modification: wrapping the three UPDATE statements in a database transaction. The language is directive ("should run", "Wrap the three operations"), not suggestive or optional. The reviewer identifies a concrete correctness issue (inconsistent state if a middle operation fails) and prescribes the specific fix (use `self.db.transaction(|txn| { ... })`).

This is not a suggestion (optional alternative approach), not a question (request for clarification), and not a nit (minor style feedback). It is a direct request for a code change to fix a data integrity issue.

## Action

Sub-task creation triggered. The code change request requires wrapping `soft_delete` operations in a database transaction to ensure atomicity of the cascading soft-delete across `sbom`, `sbom_package`, and `sbom_advisory` tables.
