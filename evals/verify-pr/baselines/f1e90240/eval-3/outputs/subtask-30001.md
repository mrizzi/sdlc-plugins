## Repository
trustify-backend

## Target Branch
main

## Description
Wrap the three UPDATE statements in `SbomService::soft_delete` inside a single database transaction to ensure atomicity. Currently, the method executes three independent `update_many` calls (sbom, sbom_package, sbom_advisory) without transactional protection. If the second or third update fails after the first succeeds, the database is left in an inconsistent state where the SBOM is marked as deleted but some related join table rows are not. Wrapping all three operations in a transaction ensures they either all succeed or all roll back.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` -- wrap the three `update_many` calls in `soft_delete` inside `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each `exec` call

## Implementation Notes
- Use `self.db.transaction(|txn| { ... })` to begin a transaction, following the SeaORM transaction pattern used elsewhere in the codebase
- Replace `&self.db` with `txn` in each of the three `.exec()` calls inside the transaction closure
- The transaction closure should be async and return `Result<(), DbErr>`
- The existing `chrono::Utc::now()` timestamp computation should remain outside the transaction (it does not need DB access)
- Reference: the ingestor module (`modules/ingestor/src/graph/sbom/mod.rs`) likely uses transactions for multi-statement operations -- follow that pattern

## Acceptance Criteria
- [ ] All three UPDATE statements (sbom, sbom_package, sbom_advisory) execute within a single database transaction
- [ ] If any UPDATE fails, all changes are rolled back (no partial soft-delete state)
- [ ] The endpoint still returns 204 No Content on successful deletion
- [ ] Existing tests continue to pass

## Test Requirements
- [ ] Verify that the existing `test_delete_sbom_returns_204` test still passes with transactional soft-delete
- [ ] Verify that the existing `test_delete_sbom_cascades_to_join_tables` test still passes

## Review Context
**Comment ID:** 30001
**Reviewer:** reviewer-a
**File:** `modules/fundamental/src/sbom/service/sbom.rs`, line 60
**Comment:** The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.

## Target PR
https://github.com/trustify/trustify-backend/pull/744
