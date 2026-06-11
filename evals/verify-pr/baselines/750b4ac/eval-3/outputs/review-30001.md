## Review Comment 30001 -- Classification: code change request

**Comment:** "The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call."

**File:** modules/fundamental/src/sbom/service/sbom.rs, line 60

**Classification reasoning:**

The reviewer directly requests a code modification using imperative language: "should run", "Wrap the three operations". This is not a suggestion of an alternative approach -- it identifies a concrete correctness defect (partial failure leading to inconsistent state) and prescribes the exact fix (wrap in a database transaction, use `txn` instead of `self.db`).

The language is directive, not suggestive:
- "should run all three UPDATE statements inside a single database transaction" -- a requirement, not an option
- "Wrap the three operations in `self.db.transaction(|txn| { ... })`" -- a specific instruction for what code to write
- "use `txn` instead of `self.db` for each exec call" -- precise implementation guidance

This meets the definition of **code change request**: the reviewer asks for a code modification with a clear rationale (data consistency) and a specific implementation path.

**Action:** Sub-task created to wrap the three UPDATE operations in `soft_delete` inside a database transaction.
