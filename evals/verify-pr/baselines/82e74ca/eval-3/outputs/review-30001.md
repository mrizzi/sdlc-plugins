# Review Comment Classification: #30001

**Comment by:** reviewer-a
**File:** `modules/fundamental/src/sbom/service/sbom.rs` (line 60)
**Date:** 2026-04-20T14:32:00Z

## Original Comment

> The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.

## Classification: Code Change Request

## Reasoning

The reviewer explicitly requests a specific code modification: wrapping three UPDATE statements in a database transaction to prevent inconsistent state. This is a direct, imperative request for a code change ("should run", "Wrap the three operations"), not a suggestion or question. The feedback identifies a concrete correctness bug — if any of the three sequential UPDATE operations fails after a prior one succeeds, the database will be left in an inconsistent state with partially soft-deleted data.

This is a universally applicable concern (transaction safety for multi-table updates) and constitutes a clear code change request. A sub-task will be created.

## Convention Check

Not applicable — this is already classified as a code change request, not a suggestion.

## Action

Sub-task created to wrap the three UPDATE operations in `soft_delete` inside a database transaction.
