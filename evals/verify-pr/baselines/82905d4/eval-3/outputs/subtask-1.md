## Repository
trustify-backend

## Description
Wrap the three UPDATE statements in the `soft_delete` method in a database transaction to ensure atomicity. Currently, the method executes three independent `update_many` calls (for `sbom`, `sbom_package`, and `sbom_advisory`) without transactional guarantees. If any UPDATE fails after a preceding one succeeds, the database is left in an inconsistent state where some related rows are marked as deleted and others are not.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` — wrap the three UPDATE statements in `soft_delete` inside a `self.db.transaction(|txn| { ... })` block, replacing `&self.db` with `txn` for each `exec` call

## Implementation Notes
- Use SeaORM's transaction API: `self.db.transaction::<_, (), DbErr>(|txn| { Box::pin(async move { ... }) }).await?`
- Replace `&self.db` with `txn` in all three `exec()` calls within the `soft_delete` method
- The transaction ensures that if `sbom_advisory` update fails, the `sbom` and `sbom_package` updates are rolled back
- Follow existing transaction patterns in the `modules/ingestor/` module which likely uses the same SeaORM transaction API for multi-table operations

## Acceptance Criteria
- [ ] The three UPDATE statements in `soft_delete` execute within a single database transaction
- [ ] If any UPDATE fails, all preceding UPDATEs in the method are rolled back
- [ ] The `soft_delete` method returns an error if the transaction fails
- [ ] Existing tests continue to pass

## Test Requirements
- [ ] Existing `test_delete_sbom_returns_204` continues to pass with transactional soft_delete
- [ ] Existing `test_delete_sbom_cascades_to_join_tables` continues to pass

## Target PR
https://github.com/trustify/trustify-backend/pull/744

## Review Context
**Reviewer:** reviewer-a
**File:** `modules/fundamental/src/sbom/service/sbom.rs` (line 60)
**Comment:** The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.
