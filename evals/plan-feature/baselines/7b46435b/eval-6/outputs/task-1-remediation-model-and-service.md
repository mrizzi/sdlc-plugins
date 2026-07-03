## Repository
trustify-backend

## Target Branch
main

## Description
Create the remediation summary models and aggregation service methods. This task introduces a `RemediationSummary` response struct that groups vulnerability counts by severity (Critical, High, Medium, Low) and remediation status (Open, In Progress, Resolved), and a `ProductRemediation` struct for per-product breakdowns with total, open, in_progress, and resolved counts. Service-layer methods compute these aggregations from existing vulnerability-SBOM relationship data. No new database tables are required -- all aggregations are computed from existing entity relationships (`sbom_advisory`, `advisory`, `sbom`, `package` entities).

Parent Epic: TC-9006: trustify-backend

additional_fields: { "labels": ["ai-generated-jira"], "priority": {"name": "Major"}, "fixVersions": [{"name": "RHTPA 1.5.0"}] }

## Files to Create
- `modules/fundamental/src/remediation/mod.rs` -- remediation domain module root, re-exports model and service sub-modules
- `modules/fundamental/src/remediation/model/mod.rs` -- model sub-module root
- `modules/fundamental/src/remediation/model/summary.rs` -- `RemediationSummary` struct with fields for each severity x status combination and totals
- `modules/fundamental/src/remediation/model/product.rs` -- `ProductRemediation` struct with product name/ID, total, open, in_progress, resolved counts
- `modules/fundamental/src/remediation/service/mod.rs` -- `RemediationService` with `summary()` and `by_product()` methods

## Files to Modify
- `modules/fundamental/src/lib.rs` -- add `pub mod remediation;` to register the new domain module

## API Changes
- `RemediationSummary` -- NEW response model: severity x status matrix with totals
- `ProductRemediation` -- NEW response model: per-product remediation counts `{ name: String, total: u64, open: u64, in_progress: u64, resolved: u64 }`

## Implementation Notes
Follow the existing domain module pattern established by the `sbom` and `advisory` modules in `modules/fundamental/src/`: each domain has `model/` + `service/` + `endpoints/` sub-modules.

The `RemediationSummary` struct should derive `Serialize`, `Deserialize`, `Clone`, `Debug`, and `utoipa::ToSchema`, following the pattern in `modules/fundamental/src/sbom/model/summary.rs` (`SbomSummary`).

The aggregation service methods should:
- `summary()`: join vulnerability data through `entity/src/sbom_advisory.rs` and `entity/src/advisory.rs` entities, group by severity (using the severity field from `AdvisorySummary` in `modules/fundamental/src/advisory/model/summary.rs`) and remediation status. Use SeaORM's `select_only()` with `column_as()` and `group_by()`.
- `by_product()`: group by product (derived from SBOM metadata via `entity/src/sbom.rs` and `entity/src/sbom_package.rs`), computing total, open, and resolved counts per product. Return `PaginatedResults<ProductRemediation>` using the wrapper from `common/src/model/paginated.rs`.

Use the same `Result<T, AppError>` error handling pattern with `.context()` wrapping from `common/src/error.rs`, consistent with all existing service methods.

Per CONVENTIONS.md: follow the model/ + service/ + endpoints/ module pattern for new domain modules.
Applies: task creates `modules/fundamental/src/remediation/model/summary.rs` matching the convention's `.rs` module scope.

Per CONVENTIONS.md: all service methods return `Result<T, AppError>` with `.context()` wrapping.
Applies: task creates `modules/fundamental/src/remediation/service/mod.rs` matching the convention's `.rs` module scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` -- established struct layout and derive macros pattern to follow for new model structs
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` -- contains the severity field definition; reuse severity enum or string mapping for consistency
- `common/src/db/query.rs` -- shared query builder helpers for filtering, pagination, and sorting
- `common/src/model/paginated.rs::PaginatedResults<T>` -- standard paginated response wrapper for the by-product method
- `common/src/error.rs::AppError` -- standard error type used across all service methods

## Acceptance Criteria
- [ ] `RemediationSummary` struct exists with severity x status count fields and totals
- [ ] `ProductRemediation` struct exists with product identifier, total, open, in_progress, resolved fields
- [ ] `RemediationService::summary()` method compiles and returns correct aggregated counts from the database
- [ ] `RemediationService::by_product()` method compiles and returns correct per-product breakdown with pagination
- [ ] Aggregations use existing entity relationships without creating new database tables
- [ ] New module follows the established model/ + service/ structure under `modules/fundamental/src/remediation/`

## Test Requirements
- [ ] Unit test: `RemediationSummary` serializes to expected JSON shape with severity x status fields
- [ ] Unit test: `ProductRemediation` serializes to expected JSON shape with product breakdown fields
- [ ] Unit test: service methods correctly aggregate test data by severity and status

## Verification Commands
- `cargo build -p trustify-fundamental` -- compiles without errors
- `cargo test -p trustify-fundamental remediation` -- unit tests pass

## Dependencies
- None (first task in the chain)
