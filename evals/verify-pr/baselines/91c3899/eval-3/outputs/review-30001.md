# Review Comment Classification: 30001

## Comment

**Author:** reviewer-a
**File:** `modules/fundamental/src/sbom/service/sbom.rs`, line 60
**Text:**
> The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.

## Classification: CODE CHANGE REQUEST

## Reasoning

The reviewer uses directive language throughout:

1. **"should run all three UPDATE statements inside a single database transaction"** -- this is a direct instruction to change the code, not a suggestion of an optional approach.
2. **"Wrap the three operations in `self.db.transaction(|txn| { ... })`"** -- this specifies the exact code change required, including the API call and variable name.
3. **"use `txn` instead of `self.db` for each exec call"** -- this prescribes a concrete modification to existing code.

The comment identifies a real correctness issue: without a transaction boundary, partial failures across the three UPDATE statements (sbom, sbom_package, sbom_advisory) would leave the database in an inconsistent state. This is not stylistic or optional -- it is a functional defect that must be fixed.

The directive tone ("should", "wrap", "use ... instead of") combined with specific code references and a concrete bug justification clearly marks this as a code change request.

## Action

Sub-task creation is triggered for this comment.
