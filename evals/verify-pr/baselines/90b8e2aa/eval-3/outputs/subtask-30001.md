## Repository
trustify-backend

## Target Branch
TC-9103

## Description
Wrap the three UPDATE statements in the `soft_delete` method inside a single database transaction to ensure atomicity. Currently, the SBOM record, sbom_package rows, and sbom_advisory rows are updated in separate, non-transactional database calls. If any intermediate update fails (e.g., the sbom_advisory update fails after sbom_package succeeds), the database will be left in an inconsistent state with partially-deleted records. The fix is to use `self.db.transaction(|txn| { ... })` and execute all three updates against `txn` instead of `self.db`.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` -- wrap the three `update_many` calls in the `soft_delete` method inside a database transaction

## Implementation Notes
- Use the SeaORM transaction API: `self.db.transaction::<_, (), DbErr>(|txn| { Box::pin(async move { ... }) }).await?`
- Replace `&self.db` with `txn` in each of the three `exec()` calls inside the transaction closure
- Follow the existing transaction patterns in the codebase (check `modules/ingestor/` for examples of transaction usage)
- The transaction ensures all three updates either succeed together or roll back together, preventing inconsistent state

## Acceptance Criteria
- [ ] The `soft_delete` method wraps all three UPDATE statements (sbom, sbom_package, sbom_advisory) inside a single database transaction
- [ ] Each `exec()` call inside the transaction uses the transaction handle (`txn`) instead of `self.db`
- [ ] If any of the three updates fails, all changes are rolled back (no partial deletes)
- [ ] All existing tests continue to pass

## Test Requirements
- [ ] Existing `test_delete_sbom_cascades_to_join_tables` test continues to pass with the transactional implementation

## Target PR
https://github.com/trustify/trustify-backend/pull/744

## Review Context
**Comment ID:** 30001
**Author:** reviewer-a
**File:** `modules/fundamental/src/sbom/service/sbom.rs`, line 60
**Original comment:**
> The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.
