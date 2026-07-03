## Repository
trustify-backend

## Target Branch
main

## Description
Create the advisory severity summary model and aggregation service method. This task introduces an `AdvisorySeveritySummary` response struct and a service-layer method on `SbomService` that queries the `sbom_advisory` join table to compute per-severity counts (critical, high, medium, low, total) for a given SBOM. The aggregation must deduplicate by advisory ID to avoid double-counting and support an optional severity threshold filter for alerting use cases.

additional_fields: { "labels": ["ai-generated-jira"], "priority": "Major", "fixVersions": "RHTPA 1.5.0" }

## Files to Create
- `modules/fundamental/src/sbom/model/advisory_summary.rs` -- `AdvisorySeveritySummary` struct with fields: critical, high, medium, low, total (all u64), and `SeverityThreshold` enum (Critical, High, Medium, Low) for optional filtering

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` -- add `pub mod advisory_summary;` and re-export `AdvisorySeveritySummary`
- `modules/fundamental/src/sbom/service/sbom.rs` -- add `advisory_severity_summary(&self, sbom_id: Uuid, threshold: Option<SeverityThreshold>) -> Result<AdvisorySeveritySummary, AppError>` method that joins `sbom_advisory` with `advisory`, groups by severity, deduplicates by advisory ID, and applies optional threshold filtering

## API Changes
- `AdvisorySeveritySummary` -- NEW response model: `{ critical: u64, high: u64, medium: u64, low: u64, total: u64 }`

## Implementation Notes
Follow the existing model pattern in `modules/fundamental/src/sbom/model/summary.rs` (`SbomSummary` struct) for struct layout and derive macros. The new `AdvisorySeveritySummary` should derive `Serialize`, `Deserialize`, `Clone`, `Debug`, and `utoipa::ToSchema`.

The aggregation query joins `entity/src/sbom_advisory.rs` (SBOM-Advisory join table) with `entity/src/advisory.rs` (which contains the severity field, referenced in `modules/fundamental/src/advisory/model/summary.rs` `AdvisorySummary`). Use SeaORM's `select_only()` with `column_as()` and `group_by()` to count advisories per severity level. Apply `distinct` on advisory ID to deduplicate.

The service method belongs in `modules/fundamental/src/sbom/service/sbom.rs` alongside existing `SbomService` methods (fetch, list, ingest). Use the same `Result<T, AppError>` error handling pattern with `.context()` wrapping from `common/src/error.rs`.

When `threshold` is provided, filter the query to only include severities at or above the given level. The `SeverityThreshold` enum should map to the severity ordering: Critical > High > Medium > Low.

Per CONVENTIONS.md: all handlers and service methods return `Result<T, AppError>` with `.context()` wrapping.
Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's `.rs` module scope.

## Reuse Candidates
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` -- contains the severity field definition; reuse the severity enum or string mapping for consistency
- `common/src/db/query.rs` -- shared query builder helpers for filtering; reuse for conditional filtering on severity threshold
- `common/src/error.rs::AppError` -- standard error type used across all service methods

## Acceptance Criteria
- [ ] `AdvisorySeveritySummary` struct exists with fields: critical, high, medium, low, total
- [ ] `SeverityThreshold` enum exists with variants: Critical, High, Medium, Low
- [ ] `SbomService::advisory_severity_summary` method compiles and returns correct counts from the database
- [ ] Advisory IDs are deduplicated in the count (each advisory counted once regardless of how many times it links to the SBOM)
- [ ] When threshold is `Some(Critical)`, only critical count and total are populated; others are zero

## Test Requirements
- [ ] Unit test: `AdvisorySeveritySummary` serializes to expected JSON shape `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }`
- [ ] Unit test: `SeverityThreshold` correctly filters severity levels (Critical includes only Critical; High includes Critical + High; etc.)

## Verification Commands
- `cargo build -p trustify-fundamental` -- compiles without errors
- `cargo test -p trustify-fundamental advisory_summary` -- unit tests pass
