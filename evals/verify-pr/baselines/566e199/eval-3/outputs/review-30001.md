# Review Comment Classification: 30001

## Comment

**Author:** reviewer-a
**File:** `modules/fundamental/src/sbom/service/sbom.rs`, line 60
**Text:** "The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call."

## Classification: code change request

## Reasoning

The reviewer uses imperative language: "should run", "Wrap the three operations". This is a direct instruction to change the code, not a tentative suggestion or optional improvement. The reviewer identifies a concrete correctness defect (inconsistent state if a partial failure occurs during the three sequential UPDATE statements) and prescribes a specific fix (wrapping in a database transaction). The language is directive, not suggestive -- there is no hedging like "you might consider" or "it would be nice to". This is a clear request for a code modification to fix a data consistency bug.

## Sub-task required: Yes

A sub-task will be created to wrap the three UPDATE operations in `soft_delete` inside a single database transaction.
