# Review Comment Classification: 30001

## Comment
**Author:** reviewer-a
**File:** `modules/fundamental/src/sbom/service/sbom.rs` (line 60)
**Text:** "The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call."

## Classification: code change request

## Reasoning
The reviewer directly requests a specific code modification: wrapping the three UPDATE statements in a database transaction. The language is imperative ("should run", "Wrap the three operations") and identifies a concrete correctness issue (inconsistent state on partial failure). This is not a suggestion of an alternative approach -- it identifies a bug-class problem (non-atomic multi-table updates) and prescribes the fix. This meets the definition of a code change request.
