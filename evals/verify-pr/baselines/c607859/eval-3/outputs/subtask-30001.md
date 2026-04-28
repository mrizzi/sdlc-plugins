# Sub-Task: Wrap soft_delete operations in a database transaction

**Parent:** TC-9103
**Labels:** ai-generated-jira, review-feedback

## Repository
trustify-backend

## Description
Wrap the three UPDATE statements in the `soft_delete` method of `SbomService` inside a single database transaction. Currently, the method executes three independent `update_many` calls (for `sbom`, `sbom_package`, and `sbom_advisory`) without transactional guarantees. If the second or third update fails after the first succeeds, the database is left in an inconsistent state where the SBOM is marked as deleted but related join table entries are not.

The fix should use `self.db.transaction(|txn| { ... })` to wrap all three operations, and replace `&self.db` with `txn` in each `.exec()` call within the transaction closure.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` -- wrap the three `update_many` calls in `soft_delete` inside a `self.db.transaction()` closure

## Implementation Notes
- Use SeaORM's `TransactionTrait::transaction()` method on `self.db` to create a transaction scope
- Inside the transaction closure, use the transaction handle (`txn`) instead of `self.db` for each `.exec()` call
- The transaction automatically commits on successful completion of the closure and rolls back on error
- Follow the existing error handling pattern -- the `?` operator inside the closure will propagate errors and trigger rollback
- Reference SeaORM transaction documentation for the exact closure signature: `self.db.transaction::<_, (), DbErr>(|txn| { Box::pin(async move { ... }) }).await?`

## Acceptance Criteria
- [ ] All three UPDATE statements (`sbom`, `sbom_package`, `sbom_advisory`) execute within a single database transaction
- [ ] If any UPDATE fails, all previously successful UPDATEs in the same `soft_delete` call are rolled back
- [ ] Existing tests in `tests/api/sbom_delete.rs` continue to pass
- [ ] The `soft_delete` method signature and return type remain unchanged

## Test Requirements
- [ ] Existing integration tests pass without modification (the behavioral contract is unchanged; only atomicity is added)

## Target PR
https://github.com/trustify/trustify-backend/pull/744

## Review Context
**Review comment ID:** 30001
**Author:** reviewer-a
**File:** `modules/fundamental/src/sbom/service/sbom.rs` (line 60)
**Comment:**
> The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.
