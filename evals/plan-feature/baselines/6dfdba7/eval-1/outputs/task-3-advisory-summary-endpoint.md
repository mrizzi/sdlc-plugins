## Repository
trustify-backend

## Description
Create the HTTP handler for `GET /api/v2/sbom/{id}/advisory-summary` that extracts path and query parameters, calls the service-layer aggregation method, and returns the JSON response. This endpoint is the primary deliverable of TC-9001, enabling frontend dashboards and alerting integrations to retrieve severity breakdowns in a single call.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — Axum handler function for the advisory summary endpoint

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Register the new route `GET /api/v2/sbom/{id}/advisory-summary` in the SBOM router, add `mod advisory_summary;` declaration

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary` — NEW: Returns `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }` JSON response
- `GET /api/v2/sbom/{id}/advisory-summary?threshold=critical` — NEW: Optional query parameter to filter counts to only severities at or above the given threshold

## Implementation Notes
- Follow the handler pattern in `modules/fundamental/src/sbom/endpoints/get.rs` for path parameter extraction (Axum `Path<Uuid>` extractor), dependency injection of the service and database connection, and error-to-response mapping.
- The handler function signature should be similar to:
  ```rust
  pub async fn advisory_summary(
      Path(id): Path<Uuid>,
      Query(params): Query<AdvisorySummaryParams>,
      State(service): State<SbomService>,
      db: DatabaseConnection,
  ) -> Result<Json<AdvisorySeveritySummary>, AppError>
  ```
- Define `AdvisorySummaryParams` struct in the same file with an optional `threshold: Option<String>` field.
- Route registration in `modules/fundamental/src/sbom/endpoints/mod.rs` should follow the pattern used for `get.rs` and `list.rs`. The route path is `/:id/advisory-summary` nested under the existing `/api/v2/sbom` prefix.
- Return `Json(summary)` on success; the `AppError` implementation in `common/src/error.rs` handles error-to-HTTP-status conversion (404 for not found).

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — Pattern for path extraction, service injection, and error handling in an SBOM-scoped endpoint
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Route registration pattern
- `common/src/error.rs::AppError` — Maps service errors to HTTP status codes via `IntoResponse`

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns 200 with JSON severity counts for a valid SBOM
- [ ] Endpoint returns 404 when the SBOM ID does not exist
- [ ] Optional `?threshold=` query parameter is accepted and filters results
- [ ] Response content type is `application/json`
- [ ] Route is registered in the SBOM endpoint router

## Test Requirements
- [ ] Integration test: GET request to `/api/v2/sbom/{valid-id}/advisory-summary` returns 200 with expected JSON shape
- [ ] Integration test: GET request with non-existent SBOM ID returns 404
- [ ] Integration test: GET request with `?threshold=critical` returns filtered counts

## Verification Commands
- `cargo check -p trustify-fundamental` — should compile without errors

## Dependencies
- Depends on: Task 1 — Advisory summary model
- Depends on: Task 2 — Severity aggregation service method
