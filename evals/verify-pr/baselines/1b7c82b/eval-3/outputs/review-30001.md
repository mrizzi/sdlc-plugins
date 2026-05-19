# Review Comment Classification: 30001

## Comment

> The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.

**File:** `modules/fundamental/src/sbom/service/sbom.rs`, line 60
**Author:** reviewer-a

## Classification: code change request

## Reasoning

The reviewer uses imperative language ("should run", "Wrap the three operations") and explicitly describes a required code modification. The comment identifies a concrete correctness bug: the three UPDATE statements for sbom, sbom_package, and sbom_advisory are executed independently without a transaction, which can leave the database in an inconsistent state if one of the later updates fails after earlier ones succeed. This is not optional or stylistic -- it is a data integrity concern that requires a code change.

The reviewer provides a specific fix: wrap the operations in `self.db.transaction(|txn| { ... })` and replace `self.db` with `txn` for each exec call.

**Triggers sub-task creation:** Yes
