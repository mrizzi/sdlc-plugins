# Classification Reasoning for Comment 30001

## Comment
> The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.

**File:** `modules/fundamental/src/sbom/service/sbom.rs`, line 60
**Author:** reviewer-a

## Classification: code change request

## Reasoning

The reviewer's language is directive, not suggestive:

1. **"should run"** — a prescriptive statement about required behavior, not a proposal of an alternative approach.
2. **"Wrap the three operations in..."** — an imperative command specifying exactly what code change to make.
3. **Correctness justification** — the reviewer explains a concrete failure scenario ("If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state"), establishing that this is a correctness defect, not a stylistic preference.

The comment identifies a real correctness bug: three database updates that must be atomic are executed independently. The reviewer does not use hedging language like "you might consider," "it would be nice," or "have you thought about" — instead, they state a requirement and provide specific implementation instructions.

This meets the definition of a **code change request**: the reviewer asks for a code modification to fix a correctness issue.

## Action

Sub-task created to wrap the three UPDATE statements in `soft_delete` inside a database transaction.
