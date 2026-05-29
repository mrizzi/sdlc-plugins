## Repository
trustify-backend

## Target Branch
main

## Description
Wrap the three UPDATE operations in `SbomService::soft_delete` inside a single database transaction to ensure atomicity. Currently, the `soft_delete` method executes three separate `update_many` calls (on `sbom`, `sbom_package`, and `sbom_advisory`) without transaction wrapping. If any of the later updates fail after earlier ones succeed, the database will be left in an inconsistent state with partially soft-deleted records.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` -- wrap the three `update_many` calls in `soft_delete` inside `self.db.transaction(|txn| { ... })` and replace `self.db` with `txn` for each `.exec()` call

## Implementation Notes
- Use `self.db.transaction(|txn| { ... })` to create a transaction scope around all three UPDATE operations in the `soft_delete` method
- Replace `&self.db` with `txn` in each `.exec()` call within the transaction closure
- Follow the existing SeaORM transaction pattern used elsewhere in the codebase (check `modules/ingestor/src/graph/sbom/mod.rs` for transaction usage examples)
- The transaction ensures that if the `sbom_advisory` update fails, the `sbom` and `sbom_package` updates are rolled back, preventing inconsistent state
- The `now` timestamp variable should be captured before the transaction and moved into the closure

## Acceptance Criteria
- [ ] The `soft_delete` method wraps all three UPDATE operations in a single database transaction
- [ ] If any UPDATE fails, all previous UPDATEs within the method are rolled back
- [ ] Successful soft-delete behavior is unchanged (all three tables are updated with the same `deleted_at` timestamp)

## Test Requirements
- [ ] Existing tests continue to pass (test_delete_sbom_returns_204, test_delete_nonexistent_sbom_returns_404, test_delete_already_deleted_sbom_returns_409, test_list_sboms_include_deleted, test_delete_sbom_cascades_to_join_tables)

## Review Context
**Original comment by reviewer-a on `modules/fundamental/src/sbom/service/sbom.rs` line 60:**
> The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.

## Target PR
https://github.com/trustify/trustify-backend/pull/744
