**Summary:** Add remediation domain model and aggregation service
**Issue Type:** Task
**Parent Epic:** TC-9006: trustify-backend

## Repository
trustify-backend

## Target Branch
main

## Description
Add a new `remediation` domain module under `modules/fundamental/src/` following the established module pattern (model/ + service/ + endpoints/). This task covers the model definitions and aggregation service layer that computes remediation statistics from existing vulnerability and SBOM relationship data. The service provides aggregation logic for:
- Summary counts by severity (Critical/High/Medium/Low) crossed with status (Open/In Progress/Resolved)
- Per-product remediation breakdown with total, open, and resolved counts

Per the non-functional requirements, all aggregations are computed from existing entity tables — no new database tables are created.

## Files to Create
- `modules/fundamental/src/remediation/mod.rs` — Remediation module root, re-exports model and service
- `modules/fundamental/src/remediation/model/mod.rs` — Model module root
- `modules/fundamental/src/remediation/model/summary.rs` — RemediationSummary struct with severity-status count matrix
- `modules/fundamental/src/remediation/model/by_product.rs` — ProductRemediation struct with per-product counts
- `modules/fundamental/src/remediation/service/mod.rs` — RemediationService with aggregation queries

## Implementation Notes
Follow the established module pattern in `modules/fundamental/src/`. Each domain module has `model/`, `service/`, and `endpoints/` subdirectories.

Per CONVENTIONS.md §Module pattern: follow the model/ + service/ + endpoints/ structure used by existing modules like `sbom/` and `advisory/`.
Applies: task creates `modules/fundamental/src/remediation/model/mod.rs` matching the convention's `.rs` module scope.

Per CONVENTIONS.md §Error handling: all service methods return `Result<T, AppError>` with `.context()` wrapping for error context.
Applies: task creates `modules/fundamental/src/remediation/service/mod.rs` matching the convention's `.rs` scope.

Per CONVENTIONS.md §Response types: aggregation results should be structured consistently with existing response types using `PaginatedResults<T>` from `common/src/model/paginated.rs` where pagination applies.
Applies: task creates `modules/fundamental/src/remediation/model/summary.rs` matching the convention's `.rs` scope.

The aggregation service should use SeaORM queries to join existing entity tables (`entity/src/advisory.rs`, `entity/src/sbom_advisory.rs`, `entity/src/sbom.rs`) and compute counts using SQL GROUP BY. Leverage the query builder helpers in `common/src/db/query.rs` for filtering and pagination support.

The `RemediationSummary` struct should contain a matrix of counts organized by severity and status:
```rust
pub struct SeverityStatusCounts {
    pub severity: String,
    pub open: i64,
    pub in_progress: i64,
    pub resolved: i64,
}

pub struct StatusCounts {
    pub open: i64,
    pub in_progress: i64,
    pub resolved: i64,
}

pub struct RemediationSummary {
    pub by_severity: Vec<SeverityStatusCounts>,
    pub totals: StatusCounts,
}
```

The `ProductRemediation` struct should include:
```rust
pub struct ProductRemediation {
    pub product_name: String,
    pub total: i64,
    pub open: i64,
    pub in_progress: i64,
    pub resolved: i64,
}
```

## Reuse Candidates
- `common/src/db/query.rs` — shared query builder helpers for filtering, pagination, and sorting; reuse for building aggregation queries
- `common/src/model/paginated.rs::PaginatedResults` — paginated response wrapper; use for the by-product endpoint response type
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — includes severity field; follow this model struct pattern for RemediationSummary
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — follow the service pattern (fetch, list methods returning Result<T, AppError>)

## Acceptance Criteria
- [ ] `RemediationSummary` struct models severity x status aggregation with per-severity and total counts
- [ ] `ProductRemediation` struct models per-product remediation counts (total, open, in_progress, resolved)
- [ ] `RemediationService` computes aggregations from existing entity tables without creating new database tables
- [ ] Service methods return `Result<T, AppError>` following established error handling patterns
- [ ] Module structure follows the model/ + service/ pattern consistent with sibling modules

## Test Requirements
- [ ] Unit test: `RemediationService::get_summary` returns correct severity x status counts when test data contains vulnerabilities across multiple severities and statuses
- [ ] Unit test: `RemediationService::get_by_product` returns correct per-product breakdown with accurate totals
- [ ] Unit test: aggregation handles empty datasets gracefully (returns zero counts, not errors)

## Dependencies
- None (first task)
