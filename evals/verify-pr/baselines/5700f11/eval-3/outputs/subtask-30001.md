## Repository
trustify-backend

## Description
Wrap the three UPDATE statements in the `soft_delete` method inside a single database transaction to prevent inconsistent state when a partial failure occurs. Currently, the `sbom`, `sbom_package`, and `sbom_advisory` updates each execute independently against `self.db`. If the second or third update fails after earlier ones succeed, the database is left in an inconsistent state (e.g., the SBOM is marked deleted but its related `sbom_advisory` rows are not).

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` — wrap the three `update_many` calls in `soft_delete` inside `self.db.transaction(|txn| { ... })` and replace `&self.db` with `txn` in each `.exec()` call

## Implementation Notes
- Use SeaORM's `TransactionTrait::transaction` method on `self.db` to create an atomic transaction scope
- Inside the transaction closure, use `txn` (the transaction handle) instead of `&self.db` for all three `exec` calls
- The existing `update_many` pattern for each table (`sbom`, `sbom_package`, `sbom_advisory`) remains the same; only the executor changes from `&self.db` to `txn`
- Follow the error handling pattern used in other transactional operations in the codebase — propagate errors with `?` inside the closure so the transaction rolls back on failure
- The `chrono::Utc::now()` timestamp should be captured once before the transaction and reused for all three updates to ensure consistency

## Acceptance Criteria
- [ ] The three UPDATE statements in `soft_delete` execute within a single database transaction
- [ ] If any of the three updates fails, all changes are rolled back (no partial updates)
- [ ] The `deleted_at` timestamp is identical across the `sbom`, `sbom_package`, and `sbom_advisory` rows for a given deletion
- [ ] Existing tests continue to pass with no behavioral change on the success path

## Test Requirements
- [ ] Existing `test_delete_sbom_returns_204` continues to pass
- [ ] Existing `test_delete_sbom_cascades_to_join_tables` continues to pass

## Target PR
https://github.com/trustify/trustify-backend/pull/744

## Review Context
**Reviewer:** reviewer-a
**File:** `modules/fundamental/src/sbom/service/sbom.rs` (line 60)
**Comment:** "The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call."
