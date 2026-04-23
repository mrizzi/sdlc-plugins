<!-- SYNTHETIC TEST DATA — mock Jira task description for eval testing; names, URLs, and identifiers are fictional -->

# Jira Task: TC-9103

**Key**: TC-9103
**Summary**: Add SBOM deletion endpoint
**Status**: In Review
**Labels**: ai-generated-jira
**PR URL**: https://github.com/trustify/trustify-backend/pull/744
**Web URL**: https://redhat.atlassian.net/browse/TC-9103
**Parent Feature**: TC-9001

---

## Repository
trustify-backend

## Description
Add a `DELETE /api/v2/sbom/{id}` endpoint that soft-deletes an SBOM by setting a `deleted_at` timestamp. The SBOM is excluded from list queries but remains accessible via direct GET with a `?include_deleted=true` parameter. Related join table entries (sbom_package, sbom_advisory) are cascade-updated to mark them as deleted.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the DELETE route
- `modules/fundamental/src/sbom/endpoints/list.rs` — filter out soft-deleted SBOMs by default, add `include_deleted` parameter
- `modules/fundamental/src/sbom/endpoints/get.rs` — add `include_deleted` parameter support
- `modules/fundamental/src/sbom/service/sbom.rs` — add soft-delete logic with cascade updates
- `entity/src/sbom.rs` — add `deleted_at` column to entity

## Files to Create
- `migration/src/m0042_sbom_soft_delete/mod.rs` — migration adding `deleted_at` column
- `tests/api/sbom_delete.rs` — integration tests for deletion endpoint

## Implementation Notes
- Follow the existing endpoint registration pattern in `modules/fundamental/src/sbom/endpoints/mod.rs` using `.route()` with `delete(handler)`
- Use `chrono::Utc::now()` for the `deleted_at` timestamp, matching the pattern in ingestor module
- Cascade logic: update `sbom_package` and `sbom_advisory` rows where `sbom_id` matches, setting their `deleted_at` to the same timestamp
- Return 204 No Content on successful deletion, 404 if SBOM not found, 409 if already deleted

## Acceptance Criteria
- [ ] `DELETE /api/v2/sbom/{id}` sets `deleted_at` on the SBOM record
- [ ] `DELETE /api/v2/sbom/{id}` returns 204 No Content on success
- [ ] `DELETE /api/v2/sbom/{id}` returns 404 for non-existent SBOM
- [ ] `DELETE /api/v2/sbom/{id}` returns 409 Conflict if SBOM is already deleted
- [ ] `GET /api/v2/sbom` excludes soft-deleted SBOMs by default
- [ ] `GET /api/v2/sbom?include_deleted=true` includes soft-deleted SBOMs
- [ ] Related `sbom_package` and `sbom_advisory` rows are cascade-updated
- [ ] Migration adds `deleted_at` column with NULL default to `sbom` table

## Test Requirements
- [ ] Test DELETE returns 204 and SBOM is excluded from list
- [ ] Test DELETE on non-existent SBOM returns 404
- [ ] Test DELETE on already-deleted SBOM returns 409
- [ ] Test GET with `include_deleted=true` returns deleted SBOMs
- [ ] Test cascade update marks related join table rows
