## Repository
trustify-backend

## Target Branch
main

## Parent Epic
TC-9006: trustify-backend

## Description
Create the remediation module structure and define model structs for the vulnerability remediation tracking feature. This task establishes the data types used by the remediation summary and by-product aggregation endpoints. The models represent aggregated views computed from existing SBOM-advisory-vulnerability relationships — no new database tables are required.

## Files to Create
- `modules/remediation/Cargo.toml` — Crate manifest for the remediation module
- `modules/remediation/src/lib.rs` — Module root re-exporting model and (future) service/endpoint submodules
- `modules/remediation/src/model/mod.rs` — Model submodule root
- `modules/remediation/src/model/summary.rs` — `RemediationSummary` struct with severity-by-status counts (Critical/High/Medium/Low x Open/In Progress/Resolved) and totals
- `modules/remediation/src/model/by_product.rs` — `ProductRemediation` struct with product name, total/open/in-progress/resolved counts

## Files to Modify
- `Cargo.toml` — Add `trustify-remediation` workspace member

## Implementation Notes
Follow the existing module pattern in `modules/fundamental/src/` where each domain has a `model/` subdirectory with typed structs. Reference `modules/fundamental/src/advisory/model/summary.rs` for struct conventions (derive macros, serde attributes, field naming).

Per CONVENTIONS.md: the module pattern requires `model/ + service/ + endpoints/` structure. This task creates the `model/` layer; service and endpoints follow in subsequent tasks.
Applies: task creates `modules/remediation/src/model/summary.rs` and `modules/remediation/src/model/by_product.rs` matching the convention's `.rs` module scope.

The `RemediationSummary` struct should include:
- `total_open: i64`, `total_in_progress: i64`, `total_resolved: i64`
- `by_severity: Vec<SeverityBreakdown>` where `SeverityBreakdown` has `severity: String`, `open: i64`, `in_progress: i64`, `resolved: i64`

The `ProductRemediation` struct should include:
- `product_name: String`, `product_id: String`
- `total: i64`, `open: i64`, `in_progress: i64`, `resolved: i64`

Use `PaginatedResults<ProductRemediation>` from `common/src/model/paginated.rs` for the by-product list response.

## Reuse Candidates
- `common/src/model/paginated.rs::PaginatedResults<T>` — Wraps list responses with pagination metadata; use for the by-product endpoint response type
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — Reference for struct derive patterns and serde configuration

## Acceptance Criteria
- [ ] `RemediationSummary` struct is defined with severity-by-status breakdown fields
- [ ] `ProductRemediation` struct is defined with per-product aggregation fields
- [ ] `SeverityBreakdown` struct is defined for the nested severity grouping
- [ ] All structs derive `Serialize`, `Deserialize`, `Debug`, `Clone`
- [ ] Module compiles as a workspace member without errors

## Test Requirements
- [ ] Module compiles successfully (`cargo check -p trustify-remediation`)
- [ ] Struct serialization round-trips correctly (unit test in model module)

## Dependencies
- Depends on: None

## additional_fields
- labels: ["ai-generated-jira"]
- priority: Major
- fixVersions: ["RHTPA 1.5.0"]
