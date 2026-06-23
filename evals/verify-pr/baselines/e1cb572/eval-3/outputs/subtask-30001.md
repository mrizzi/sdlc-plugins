## Repository
trustify-backend

## Description
Wrap the three UPDATE statements in the `soft_delete` method inside a single database transaction to prevent inconsistent state when one of the cascade updates fails. Currently, the SBOM record, `sbom_package` rows, and `sbom_advisory` rows are updated in three separate database calls without transactional guarantees. If the `sbom_advisory` update fails after the `sbom_package` update succeeds, the database is left in an inconsistent state where some related rows are marked as deleted and others are not.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` -- wrap the three `update_many` calls in `soft_delete` inside a `self.db.transaction(|txn| { ... })` block

## Implementation Notes
- Use `self.db.transaction(|txn| { ... })` to wrap all three UPDATE statements in a single transaction
- Replace `self.db` with `txn` for each `.exec()` call inside the transaction closure
- Follow the existing transaction pattern used in the ingestor module (`modules/ingestor/src/`) for reference on SeaORM transaction usage
- The three operations that must be inside the transaction:
  1. Update `sbom::Entity` to set `deleted_at`
  2. Update `sbom_package::Entity` to set `deleted_at` for matching `sbom_id`
  3. Update `sbom_advisory::Entity` to set `deleted_at` for matching `sbom_id`
- Ensure the transaction rolls back all changes if any individual update fails

## Acceptance Criteria
- [ ] All three UPDATE statements in `soft_delete` execute within a single database transaction
- [ ] If any UPDATE fails, the transaction rolls back and no partial changes are persisted
- [ ] Existing integration tests continue to pass (the transactional wrapping should not change observable behavior on success)

## Test Requirements
- [ ] Verify that a successful soft-delete still marks all three entities (sbom, sbom_package, sbom_advisory) with `deleted_at`
- [ ] Verify that the existing `test_delete_sbom_cascades_to_join_tables` test continues to pass

## Target PR
https://github.com/trustify/trustify-backend/pull/744

## Review Context
**Comment ID:** 30001
**Author:** reviewer-a
**File:** `modules/fundamental/src/sbom/service/sbom.rs` (line 60)
**Comment text:** "The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call."
