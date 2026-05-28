# Review Comment Classification: 30001

## Comment

> The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.

**Author:** reviewer-a
**File:** modules/fundamental/src/sbom/service/sbom.rs
**Line:** 60

## Classification: code change request

## Reasoning

The reviewer explicitly instructs a specific code change: wrap the three UPDATE statements in a database transaction using `self.db.transaction(|txn| { ... })`. The language is directive ("should run", "Wrap the three operations"), not suggestive or optional. The reviewer identifies a concrete correctness issue (inconsistent state if a middle operation fails) and prescribes the exact fix pattern. This is a clear code change request, not a suggestion or question.

## Action

Create sub-task to address this feedback.
