# Review Comment Classification: 30001

## Comment

**Author:** reviewer-a
**File:** `modules/fundamental/src/sbom/service/sbom.rs` (line 60)
**Text:** The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.

## Classification: CODE CHANGE REQUEST

## Reasoning

The reviewer explicitly asks for a code modification: "should run all three UPDATE statements inside a single database transaction." This is not phrased as a suggestion or a question -- it identifies a concrete correctness defect (risk of partial updates leaving inconsistent state) and prescribes a specific fix (wrap the operations in `self.db.transaction(|txn| { ... })`).

The language is imperative ("should run", "Wrap the three operations"), and the concern is a genuine data consistency risk: if one of the three UPDATE statements fails after earlier ones succeed, the database would be left in an inconsistent state where some tables are marked deleted and others are not.

This requires a code change and a sub-task is created.
