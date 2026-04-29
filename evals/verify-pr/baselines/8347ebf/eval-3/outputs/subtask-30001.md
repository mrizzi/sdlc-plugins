## Repository
trustify-backend

## Description
Wrap the three UPDATE statements in the `soft_delete` method inside a single database transaction to ensure atomicity. Currently, if the `sbom_advisory` update fails after `sbom_package` succeeds, the database is left in an inconsistent state with partially soft-deleted records. The fix ensures all three updates (sbom, sbom_package, sbom_advisory) either all succeed or all roll back.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` -- wrap the three `update_many` calls in `self.db.transaction(|txn| { ... })` and replace `&self.db` with `txn` in each `.exec()` call

## Implementation Notes
- Use SeaORM's transaction API: `self.db.transaction::<_, (), DbErr>(|txn| { Box::pin(async move { ... }) }).await?`
- Replace `&self.db` with `txn` as the executor for all three `Entity::update_many().exec()` calls inside the transaction closure
- Follow the existing transaction pattern used in the ingestor module (`modules/ingestor/src/graph/sbom/mod.rs`) which demonstrates SeaORM transaction usage in this codebase
- The transaction boundary should encompass only the three UPDATE statements, not the initial fetch

## Reuse Candidates
- `modules/ingestor/src/graph/sbom/mod.rs` -- contains existing SeaORM transaction usage patterns that demonstrate the correct closure and executor syntax

## Acceptance Criteria
- [ ] The `soft_delete` method wraps all three UPDATE statements in a single database transaction
- [ ] Each `.exec()` call uses the transaction handle (`txn`) instead of `self.db`
- [ ] If any UPDATE fails, all changes are rolled back (no partial soft-delete state)
- [ ] Existing tests in `tests/api/sbom_delete.rs` continue to pass

## Test Requirements
- [ ] Existing test `test_delete_sbom_returns_204` passes with transactional soft-delete
- [ ] Existing test `test_delete_sbom_cascades_to_join_tables` passes with transactional soft-delete

## Review Context
**Reviewer:** reviewer-a
**Comment ID:** 30001
**File:** `modules/fundamental/src/sbom/service/sbom.rs` (line 60)
**Comment:** "The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call."

## Target PR
https://github.com/trustify/trustify-backend/pull/744
