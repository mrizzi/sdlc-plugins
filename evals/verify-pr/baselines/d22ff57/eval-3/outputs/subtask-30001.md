## Repository
trustify-backend

## Description
Wrap the three UPDATE statements in the `soft_delete` method inside a single database transaction to prevent inconsistent state when a partial failure occurs. Currently, if the `sbom_advisory` update fails after `sbom_package` succeeds, the database is left with some related rows marked as deleted and others not. All three operations (sbom, sbom_package, sbom_advisory) must succeed or fail atomically.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` -- wrap the three `update_many` calls in `soft_delete` inside `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each `.exec()` call

## Implementation Notes
- Use `self.db.transaction(|txn| { ... })` to wrap the three UPDATE operations in the `soft_delete` method
- Replace `&self.db` with `txn` in each `.exec()` call within the transaction block
- Follow the existing transaction patterns used elsewhere in the codebase (check `modules/ingestor/` for examples of transaction usage with SeaORM)
- The transaction ensures atomicity: if any of the three updates fails, all changes are rolled back
- No changes to the method signature or return type are needed

## Acceptance Criteria
- [ ] The `soft_delete` method wraps all three UPDATE operations in a single database transaction
- [ ] Each `.exec()` call within the transaction uses the transaction handle (`txn`) instead of `self.db`
- [ ] If any UPDATE fails, the entire operation is rolled back (no partial updates)
- [ ] Existing tests continue to pass

## Test Requirements
- [ ] Existing deletion tests pass without modification (the behavioral contract is unchanged)

## Target PR
https://github.com/trustify/trustify-backend/pull/744

## Review Context
**Comment ID:** 30001
**Reviewer:** reviewer-a
**File:** `modules/fundamental/src/sbom/service/sbom.rs`, line 60
**Comment text:**
> The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.
