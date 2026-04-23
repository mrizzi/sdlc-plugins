# Review Comment 30001 — Classification

**Comment by:** reviewer-a
**File:** `modules/fundamental/src/sbom/service/sbom.rs` (line 60)
**Text:** The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.

## Classification: Code Change Request

### Reasoning

The reviewer directly requests a code modification: wrapping three sequential UPDATE statements in a database transaction. This is not a suggestion or style preference -- it identifies a concrete correctness bug where partial failure of the cascade updates would leave the database in an inconsistent state (e.g., sbom_package rows marked deleted but sbom_advisory rows not, or vice versa).

The language is imperative ("should run", "Wrap the three operations") and identifies a specific failure scenario with a specific fix. This meets the definition of a code change request.

### Universality Test (for root-cause investigation)

The knowledge required to prevent this defect -- "multiple related database writes that must succeed or fail together should be wrapped in a transaction" -- is universal. It applies to any repository using any database framework. This is a language-agnostic analysis method ("check whether related writes are wrapped in a transaction"), not a fact requiring specific API knowledge. Therefore this is classified as a **skill gap**.

### Action

Sub-task created to wrap the three UPDATE statements in `soft_delete` in a database transaction.
