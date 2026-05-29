## Repository
trustify-backend

## Target Branch
TC-9103

## Description
Wrap the three UPDATE statements in the `soft_delete` method inside a single database transaction to prevent inconsistent state when a partial failure occurs. Currently, the sbom, sbom_package, and sbom_advisory updates execute as independent queries -- if the sbom_advisory update fails after sbom_package succeeds, the database is left in an inconsistent state with some join table rows marked as deleted and others not.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` -- wrap the three `update_many` calls in `self.db.transaction(|txn| { ... })` and replace `&self.db` with `txn` for each `exec` call

## Implementation Notes
- Use `self.db.transaction(|txn| { ... })` to wrap all three UPDATE operations in a single transaction
- Replace `&self.db` with `txn` in each `.exec()` call inside the transaction closure
- The transaction pattern is used elsewhere in the codebase for multi-step database operations -- follow the existing pattern from the ingestor module's SBOM ingestion logic in `modules/ingestor/src/graph/sbom/mod.rs`
- Ensure the transaction rolls back automatically if any of the three updates fails
- The `now` timestamp should be computed before the transaction begins so all three updates use the same timestamp

## Acceptance Criteria
- [ ] All three UPDATE statements (sbom, sbom_package, sbom_advisory) execute within a single database transaction
- [ ] If any UPDATE fails, the entire transaction rolls back (no partial state)
- [ ] Existing tests continue to pass with the transactional implementation
- [ ] The `soft_delete` method signature remains unchanged

## Test Requirements
- [ ] Existing cascade test (`test_delete_sbom_cascades_to_join_tables`) still passes with transactional implementation

## Review Context
Reviewer reviewer-a commented on `modules/fundamental/src/sbom/service/sbom.rs` line 60:

> The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.

## Target PR
https://github.com/trustify/trustify-backend/pull/744
