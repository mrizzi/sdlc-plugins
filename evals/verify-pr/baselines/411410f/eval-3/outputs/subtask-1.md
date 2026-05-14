## Repository
trustify-backend

## Target Branch
main

## Description
Wrap the three UPDATE statements in the `soft_delete` method inside a single database transaction to prevent inconsistent state when a partial failure occurs. Currently, the `sbom`, `sbom_package`, and `sbom_advisory` updates execute independently — if the `sbom_advisory` update fails after `sbom_package` succeeds, the database is left in an inconsistent state where some related rows are marked as deleted but others are not.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` — wrap the three `update_many` calls in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each `exec` call

## Implementation Notes
- Use SeaORM's `TransactionTrait::transaction()` method on `self.db` to wrap all three UPDATE operations
- Replace `&self.db` with `&txn` in each `.exec()` call inside the transaction closure
- The transaction ensures atomicity: if any UPDATE fails, all changes are rolled back
- Follow the existing transaction patterns in the codebase (check `modules/ingestor/` for examples of transaction usage)
- The method signature and return type should remain unchanged

## Acceptance Criteria
- [ ] The three UPDATE statements in `soft_delete` execute inside a single database transaction
- [ ] If any UPDATE fails, the entire operation is rolled back (no partial updates)
- [ ] The method continues to return `Result<()>` with the same error semantics
- [ ] Existing tests continue to pass

## Test Requirements
- [ ] Verify that the cascade update test (`test_delete_sbom_cascades_to_join_tables`) still passes with transactional execution

## Review Context
**PR Comment ID:** 30001
**Reviewer:** reviewer-a
**File:** `modules/fundamental/src/sbom/service/sbom.rs` (line 60)
**Comment:** The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.

## Target PR
https://github.com/trustify/trustify-backend/pull/744
