# Task 4 — Add optional threshold query parameter to advisory-summary endpoint

## Repository
trustify-backend

## Target Branch
main

## Description
Add support for the optional `?threshold=critical` query parameter on `GET /api/v2/sbom/{id}/advisory-summary`. When provided, the response filters severity counts to include only severities at or above the specified threshold. For example, `?threshold=high` returns counts for critical and high only, omitting medium and low. This supports alerting integrations that need to check for advisories above a severity threshold.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — add query parameter extraction for `threshold`, filter severity counts based on the threshold value
- `modules/fundamental/src/sbom/service/sbom.rs` — extend `get_advisory_severity_summary` method to accept an optional threshold parameter and filter counts accordingly

## Implementation Notes
- Define a severity ordering: critical > high > medium > low. When `threshold=high`, include critical and high counts; when `threshold=critical`, include only critical counts.
- Add a query parameter struct (e.g., `AdvisorySummaryQuery`) with an optional `threshold` field of type `Option<String>` or a severity enum type. Use Axum's `Query` extractor following the pattern used for pagination parameters in other endpoints.
- Reference `common/src/db/query.rs` for how query parameters and filtering are handled across the codebase — use shared patterns for query parameter extraction.
- The severity enum values should match those used in `AdvisorySummary` from `modules/fundamental/src/advisory/model/summary.rs` to maintain consistency.
- When threshold is applied, the response should still include all severity fields but set filtered-out severities to 0, and the total should reflect only the counted severities. Alternatively, omit filtered severities entirely — follow whichever pattern is most consistent with existing API behavior.
- Per CONVENTIONS.md §Query helpers: shared filtering, pagination, and sorting via `common/src/db/query.rs`.
  Applies: task modifies `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's `.rs` endpoint scope.
- Per CONVENTIONS.md §Error handling: all handlers return `Result<T, AppError>` with `.context()` wrapping.
  Applies: task modifies `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's `.rs` module scope.

## Reuse Candidates
- `common/src/db/query.rs` — shared query builder helpers for filtering and pagination; reference for query parameter handling patterns
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — contains severity field definition; use for severity enum values
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — the endpoint handler created in Task 2; extend with query parameter support

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=critical` returns only critical severity count
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns critical and high severity counts
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=medium` returns critical, high, and medium severity counts
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` without threshold parameter returns all severity counts (backward compatible)
- [ ] Invalid threshold values return an appropriate error response

## Test Requirements
- [ ] Integration test for each threshold level (critical, high, medium) verifying correct filtering
- [ ] Integration test verifying that omitting the threshold parameter returns all counts (no regression)
- [ ] Integration test for invalid threshold value returning an error response

## Verification Commands
- `cargo build` — project compiles without errors
- `cargo test` — all tests pass including new threshold tests

## Dependencies
- Depends on: Task 2 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint and route registration

[sdlc-workflow] Description digest: sha256-md:99a97b9f29926aa786a0ad8030192833ebe5d311e369133d180cc0f3d70d424e
