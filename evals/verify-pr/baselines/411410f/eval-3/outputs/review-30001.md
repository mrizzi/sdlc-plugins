# Review Comment Classification: 30001

**Comment ID:** 30001
**Reviewer:** reviewer-a
**File:** `modules/fundamental/src/sbom/service/sbom.rs` (line 60)
**Classification:** code change request

## Comment Text

> The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.

## Classification Reasoning

The reviewer explicitly requests a code modification: wrapping the three UPDATE statements in a database transaction. This is a concrete, actionable change to the implementation that addresses a correctness concern (data consistency). The language is directive ("should run", "Wrap the three operations"), not suggestive or questioning. The reviewer identifies a specific failure scenario (partial update leaving inconsistent state) and prescribes a specific fix (use `self.db.transaction()`).

This is a **code change request** because:
1. The reviewer asks for a specific code change (transaction wrapping)
2. The concern is correctness-related (data consistency on partial failure)
3. The language is imperative, not optional

**Action:** Sub-task created to address this feedback.
