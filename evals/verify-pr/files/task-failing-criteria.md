<!-- SYNTHETIC TEST DATA — mock Jira task description for eval testing; names, URLs, and identifiers are fictional -->

# Jira Task: TC-9102

**Key**: TC-9102
**Summary**: Add severity threshold filter to advisory summary endpoint
**Status**: In Review
**Labels**: ai-generated-jira
**PR URL**: https://github.com/trustify/trustify-backend/pull/743
**Web URL**: https://redhat.atlassian.net/browse/TC-9102
**Parent Feature**: TC-9001

---

## Repository
trustify-backend

## Description
Add an optional `threshold` query parameter to the `GET /api/v2/sbom/{id}/advisory-summary` endpoint that filters the severity counts to include only severities at or above the specified threshold. For example, `?threshold=high` returns counts for `critical` and `high` only, omitting `medium` and `low`. The severity ordering is: critical > high > medium > low.

## Files to Modify
- `modules/fundamental/src/advisory/endpoints/get.rs` — add threshold parameter to the summary handler
- `modules/fundamental/src/advisory/service/advisory.rs` — add threshold filtering logic to the aggregation query

## Files to Create
- `tests/api/advisory_summary.rs` — integration tests for threshold filtering

## Implementation Notes
- Follow the existing query parameter pattern in `modules/fundamental/src/advisory/endpoints/list.rs`
- Define a `Severity` enum with `Critical`, `High`, `Medium`, `Low` variants implementing `Ord`
- Reuse `common/src/error.rs::AppError` for validation errors (return 400 for invalid threshold values)
- The aggregation query already exists in `advisory.rs` — extend it with an optional WHERE clause on severity rank

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns counts for critical and high only
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all severity counts (backward compatible)
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=invalid` returns 400 Bad Request
- [ ] Severity ordering is correct: critical > high > medium > low
- [ ] Response includes a `threshold_applied` boolean field indicating whether filtering is active
- [ ] Endpoint returns 404 for non-existent SBOM IDs (existing behavior preserved)

## Test Requirements
- [ ] Test threshold=critical returns only critical count
- [ ] Test threshold=high returns critical and high counts
- [ ] Test threshold=medium returns critical, high, and medium counts
- [ ] Test no threshold returns all four severity counts
- [ ] Test invalid threshold value returns 400
- [ ] Test non-existent SBOM ID returns 404
