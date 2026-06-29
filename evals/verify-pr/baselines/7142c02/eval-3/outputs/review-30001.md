# Review Comment Classification: 30001

**Reviewer**: reviewer-a
**File**: `modules/fundamental/src/sbom/service/sbom.rs`, line 60
**Date**: 2026-04-20T14:32:00Z

## Comment Text

> The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.

## Classification: Code Change Request

**Reasoning**: The reviewer explicitly directs a specific code modification: wrapping the three UPDATE statements inside a database transaction. The language is directive throughout -- "should run", "Wrap the three operations" -- and the reviewer provides the exact code pattern to follow (`self.db.transaction(|txn| { ... })`). This is not a suggestion or question; it is a concrete, imperative request to change the implementation.

The concern is technically valid and represents a correctness issue. The `soft_delete` method currently executes three independent `update_many` calls against the `sbom`, `sbom_package`, and `sbom_advisory` tables in sequence without any transactional wrapping. If the second or third UPDATE fails after earlier ones succeed, the database is left in an inconsistent partially-deleted state. This is a data integrity bug, not merely a style preference.

The directive phrasing, the specificity of the requested change (exact API call with parameter names), and the correctness impact all clearly classify this as a code change request.

**Action**: Create sub-task (subtask-30001.md)
