## Repository
trustify-backend

## Target Branch
tc-9103-sbom-delete

## Target PR
https://github.com/trustify/trustify-backend/pull/744

## Description
Wrap the three UPDATE statements in the `soft_delete` method inside a single database transaction to prevent inconsistent state when a partial failure occurs. Currently, the SBOM, sbom_package, and sbom_advisory updates execute as independent operations against `self.db`. If the sbom_advisory update fails after the sbom_package update succeeds, the database is left in an inconsistent state where some tables are marked deleted and others are not.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` -- wrap the three `update_many().exec()` calls in a transaction

## Implementation Notes
- Use `self.db.transaction(|txn| { ... })` (SeaORM transaction API) to wrap all three UPDATE statements
- Replace `&self.db` with `txn` inside the transaction closure for each `exec` call
- The transaction should encompass: updating `sbom::Entity`, `sbom_package::Entity`, and `sbom_advisory::Entity`
- If any UPDATE fails, the transaction rolls back automatically, preventing partial state
- Follow the existing SeaORM transaction pattern used elsewhere in the codebase

## Acceptance Criteria
- [ ] The `soft_delete` method wraps all three UPDATE statements in a single database transaction
- [ ] If any UPDATE fails, the entire operation rolls back (no partial deletes)
- [ ] Existing tests continue to pass (no behavioral change for the happy path)
- [ ] The transaction uses `txn` instead of `self.db` for each exec call within the closure

## Review Context
**Comment ID:** 30001
**Author:** reviewer-a
**File:** `modules/fundamental/src/sbom/service/sbom.rs` (line 60)
**Original comment:** "The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call."
