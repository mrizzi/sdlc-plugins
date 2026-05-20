## Repository
trustify-backend

## Target Branch
TC-9103

## Description
Wrap the three UPDATE statements in the `soft_delete` method inside a single database transaction to ensure atomicity. Currently, if the `sbom_advisory` update fails after the `sbom_package` update succeeds, the database is left in an inconsistent state where some related rows are marked as deleted and others are not. All three operations (sbom, sbom_package, sbom_advisory) must succeed or fail together.

## Target PR
https://github.com/trustify/trustify-backend/pull/744

## Review Context
**Comment ID:** 30001
**Author:** reviewer-a
**File:** `modules/fundamental/src/sbom/service/sbom.rs`, line 60
**Original comment:**
> The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` -- wrap the three `update_many` calls in `soft_delete` inside a `self.db.transaction(|txn| { ... })` block and replace `&self.db` with `txn` for each `.exec()` call

## Implementation Notes
- Use `self.db.transaction(|txn| { ... })` to wrap all three UPDATE operations in the `soft_delete` method
- Replace `&self.db` with `txn` in each `.exec()` call within the transaction closure
- Follow the existing SeaORM transaction pattern used elsewhere in the codebase
- The transaction ensures that if any of the three updates fail, all changes are rolled back
- The method signature and return type remain unchanged; only the internal implementation changes

## Acceptance Criteria
- [ ] The `soft_delete` method wraps all three UPDATE statements (sbom, sbom_package, sbom_advisory) in a single database transaction
- [ ] Each `.exec()` call within the transaction uses the transaction handle (`txn`) instead of `self.db`
- [ ] If any UPDATE fails, all changes are rolled back (no partial state)
- [ ] Existing tests continue to pass (test_delete_sbom_returns_204, test_delete_sbom_cascades_to_join_tables)
