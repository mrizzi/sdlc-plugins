## Repository
trustify-backend

## Description
Wrap the three UPDATE statements in the `soft_delete` method inside a single database transaction. Currently, the method executes three sequential `update_many` calls against `sbom`, `sbom_package`, and `sbom_advisory` tables without transaction wrapping. If any intermediate update fails (e.g., the `sbom_advisory` update fails after `sbom_package` succeeds), the database is left in an inconsistent state with partially marked soft-deleted records.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` -- wrap the three UPDATE statements in `soft_delete` inside a `self.db.transaction(|txn| { ... })` block

## Implementation Notes
- Use SeaORM's `self.db.transaction(|txn| { ... })` API to wrap all three `update_many` operations in a single transaction
- Replace `&self.db` with `txn` as the executor for each `exec()` call inside the transaction closure
- Follow the existing transaction usage pattern in the ingestor module (`modules/ingestor/src/`) where multi-table mutations are wrapped in transactions
- The three operations to wrap are: (1) update `sbom` setting `deleted_at`, (2) update `sbom_package` where `sbom_id` matches, (3) update `sbom_advisory` where `sbom_id` matches
- Ensure the `now` timestamp is computed before entering the transaction closure so all three tables receive the same timestamp

## Acceptance Criteria
- [ ] The `soft_delete` method wraps all three UPDATE statements in a single database transaction
- [ ] If any UPDATE fails, the entire operation is rolled back (no partial soft-delete state)
- [ ] All existing tests continue to pass (test_delete_sbom_returns_204, test_delete_nonexistent_sbom_returns_404, test_delete_already_deleted_sbom_returns_409, test_list_sboms_include_deleted, test_delete_sbom_cascades_to_join_tables)
- [ ] The transaction uses `txn` as the executor instead of `self.db` for each operation

## Test Requirements
- [ ] Existing tests in `tests/api/sbom_delete.rs` pass without modification (transaction wrapping should not change observable behavior for successful operations)

## Target PR
https://github.com/trustify/trustify-backend/pull/744

## Review Context
**Comment ID:** 30001
**Author:** reviewer-a
**File:** modules/fundamental/src/sbom/service/sbom.rs (line 60)
**Comment text:** "The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call."
