# Review Comment Classification: 30001

## Comment

**Author:** reviewer-a
**File:** `modules/fundamental/src/sbom/service/sbom.rs`, line 60
**Text:** "The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call."

## Classification: code change request

## Reasoning

The reviewer uses directive language ("should run", "Wrap the three operations") and identifies a concrete correctness defect: the three UPDATE statements in `soft_delete` are not wrapped in a transaction, which can produce inconsistent state if a partial failure occurs (e.g., `sbom_package` updated but `sbom_advisory` update fails). The reviewer prescribes the exact fix: wrap in `self.db.transaction(|txn| { ... })` and use `txn` for each `exec` call. This is a request for a specific code modification to fix a data integrity issue, not a suggestion of an alternative approach. It meets the definition of a code change request.

## Action

Sub-task created to address this feedback.
