## Repository
trustify-backend

## Target Branch
main

## Description
Wrap the three UPDATE operations in the `soft_delete` method inside a single database transaction to prevent inconsistent state when a partial failure occurs. Currently, the `sbom`, `sbom_package`, and `sbom_advisory` updates are executed independently -- if the `sbom_advisory` update fails after `sbom_package` succeeds, the data will be left in an inconsistent state with some join table rows marked as deleted and others not.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` -- wrap the three `update_many` calls in `soft_delete` inside `self.db.transaction(|txn| { ... })` and replace `&self.db` with `txn` for each `exec` call

## Implementation Notes
- Use SeaORM's `TransactionTrait::transaction` method on `self.db` to begin a transaction
- Inside the transaction closure, perform all three `update_many` operations using the transaction handle (`txn`) instead of `self.db`
- Follow the existing transaction patterns in the codebase (e.g., in the ingestor module where multi-table writes are wrapped in transactions)
- The method signature and return type do not need to change; the transaction either commits all three updates or rolls back entirely
- Pattern: `self.db.transaction::<_, (), DbErr>(|txn| { Box::pin(async move { ... }) }).await?;`

## Acceptance Criteria
- [ ] All three UPDATE operations in `soft_delete` (sbom, sbom_package, sbom_advisory) execute within a single database transaction
- [ ] If any UPDATE fails, the entire transaction is rolled back and no rows are modified
- [ ] The method continues to return `Result<()>` with the same success/error semantics
- [ ] Existing tests in `tests/api/sbom_delete.rs` continue to pass

## Test Requirements
- [ ] Existing integration tests pass without modification (transaction wrapping is transparent to callers)

## Target PR
https://github.com/trustify/trustify-backend/pull/744

## Review Context
**Comment ID:** 30001
**Reviewer:** reviewer-a
**File:** modules/fundamental/src/sbom/service/sbom.rs, line 60
**Comment:** "The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call."
