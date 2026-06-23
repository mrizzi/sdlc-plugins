## Review Comment 30001 — Classification

**Comment ID:** 30001
**Author:** reviewer-a
**File:** modules/fundamental/src/sbom/service/sbom.rs
**Line:** 60
**Content:** The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.

### Classification: code change request

### Reasoning

The reviewer explicitly requests a specific code modification: wrapping the three UPDATE statements in a database transaction. The language is directive ("should run", "Wrap the three operations"), identifies a concrete bug (partial failure leaving inconsistent state), and prescribes an exact fix (use `self.db.transaction(|txn| { ... })`). This is not a suggestion of an alternative approach — it identifies a correctness defect where concurrent or partial failures could corrupt data integrity. The reviewer is asking for a required code change, not proposing an optional improvement.

### Action

Sub-task created to address this feedback.
