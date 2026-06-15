## Repository
trustify-backend

## Target Branch
main

## Description
Wrap the three sequential `update_many` calls in the `soft_delete` method inside a single database transaction to prevent inconsistent state when a partial failure occurs. Currently, if the `sbom_advisory` update fails after `sbom_package` succeeds, the database is left in an inconsistent state where the SBOM and packages are marked deleted but advisories are not.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` -- wrap the three `update_many` calls in `self.db.transaction(|txn| { ... })` and replace `&self.db` with `txn` for each `exec` call

## Implementation Notes
- Use `self.db.transaction(|txn| { ... })` to wrap all three UPDATE operations (sbom, sbom_package, sbom_advisory) in a single transaction
- Replace `exec(&self.db)` with `exec(txn)` for each of the three `update_many` calls inside the transaction closure
- Follow the existing SeaORM transaction pattern used elsewhere in the codebase
- The transaction ensures atomicity: either all three tables are updated or none are, preventing inconsistent cascade state

## Acceptance Criteria
- [ ] The `soft_delete` method wraps all three `update_many` operations inside a single database transaction
- [ ] Each `exec` call within the transaction uses the transaction handle (`txn`) instead of `self.db`
- [ ] If any of the three UPDATE operations fails, the entire transaction rolls back and no tables are modified
- [ ] Existing tests continue to pass (test_delete_sbom_returns_204, test_delete_sbom_cascades_to_join_tables)

## Test Requirements
- [ ] Verify that the cascade update still works correctly within a transaction
- [ ] Confirm that existing tests in tests/api/sbom_delete.rs pass without modification

## Target PR
https://github.com/trustify/trustify-backend/pull/744

## Review Context
**Comment ID:** 30001
**Author:** reviewer-a
**File:** modules/fundamental/src/sbom/service/sbom.rs:60
**Original comment:** "The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call."
