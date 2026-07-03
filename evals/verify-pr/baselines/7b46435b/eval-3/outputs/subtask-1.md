## Repository
trustify-backend

## Target Branch
main

## Description
Wrap the three UPDATE operations in `SbomService::soft_delete` inside a single database transaction to ensure atomicity. Currently, the method executes three sequential `update_many` calls (on `sbom`, `sbom_package`, and `sbom_advisory`) without transaction wrapping. If the second or third operation fails after the first succeeds, the database will be left in an inconsistent state where the SBOM is marked as deleted but some related join table rows are not.

## Target PR
https://github.com/trustify/trustify-backend/pull/744

## Review Context
**Comment ID:** 30001
**Author:** reviewer-a
**File:** `modules/fundamental/src/sbom/service/sbom.rs` (line 60)
**Text:** "The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call."

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` -- wrap the three `update_many` calls in `soft_delete` inside `self.db.transaction(|txn| { ... })` and replace `&self.db` with `txn` for each `.exec()` call

## Implementation Notes
- Use the SeaORM transaction API: `self.db.transaction::<_, (), DbErr>(|txn| { Box::pin(async move { ... }) }).await?`
- Replace each `.exec(&self.db)` with `.exec(txn)` inside the transaction closure
- The three operations that must be inside the transaction are:
  1. `sbom::Entity::update_many()` setting `DeletedAt` on the SBOM record
  2. `sbom_package::Entity::update_many()` setting `DeletedAt` on related package rows
  3. `sbom_advisory::Entity::update_many()` setting `DeletedAt` on related advisory rows
- Follow the existing error handling pattern: the transaction will automatically roll back on any `?` propagation inside the closure
- The `chrono::Utc::now()` timestamp should be computed once before or at the start of the transaction to ensure all three tables receive the same timestamp

## Acceptance Criteria
- [ ] All three UPDATE operations in `soft_delete` execute within a single database transaction
- [ ] If any of the three operations fails, all changes are rolled back (no partial updates)
- [ ] The `deleted_at` timestamp is identical across the SBOM record and its related join table rows

## Test Requirements
- [ ] Existing tests in `tests/api/sbom_delete.rs` continue to pass (no behavioral regression)
