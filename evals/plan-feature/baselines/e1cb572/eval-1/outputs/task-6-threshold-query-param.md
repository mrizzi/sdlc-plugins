# Task 6: Add optional threshold query parameter filtering to advisory summary endpoint

## Repository
trustify-backend

## Target Branch
main

## Description
Enhance the advisory summary endpoint and service layer to support an optional `?threshold=critical|high|medium|low` query parameter that filters severity counts to include only advisories at or above the specified severity level. When `?threshold=high` is provided, the response includes counts for Critical and High severities only, with Medium and Low returned as 0 and the total reflecting only the included counts.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` — update the `advisory_severity_summary` method to apply the threshold filter in the database query. When a threshold is provided, add a `WHERE` clause that restricts the severity aggregation to levels at or above the threshold. Map severity levels to ordinals (Critical=4, High=3, Medium=2, Low=1) and filter with `severity_ordinal >= threshold_ordinal`.
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — ensure the handler extracts the optional `threshold` query parameter from the `AdvisorySummaryQuery` struct and passes it to the service method. Update the OpenAPI documentation annotations (`#[utoipa::path(...)]`) to describe the `threshold` query parameter including its allowed values and behavior.
- `modules/fundamental/src/sbom/model/severity_threshold.rs` — add a `min_ordinal(&self) -> i32` method to `SeverityThreshold` that returns the numeric ordinal for filtering, and a `includes(&self, severity: &str) -> bool` convenience method that checks whether a given severity level meets or exceeds the threshold.

## Implementation Notes
- The threshold filtering should happen at the database query level, not by post-processing the full aggregation result. This ensures performance is maintained for SBOMs with hundreds of advisories.
- In `modules/fundamental/src/sbom/service/sbom.rs`, modify the aggregation query to add a conditional `WHERE` clause. When threshold is `Some(SeverityThreshold::High)`, add `.filter(advisory::Column::Severity.is_in(vec!["critical", "high"]))` or equivalent SeaORM filter. Reference the existing filtering patterns in `common/src/db/query.rs`.
- The `total` field in the response must equal the sum of the included severity counts (not the total across all severities). When threshold=high, total = critical + high.
- Severity levels excluded by the threshold must be returned as 0 in the response (not omitted from the JSON), so the response shape is always consistent.
- For the `SeverityThreshold` ordinal mapping:
  - `Critical` -> 4 (includes only Critical)
  - `High` -> 3 (includes Critical, High)
  - `Medium` -> 2 (includes Critical, High, Medium)
  - `Low` -> 1 (includes all — equivalent to no filter)
- Per Key Conventions §Error handling: all service methods return `Result<T, AppError>` with `.context()` wrapping. Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's `.rs` service files scope.
- Per Key Conventions §Module pattern: follow the `model/ + service/ + endpoints/` directory structure. Applies: task modifies `modules/fundamental/src/sbom/model/severity_threshold.rs` matching the convention's `.rs` module files scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/severity_threshold.rs::SeverityThreshold` — enum created in Task 1; add ordinal methods here
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — service method to modify with threshold filtering
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — endpoint handler that already accepts the threshold parameter
- `common/src/db/query.rs` — reference for SeaORM filtering patterns and query builder conventions
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — reference for severity field values to ensure consistent level naming

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=critical` returns only critical count (high, medium, low are 0)
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns critical and high counts (medium, low are 0)
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=medium` returns critical, high, and medium counts (low is 0)
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=low` returns all counts (equivalent to no threshold)
- [ ] `total` field equals the sum of the non-zero severity counts for the applied threshold
- [ ] Response shape is always consistent — all five fields present regardless of threshold
- [ ] Invalid threshold value (e.g., `?threshold=unknown`) returns 400 Bad Request
- [ ] Threshold parameter is case-insensitive (`?threshold=HIGH` works)
- [ ] OpenAPI documentation includes the threshold query parameter description

## Test Requirements
- [ ] Integration test: call with `?threshold=critical` on an SBOM with advisories at all severity levels, verify only critical count is non-zero
- [ ] Integration test: call with `?threshold=high`, verify critical and high counts are correct and medium/low are 0
- [ ] Integration test: call with `?threshold=low`, verify response matches a call without the threshold parameter
- [ ] Integration test: call with `?threshold=CRITICAL` (uppercase), verify case-insensitive parsing works
- [ ] Unit test: `SeverityThreshold::min_ordinal` returns correct ordinal for each variant
- [ ] Unit test: `SeverityThreshold::includes` returns correct boolean for each severity level at each threshold

## Verification Commands
- `cargo check -p trustify-fundamental` — compiles without errors
- `cargo test -p trustify-fundamental -- sbom::service` — service tests pass
- `cargo test -p trustify-fundamental -- sbom::endpoints` — endpoint tests pass
- `cargo test --test api -- sbom_advisory_summary` — integration tests pass

## Dependencies
- Depends on: Task 3 — Add advisory-summary endpoint handler and route registration

---

> [sdlc-workflow] Description digest: sha256-md:f6c9h0e51g8d430286i5f1c79e0gd3h56j3fei37i9g16502hdc8e74f9i2g1365
