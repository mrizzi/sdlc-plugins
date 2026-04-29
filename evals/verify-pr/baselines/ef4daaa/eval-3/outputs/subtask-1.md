## Repository
trustify-backend

## Description
Wrap the three UPDATE statements in the `soft_delete` method inside a single database transaction to ensure atomicity. Currently, the `sbom`, `sbom_package`, and `sbom_advisory` tables are updated with separate `exec` calls against `self.db`. If the `sbom_advisory` update fails after `sbom_package` succeeds, the database will be left in an inconsistent state where some related rows are marked deleted and others are not.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` -- wrap the three `update_many` calls in `soft_delete` inside a `self.db.transaction(|txn| { ... })` block, replacing `&self.db` with `txn` in each `exec` call

## Implementation Notes
- Use `self.db.transaction(|txn| { ... })` to wrap all three UPDATE statements (sbom, sbom_package, sbom_advisory) in a single transaction
- Replace `&self.db` with `txn` for all three `exec` calls inside the transaction closure
- The transaction ensures that either all three tables are updated atomically, or none are, preventing inconsistent state on partial failure
- Follow the existing error handling pattern using `?` operator inside the transaction closure
- The `chrono::Utc::now()` timestamp should be captured once before the transaction and reused for all three updates (current behavior is correct in this regard)

## Acceptance Criteria
- [ ] All three UPDATE statements in `soft_delete` execute within a single database transaction
- [ ] If any UPDATE fails, all changes are rolled back (no partial soft-delete state)
- [ ] The method returns the transaction error if any step fails

## Test Requirements
- [ ] Existing tests continue to pass (transaction wrapping should not change observable behavior on success)

## Target PR
https://github.com/trustify/trustify-backend/pull/744

## Review Context
**Comment ID:** 30001
**File:** `modules/fundamental/src/sbom/service/sbom.rs` (line 60)
**Reviewer:** reviewer-a
**Comment:** "The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call."
