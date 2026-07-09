# Review Comment Classification: 30001

**Reviewer**: reviewer-a
**File**: `modules/fundamental/src/sbom/service/sbom.rs`, line 60
**Date**: 2026-04-20T14:32:00Z

## Comment Text

> The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.

## Classification: code change request

## Reasoning

The reviewer explicitly directs a specific code modification: wrap the three UPDATE statements inside a database transaction using `self.db.transaction(|txn| { ... })`. The language is imperative and directive throughout:

1. "should run" -- prescriptive, not optional
2. "Wrap the three operations" -- direct instruction
3. "use `txn` instead of `self.db` for each exec call" -- exact implementation detail

The reviewer identifies a concrete correctness defect: without transactional wrapping, if the `sbom_advisory` update fails after `sbom_package` succeeds, the database is left in an inconsistent partially-deleted state. This is not a style preference or suggestion -- it is a correctness bug with a prescribed fix.

Key classification indicators:
- Imperative language throughout (no "could", "might", "consider")
- Identifies a specific correctness issue (data inconsistency on partial failure)
- Provides the exact code pattern to use (`self.db.transaction(|txn| { ... })`)
- The change is necessary for data integrity, not optional

## Action

Sub-task created (subtask-30001.md) to address this feedback.
