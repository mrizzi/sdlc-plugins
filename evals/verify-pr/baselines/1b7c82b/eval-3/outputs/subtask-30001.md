## Repository
trustify-backend

## Target Branch
main

## Description
Wrap the three UPDATE statements in the `soft_delete` method inside a single database transaction to ensure atomicity. Currently, the sbom, sbom_package, and sbom_advisory updates are executed independently against `self.db`. If any update fails after a preceding one succeeds, the database is left in an inconsistent state (e.g., the sbom record is marked as deleted but the sbom_advisory rows are not). All three operations must succeed or fail together.

## Target PR
https://github.com/trustify/trustify-backend/pull/744

## Review Context
Reviewer **reviewer-a** commented on `modules/fundamental/src/sbom/service/sbom.rs` (line 60):

> The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` — wrap the three `update_many().exec()` calls in the `soft_delete` method inside a `self.db.transaction(|txn| { ... })` block, replacing `&self.db` with `txn` for each exec call

## Implementation Notes
- Use the SeaORM transaction API: `self.db.transaction::<_, (), DbErr>(|txn| { Box::pin(async move { ... }) }).await?`
- Replace each `.exec(&self.db)` with `.exec(txn)` inside the transaction closure
- The three UPDATE statements are: (1) set `deleted_at` on the sbom record, (2) set `deleted_at` on sbom_package rows where sbom_id matches, (3) set `deleted_at` on sbom_advisory rows where sbom_id matches
- Follow the existing transaction patterns used elsewhere in the codebase (e.g., in the ingestor module)
- The `now` timestamp should be computed once before the transaction and captured by the closure

## Acceptance Criteria
- [ ] The `soft_delete` method wraps all three UPDATE operations in a single database transaction
- [ ] If any UPDATE fails, the entire transaction is rolled back (no partial updates)
- [ ] Each `.exec()` call uses the transaction handle (`txn`) instead of `self.db`
- [ ] Existing tests for deletion continue to pass (204 response, cascade updates, 409 on re-delete)

## Test Requirements
- [ ] Existing test `test_delete_sbom_returns_204` continues to pass
- [ ] Existing test `test_delete_sbom_cascades_to_join_tables` continues to pass
