## Repository
trustify-backend

## Target Branch
main

## Description
Wrap the three UPDATE statements in the `soft_delete` method in a database transaction to ensure atomicity. Currently, the method executes three sequential updates (sbom, sbom_package, sbom_advisory) without transactional wrapping. If a middle or final update fails after earlier updates succeed, the database is left in an inconsistent state with partially-applied soft deletes. The fix wraps all three operations in `self.db.transaction(|txn| { ... })` and uses `txn` instead of `self.db` for each `exec` call.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` -- wrap the three UPDATE operations in the `soft_delete` method inside a database transaction

## Implementation Notes
- Use `self.db.transaction(|txn| { ... })` to create a transaction scope around the three update operations in the `soft_delete` method
- Replace `&self.db` with `txn` in each `.exec()` call within the transaction closure
- The transaction ensures that if any of the three updates (sbom, sbom_package, sbom_advisory) fails, all changes are rolled back
- Follow the existing transaction patterns in the codebase (check IngestorService or similar services for `transaction()` usage examples)
- The `chrono::Utc::now()` timestamp assignment remains the same; only the execution context changes from direct database connection to transaction handle

## Acceptance Criteria
- [ ] The `soft_delete` method in `SbomService` wraps all three UPDATE operations inside a single database transaction
- [ ] Each `.exec()` call within `soft_delete` uses the transaction handle instead of `self.db`
- [ ] If any UPDATE fails, all preceding updates in the method are rolled back (no partial soft-delete state)
- [ ] Existing integration tests in `tests/api/sbom_delete.rs` continue to pass

## Test Requirements
- [ ] Existing tests pass without modification (the transactional wrapping is transparent to the API contract)

## Target PR
https://github.com/trustify/trustify-backend/pull/744

## Review Context
**Comment ID:** 30001
**Author:** reviewer-a
**File:** modules/fundamental/src/sbom/service/sbom.rs (line 60)
**Original comment:** "The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call."
