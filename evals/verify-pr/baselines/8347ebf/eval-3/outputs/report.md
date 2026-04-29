## Verification Report for TC-9103

| Check | Result | Details |
|-------|--------|---------|
| Review Feedback | WARN | 2 code change requests identified; sub-tasks created for transaction wrapping (30001) and migration index (30002) |
| Root-Cause Investigation | DONE | Transaction atomicity: implement-task gap (universal method -- multi-table writes should use transactions). Missing index: convention gap (no documented index convention for soft-delete columns). |
| Scope Containment | FAIL | `modules/fundamental/src/sbom/endpoints/get.rs` listed in task Files to Modify but not changed in PR |
| Diff Size | PASS | 6 files changed; proportionate to task scope (new endpoint, migration, service logic, tests) |
| Commit Traceability | WARN | Commit messages not available for verification in provided data |
| Sensitive Patterns | PASS | No secrets, credentials, or sensitive patterns detected in added lines |
| CI Status | PASS | All CI checks pass |
| Acceptance Criteria | FAIL | 7 of 8 criteria met; missing: `GET /api/v2/sbom/{id}` does not support `include_deleted` parameter (get.rs unchanged) |
| Test Quality | PASS | All 5 test functions have doc comments; no repetitive test patterns detected |
| Test Change Classification | ADDITIVE | New test file `tests/api/sbom_delete.rs` with 5 test functions; no modified or deleted test files |
| Verification Commands | N/A | No verification commands specified in task |

### Overall: FAIL

Two issues require attention before this PR can be merged:

1. **Missing get.rs changes (Scope Containment FAIL):** The task specifies adding `include_deleted` parameter support to `modules/fundamental/src/sbom/endpoints/get.rs`, but this file has no changes in the PR. Reviewer comment 30004 also flags this gap -- direct GET requests for a soft-deleted SBOM currently return the deleted SBOM without requiring `include_deleted=true`, which contradicts the task's acceptance criteria.

2. **Acceptance Criteria gap:** The acceptance criterion "GET /api/v2/sbom?include_deleted=true includes soft-deleted SBOMs" is met for the list endpoint, but the corresponding single-resource GET endpoint (`/api/v2/sbom/{id}`) does not filter by `deleted_at` and does not accept the `include_deleted` parameter.

Additionally, 2 sub-tasks were created from review feedback:
- **Sub-task for comment 30001:** Wrap `soft_delete` method's three UPDATE statements in a database transaction for atomicity
- **Sub-task for comment 30002:** Add partial index on `sbom.deleted_at` column in the migration

### Review Comment Summary

| Comment ID | File | Classification | Action |
|------------|------|----------------|--------|
| 30001 | `modules/fundamental/src/sbom/service/sbom.rs` | Code change request | Sub-task created |
| 30002 | `migration/src/m0042_sbom_soft_delete/mod.rs` | Code change request | Sub-task created |
| 30003 | `modules/fundamental/src/sbom/endpoints/mod.rs` | Nit | No sub-task |
| 30004 | `modules/fundamental/src/sbom/endpoints/get.rs` | Question | No sub-task |

### Root-Cause Analysis

**Comment 30001 (transaction wrapping):** The knowledge required to prevent this defect is universal -- any multi-table write operation should be wrapped in a transaction to ensure atomicity. This is a method-level principle ("verify that multi-table mutations use transactions") that applies to any language or framework. Classification: **skill gap (implement-task phase)**. The implement-task skill should check that service methods performing multiple write operations across tables use transaction boundaries.

**Comment 30002 (missing index):** The knowledge required to add a partial index for soft-delete filtering is repo-specific -- it depends on the project's database performance conventions and indexing strategy. No CONVENTIONS.md exists in the repository documenting index creation patterns for migration files. Classification: **convention gap**. A CONVENTIONS.md entry should document the expectation that new nullable filter columns (especially soft-delete columns used in WHERE clauses) include appropriate indexes in their migrations.
