## Repository
trustify-backend

## Description
Wrap the three UPDATE statements in the `soft_delete` method inside a single database transaction to prevent inconsistent state. Currently, the `sbom`, `sbom_package`, and `sbom_advisory` updates execute as independent queries. If any intermediate update fails (e.g., the `sbom_advisory` update fails after `sbom_package` succeeds), the database is left in a partially-deleted state where some related records have `deleted_at` set and others do not. All three operations must succeed or fail atomically.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` -- wrap the three `update_many` calls in `soft_delete` inside a `self.db.transaction(|txn| { ... })` block, replacing `&self.db` with `txn` for each `.exec()` call

## Implementation Notes
- Use the SeaORM transaction API: `self.db.transaction::<_, (), DbErr>(|txn| { Box::pin(async move { ... }) }).await?`
- Replace `&self.db` with `txn` in each of the three `.exec()` calls inside the transaction closure
- The three UPDATE operations target: `sbom::Entity`, `sbom_package::Entity`, and `sbom_advisory::Entity`, all setting their `deleted_at` column to `chrono::Utc::now()`
- Compute the `now` timestamp outside the transaction closure so all three records receive the exact same timestamp
- Follow existing transaction patterns in the codebase (check `modules/ingestor/src/graph/sbom/mod.rs` for multi-table transaction usage)

## Acceptance Criteria
- [ ] The `soft_delete` method wraps all three UPDATE statements in a single database transaction
- [ ] If any UPDATE fails, the entire operation is rolled back (no partial deletions)
- [ ] Existing tests in `tests/api/sbom_delete.rs` continue to pass without modification
- [ ] The `deleted_at` timestamp is identical across all three tables for a given deletion

## Target PR
https://github.com/trustify/trustify-backend/pull/744

## Review Context
Reviewer **reviewer-a** commented on `modules/fundamental/src/sbom/service/sbom.rs` (line 60):

> The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.
