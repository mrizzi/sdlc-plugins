## Repository
trustify-backend

## Description
Add `include_deleted` query parameter support to the `GET /api/v2/sbom/{id}` endpoint in `get.rs`. Currently, the direct GET endpoint returns soft-deleted SBOMs without any filtering, which contradicts the task's acceptance criteria. The endpoint should check the `deleted_at` field and return 404 for soft-deleted SBOMs by default, unless `include_deleted=true` is passed as a query parameter.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/get.rs` -- add `include_deleted` query parameter; filter out soft-deleted SBOMs when parameter is absent or false

## Implementation Notes
- Follow the same pattern used in `list.rs` for the `include_deleted` parameter: add it to a query params struct and use `unwrap_or(false)`
- After fetching the SBOM via `SbomService::fetch`, check if `deleted_at` is set and `include_deleted` is false; if so, return `AppError::NotFound`
- This ensures consistent behavior between the list and get endpoints for soft-deleted SBOMs
- The `SbomService::fetch` method does not need modification -- the filtering is done at the endpoint level after fetching

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}` returns 404 for soft-deleted SBOMs when `include_deleted` is not set
- [ ] `GET /api/v2/sbom/{id}?include_deleted=true` returns the soft-deleted SBOM
- [ ] Non-deleted SBOMs are returned normally regardless of the `include_deleted` parameter

## Test Requirements
- [ ] Test GET for a soft-deleted SBOM returns 404 without `include_deleted`
- [ ] Test GET for a soft-deleted SBOM with `include_deleted=true` returns the SBOM
- [ ] Test GET for a non-deleted SBOM returns 200 normally

## Target PR
https://github.com/trustify/trustify-backend/pull/744

## Review Context
**Comment ID:** 30004
**File:** `modules/fundamental/src/sbom/endpoints/get.rs` (line 1)
**Reviewer:** reviewer-a
**Comment:** "Have you considered what happens when someone queries `/api/v2/sbom/{id}` for a soft-deleted SBOM without `include_deleted=true`? Looking at `get.rs`, it doesn't filter by `deleted_at` -- so direct GET still returns deleted SBOMs. Is that intentional?"

This sub-task addresses an acceptance criteria gap: the task specification lists `get.rs` in "Files to Modify" with "add `include_deleted` parameter support", but the PR does not include changes to this file.
