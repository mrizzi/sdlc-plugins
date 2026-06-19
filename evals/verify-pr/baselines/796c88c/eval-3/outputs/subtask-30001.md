# Sub-Task: Wrap soft_delete operations in a database transaction

## Repository
trustify-backend

## Description
The `soft_delete` method in `SbomService` performs three sequential UPDATE statements (sbom, sbom_package, sbom_advisory) without transaction wrapping. If an intermediate update fails (e.g., sbom_package succeeds but sbom_advisory fails), the database is left in an inconsistent state with partially-deleted records. Wrap all three UPDATE operations in a single database transaction to ensure atomicity.

## Target PR
https://github.com/trustify/trustify-backend/pull/744

## Review Context
**Comment ID:** 30001
**Author:** reviewer-a
**File:** modules/fundamental/src/sbom/service/sbom.rs, line 60
**Original comment:**
> The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` -- wrap the three `update_many` calls in `soft_delete` inside a `self.db.transaction(|txn| { ... })` block and replace `&self.db` with `txn` in each `.exec()` call

## Implementation Notes
- Use SeaORM's `TransactionTrait::transaction()` method on `self.db` to create a transaction scope
- Inside the transaction closure, use the `txn` parameter (which implements `ConnectionTrait`) instead of `&self.db` for all three `.exec()` calls
- The transaction will automatically roll back if any operation returns an error
- Follow the existing transaction patterns in the codebase (check ingestor module for examples of transaction usage)

## Acceptance Criteria
- [ ] The `soft_delete` method wraps all three UPDATE operations (sbom, sbom_package, sbom_advisory) in a single database transaction
- [ ] Each `.exec()` call uses the transaction connection (`txn`) instead of `&self.db`
- [ ] If any of the three updates fails, all changes are rolled back (no partial state)
- [ ] Existing tests continue to pass (test_delete_sbom_returns_204, test_delete_sbom_cascades_to_join_tables)

## Test Requirements
- [ ] Verify that existing deletion tests pass with the transaction wrapping
- [ ] Verify atomicity: if a cascade update fails, the sbom record's deleted_at should not be set
