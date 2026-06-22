## Repository
trustify-backend

## Target Branch
main

## Description
Wrap the three UPDATE operations in the `soft_delete()` method inside a single database transaction to prevent partial updates that would leave the database in an inconsistent state. Currently, the method performs three independent `update_many` calls (sbom, sbom_package, sbom_advisory) without transactional boundaries. If the sbom_advisory update fails after sbom_package succeeds, the database would have the parent SBOM marked as deleted but some child rows unmarked.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` — wrap the three `update_many` operations in `soft_delete()` inside `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each `exec` call

## Implementation Notes
- Use the SeaORM transaction API: `self.db.begin().await?` to start a transaction, then pass the transaction handle to each `exec()` call, and commit at the end.
- Alternatively, use the closure-based API `self.db.transaction::<_, (), DbErr>(|txn| { Box::pin(async move { ... }) }).await?` which auto-commits on success and rolls back on error.
- Follow the existing error handling pattern in the codebase using `Result<(), DbErr>` with `?` propagation.
- The `chrono::Utc::now()` timestamp should be computed once before the transaction begins (already done in current code) so all three tables receive the same timestamp.

## Acceptance Criteria
- [ ] All three UPDATE operations (sbom, sbom_package, sbom_advisory) execute within a single database transaction
- [ ] If any UPDATE fails, all previously successful UPDATEs within the transaction are rolled back
- [ ] The `soft_delete()` method returns an error if the transaction fails, propagating the underlying database error
- [ ] Existing tests continue to pass (test_delete_sbom_returns_204, test_delete_already_deleted_sbom_returns_409, test_delete_sbom_cascades_to_join_tables)

## Test Requirements
- [ ] Existing integration tests in `tests/api/sbom_delete.rs` continue to pass without modification
- [ ] Verify that cascade deletion still works correctly with transaction wrapping (test_delete_sbom_cascades_to_join_tables)

## Review Context
**Original review comment (ID 30001) by reviewer-a on `modules/fundamental/src/sbom/service/sbom.rs` line 60:**

> The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.

## Target PR
https://github.com/trustify/trustify-backend/pull/744
