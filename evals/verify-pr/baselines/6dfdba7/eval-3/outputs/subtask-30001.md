## Repository
trustify-backend

## Description
Wrap the three UPDATE statements in the `soft_delete` method in a single database transaction to prevent inconsistent state. Currently, if the `sbom_advisory` update fails after the `sbom_package` update succeeds, the database is left with partially-deleted join table rows. Using `self.db.transaction(|txn| { ... })` ensures all three updates (sbom, sbom_package, sbom_advisory) either succeed together or roll back together.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` — wrap the three `update_many` calls in `soft_delete` inside a `self.db.transaction()` block, using the transaction handle `txn` instead of `self.db` for each `.exec()` call

## Implementation Notes
- Use SeaORM's transaction API: `self.db.transaction::<_, (), DbErr>(|txn| { Box::pin(async move { ... }) }).await?`
- Replace `&self.db` with `txn` in each of the three `.exec()` calls inside the transaction closure
- The existing pattern for transactions can be found in the ingestor module (`modules/ingestor/src/`) which uses similar multi-table updates during SBOM ingestion
- Ensure the `now` timestamp is captured before entering the transaction so all three tables receive the same `deleted_at` value
- The return type of the transaction closure should be `Result<(), DbErr>`

## Acceptance Criteria
- [ ] The `soft_delete` method wraps all three UPDATE statements in a single database transaction
- [ ] If any of the three updates fails, all changes are rolled back (no partial deletes)
- [ ] The method continues to return `Result<()>` with the same error semantics
- [ ] Existing tests in `tests/api/sbom_delete.rs` continue to pass

## Test Requirements
- [ ] Existing cascade test (`test_delete_sbom_cascades_to_join_tables`) validates that all three tables are updated atomically

## Review Context
**Reviewer:** reviewer-a
**PR Comment:** "The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call."
**File:** `modules/fundamental/src/sbom/service/sbom.rs`, line 60

## Target PR
https://github.com/trustify/trustify-backend/pull/744
