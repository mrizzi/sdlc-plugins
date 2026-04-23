<!-- SYNTHETIC TEST DATA — well-structured task description for implement-task golden path eval testing -->

# Mock Jira Task

**Key**: TC-9201
**Summary**: Add advisory severity aggregation service and endpoint
**Status**: To Do
**Labels**: ai-generated-jira
**Linked Issues**: is incorporated by TC-9001

---

## Repository
trustify-backend

## Description
Add a service method and REST endpoint that aggregates vulnerability advisory severity
counts for a given SBOM. The endpoint returns a summary with counts per severity level
(Critical, High, Medium, Low) and a total, enabling dashboard widgets to render severity
breakdowns without client-side counting.

## Files to Modify
- `modules/fundamental/src/advisory/service/advisory.rs` — add `severity_summary` method to AdvisoryService
- `modules/fundamental/src/advisory/endpoints/mod.rs` — register the new route
- `server/src/main.rs` — no changes needed (routes auto-mount via module registration)

## Files to Create
- `modules/fundamental/src/advisory/model/severity_summary.rs` — SeveritySummary response struct
- `modules/fundamental/src/advisory/endpoints/severity_summary.rs` — GET handler for /api/v2/sbom/{id}/advisory-summary
- `tests/api/advisory_summary.rs` — integration tests for the new endpoint

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary` — NEW: returns `{ critical: N, high: N, medium: N, low: N, total: N }`

## Implementation Notes
- Follow the existing endpoint pattern in `modules/fundamental/src/advisory/endpoints/get.rs` — extract path params via `Path<Id>`, call service, return JSON
- The `AdvisoryService` in `modules/fundamental/src/advisory/service/advisory.rs` has `fetch` and `list` methods — add a `severity_summary` method following the same pattern (takes `&self, sbom_id: Id, tx: &Transactional<'_>`) 
- Use the `sbom_advisory` join table in `entity/src/sbom_advisory.rs` to find advisories linked to the SBOM
- The `AdvisorySummary` struct in `modules/fundamental/src/advisory/model/summary.rs` has a `severity` field — use this to count by severity level
- Register the new route in `modules/fundamental/src/advisory/endpoints/mod.rs` following the pattern of existing `Router::new().route("/path", get(handler))` registrations
- Error handling: return `AppError` with `.context()` wrapping, matching the pattern in `common/src/error.rs`
- Response type: return the struct directly (Axum's `Json` extractor handles serialization)

## Acceptance Criteria
- [ ] GET /api/v2/sbom/{id}/advisory-summary returns `{ critical: N, high: N, medium: N, low: N, total: N }`
- [ ] Returns 404 when SBOM ID does not exist, consistent with existing SBOM endpoints
- [ ] Counts only unique advisories (deduplicates by advisory ID)
- [ ] All severity levels default to 0 when no advisories exist at that level
- [ ] Response time under 200ms for SBOMs with up to 500 advisories

## Test Requirements
- [ ] Test that a valid SBOM with known advisories returns correct severity counts
- [ ] Test that a non-existent SBOM ID returns 404
- [ ] Test that an SBOM with no advisories returns all zeros
- [ ] Test that duplicate advisory links are deduplicated in the count

## Dependencies
- Depends on: None
