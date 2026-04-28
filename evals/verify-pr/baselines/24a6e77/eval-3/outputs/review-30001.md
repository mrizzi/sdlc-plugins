# Review Comment Classification: 30001

## Comment

**Author:** reviewer-a
**File:** `modules/fundamental/src/sbom/service/sbom.rs` (line 60)
**Date:** 2026-04-20T14:32:00Z

> The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.

## Classification: code change request

## Reasoning

The reviewer explicitly requests a concrete code modification: wrapping the three sequential UPDATE operations in `soft_delete` inside a database transaction. The language is directive ("should run", "Wrap the three operations"), identifies a specific correctness issue (inconsistent state on partial failure), and prescribes the exact fix (use `self.db.transaction(|txn| { ... })`). This is not a suggestion of an alternative approach -- it identifies a genuine data integrity bug where a partial failure leaves the database in an inconsistent state. The reviewer requires this change before merging, consistent with the overall review state of CHANGES_REQUESTED.

## Action

Sub-task created: This code change request triggers creation of a Jira sub-task to wrap the three UPDATE statements in a database transaction (see subtask-30001.md).
