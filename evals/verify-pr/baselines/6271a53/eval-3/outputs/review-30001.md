# Review Comment Classification: 30001

## Comment
> The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.

**File:** `modules/fundamental/src/sbom/service/sbom.rs`
**Line:** 60
**Author:** reviewer-a

## Classification: Code Change Request

## Reasoning

The reviewer explicitly requests a code modification: wrapping three UPDATE statements in a database transaction. The language is imperative ("should run", "Wrap the three operations") and describes a specific code change with concrete implementation guidance (`self.db.transaction(|txn| { ... })`).

This is not a suggestion or optional improvement -- it identifies a correctness bug where partial failure of the cascade updates would leave the database in an inconsistent state. The reviewer prescribes a specific fix (use a transaction) with clear rationale (atomicity of related updates).

**Classification criteria met:**
- Reviewer asks for a code modification: YES
- Specific file and change described: YES
- Imperative language used: YES ("should", "Wrap")
- Correctness concern (not just style): YES (data consistency)

## Action
Sub-task creation triggered. See `subtask-30001.md`.
