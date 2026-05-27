## Repository
trustify-backend

## Description
Wrap the three UPDATE statements in the `soft_delete` method inside a single database transaction to ensure atomicity. Currently, the `soft_delete` method in `SbomService` executes three separate UPDATE operations (sbom, sbom_package, sbom_advisory) without a transaction boundary. If any intermediate UPDATE fails (e.g., the sbom_advisory update fails after sbom_package succeeds), the database will be left in an inconsistent state where some related records are marked as deleted and others are not.

The fix is to use SeaORM's `self.db.transaction(|txn| { ... })` to wrap all three UPDATE statements, and replace `&self.db` with `txn` for each `.exec()` call within the transaction closure.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` -- modify the `soft_delete` method to wrap operations in a transaction

## Implementation Notes
- Use SeaORM's transaction API: `self.db.transaction::<_, (), DbErr>(|txn| { Box::pin(async move { ... }) }).await?`
- Replace `&self.db` with `txn` in each of the three `exec()` calls inside the transaction closure
- The transaction will automatically roll back if any operation returns an error
- Follow the existing error handling pattern using `Result<()>` return type
- Reference SeaORM transaction documentation for the exact closure signature
- The three operations that must be inside the transaction:
  1. `sbom::Entity::update_many()...exec(txn)` -- mark the SBOM as deleted
  2. `sbom_package::Entity::update_many()...exec(txn)` -- cascade to sbom_package rows
  3. `sbom_advisory::Entity::update_many()...exec(txn)` -- cascade to sbom_advisory rows

## Acceptance Criteria
- [ ] The `soft_delete` method wraps all three UPDATE statements in a single database transaction
- [ ] Each `.exec()` call uses the transaction handle (`txn`) instead of `self.db`
- [ ] If any UPDATE fails, the entire operation is rolled back (no partial updates)
- [ ] All existing tests in `tests/api/sbom_delete.rs` continue to pass
- [ ] The cascade test (`test_delete_sbom_cascades_to_join_tables`) confirms atomicity

## Target PR
https://github.com/trustify/trustify-backend/pull/744

## Review Context
"The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call."
