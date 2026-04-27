## Repository
trustify-backend

## Description
Wrap the three UPDATE statements in the `soft_delete` method inside a single database transaction to prevent inconsistent state if any individual update fails. Currently, the `sbom`, `sbom_package`, and `sbom_advisory` tables are updated independently. If the `sbom_advisory` update fails after `sbom_package` succeeds, the database is left in an inconsistent state where some join table rows are marked deleted and others are not.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` -- wrap the three `update_many` calls in `soft_delete` inside a `self.db.transaction()` block

## Implementation Notes
- Use `self.db.transaction(|txn| { ... })` to create a transaction scope around all three UPDATE operations in the `soft_delete` method
- Replace `&self.db` with `txn` for each `exec()` call inside the transaction block
- Follow the existing SeaORM transaction pattern used elsewhere in the codebase (check `modules/ingestor/src/` for examples of transaction usage)
- The `async_trait` and `TransactionTrait` imports from `sea_orm` will likely be needed
- Ensure the transaction is committed only after all three updates succeed; if any fails, the entire operation rolls back

## Acceptance Criteria
- [ ] The `soft_delete` method wraps all three UPDATE operations in a single database transaction
- [ ] If any individual UPDATE fails, no changes are persisted (full rollback)
- [ ] Existing tests continue to pass with the transactional implementation

## Test Requirements
- [ ] Verify that the existing `test_delete_sbom_cascades_to_join_tables` test still passes with the transactional implementation

## Target PR
https://github.com/trustify/trustify-backend/pull/744

## Review Context
**Comment ID:** 30001
**Reviewer:** reviewer-a
**File:** modules/fundamental/src/sbom/service/sbom.rs, line 60
**Comment:** "The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call."
