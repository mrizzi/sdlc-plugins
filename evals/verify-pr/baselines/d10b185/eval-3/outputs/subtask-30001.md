# Sub-Task for Review Comment 30001

**Parent:** TC-9103
**Summary:** Wrap soft_delete operations in a database transaction for atomicity
**Labels:** ai-generated-jira, review-feedback

---

## Repository
trustify-backend

## Target Branch
main

## Description
The `soft_delete` method in `SbomService` executes three independent UPDATE statements (for `sbom`, `sbom_package`, and `sbom_advisory` tables) without transactional guarantees. If any intermediate operation fails (e.g., the `sbom_advisory` update fails after `sbom_package` succeeds), the database will be left in an inconsistent state with some records marked as deleted and others not. Wrap all three operations in a single database transaction to ensure atomicity.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` -- wrap the three UPDATE statements in `soft_delete` inside a `self.db.transaction(|txn| { ... })` block and use `txn` instead of `self.db` for each `exec` call

## Implementation Notes
- Use SeaORM's transaction API: `self.db.transaction::<_, (), DbErr>(|txn| { Box::pin(async move { ... }) }).await?`
- Replace `&self.db` with `txn` in each of the three `exec()` calls inside the transaction closure
- The existing pattern for transactions can be found in the ingestor module (`modules/ingestor/src/`) which uses the same SeaORM transaction API
- Preserve the existing `chrono::Utc::now()` timestamp usage -- all three updates should use the same timestamp value, which is already the case in the current implementation
- The function signature and return type do not need to change

## Acceptance Criteria
- [ ] The three UPDATE statements in `soft_delete` are wrapped in a single database transaction
- [ ] If any UPDATE fails, all changes are rolled back (no partial state)
- [ ] The `txn` handle is used for all three `exec` calls instead of `self.db`
- [ ] Existing tests continue to pass

## Test Requirements
- [ ] Existing integration tests in `tests/api/sbom_delete.rs` pass without modification

## Target PR
https://github.com/trustify/trustify-backend/pull/744

## Review Context
**Comment ID:** 30001
**Author:** reviewer-a
**File:** `modules/fundamental/src/sbom/service/sbom.rs` (line 60)
**Comment:**
> The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.
