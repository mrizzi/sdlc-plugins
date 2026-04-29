## Repository
trustify-backend

## Description
Wrap the three UPDATE statements in the `soft_delete` method inside a single database transaction to prevent inconsistent state when a partial failure occurs. Currently, if the `sbom_advisory` update fails after `sbom_package` succeeds, the database is left in an inconsistent state where some join table rows are marked as deleted but others are not.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` -- wrap the three `update_many` calls in `self.db.transaction(|txn| { ... })` and replace `self.db` with `txn` for each `exec` call

## Implementation Notes
- Use the SeaORM transaction API: `self.db.transaction::<_, (), DbErr>(|txn| { Box::pin(async move { ... }) }).await?`
- Replace `&self.db` with `txn` in each of the three `exec()` calls inside the `soft_delete` method
- The transaction ensures that all three UPDATE statements (sbom, sbom_package, sbom_advisory) either all succeed or all roll back
- Follow existing transaction patterns in the codebase (e.g., the ingestor module likely uses transactions for multi-table operations)

## Acceptance Criteria
- [ ] The `soft_delete` method wraps all three UPDATE operations in a single database transaction
- [ ] If any UPDATE fails, the entire operation is rolled back (no partial state)
- [ ] Existing tests continue to pass with the transactional implementation
- [ ] The DELETE endpoint still returns 204 on success, 404 on not found, 409 on already deleted

## Test Requirements
- [ ] Verify that the existing `test_delete_sbom_cascades_to_join_tables` test still passes
- [ ] Verify that a transaction rollback does not leave partial state (may require a failure simulation test)

## Review Context
**Original review comment (PR #744, comment 30001):**
> The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.

**File:** `modules/fundamental/src/sbom/service/sbom.rs`, line 60

## Target PR
https://github.com/trustify/trustify-backend/pull/744
