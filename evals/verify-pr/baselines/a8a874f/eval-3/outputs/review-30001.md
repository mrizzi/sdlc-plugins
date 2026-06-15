# Review Comment Classification: 30001

## Comment

**Author:** reviewer-a
**File:** modules/fundamental/src/sbom/service/sbom.rs (line 60)
**Text:** "The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call."

## Classification: Code Change Request

## Reasoning

The reviewer uses imperative language throughout: "should run", "Wrap the three operations", "use `txn` instead of `self.db`". This is a direct instruction to modify the code, not a suggestion or question. The reviewer identifies a concrete correctness defect -- partial failure across the three sequential UPDATE statements would leave the database in an inconsistent state where some join table rows are marked deleted but others are not. The reviewer prescribes a specific fix: wrapping the operations in `self.db.transaction(|txn| { ... })`.

This is unambiguously a code change request because:
1. The language is directive ("should run", "Wrap", "use")
2. It identifies a real bug (inconsistent state on partial failure)
3. It prescribes a specific code change with implementation details

## Action

Sub-task created to wrap the three UPDATE statements in a database transaction.
