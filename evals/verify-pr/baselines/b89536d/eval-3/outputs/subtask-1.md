## Repository
trustify-backend

## Target Branch
main

## Description
Wrap the three UPDATE statements in the `soft_delete` method inside a single database transaction to prevent inconsistent state. Currently, the SBOM, sbom_package, and sbom_advisory updates are executed as independent queries. If the sbom_advisory update fails after sbom_package succeeds, the database will be left in an inconsistent state with partially applied soft-deletion.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` -- wrap the three `update_many` calls in `self.db.transaction(|txn| { ... })` and use `txn` for each `exec` call

## Implementation Notes
- Use SeaORM's transaction API: `self.db.transaction::<_, (), DbErr>(|txn| { Box::pin(async move { ... }) }).await?`
- Replace `&self.db` with `txn` in all three `exec()` calls within the `soft_delete` method
- The transaction ensures atomicity: if any of the three UPDATE statements fails, all changes are rolled back
- Follow the existing error handling pattern using `?` operator inside the transaction closure

## Acceptance Criteria
- [ ] The `soft_delete` method wraps all three UPDATE statements in a single database transaction
- [ ] Each `exec()` call uses the transaction handle (`txn`) instead of `self.db`
- [ ] If any UPDATE fails, no changes are persisted (rollback behavior)
- [ ] Existing tests continue to pass

## Test Requirements
- [ ] Verify that the existing `test_delete_sbom_cascades_to_join_tables` test still passes with transactional execution

## Target PR
https://github.com/trustify/trustify-backend/pull/744

## Review Context
**Comment ID:** 30001
**Author:** reviewer-a
**File:** modules/fundamental/src/sbom/service/sbom.rs, line 60
**Comment:**
> The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.
