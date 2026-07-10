# Sub-Task: Wrap soft_delete cascade operations in a database transaction

**Issue Type:** Sub-task
**Parent:** TC-9103
**Summary:** Wrap soft_delete cascade operations in a database transaction
**Labels:** ai-generated-jira, review-feedback

---

## Repository
trustify-backend

## Description
The `soft_delete` method in `SbomService` performs three sequential UPDATE operations (on `sbom`, `sbom_package`, and `sbom_advisory` tables) without transactional wrapping. If any intermediate operation fails (e.g., the `sbom_advisory` update fails after `sbom_package` succeeds), the database is left in an inconsistent state with partially applied soft-deletion. Wrap all three UPDATE statements in a single database transaction to ensure atomicity.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` -- wrap the three `update_many` calls in `soft_delete` inside `self.db.transaction(|txn| { ... })` and replace `&self.db` with `txn` for each `exec` call

## Implementation Notes
- Use SeaORM's transaction API: `self.db.transaction::<_, (), DbErr>(|txn| { Box::pin(async move { ... }) }).await?`
- Replace each `.exec(&self.db)` with `.exec(txn)` inside the transaction closure
- The existing pattern for transactions in the codebase uses `DatabaseConnection::transaction()` -- follow the same pattern used elsewhere in the service layer
- Ensure the transaction rolls back automatically if any of the three UPDATE operations returns an error
- The `now` timestamp computation can remain outside the transaction since it is a pure value with no database dependency

## Acceptance Criteria
- [ ] The `soft_delete` method wraps all three UPDATE operations (`sbom`, `sbom_package`, `sbom_advisory`) in a single database transaction
- [ ] If any UPDATE operation fails, the entire transaction is rolled back (no partial soft-deletion)
- [ ] The method continues to return `Result<()>` with the same success/error semantics
- [ ] Existing tests in `tests/api/sbom_delete.rs` continue to pass

## Test Requirements
- [ ] Verify that the existing `test_delete_sbom_returns_204` test still passes with transactional wrapping
- [ ] Verify that the existing `test_delete_sbom_cascades_to_join_tables` test still passes

## Target PR
https://github.com/trustify/trustify-backend/pull/744

## Review Context
**Comment ID:** 30001
**Author:** reviewer-a
**File:** `modules/fundamental/src/sbom/service/sbom.rs`, line 60
**Comment:**
> The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.
