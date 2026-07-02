## Repository
trustify-backend

## Target Branch
main

## Description
Add a new `remediation` module with aggregation models and service layer for computing remediation status from existing advisory and SBOM relationship data. The service provides two aggregation methods: one that groups vulnerability counts by severity (Critical/High/Medium/Low) and status (Open/In Progress/Resolved), and another that computes per-product remediation breakdowns with total, open, and resolved counts per product.

## Files to Create
- `modules/remediation/Cargo.toml` — crate manifest for the remediation module with dependencies on entity, common, and SeaORM
- `modules/remediation/src/lib.rs` — module root exporting model and service sub-modules
- `modules/remediation/src/model/mod.rs` — model sub-module root
- `modules/remediation/src/model/summary.rs` — RemediationSummary struct (severity, status, count fields) and ProductRemediation struct (product name, total, open, in_progress, resolved counts)
- `modules/remediation/src/service/mod.rs` — RemediationService with methods: `get_summary()` returning severity-by-status aggregation, and `get_by_product()` returning per-product breakdown

## Files to Modify
- `Cargo.toml` — add `modules/remediation` to workspace members list

## Implementation Notes
- Per CONVENTIONS.md §Module pattern: follow the `model/ + service/ + endpoints/` directory structure used by existing domain modules. See `modules/fundamental/src/sbom/` for the established pattern.
  Applies: task creates `modules/remediation/src/model/summary.rs` matching the convention's module structure scope.
- Per CONVENTIONS.md §Error handling: all service methods must return `Result<T, AppError>` with `.context()` wrapping on database errors. See `modules/fundamental/src/advisory/service/advisory.rs` for the established pattern.
  Applies: task creates `modules/remediation/src/service/mod.rs` matching the convention's Rust service file scope.
- Query existing `advisory`, `sbom_advisory`, and related entity tables to compute aggregations — the feature requirement specifies no new database tables.
- Use SeaORM query builder for aggregation queries. Reference `common/src/db/query.rs` for shared query builder helpers (filtering, pagination, sorting).
- The `AdvisorySummary` struct in `modules/fundamental/src/advisory/model/summary.rs` includes a severity field — use this as the severity data source for aggregation.
- Summary endpoint response time target: p95 < 500ms. Consider query optimization and appropriate indexing for aggregation queries.

## Reuse Candidates
- `common/src/db/query.rs::query` — shared query builder helpers for filtering, pagination, and sorting; reuse for building aggregation queries
- `common/src/model/paginated.rs::PaginatedResults<T>` — response wrapper for paginated results; reuse for the by-product endpoint if pagination is needed
- `common/src/error.rs::AppError` — error type implementing IntoResponse; reuse for all service error handling
- `entity/src/advisory.rs` — Advisory entity definition; use as the primary data source for severity-based aggregation
- `entity/src/sbom_advisory.rs` — SBOM-Advisory join table; use to correlate vulnerabilities with SBOMs for product-level aggregation
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — reference implementation for service patterns including query construction and error handling

## Acceptance Criteria
- [ ] `modules/remediation/` module exists with model and service sub-modules
- [ ] `RemediationSummary` struct captures severity, status, and count fields
- [ ] `ProductRemediation` struct captures product name with total, open, in_progress, and resolved counts
- [ ] `RemediationService::get_summary()` returns aggregated counts grouped by severity (Critical/High/Medium/Low) and status (Open/In Progress/Resolved)
- [ ] `RemediationService::get_by_product()` returns per-product remediation breakdown
- [ ] Service methods return `Result<T, AppError>` with proper error context
- [ ] No new database tables are created — aggregations use existing entity tables

## Test Requirements
- [ ] Unit test for `RemediationService::get_summary()` verifying correct grouping by severity and status
- [ ] Unit test for `RemediationService::get_by_product()` verifying correct per-product aggregation
- [ ] Test that empty dataset returns zero counts without errors

## Dependencies
- None
