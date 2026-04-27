## Repository
trustify-backend

## Description
Wrap the three UPDATE statements in the `soft_delete` method inside a single database transaction to prevent inconsistent state when a cascade update fails partway through. Currently, the `sbom`, `sbom_package`, and `sbom_advisory` updates execute as independent queries -- if the `sbom_advisory` update fails after `sbom_package` succeeds, the database is left with partially soft-deleted records. All three operations must succeed or fail atomically.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` — wrap the three `update_many` calls in `soft_delete` inside `self.db.transaction(|txn| { ... })` and replace `&self.db` with `txn` for each `.exec()` call

## Implementation Notes
- Use SeaORM's `TransactionTrait::transaction` method on `self.db` to create a transaction closure
- Inside the closure, use the transaction handle (`txn`) instead of `self.db` for all three `Entity::update_many().exec()` calls
- The transaction will automatically rollback if any operation returns an error
- Follow the existing error handling pattern: the `?` operator inside the transaction closure will trigger rollback on failure
- Reference: SeaORM transaction pattern is `self.db.transaction::<_, _, DbErr>(|txn| { Box::pin(async move { ... }) }).await`

## Acceptance Criteria
- [ ] The `soft_delete` method wraps all three UPDATE statements in a single database transaction
- [ ] If any of the three updates fails, all changes are rolled back (no partial soft-delete state)
- [ ] The `sbom`, `sbom_package`, and `sbom_advisory` updates all use the transaction handle instead of `self.db`
- [ ] Existing tests continue to pass with the transactional implementation

## Test Requirements
- [ ] Verify that the soft-delete operation remains functionally correct (204 response, records marked as deleted)
- [ ] Verify that cascade updates to `sbom_package` and `sbom_advisory` still occur within the transaction

## Target PR
https://github.com/trustify/trustify-backend/pull/744

## Review Context
**Comment ID:** 30001
**Reviewer:** reviewer-a
**File:** `modules/fundamental/src/sbom/service/sbom.rs`, line 60
**Original comment:**
> The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.
