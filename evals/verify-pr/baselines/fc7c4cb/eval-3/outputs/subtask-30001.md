## Repository
trustify-backend

## Target Branch
TC-9103

## Description
Wrap the three UPDATE statements in the `soft_delete` method inside a single database transaction to prevent inconsistent state when one of the cascade updates fails after others have succeeded. Currently, the SBOM, sbom_package, and sbom_advisory updates execute as independent queries -- if the sbom_advisory update fails after sbom_package succeeds, the database is left in an inconsistent state where packages are marked deleted but advisories are not.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` -- wrap the three `update_many` calls in the `soft_delete` method inside a `self.db.transaction(|txn| { ... })` block and replace `self.db` with `txn` for each `exec` call

## Implementation Notes
- Use `self.db.transaction(|txn| { ... })` to create a database transaction that wraps all three UPDATE operations
- Replace `&self.db` with `txn` in each `.exec()` call within the transaction closure
- Follow the existing SeaORM transaction pattern used elsewhere in the codebase
- The transaction ensures atomicity: if any of the three updates fail, all changes are rolled back
- Preserve the existing `chrono::Utc::now()` timestamp usage and the order of operations (sbom first, then sbom_package, then sbom_advisory)

## Acceptance Criteria
- [ ] The `soft_delete` method wraps all three UPDATE statements in a single database transaction
- [ ] If any UPDATE fails, the entire operation is rolled back (no partial updates)
- [ ] The method continues to return `Result<()>` with appropriate error propagation
- [ ] Existing tests continue to pass without modification

## Target PR
https://github.com/trustify/trustify-backend/pull/744

## Review Context
**Comment ID:** 30001
**Author:** reviewer-a
**File:** `modules/fundamental/src/sbom/service/sbom.rs`, line 60
**Comment text:** "The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call."
