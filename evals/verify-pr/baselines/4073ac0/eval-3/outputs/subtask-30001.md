## Repository
trustify-backend

## Target Branch
tc-9103-sbom-delete

## Description
Wrap the three UPDATE statements in the `soft_delete` method inside a single database transaction to ensure atomicity. Currently, if the `sbom_advisory` update fails after `sbom_package` succeeds, the database is left in an inconsistent state where some related rows are marked deleted and others are not.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` — wrap the three `update_many` calls in `soft_delete` inside `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each `exec` call

## Implementation Notes
- Use SeaORM's `DatabaseConnection::transaction` method to wrap the three update operations
- Replace `self.db` with the transaction handle `txn` in each `.exec()` call
- The transaction should cover the SBOM update, sbom_package update, and sbom_advisory update
- If any operation fails, the entire transaction rolls back automatically
- Follow existing transaction usage patterns in the codebase (e.g., check ingestor module for examples)

## Acceptance Criteria
- [ ] The `soft_delete` method wraps all three UPDATE operations in a single database transaction
- [ ] If any UPDATE fails, no rows are modified (full rollback)
- [ ] Existing tests continue to pass (no behavioral change for the success path)

## Test Requirements
- [ ] Verify that the existing `test_delete_sbom_cascades_to_join_tables` test still passes with transaction wrapping

## Review Context
**Original review comment (comment 30001 by reviewer-a):**
> The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.

**File:** `modules/fundamental/src/sbom/service/sbom.rs`, line 60

## Target PR
https://github.com/trustify/trustify-backend/pull/744
