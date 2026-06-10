# Review Comment Classification: 30001

## Comment
**Author:** reviewer-a
**File:** modules/fundamental/src/sbom/service/sbom.rs (line 60)
**Text:** The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.

## Classification: code change request

## Reasoning
The reviewer explicitly requests a code modification: wrapping three UPDATE statements in a database transaction. This is not a suggestion of an alternative approach -- it identifies a concrete correctness issue (inconsistent state on partial failure) and prescribes a specific fix (use `self.db.transaction()`). The language is directive ("should run", "Wrap the three operations"), and the feedback addresses a real data integrity bug where a failure partway through the cascade updates would leave the database in an inconsistent state. This is a required code change, not an optional improvement.
