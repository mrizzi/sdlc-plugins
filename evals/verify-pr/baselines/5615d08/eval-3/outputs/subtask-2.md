## Repository
trustify-backend

## Description
Add `include_deleted` query parameter support to the `GET /api/v2/sbom/{id}` endpoint so that soft-deleted SBOMs are excluded by default from direct GET requests. Currently, the `get.rs` endpoint does not filter by `deleted_at`, meaning soft-deleted SBOMs are still returned by the GET-by-ID endpoint even after being soft-deleted. The task specification explicitly lists `get.rs` in Files to Modify, but the PR did not include changes to this file.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/get.rs` -- add `include_deleted` query parameter and filter logic to exclude soft-deleted SBOMs by default

## Implementation Notes
- Follow the same pattern used in `modules/fundamental/src/sbom/endpoints/list.rs` for the `include_deleted` parameter
- Add an `include_deleted: Option<bool>` field to the GET endpoint's query parameters (or create a query params struct if one doesn't exist)
- After fetching the SBOM, check `sbom.deleted_at.is_some()` and if `include_deleted` is not `true`, return 404 (the SBOM exists but is treated as not found for non-admin queries)
- Alternatively, modify the `SbomService::fetch` method to accept an `include_deleted` parameter and filter at the query level
- Maintain consistency with the list endpoint's behavior: without `include_deleted=true`, soft-deleted SBOMs should not be accessible

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}` returns 404 for a soft-deleted SBOM when `include_deleted` is not set or is `false`
- [ ] `GET /api/v2/sbom/{id}?include_deleted=true` returns the soft-deleted SBOM with its full details
- [ ] `GET /api/v2/sbom/{id}` continues to return 200 for non-deleted SBOMs regardless of the `include_deleted` parameter

## Test Requirements
- [ ] Test that GET for a soft-deleted SBOM returns 404 by default
- [ ] Test that GET with `include_deleted=true` for a soft-deleted SBOM returns 200 with the SBOM data
- [ ] Test that GET for a non-deleted SBOM returns 200 with or without the `include_deleted` parameter

## Review Context
**Original review comment (PR #744, comment 30004):**
> Have you considered what happens when someone queries `/api/v2/sbom/{id}` for a soft-deleted SBOM without `include_deleted=true`? Looking at `get.rs`, it doesn't filter by `deleted_at` -- so direct GET still returns deleted SBOMs. Is that intentional?

**File:** `modules/fundamental/src/sbom/endpoints/get.rs`, line 1

## Target PR
https://github.com/trustify/trustify-backend/pull/744
