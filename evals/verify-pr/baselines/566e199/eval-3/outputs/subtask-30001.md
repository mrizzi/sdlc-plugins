## Repository
trustify-backend

## Description
Wrap the three UPDATE statements in the `soft_delete` method of `SbomService` inside a single database transaction. Currently, the method executes three sequential `update_many` calls (for `sbom`, `sbom_package`, and `sbom_advisory`) without transactional wrapping. If any of the later updates fail after earlier ones succeed, the database is left in an inconsistent state with partially soft-deleted records. Use `self.db.transaction(|txn| { ... })` and replace `self.db` with `txn` for each `exec` call inside the closure.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` -- wrap the three update_many calls in soft_delete inside a database transaction

## Implementation Notes
- Use SeaORM's `self.db.transaction(|txn| { ... })` pattern to wrap the three UPDATE operations
- Replace `&self.db` with `txn` (or `&txn`) for each `.exec()` call inside the transaction closure
- The transaction ensures atomicity: if `sbom_advisory` update fails, the `sbom` and `sbom_package` updates are rolled back
- Follow existing transaction patterns in the codebase if any exist (check ingestor module for examples)

## Acceptance Criteria
- [ ] The `soft_delete` method wraps all three UPDATE operations in a single database transaction
- [ ] If any UPDATE fails, all previously successful UPDATEs within the transaction are rolled back
- [ ] Existing tests continue to pass (no behavioral change for the success path)

## Target PR
https://github.com/trustify/trustify-backend/pull/744

## Review Context
**Comment ID:** 30001
**Author:** reviewer-a
**File:** `modules/fundamental/src/sbom/service/sbom.rs`, line 60
**Text:** "The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call."
