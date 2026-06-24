# Review Comment Classification: 30001

## Comment

**Author:** reviewer-a
**File:** `modules/fundamental/src/sbom/service/sbom.rs`, line 60
**Body:** "The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call."

## Classification: Code Change Request

## Reasoning

The reviewer uses imperative, directive language throughout the comment: "should run", "Wrap the three operations", "use `txn` instead of `self.db`". This is not a tentative suggestion or a question -- it is an explicit instruction to change the code. The reviewer identifies a concrete correctness defect (partial failure leading to inconsistent state between `sbom_package` and `sbom_advisory` tables) and prescribes a specific fix (wrapping in a database transaction). The language is unambiguous and demands a code modification.

This is a textbook code change request: it identifies a bug (lack of atomicity), explains the consequence (inconsistent state), and specifies the exact remediation (transaction wrapping with `txn` handle).

## Action

Sub-task created: subtask-30001.md
