# Review Comment Classification: 30001

**Comment ID:** 30001
**Reviewer:** reviewer-a
**File:** modules/fundamental/src/sbom/service/sbom.rs (line 60)
**Classification:** code change request

## Reasoning

The reviewer explicitly requests a code modification: wrapping the three UPDATE statements in `soft_delete` inside a single database transaction using `self.db.transaction(|txn| { ... })`. The language is directive ("should run", "wrap the three operations") and identifies a concrete correctness issue -- if the `sbom_advisory` update fails after `sbom_package` succeeds, the database will be in an inconsistent state with partially-applied soft deletes.

This is not a suggestion or style preference; it addresses a data integrity concern where a partial failure would leave orphaned records in an inconsistent state. The fix is clearly specified: use a transaction to ensure atomicity.

**Action:** Sub-task created to address this feedback.
