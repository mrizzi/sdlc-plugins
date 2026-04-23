# Review Comment Classification: 30001

**Comment ID:** 30001
**Reviewer:** reviewer-a
**File:** `modules/fundamental/src/sbom/service/sbom.rs` (line 60)
**Comment:** The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.

## Classification: Code Change Request

## Reasoning

The reviewer uses directive language ("should run ... inside a single database transaction") and identifies a concrete correctness defect: the three UPDATE statements in `soft_delete` are executed independently against `self.db`, meaning a failure partway through (e.g., the `sbom_advisory` update fails after `sbom_package` succeeds) would leave the database in an inconsistent state. The reviewer provides a specific fix: wrap the operations in `self.db.transaction(|txn| { ... })` and use `txn` for each `exec` call.

This is not a style preference or optional suggestion -- it identifies a data integrity bug where partial failures lead to inconsistent state. The language is imperative and the fix is concrete, making this a clear code change request.

## Action

Sub-task created. See `subtask-30001.md` for the full sub-task description.
