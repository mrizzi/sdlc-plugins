# Review Comment 30001 — Classification

**Comment by:** reviewer-a
**File:** `modules/fundamental/src/sbom/service/sbom.rs` (line 60)
**Content:** The `soft_delete` method should run all three UPDATE statements inside a single database transaction to prevent inconsistent state.

## Classification: code change request

## Reasoning

The reviewer explicitly requests a code modification: wrapping the three UPDATE statements (sbom, sbom_package, sbom_advisory) in a single database transaction using `self.db.transaction(|txn| { ... })`. This is a direct, actionable request for a code change, not a suggestion or question.

The concern is a correctness issue: if the sbom_advisory update fails after sbom_package succeeds, the database would be left in an inconsistent state with some join table rows marked deleted and others not. This is a data integrity bug that requires a fix.

**Initial classification:** code change request
**Convention check:** N/A (already classified as code change request)
**Final classification:** code change request

**Action:** Sub-task created to wrap the soft_delete operations in a database transaction.
