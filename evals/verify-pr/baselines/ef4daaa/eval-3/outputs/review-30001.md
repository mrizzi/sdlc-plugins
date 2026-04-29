# Review Comment Classification: 30001

**Comment ID:** 30001
**Author:** reviewer-a
**File:** `modules/fundamental/src/sbom/service/sbom.rs` (line 60)
**Comment text:** "The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call."

## Classification: code change request

## Reasoning

The reviewer explicitly directs a specific code modification: wrapping the three UPDATE operations in a database transaction. The language is imperative ("should run", "Wrap the three operations"), identifies a concrete correctness defect (inconsistent state if a middle operation fails), and prescribes the exact fix pattern (`self.db.transaction(|txn| { ... })`). This is not a suggestion of an alternative approach -- it identifies a real data integrity bug where partial failure of the cascade updates would leave the database in an inconsistent state. The reviewer is requesting a mandatory code change to ensure atomicity of the soft-delete operation.
