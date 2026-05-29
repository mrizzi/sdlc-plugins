# Review Comment Classification: 30001

## Comment

**Author:** reviewer-a
**File:** `modules/fundamental/src/sbom/service/sbom.rs`, line 60
**Text:** "The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call."

## Classification: code change request

## Reasoning

The reviewer explicitly requests a concrete code modification: wrapping three sequential UPDATE statements inside a database transaction to prevent inconsistent state if one of them fails. This is not a suggestion of an alternative approach -- it is a direct request to fix a correctness issue (lack of transactional atomicity in a multi-table update). The language is imperative ("should run", "Wrap the three operations") and identifies a specific defect (partial failure leading to inconsistent state).

This is a clear **code change request** because:
1. The reviewer uses directive language ("should", "Wrap")
2. It identifies a concrete bug (non-atomic multi-table updates)
3. It prescribes the exact fix (use `self.db.transaction(|txn| { ... })`)
4. The feedback addresses data integrity, which is a correctness concern, not a stylistic preference

**Sub-task required:** Yes -- this feedback triggers sub-task creation.
