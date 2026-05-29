# Review Comment 30001 Classification

**Comment by:** reviewer-a
**File:** `modules/fundamental/src/sbom/service/sbom.rs`, line 60
**Text:** The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.

## Classification: Code Change Request

**Reasoning:**

The reviewer is making a direct, imperative request for a code modification: "should run all three UPDATE statements inside a single database transaction." This is not a suggestion of an alternative approach -- it identifies a concrete correctness bug (inconsistent state on partial failure) and prescribes a specific fix (wrap in `self.db.transaction()`). The language is directive ("should", "Wrap the three operations"), not exploratory or optional. The reviewer provides a specific technical remedy with API references.

This is a clear code change request because:
1. It identifies a real data consistency bug (partial cascade failure leaves orphaned state)
2. The fix is mandatory for correctness, not optional
3. The reviewer uses imperative language prescribing the exact solution
