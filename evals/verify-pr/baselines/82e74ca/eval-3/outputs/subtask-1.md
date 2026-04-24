## Repository
trustify-backend

## Description
Wrap the three UPDATE operations in the `soft_delete` method inside a single database transaction to prevent inconsistent state. Currently, the method executes three sequential `update_many` calls (for `sbom`, `sbom_package`, and `sbom_advisory`) without transactional protection. If any intermediate update fails, the database will be left in a partially soft-deleted state.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` — wrap the three `update_many` calls in `soft_delete` inside `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each `.exec()` call

## Implementation Notes
- Use SeaORM's `TransactionTrait::transaction` method on `self.db` to wrap all three UPDATE operations
- Replace `&self.db` with `&txn` in each `.exec()` call inside the transaction closure
- Follow the existing error handling pattern — the transaction will automatically rollback on `Err`
- The `chrono::Utc::now()` timestamp should be computed once before the transaction and used for all three updates (already the case in current code)
- Reference `common/src/db/mod.rs` for any existing transaction utilities in the project

## Acceptance Criteria
- [ ] The three UPDATE operations in `soft_delete` run inside a single database transaction
- [ ] If any UPDATE fails, all changes are rolled back (no partial soft-delete state)
- [ ] The method still returns `Result<()>` with the same error semantics
- [ ] Existing tests continue to pass

## Test Requirements
- [ ] Existing `test_delete_sbom_returns_204` test continues to pass
- [ ] Existing `test_delete_sbom_cascades_to_join_tables` test continues to pass

## Target PR
https://github.com/trustify/trustify-backend/pull/744

## Review Context
**Reviewer:** reviewer-a
**File:** `modules/fundamental/src/sbom/service/sbom.rs` (line 60)
**Comment:** "The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call."
