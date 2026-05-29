## Repository
trustify-backend

## Description
Wrap the three UPDATE statements in the `soft_delete` method inside a single database transaction to ensure atomicity. Currently, the SBOM record, `sbom_package` rows, and `sbom_advisory` rows are updated sequentially without a transaction boundary. If any update fails after a previous one succeeds, the database is left in an inconsistent state where some entities are marked as deleted while others are not.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` -- wrap the three `update_many` calls in the `soft_delete` method inside `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each `.exec()` call

## Implementation Notes
- Use SeaORM's transaction API: `self.db.transaction::<_, (), DbErr>(|txn| { Box::pin(async move { ... }) }).await?`
- Replace `&self.db` with `txn` in each of the three `Entity::update_many().exec()` calls inside the transaction closure
- The three updates are: (1) `sbom::Entity::update_many()` setting `deleted_at` on the SBOM, (2) `sbom_package::Entity::update_many()` setting `deleted_at` on related packages, (3) `sbom_advisory::Entity::update_many()` setting `deleted_at` on related advisories
- Follow the existing transaction patterns used elsewhere in the codebase (e.g., check `modules/ingestor/src/graph/sbom/mod.rs` for transaction usage examples)
- The `chrono::Utc::now()` timestamp should be computed once before the transaction and reused for all three updates to ensure consistency

## Acceptance Criteria
- [ ] The `soft_delete` method wraps all three UPDATE operations in a single database transaction
- [ ] If any UPDATE fails, the entire transaction is rolled back (no partial updates)
- [ ] All three tables (`sbom`, `sbom_package`, `sbom_advisory`) use the same `txn` connection within the transaction
- [ ] Existing tests continue to pass (test_delete_sbom_returns_204, test_delete_sbom_cascades_to_join_tables)

## Target PR
https://github.com/trustify/trustify-backend/pull/744

## Review Context
**Comment ID:** 30001
**File:** `modules/fundamental/src/sbom/service/sbom.rs`, line 60
**Reviewer:** reviewer-a
**Comment:** "The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call."
