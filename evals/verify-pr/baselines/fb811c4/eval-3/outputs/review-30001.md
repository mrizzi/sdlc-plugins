# Review Comment Classification: 30001

## Comment

**Author:** reviewer-a
**File:** modules/fundamental/src/sbom/service/sbom.rs:60
**Text:** "The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call."

## Classification: code change request

## Reasoning

The reviewer uses directive language: "should run", "Wrap the three operations". This is not suggestive or optional -- the reviewer is requesting a specific code modification with a concrete implementation approach (wrapping in `self.db.transaction()`). The comment identifies a real correctness issue (inconsistent state on partial failure) and prescribes the exact fix. This clearly constitutes a code change request that requires a tracked sub-task.

## Action

Sub-task created to address this feedback.
