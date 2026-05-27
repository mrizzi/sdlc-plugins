## Review Comment 30001 — Classification

### Comment
**Reviewer**: reviewer-a
**File**: `modules/fundamental/src/sbom/service/sbom.rs`, line 60
**Text**: "The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call."

### Classification: Code Change Request

### Reasoning
The reviewer uses imperative language ("should run", "Wrap the three operations") and provides a specific, prescriptive code change to make. The reviewer identifies a correctness bug: partial failure of the cascade updates would leave the database in an inconsistent state. This is not a suggestion or preference -- it is a direct request to fix a data integrity issue by wrapping the three UPDATE statements in a transaction. The language is directive, not optional, and the reviewer's overall review state is `CHANGES_REQUESTED`, reinforcing that this must be addressed before merge.

### Action
Create sub-task (subtask-30001.md) for wrapping the soft_delete operations in a database transaction.
