## Repository
trustify-backend

## Description
Wrap the three sequential UPDATE operations in the `soft_delete` method inside a database transaction to ensure atomicity. Currently, the method executes three independent `update_many` calls (for `sbom`, `sbom_package`, and `sbom_advisory` tables) without transaction wrapping. If any intermediate update fails (e.g., the `sbom_advisory` update fails after `sbom_package` succeeds), the database is left in an inconsistent state where some related records are marked as deleted and others are not.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` -- wrap the three UPDATE statements in `soft_delete` inside a `self.db.transaction(|txn| { ... })` block and replace `self.db` with `txn` for each `exec` call

## Implementation Notes
- Use SeaORM's transaction API: `self.db.transaction::<_, (), DbErr>(|txn| { Box::pin(async move { ... }) }).await?`
- Replace all three `.exec(&self.db)` calls with `.exec(txn)` inside the transaction closure
- The existing pattern for transactions in SeaORM uses `DatabaseTransaction` as the connection parameter -- follow the same async closure pattern used elsewhere in the codebase
- The `chrono::Utc::now()` timestamp assignment remains unchanged; all three updates should use the same `now` value within the transaction

## Acceptance Criteria
- [ ] All three UPDATE operations (`sbom`, `sbom_package`, `sbom_advisory`) execute within a single database transaction
- [ ] If any UPDATE fails, the entire transaction rolls back and no partial updates persist
- [ ] The `soft_delete` method returns an error if the transaction fails
- [ ] Existing tests continue to pass with no behavioral changes for the success path

## Test Requirements
- [ ] Existing integration tests for SBOM deletion still pass (no behavioral regression)

## Target PR
https://github.com/trustify/trustify-backend/pull/744

## Review Context
**Comment ID:** 30001
**Author:** reviewer-a
**File:** `modules/fundamental/src/sbom/service/sbom.rs` (line 60)
**Comment:**
> The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.
