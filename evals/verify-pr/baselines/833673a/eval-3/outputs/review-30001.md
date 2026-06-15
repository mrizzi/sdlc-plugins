## Review Comment Classification: 30001

**Comment ID:** 30001
**Author:** reviewer-a
**File:** modules/fundamental/src/sbom/service/sbom.rs, line 60
**Classification:** code change request

### Comment Text

> The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.

### Classification Reasoning

The reviewer explicitly asks for a code modification: wrapping three UPDATE statements in a database transaction to prevent inconsistent state. This is a direct request for a specific code change (use `self.db.transaction(|txn| { ... })`), not a suggestion of an alternative approach. The reviewer identifies a concrete correctness issue -- partial failure of the cascade updates would leave the database in an inconsistent state where some related entities are marked as deleted and others are not. This is a clear code change request that requires a fix.

### Action

Sub-task created to address this feedback. The soft_delete method must be wrapped in a transaction to ensure atomicity of the SBOM deletion and cascade updates to sbom_package and sbom_advisory tables.
