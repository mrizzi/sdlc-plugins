# Task 1 — Add AdvisorySeveritySummary model and severity aggregation service method

## Repository
trustify-backend

## Target Branch
main

## Description
Add the `AdvisorySeveritySummary` response model and a severity aggregation query method to `SbomService`. This provides the data layer for the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint. The service method queries the `sbom_advisory` join table, groups advisories by severity, deduplicates by advisory ID, and returns counts for each severity level (critical, high, medium, low) plus a total.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` — add `get_advisory_severity_summary` method to SbomService that queries severity counts from the sbom_advisory join table
- `modules/fundamental/src/sbom/model/mod.rs` — re-export the new AdvisorySeveritySummary struct

## Files to Create
- `modules/fundamental/src/sbom/model/advisory_severity_summary.rs` — define AdvisorySeveritySummary struct with fields: critical (u64), high (u64), medium (u64), low (u64), total (u64)

## Implementation Notes
- Follow the existing model pattern in `modules/fundamental/src/sbom/model/summary.rs` (SbomSummary) and `modules/fundamental/src/sbom/model/details.rs` (SbomDetails) for struct definition, derive macros (Serialize, Deserialize, Clone, Debug), and module re-exports.
- The new `AdvisorySeveritySummary` struct should derive `serde::Serialize` and `serde::Deserialize` for JSON response serialization, matching the pattern used by `SbomSummary`.
- The service method should be added to `SbomService` in `modules/fundamental/src/sbom/service/sbom.rs`, following the existing method patterns (fetch, list, ingest) for error handling with `Result<T, AppError>` and `.context()` wrapping from `common/src/error.rs`.
- Use the `sbom_advisory` entity from `entity/sbom_advisory.rs` as the join table to find advisories linked to a given SBOM. Use the `advisory` entity from `entity/advisory.rs` to access the severity field.
- Reference `AdvisorySummary` in `modules/fundamental/src/advisory/model/summary.rs` for the severity field definition — the aggregation query should group by this field.
- Deduplicate advisories by advisory ID before counting to satisfy the requirement of counting only unique advisories.
- Use SeaORM query builder patterns consistent with the existing codebase. Reference `common/src/db/query.rs` for shared query helper patterns.
- The method should accept an SBOM ID parameter and return `Result<AdvisorySeveritySummary, AppError>`, returning a Not Found error if the SBOM does not exist (check SBOM existence first, consistent with existing SBOM endpoint behavior in `modules/fundamental/src/sbom/endpoints/get.rs`).
- Per CONVENTIONS.md §Framework: use SeaORM for database access.
  Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's `.rs` module scope.
- Per CONVENTIONS.md §Error handling: all service methods return `Result<T, AppError>` with `.context()` wrapping.
  Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's `.rs` module scope.
- Per CONVENTIONS.md §Module pattern: each domain module follows `model/ + service/ + endpoints/` structure.
  Applies: task creates `modules/fundamental/src/sbom/model/advisory_severity_summary.rs` matching the convention's module directory scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — existing model struct in the same module; follow its derive macros and serialization patterns
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — contains the severity field definition; reference for severity enum values
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — existing service with fetch/list methods; follow its error handling and query patterns
- `entity/sbom_advisory.rs` — SBOM-Advisory join table entity; use for the aggregation query
- `common/src/error.rs::AppError` — shared error type; use for error returns

## Acceptance Criteria
- [ ] `AdvisorySeveritySummary` struct exists with fields: critical, high, medium, low, total (all u64)
- [ ] `SbomService` has a `get_advisory_severity_summary` method that accepts an SBOM ID and returns severity counts
- [ ] The method deduplicates advisories by advisory ID before counting
- [ ] The method returns an appropriate error if the SBOM ID does not exist
- [ ] The struct derives Serialize and Deserialize for JSON serialization

## Test Requirements
- [ ] Unit test verifying AdvisorySeveritySummary serializes to the expected JSON shape `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }`
- [ ] The service method is covered by integration tests in Task 5

## Dependencies
- None

[sdlc-workflow] Description digest: sha256-md:3209938dd2bf2822df294251b69839139d1bf9e5f2a28b7ca575b44c6d190f30
