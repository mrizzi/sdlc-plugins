# Sub-Task: Wrap soft_delete operations in database transaction

## Repository
trustify-backend

## Target Branch
TC-9103

## Description
The `soft_delete` method in `SbomService` executes three UPDATE statements (sbom, sbom_package, sbom_advisory) without a transaction boundary. If any intermediate UPDATE fails after a preceding one succeeds, the database is left in an inconsistent state with partially soft-deleted records. Wrap all three operations in a single database transaction to ensure atomicity.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` -- wrap the three `update_many` calls in `soft_delete` method inside `self.db.transaction(|txn| { ... })` and replace `&self.db` with `txn` in each `exec()` call

## Implementation Notes
- Use SeaORM's transaction API: `self.db.transaction::<_, _, DbErr>(|txn| { Box::pin(async move { ... }) }).await?`
- Replace `&self.db` with `txn` in all three `Entity::update_many().exec()` calls within the `soft_delete` method
- The transaction ensures all three UPDATE statements either all succeed or all roll back
- Follow the existing transaction usage patterns in the codebase (e.g., ingestor module's multi-step ingestion operations)

## Acceptance Criteria
- [ ] The `soft_delete` method wraps all three UPDATE operations in a single database transaction
- [ ] Each `exec()` call within the transaction uses the transaction handle (`txn`) instead of `self.db`
- [ ] If any UPDATE fails, all preceding UPDATEs are rolled back (no partial soft-deletion)
- [ ] Existing tests continue to pass (test_delete_sbom_returns_204, test_delete_sbom_cascades_to_join_tables)

## Test Requirements
- [ ] Verify that the transaction wrapping does not break existing soft-delete integration tests

## Target PR
https://github.com/trustify/trustify-backend/pull/744

## Review Context
**Comment ID:** 30001
**Author:** reviewer-a
**File:** `modules/fundamental/src/sbom/service/sbom.rs`, line 60
**Original comment:**
> The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.
