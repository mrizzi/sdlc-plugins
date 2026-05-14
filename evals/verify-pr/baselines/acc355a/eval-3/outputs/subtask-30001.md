## Repository
trustify-backend

## Target Branch
TC-9103

## Description
Wrap the three UPDATE statements in the `soft_delete` method inside a single database transaction to ensure atomicity. Currently, the sbom, sbom_package, and sbom_advisory updates execute independently. If a later update fails after an earlier one succeeds, the database is left in an inconsistent state with partially applied soft-deletion. This fix ensures all three operations succeed or fail together.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` -- wrap the three `update_many().exec()` calls in `self.db.transaction(|txn| { ... })` and replace `&self.db` with `txn` for each exec call

## Implementation Notes
- Use SeaORM's `TransactionTrait::transaction()` method on `self.db` to create a transaction closure
- Inside the closure, replace `&self.db` with the transaction handle `txn` for all three `exec()` calls
- The existing pattern for transactions in the codebase can be found in the ingestor module (`modules/ingestor/src/graph/sbom/mod.rs`) which uses similar multi-table updates
- Ensure the closure returns `Ok(())` on success; SeaORM will auto-commit on `Ok` and rollback on `Err`
- The method signature (`pub async fn soft_delete(&self, id: i64) -> Result<()>`) does not need to change

## Acceptance Criteria
- [ ] The `soft_delete` method wraps all three UPDATE operations in a single database transaction
- [ ] If any UPDATE fails, all previously applied updates within the transaction are rolled back
- [ ] Existing tests in `tests/api/sbom_delete.rs` continue to pass
- [ ] The cascade test (`test_delete_sbom_cascades_to_join_tables`) verifies that all three tables are updated atomically

## Test Requirements
- [ ] Existing deletion tests pass without modification
- [ ] Manual or integration verification that a simulated failure in one UPDATE rolls back the others (if test infrastructure supports fault injection)

## Target PR
https://github.com/trustify/trustify-backend/pull/744

## Review Context
**Comment ID**: 30001
**Author**: reviewer-a
**File**: `modules/fundamental/src/sbom/service/sbom.rs`, line 60
**Comment text**:
> The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.
