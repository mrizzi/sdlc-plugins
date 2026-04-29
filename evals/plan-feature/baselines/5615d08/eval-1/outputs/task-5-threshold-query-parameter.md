## Repository
trustify-backend

## Description
Add optional `?threshold=critical|high|medium|low` query parameter support to the advisory summary endpoint. When provided, the response only includes severity counts at or above the specified threshold level (e.g., `?threshold=high` returns critical and high counts only, with medium and low set to zero). This enables alerting integrations to filter for specific severity levels without client-side post-processing.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — Add `Query<AdvisorySummaryParams>` extractor with optional `threshold` field; filter the summary response based on threshold before returning
- `modules/fundamental/src/sbom/model/advisory_summary.rs` — Add `SeverityThreshold` enum (`Critical`, `High`, `Medium`, `Low`) and a method on `AdvisorySeveritySummary` to apply the threshold filter

## Implementation Notes
- Define a `SeverityThreshold` enum in `modules/fundamental/src/sbom/model/advisory_summary.rs` with variants `Critical`, `High`, `Medium`, `Low`. Derive `Deserialize` so Axum can parse the query parameter directly.
- Add a query parameter struct `AdvisorySummaryParams` in `modules/fundamental/src/sbom/endpoints/advisory_summary.rs`:
  ```rust
  #[derive(Deserialize)]
  struct AdvisorySummaryParams {
      threshold: Option<SeverityThreshold>,
  }
  ```
- Update the handler signature to include `Query(params): Query<AdvisorySummaryParams>`.
- Implement a method `AdvisorySeveritySummary::apply_threshold(&mut self, threshold: SeverityThreshold)` that zeroes out counts below the threshold and recalculates `total`. The severity ordering is: Critical > High > Medium > Low.
- Follow the query parameter pattern used by list endpoints in `modules/fundamental/src/sbom/endpoints/list.rs` which use Axum's `Query` extractor for filtering parameters.
- The threshold filter should be applied after the aggregation query, not within the SQL — this keeps the service method simple and makes caching more effective (one cached result can serve requests with different thresholds).

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/list.rs` — Pattern for `Query` parameter extraction in Axum handlers
- `common/src/db/query.rs` — Reference for how filtering params are structured in the codebase

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=critical` returns only critical count (high, medium, low zeroed), total equals critical count
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns critical and high counts, medium and low zeroed
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=medium` returns critical, high, and medium counts, low zeroed
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=low` returns all counts (same as no threshold)
- [ ] Omitting the `threshold` parameter returns all severity counts (backwards compatible)
- [ ] Invalid threshold value returns 400 Bad Request

## Test Requirements
- [ ] Integration test: verify `?threshold=critical` zeroes out non-critical counts
- [ ] Integration test: verify `?threshold=high` returns critical + high only
- [ ] Integration test: verify omitting threshold returns all counts unchanged
- [ ] Unit test: `AdvisorySeveritySummary::apply_threshold` correctly zeroes fields and recalculates total for each threshold level
- [ ] Integration test: invalid threshold value (e.g., `?threshold=invalid`) returns 400

## Dependencies
- Depends on: Task 3 — Advisory summary endpoint (provides the handler to extend with query parameters)
