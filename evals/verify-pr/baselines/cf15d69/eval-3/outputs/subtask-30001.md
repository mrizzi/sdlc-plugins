## Repository
trustify-backend

## Target Branch
main

## Description
Wrap the three UPDATE statements in the `soft_delete` method (`SbomService`) inside a single database transaction to ensure atomicity. Currently, the `sbom`, `sbom_package`, and `sbom_advisory` updates execute independently -- if an intermediate update fails (e.g., `sbom_advisory` update fails after `sbom_package` succeeds), the database is left in an inconsistent state with partially applied soft-deletion.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` -- wrap the three `update_many` calls in `soft_delete` inside `self.db.transaction(|txn| { ... })` and replace `&self.db` with `txn` for each `exec` call

## Implementation Notes
- Use SeaORM's transaction API: `self.db.transaction::<_, (), DbErr>(|txn| { Box::pin(async move { ... }) }).await?`
- Replace each `.exec(&self.db)` with `.exec(txn)` inside the transaction closure
- The three operations that must be wrapped are:
  1. `sbom::Entity::update_many()` setting `deleted_at` on the SBOM record
  2. `sbom_package::Entity::update_many()` setting `deleted_at` on related package rows
  3. `sbom_advisory::Entity::update_many()` setting `deleted_at` on related advisory rows
- Follow the existing transaction pattern used elsewhere in the codebase (e.g., ingestor module operations that modify multiple tables atomically)
- The `now` timestamp should be computed before entering the transaction and moved into the closure

## Acceptance Criteria
- [ ] All three UPDATE statements in `soft_delete` execute within a single database transaction
- [ ] If any of the three updates fails, all changes are rolled back (no partial soft-deletion)
- [ ] Existing tests for SBOM deletion continue to pass
- [ ] The `soft_delete` method returns an error if the transaction fails

## Test Requirements
- [ ] Verify that the soft_delete method still correctly marks all three tables when all updates succeed
- [ ] Verify that existing integration tests in `tests/api/sbom_delete.rs` pass without modification

## Target PR
https://github.com/trustify/trustify-backend/pull/744

## Review Context
**Comment ID:** 30001
**Author:** reviewer-a
**File:** `modules/fundamental/src/sbom/service/sbom.rs`, line 60
**Comment:** "The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call."
