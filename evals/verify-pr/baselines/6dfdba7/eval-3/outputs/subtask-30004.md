## Repository
trustify-backend

## Description
Add `include_deleted` query parameter support to the `GET /api/v2/sbom/{id}` endpoint. Currently, direct GET requests return soft-deleted SBOMs unconditionally, which contradicts the task design. The endpoint should filter out soft-deleted SBOMs by default and only return them when `include_deleted=true` is passed as a query parameter.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/get.rs` — add `include_deleted` query parameter to the handler; if the fetched SBOM has `deleted_at` set and `include_deleted` is not `true`, return 404
- `modules/fundamental/src/sbom/service/sbom.rs` — optionally update the `fetch` method to accept an `include_deleted` parameter, or handle the filtering at the endpoint level

## Implementation Notes
- Follow the same pattern used in `modules/fundamental/src/sbom/endpoints/list.rs` for the `include_deleted` parameter: add it to a query params struct and default to `false` via `unwrap_or(false)`
- The existing `get.rs` handler uses `SbomService::fetch(id)` — either add an `include_deleted` parameter to `fetch()` that filters by `deleted_at`, or check `deleted_at` on the returned model and return `AppError::NotFound` if the SBOM is deleted and `include_deleted` is false
- The simpler approach (check after fetch) avoids modifying the service layer signature, matching how the delete endpoint already checks `sbom.deleted_at.is_some()`
- Use `Query` extractor from axum for the query parameter, similar to `list.rs`

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/list.rs::SbomListParams` — demonstrates the `include_deleted` parameter pattern with `Option<bool>` and `unwrap_or(false)`
- `modules/fundamental/src/sbom/endpoints/mod.rs::delete_sbom` — demonstrates checking `sbom.deleted_at.is_some()` on a fetched SBOM

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}` returns 404 for soft-deleted SBOMs by default (when `include_deleted` is not set or is `false`)
- [ ] `GET /api/v2/sbom/{id}?include_deleted=true` returns soft-deleted SBOMs normally
- [ ] `GET /api/v2/sbom/{id}` continues to return non-deleted SBOMs normally regardless of the parameter

## Test Requirements
- [ ] Test that `GET /api/v2/sbom/{id}` returns 404 for a soft-deleted SBOM without the `include_deleted` parameter
- [ ] Test that `GET /api/v2/sbom/{id}?include_deleted=true` returns a soft-deleted SBOM with 200
- [ ] Test that `GET /api/v2/sbom/{id}` returns 200 for a non-deleted SBOM (regression check)

## Review Context
**Reviewer:** reviewer-a
**PR Comment:** "Have you considered what happens when someone queries `/api/v2/sbom/{id}` for a soft-deleted SBOM without `include_deleted=true`? Looking at `get.rs`, it doesn't filter by `deleted_at` -- so direct GET still returns deleted SBOMs. Is that intentional?"
**File:** `modules/fundamental/src/sbom/endpoints/get.rs`, line 1

## Target PR
https://github.com/trustify/trustify-backend/pull/744
