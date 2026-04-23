<!-- SYNTHETIC TEST DATA — task description with Reuse Candidates section for testing implement-task reuse behavior -->

# Mock Jira Task

**Key**: TC-9203
**Summary**: Add package license filter to list endpoint
**Status**: To Do
**Labels**: ai-generated-jira
**Linked Issues**: is incorporated by TC-9001

---

## Repository
trustify-backend

## Description
Add a `license` query parameter to the `GET /api/v2/package` list endpoint. This allows
consumers to filter packages by their declared license (exact match on the license SPDX
identifier). Support both single-value and comma-separated multi-value filtering.

## Files to Modify
- `modules/fundamental/src/package/endpoints/list.rs` — add license query parameter extraction and filtering
- `modules/fundamental/src/package/service/mod.rs` — add license filter to PackageService list method

## Files to Create
- `tests/api/package_license_filter.rs` — integration tests for the license filter

## API Changes
- `GET /api/v2/package?license=MIT` — MODIFY: add optional `license` query parameter for filtering
- `GET /api/v2/package?license=MIT,Apache-2.0` — MODIFY: support comma-separated license values

## Implementation Notes
- Follow the existing filter pattern in `modules/fundamental/src/advisory/endpoints/list.rs` — the advisory list endpoint already supports a `severity` query parameter using the same filtering approach
- Use the `query.rs` helpers in `common/src/db/query.rs` for building the filter — specifically the `apply_filter` function which handles both single and multi-value comma-separated parameters
- The `package_license` entity in `entity/src/package_license.rs` maps packages to licenses — join through this table when filtering
- The response shape from `GET /api/v2/package` must not change — only the input accepts a new optional parameter

## Reuse Candidates
- `common/src/db/query.rs::apply_filter` — handles comma-separated multi-value query parameter parsing and SQL IN clause generation; reuse directly for the license filter
- `modules/fundamental/src/advisory/endpoints/list.rs` — the severity filter implementation is structurally identical to the license filter needed here; follow the same Query struct pattern with an optional field
- `entity/src/package_license.rs` — existing entity for the package-license join table; use for the JOIN query rather than writing raw SQL

## Acceptance Criteria
- [ ] GET /api/v2/package?license=MIT returns only packages with MIT license
- [ ] GET /api/v2/package?license=MIT,Apache-2.0 returns packages matching either license
- [ ] GET /api/v2/package without license parameter returns all packages (no regression)
- [ ] Response shape (PaginatedResults<PackageSummary>) remains unchanged
- [ ] Invalid license values return 400 Bad Request

## Test Requirements
- [ ] Test single license filter returns only matching packages
- [ ] Test comma-separated license filter returns packages matching any listed license
- [ ] Test no license filter returns all packages unchanged
- [ ] Test invalid license value returns 400

## Dependencies
- Depends on: None
