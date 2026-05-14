# Review Comment Classification: 30001

## Comment

**Author**: reviewer-a
**File**: `modules/fundamental/src/sbom/service/sbom.rs`, line 60
**Text**: The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.

## Classification: CODE CHANGE REQUEST

## Reasoning

The reviewer is explicitly requesting a code modification to the `soft_delete` method. The comment:

1. **Identifies a concrete correctness issue**: The three UPDATE statements (sbom, sbom_package, sbom_advisory) execute independently. If a later statement fails after an earlier one succeeds, the database is left in an inconsistent state with partially applied soft-deletion.
2. **Prescribes a specific code change**: Wrap the operations in `self.db.transaction(|txn| { ... })` and use the transaction handle `txn` instead of `self.db` for each `exec` call.
3. **Is not a style nit or question** -- it addresses a data integrity bug where partial failure leaves orphaned state.

This is a clear code change request that requires a sub-task to implement the fix.

## Action

Sub-task created: subtask-30001.md
