## Plan Summary — TC-9001: Add advisory severity aggregation endpoint

### Tasks Created

1. **Task 1 — Define AdvisorySeveritySummary response model**: Create the `AdvisorySeveritySummary` struct with severity count fields in `modules/fundamental/src/sbom/model/advisory_summary.rs`
2. **Task 2 — Add severity aggregation service method**: Add `get_advisory_summary()` to `SbomService` with SeaORM query joining `sbom_advisory` and `advisory` entities, grouping by severity, deduplicating by advisory ID
3. **Task 3 — Add advisory-summary endpoint with caching**: Create `GET /api/v2/sbom/{id}/advisory-summary` handler with 5-minute `Cache-Control` header via tower-http middleware
4. **Task 4 — Add threshold query parameter support**: Extend the endpoint with optional `?threshold=critical|high|medium|low` filtering for alerting integrations
5. **Task 5 — Add cache invalidation in advisory ingestor**: Invalidate cached advisory-summary responses in `modules/ingestor/src/graph/advisory/mod.rs` when new advisories are linked to SBOMs
6. **Task 6 — Add integration tests**: End-to-end tests in `tests/api/sbom_advisory_summary.rs` covering valid responses, 404, empty sets, threshold filtering, deduplication, and cache headers

### Repositories Affected

- **trustify-backend** (all 6 tasks)

### Architecture Summary

The feature adds a server-side advisory severity aggregation endpoint to eliminate client-side counting. The implementation follows the existing module pattern (`model/ + service/ + endpoints/`): a new `AdvisorySeveritySummary` model struct is defined, a service method performs the aggregation query using SeaORM joins against the existing `sbom_advisory` and `advisory` entities (no new database tables), and an Axum handler exposes the result at `GET /api/v2/sbom/{id}/advisory-summary` with 5-minute caching. The advisory ingestor is updated to invalidate cached summaries when new correlations are created. An optional `?threshold` query parameter supports the alerting integration use case.

### Inherited Field Values

- **Priority:** Major (propagated to all tasks)
- **Fix Versions:** RHTPA 1.5.0 (propagated to all tasks, fixVersion scope defaults to "both")
