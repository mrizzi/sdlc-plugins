# Review Comment Classification: Comment 30001

## Comment

**Author:** reviewer-a
**File:** modules/fundamental/src/sbom/service/sbom.rs (line 60)
**Text:** "The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call."

## Classification: CODE CHANGE REQUEST

## Reasoning

The reviewer's language is directive and imperative:

1. **"should run all three UPDATE statements inside a single database transaction"** -- this is a direct instruction to change the code, not a suggestion or optional improvement. The word "should" here is used prescriptively (equivalent to "must"), not permissively.

2. **"Wrap the three operations in `self.db.transaction(|txn| { ... })`"** -- the reviewer provides a specific implementation instruction with exact API usage. This goes beyond suggesting an alternative; it specifies what the fix must look like.

3. **Identifies a concrete correctness problem** -- the reviewer explains the failure scenario ("if the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state"). This frames the request as fixing a bug (data inconsistency), not as an optional enhancement.

4. **No hedging language** -- the reviewer does not use phrases like "consider", "might want to", "could also", "it would be nice if", or "optionally". The tone is instructional and expects the change to be made.

All four signals align with a code change request classification. The reviewer is asking for a specific code modification to fix a correctness issue (lack of transactional wrapping for multi-table mutations).

## Action

Sub-task created to address this feedback. The fix involves wrapping the three UPDATE operations in `self.db.transaction()` in the `soft_delete` method.
