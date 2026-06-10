## Repository
trustify-backend

## Target Branch
TC-9103

## Description
Wrap the three UPDATE statements in the `soft_delete` method inside a single database transaction to ensure atomicity. Currently, the sbom, sbom_package, and sbom_advisory updates execute independently. If the sbom_advisory update fails after sbom_package succeeds, the database is left in an inconsistent state with partially-marked cascade entries. Using `self.db.transaction()` ensures all three updates either succeed together or roll back together.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` -- wrap the three `update_many` calls in the `soft_delete` method inside a `self.db.transaction(|txn| { ... })` block, replacing `&self.db` with `txn` for each `exec` call

## Implementation Notes
- Use SeaORM's `TransactionTrait::transaction()` method on `self.db` to create a transaction scope
- Inside the transaction closure, replace `&self.db` with the transaction handle (`txn`) for all three `Entity::update_many().exec()` calls
- The transaction closure should return `Ok(())` on success; any `?` error propagation will automatically trigger a rollback
- Follow the existing error handling pattern in the service module (anyhow `Result` return type)

## Acceptance Criteria
- [ ] The `soft_delete` method wraps all three UPDATE statements (sbom, sbom_package, sbom_advisory) in a single database transaction
- [ ] If any of the three UPDATE operations fails, all changes are rolled back
- [ ] The method still returns `Result<()>` with the same error propagation behavior
- [ ] Existing tests in `tests/api/sbom_delete.rs` continue to pass

## Test Requirements
- [ ] Existing cascade test (`test_delete_sbom_cascades_to_join_tables`) confirms all three tables are updated atomically

## Review Context
**PR Comment ID:** 30001
**File:** modules/fundamental/src/sbom/service/sbom.rs (line 60)
**Reviewer:** reviewer-a
**Comment:** The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.

## Target PR
https://github.com/trustify/trustify-backend/pull/744
