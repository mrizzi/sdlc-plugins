## Repository
trustify-backend

## Description
Wrap the three UPDATE statements in the `soft_delete` method inside a single database transaction to ensure atomicity. Currently, the `soft_delete` method in `SbomService` executes three separate UPDATE statements (for `sbom`, `sbom_package`, and `sbom_advisory` tables) without transaction wrapping. If the second or third UPDATE fails after a previous one succeeds, the database is left in an inconsistent state with partially-applied soft deletes.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` -- wrap the three `update_many` calls in `soft_delete` inside a `self.db.transaction(|txn| { ... })` block and use `txn` instead of `self.db` for each `exec` call

## Implementation Notes
- Use `self.db.transaction(|txn| { ... })` to create a transaction scope around the three UPDATE operations in the `soft_delete` method
- Replace `self.db` with `txn` in each `.exec()` call within the transaction block so all three updates share the same transaction context
- Follow the existing SeaORM transaction pattern used elsewhere in the codebase (check other service files in `modules/fundamental/src/*/service/` for examples of transaction usage)
- The method signature and return type should remain unchanged; only the internal implementation wraps in a transaction
- Ensure the `now` timestamp is computed before the transaction begins so all three tables receive the same `deleted_at` value

## Acceptance Criteria
- [ ] The `soft_delete` method wraps all three UPDATE statements (`sbom`, `sbom_package`, `sbom_advisory`) in a single database transaction
- [ ] Each `exec` call within the transaction uses the transaction handle (`txn`) instead of `self.db`
- [ ] If any UPDATE fails, the entire operation is rolled back (no partial soft-deletes)
- [ ] All existing tests in `tests/api/sbom_delete.rs` continue to pass
- [ ] The DELETE endpoint behavior is unchanged from the caller's perspective (204 on success, 404 on not found, 409 on already deleted)

## Target PR
https://github.com/trustify/trustify-backend/pull/744

## Review Context
**Comment ID:** 30001
**Author:** reviewer-a
**File:** `modules/fundamental/src/sbom/service/sbom.rs`, line 60
**Comment text:**
> The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.
