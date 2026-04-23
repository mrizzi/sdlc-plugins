<!-- SYNTHETIC TEST DATA — mock Jira task description for eval testing; names, URLs, and identifiers are fictional -->

# Jira Task: TC-9101

**Key**: TC-9101
**Summary**: Add license filter to package list endpoint
**Status**: In Review
**Labels**: ai-generated-jira
**PR URL**: https://github.com/trustify/trustify-backend/pull/742
**Web URL**: https://redhat.atlassian.net/browse/TC-9101
**Parent Feature**: TC-9001

---

## Repository
trustify-backend

## Description
Add a `license` query parameter to the existing `GET /api/v2/package` endpoint that filters packages by their SPDX license identifier. This enables consumers to list only packages with a specific license type (e.g., `?license=MIT`). Multiple license values are supported via comma separation (e.g., `?license=MIT,Apache-2.0`). Invalid license identifiers return a 400 Bad Request response.

## Files to Modify
- `modules/fundamental/src/package/endpoints/list.rs` — add license query parameter parsing and validation
- `modules/fundamental/src/package/service/mod.rs` — add license filter to the package query builder

## Files to Create
- `tests/api/package.rs` — integration tests for the license filter

## Implementation Notes
- Follow the existing filter pattern in `modules/fundamental/src/advisory/endpoints/list.rs` which uses `Query<FilterParams>` extraction
- Reuse `common/src/db/query.rs` helpers for building the WHERE clause
- Validate license identifiers against a known SPDX license list before querying; return `AppError::BadRequest` for invalid values
- Use `common/src/model/paginated.rs::PaginatedResults` for the response wrapper, consistent with other list endpoints

## Acceptance Criteria
- [ ] `GET /api/v2/package?license=MIT` returns only packages with MIT license
- [ ] `GET /api/v2/package?license=MIT,Apache-2.0` returns packages with either license
- [ ] `GET /api/v2/package?license=INVALID-999` returns 400 Bad Request with an error message
- [ ] Filter integrates with existing pagination — filtered results are paginated correctly
- [ ] Response shape is unchanged (still `PaginatedResults<PackageSummary>`)

## Test Requirements
- [ ] Test single license filter returns matching packages only
- [ ] Test comma-separated license filter returns union of matching packages
- [ ] Test invalid license identifier returns 400 status code
- [ ] Test filter with pagination parameters returns correct page of filtered results
