## Repository
trustify-backend

## Description
Wrap the three UPDATE statements in the `soft_delete` method inside a single database transaction to ensure atomicity. Currently, the `sbom`, `sbom_package`, and `sbom_advisory` updates execute independently. If the `sbom_advisory` update fails after `sbom_package` succeeds, the database will be left in an inconsistent state with partially-applied soft deletes.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` -- wrap the three `update_many` calls in `soft_delete` inside `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each `exec` call

## Implementation Notes
- Use SeaORM's `TransactionTrait::transaction` method on the database connection to wrap all three UPDATE operations
- Replace `self.db` with the transaction handle `txn` in each `.exec()` call within the transaction closure
- The transaction ensures that either all three tables are updated atomically, or none are -- preventing inconsistent state on partial failure
- Follow the existing error handling pattern: the transaction will automatically roll back on any `Err` return from the closure
- The `soft_delete` method signature does not need to change; the transaction is an internal implementation detail

## Acceptance Criteria
- [ ] The `soft_delete` method wraps all three UPDATE operations (`sbom`, `sbom_package`, `sbom_advisory`) in a single database transaction
- [ ] Each `.exec()` call within the transaction uses the transaction handle, not `self.db`
- [ ] If any UPDATE fails, the entire operation is rolled back (no partial soft-deletes)
- [ ] Existing tests continue to pass -- the external behavior of the DELETE endpoint is unchanged

## Test Requirements
- [ ] Test that a soft-delete failure on a join table (e.g., `sbom_advisory`) does not leave `sbom_package` rows marked as deleted
- [ ] Existing tests for DELETE 204, DELETE 404, DELETE 409, and cascade behavior continue to pass

## Review Context
Reviewer **reviewer-a** (comment 30001) on `modules/fundamental/src/sbom/service/sbom.rs` line 60:
> The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.

## Target PR
https://github.com/trustify/trustify-backend/pull/744
