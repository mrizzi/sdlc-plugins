## Repository
trustify-backend

## Target Branch
main

## Description
Wrap the three UPDATE statements in the `soft_delete` method inside a single database transaction to prevent inconsistent state if any individual update fails. Currently, the `sbom`, `sbom_package`, and `sbom_advisory` updates execute independently — if the `sbom_advisory` update fails after `sbom_package` succeeds, the database will be left in a partially-deleted state.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` — wrap the three `update_many` calls in `soft_delete` inside `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each `.exec()` call

## Implementation Notes
- Use SeaORM's `TransactionTrait::transaction()` method on the database connection to wrap all three UPDATE operations
- Replace `self.db` with the transaction handle (`txn`) in each `.exec()` call inside the transaction closure
- The transaction should be an async closure: `self.db.transaction::<_, (), DbErr>(|txn| { Box::pin(async move { ... }) }).await?`
- Follow the existing error handling pattern — if any update fails, the transaction will automatically roll back all changes
- The `chrono::Utc::now()` timestamp should be captured before the transaction begins so all three updates use the same value

## Acceptance Criteria
- [ ] All three UPDATE statements (`sbom`, `sbom_package`, `sbom_advisory`) in `soft_delete` execute within a single database transaction
- [ ] If any UPDATE fails, all previously successful UPDATEs in the same `soft_delete` call are rolled back
- [ ] The `soft_delete` method's external behavior (return type, error handling) remains unchanged
- [ ] All existing tests in `tests/api/sbom_delete.rs` continue to pass

## Test Requirements
- [ ] Verify that the existing integration tests still pass after the transaction wrapping change
- [ ] If feasible, add a test that simulates a failure mid-transaction (e.g., invalid sbom_advisory foreign key) and verifies rollback behavior

## Review Context
**Original review comment (ID: 30001) by reviewer-a on `modules/fundamental/src/sbom/service/sbom.rs` line 60:**

> The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.

## Target PR
https://github.com/trustify/trustify-backend/pull/744
