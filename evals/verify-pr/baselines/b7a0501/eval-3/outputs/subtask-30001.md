# Sub-task: Wrap soft_delete operations in a database transaction

**Parent Task**: TC-9103
**Source**: PR review comment #30001

---

## Repository
trustify-backend

## Description
The `soft_delete` method in `SbomService` currently executes three independent UPDATE statements to mark the SBOM, its related `sbom_package` rows, and its related `sbom_advisory` rows as deleted. These operations are not wrapped in a database transaction, which means a failure in any statement after a previous one succeeds will leave the database in an inconsistent state (e.g., the SBOM is marked deleted but its advisory associations are not).

Wrap all three UPDATE operations inside a single database transaction to ensure atomicity. Use SeaORM's `self.db.transaction(|txn| { ... })` and replace `self.db` with `txn` for each `exec` call within the closure.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` -- Refactor the `soft_delete` method to use a transaction

## Implementation Notes
- Use `self.db.transaction(|txn| { ... })` to create a transaction scope
- Replace `&self.db` with `txn` in each of the three `exec()` calls inside the transaction closure
- Ensure the transaction returns `Ok(())` on success and propagates errors to trigger rollback
- Follow existing transaction patterns in the codebase (e.g., check the ingestor module for examples)
- The method signature (`pub async fn soft_delete(&self, id: i64) -> Result<()>`) should remain unchanged

## Acceptance Criteria
- [ ] All three UPDATE statements (sbom, sbom_package, sbom_advisory) execute within a single database transaction
- [ ] If any UPDATE fails, all changes are rolled back (no partial soft-delete state)
- [ ] Existing tests continue to pass without modification
- [ ] The `soft_delete` method returns `Result<()>` with proper error propagation

## Target PR
https://github.com/trustify/trustify-backend/pull/744

## Review Context
Original review comment by **reviewer-a** on `modules/fundamental/src/sbom/service/sbom.rs` (line 60):

> The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.
