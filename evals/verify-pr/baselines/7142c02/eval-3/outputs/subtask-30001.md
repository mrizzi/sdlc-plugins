## Repository
trustify-backend

## Description
Wrap the three UPDATE statements in the `soft_delete` method inside a single database transaction to prevent inconsistent state if any individual update fails. Currently, the method executes three independent `update_many` calls on the `sbom`, `sbom_package`, and `sbom_advisory` tables in sequence without transactional wrapping. If the `sbom_advisory` update fails after `sbom_package` succeeds, the database is left in an inconsistent state with partially soft-deleted records.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` -- wrap the `soft_delete` method body in `self.db.transaction(|txn| { ... })` and replace `&self.db` with `txn` for each `exec` call

## Implementation Notes
- Use SeaORM's transaction API: `self.db.transaction::<_, _, DbErr>(|txn| { Box::pin(async move { ... }) }).await?`
- Replace `&self.db` with `txn` in all three `exec()` calls within the transaction closure
- Keep the same `chrono::Utc::now()` timestamp assignment -- all three tables should use the same `deleted_at` value
- Error from any update inside the transaction will cause automatic rollback of all changes
- Follow the existing error handling pattern in the codebase using `Result<T, AppError>` with `.context()` wrapping

## Acceptance Criteria
- [ ] All three UPDATE statements (`sbom`, `sbom_package`, `sbom_advisory`) execute within a single database transaction
- [ ] If any UPDATE fails, all changes are rolled back (no partial soft-delete state)
- [ ] The `deleted_at` timestamp is the same across all three tables for a given deletion
- [ ] Existing tests continue to pass with the transaction wrapping

## Target PR
https://github.com/trustify/trustify-backend/pull/744

## Review Context
Review comment #30001 by reviewer-a on `modules/fundamental/src/sbom/service/sbom.rs` line 60:

"The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call."
