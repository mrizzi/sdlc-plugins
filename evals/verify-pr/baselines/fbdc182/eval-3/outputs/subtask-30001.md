## Repository
trustify-backend

## Description
Wrap the three UPDATE statements in the `soft_delete` method inside a single database transaction to prevent inconsistent state. Currently, if one of the cascade updates fails after a preceding one succeeds, the database is left in an inconsistent state where some related records are marked as deleted while others are not.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` — wrap the three `update_many` operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each `.exec()` call

## Implementation Notes
- Use `self.db.transaction(|txn| { ... })` to wrap all three UPDATE operations (sbom, sbom_package, sbom_advisory) in a single transaction
- Replace `&self.db` with `txn` in each `.exec()` call within the transaction closure
- The transaction ensures atomicity: if any of the three updates fails, all changes are rolled back
- Follow existing transaction patterns in the codebase (e.g., check `modules/ingestor/src/graph/sbom/mod.rs` for transaction usage examples)

## Acceptance Criteria
- [ ] The `soft_delete` method wraps all three UPDATE statements in a single database transaction
- [ ] Each `.exec()` call within the transaction uses the transaction handle (`txn`) instead of `self.db`
- [ ] If any UPDATE fails, the entire operation is rolled back (no partial updates)
- [ ] Existing tests continue to pass without modification

## Test Requirements
- [ ] Verify existing soft-delete tests still pass with the transaction wrapper

## Target PR
https://github.com/trustify/trustify-backend/pull/744

## Review Context
**Reviewer:** reviewer-a
**File:** `modules/fundamental/src/sbom/service/sbom.rs` (line 60)
**Comment:** The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.
