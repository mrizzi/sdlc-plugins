## Repository
trustify-backend

## Target Branch
main

## Description
Wrap the three UPDATE statements in the `soft_delete` method inside a single database transaction to ensure atomicity. Currently, if the `sbom_advisory` update fails after `sbom_package` succeeds, the database is left in an inconsistent state where some related entities are marked as deleted and others are not. Using `self.db.transaction(|txn| { ... })` and replacing `self.db` with `txn` for each exec call ensures all three updates succeed or fail together.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` -- wrap the three `update_many` calls in `soft_delete()` inside `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each `.exec()` call

## API Changes
- `DELETE /api/v2/sbom/{id}` -- MODIFY: no external API change, but the underlying soft-delete operation now runs atomically within a transaction

## Implementation Notes
- Use SeaORM's transaction API: `self.db.transaction::<_, _, DbErr>(|txn| { Box::pin(async move { ... }) }).await?`
- Replace each `.exec(&self.db)` with `.exec(txn)` inside the transaction closure
- The three UPDATE statements are: (1) set `deleted_at` on the `sbom` row, (2) set `deleted_at` on matching `sbom_package` rows, (3) set `deleted_at` on matching `sbom_advisory` rows
- All three must use the same `now` timestamp, which is already computed before the updates
- Follow the existing transaction pattern used elsewhere in the codebase (e.g., in the ingestor module for multi-table ingestion operations)

## Acceptance Criteria
- [ ] The `soft_delete` method wraps all three UPDATE statements in a single database transaction
- [ ] If any UPDATE fails, the entire operation is rolled back (no partial deletes)
- [ ] The existing behavior (setting `deleted_at` on sbom, sbom_package, and sbom_advisory) is preserved
- [ ] All existing tests in `tests/api/sbom_delete.rs` continue to pass

## Test Requirements
- [ ] Verify that the existing `test_delete_sbom_returns_204` test still passes with the transactional implementation
- [ ] Verify that the existing `test_delete_sbom_cascades_to_join_tables` test still passes, confirming cascade behavior within the transaction

## Review Context
**Original review comment (comment 30001, reviewer-a):**
> The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.

**File:** `modules/fundamental/src/sbom/service/sbom.rs`, line 60

## Target PR
https://github.com/trustify/trustify-backend/pull/744
