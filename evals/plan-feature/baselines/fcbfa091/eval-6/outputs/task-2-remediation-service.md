## Repository
trustify-backend

## Target Branch
main

## Parent Epic
TC-9006: trustify-backend

## Description
Implement the remediation aggregation service that computes summary and per-product remediation statistics from existing SBOM, advisory, and vulnerability data. This service queries existing tables (no new migrations) and returns the model types defined in Task 1. The summary endpoint must meet the p95 < 500ms performance requirement for up to 10,000 tracked vulnerabilities.

## Files to Create
- `modules/remediation/src/service/mod.rs` — `RemediationService` with methods `get_summary()` and `get_by_product()`

## Files to Modify
- `modules/remediation/src/lib.rs` — Re-export the `service` submodule

## API Changes
- `RemediationService::get_summary(&self, db: &DbConn) -> Result<RemediationSummary, AppError>` — NEW: aggregates vulnerability counts by severity and remediation status
- `RemediationService::get_by_product(&self, db: &DbConn, params: &Query) -> Result<PaginatedResults<ProductRemediation>, AppError>` — NEW: aggregates remediation status per product with pagination support

## Implementation Notes
Follow the service pattern from `modules/fundamental/src/advisory/service/advisory.rs` — the service struct holds no state and methods accept a database connection reference. Use `.context()` wrapping on all fallible operations as per the error handling convention.

Per CONVENTIONS.md: all service methods return `Result<T, AppError>` with `.context()` wrapping.
Applies: task creates `modules/remediation/src/service/mod.rs` matching the convention's `.rs` module scope.

For `get_summary()`:
- Join `sbom_advisory` with `advisory` to get severity and status fields
- Group by (severity, status) and count
- Pivot the result into the `RemediationSummary` struct with `SeverityBreakdown` entries

For `get_by_product()`:
- Join `sbom` -> `sbom_advisory` -> `advisory` to correlate products with vulnerability status
- Group by SBOM/product identifier, aggregate open/in-progress/resolved counts
- Apply pagination using `common/src/db/query.rs` helpers

Use the query builder helpers from `common/src/db/query.rs` for filtering, pagination, and sorting to stay consistent with existing service implementations.

## Reuse Candidates
- `common/src/db/query.rs` — Shared query builder helpers for filtering, pagination, sorting; use for the by-product query
- `common/src/error.rs::AppError` — Error type with `IntoResponse` implementation; use as the error return type
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — Reference for service method patterns and database query structure
- `entity/src/sbom_advisory.rs` — SBOM-Advisory join entity for building the aggregation query
- `entity/src/advisory.rs` — Advisory entity with severity field

## Acceptance Criteria
- [ ] `RemediationService::get_summary()` returns correctly aggregated counts from existing vulnerability data
- [ ] `RemediationService::get_by_product()` returns paginated per-product remediation breakdown
- [ ] Severity grouping covers Critical, High, Medium, and Low levels
- [ ] Status grouping covers Open, In Progress, and Resolved states
- [ ] All database errors are wrapped with `.context()` for meaningful error messages
- [ ] Query performance supports p95 < 500ms for up to 10,000 vulnerabilities

## Test Requirements
- [ ] Unit test: `get_summary()` returns correct aggregation for a known dataset
- [ ] Unit test: `get_by_product()` returns correct per-product counts
- [ ] Unit test: `get_by_product()` respects pagination parameters
- [ ] Unit test: empty dataset returns zero counts, not errors

## Dependencies
- Depends on: Task 1 — Remediation module models

## additional_fields
- labels: ["ai-generated-jira"]
- priority: Major
- fixVersions: ["RHTPA 1.5.0"]
