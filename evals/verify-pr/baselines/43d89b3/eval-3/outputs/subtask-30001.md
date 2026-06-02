## Repository
trustify-backend

## Target Branch
TC-9103

## Description
Wrap the three UPDATE statements in the `soft_delete` method inside a single database transaction. Currently, the sbom, sbom_package, and sbom_advisory updates execute independently. If a later update fails after earlier ones succeed, the database is left in an inconsistent state with partially-applied soft deletes. Using a transaction ensures atomicity: either all three tables are updated or none are.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` — wrap the three `update_many` calls in `soft_delete` inside `self.db.transaction(|txn| { ... })` and replace `&self.db` with `txn` for each `exec` call

## Implementation Notes
- Use SeaORM's transaction API: `self.db.transaction::<_, (), DbErr>(|txn| { Box::pin(async move { ... }) }).await?`
- Replace each `.exec(&self.db)` with `.exec(txn)` inside the transaction closure
- The three update operations (sbom, sbom_package, sbom_advisory) should all use the same `txn` connection reference
- Follow the existing error handling pattern with `Result<()>` return type
- The `chrono::Utc::now()` timestamp should be computed once before the transaction and captured by the closure

## Acceptance Criteria
- [ ] The `soft_delete` method wraps all three UPDATE statements in a single database transaction
- [ ] If any UPDATE fails, the entire operation is rolled back (no partial soft-deletes)
- [ ] The method continues to return `Result<()>` with the same error type
- [ ] Existing tests pass without modification

## Test Requirements
- [ ] Verify that the existing `test_delete_sbom_cascades_to_join_tables` test still passes with transactional writes
- [ ] Verify that a transaction rollback leaves all three tables unchanged (if testable with the existing test infrastructure)

## Target PR
https://github.com/trustify/trustify-backend/pull/744

## Review Context
**Comment ID:** 30001
**File:** `modules/fundamental/src/sbom/service/sbom.rs`, line 60
**Reviewer:** reviewer-a
**Comment:** The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.
