## Repository
trustify-backend

## Description
Implement the SBOM comparison service logic and HTTP endpoint. The service loads package and advisory data for two SBOMs, computes the diff on-the-fly (no new database tables), and returns a structured `SbomComparison` response. The endpoint is registered at `GET /api/v2/sbom/compare?left={id1}&right={id2}`.

## Files to Create
- `modules/fundamental/src/sbom/service/compare.rs` — `SbomService::compare(left_id, right_id)` method that computes the diff between two SBOMs
- `modules/fundamental/src/sbom/endpoints/compare.rs` — Axum handler for `GET /api/v2/sbom/compare`, extracts `left` and `right` query params, calls the service, returns JSON

## Files to Modify
- `modules/fundamental/src/sbom/service/mod.rs` — Add `pub mod compare;` to include the comparison service module
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Register the `/compare` route in the SBOM router

## API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — NEW: Returns `SbomComparison` JSON. Returns 400 if either param is missing, 404 if either SBOM not found.

## Implementation Notes
- The service method should live in `modules/fundamental/src/sbom/service/compare.rs` as an `impl SbomService` block, following the pattern in `modules/fundamental/src/sbom/service/sbom.rs`.
- Use `PackageService::list()` from `modules/fundamental/src/sbom/../package/service/mod.rs` to load packages for each SBOM, or query `entity::sbom_package` directly via SeaORM.
- Use `AdvisoryService::list()` from `modules/fundamental/src/advisory/service/advisory.rs` to load advisories linked to each SBOM via `entity::sbom_advisory`.
- Diff computation: build `HashMap<String, PackageInfo>` for each SBOM keyed by package name, then iterate to find added, removed, and version-changed packages.
- For vulnerability diff: build sets of advisory IDs for each SBOM, compute set differences for new/resolved.
- For license changes: compare the `license` field on packages present in both SBOMs.
- The endpoint handler should follow the pattern in `modules/fundamental/src/sbom/endpoints/get.rs` — extract query params, call service, return `Result<Json<SbomComparison>, AppError>`.
- Use `.context()` for error wrapping as per `common/src/error.rs::AppError` conventions.
- The endpoint must respond within 1 second for SBOMs with up to 2000 packages each (per NFR). Avoid N+1 queries — batch-load all packages and advisories.
- Query helpers from `common/src/db/query.rs` may be useful for filtering packages by SBOM ID.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — pattern for service method implementation
- `modules/fundamental/src/sbom/endpoints/get.rs` — pattern for endpoint handler with error handling
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — loading advisories for SBOM-advisory join
- `common/src/db/query.rs` — shared query builder helpers for filtering
- `common/src/error.rs::AppError` — error type with `.context()` wrapping

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/compare?left={id1}&right={id2}` returns a valid `SbomComparison` JSON response
- [ ] Endpoint returns 400 Bad Request when `left` or `right` query parameter is missing
- [ ] Endpoint returns 404 Not Found when either SBOM ID does not exist
- [ ] Diff correctly identifies added, removed, and version-changed packages
- [ ] Diff correctly identifies new and resolved vulnerabilities
- [ ] Diff correctly identifies license changes
- [ ] No new database tables or migrations are created
- [ ] Response time is under 1 second for SBOMs with up to 2000 packages

## Test Requirements
- [ ] Unit tests for diff computation logic (added/removed/changed detection with mock data)
- [ ] Verify 400 response for missing query parameters
- [ ] Verify 404 response for nonexistent SBOM IDs

## Verification Commands
- `cargo check -p trustify-module-fundamental` — compiles without errors
- `cargo test -p trustify-module-fundamental compare` — comparison unit tests pass

## Dependencies
- Depends on: Task 1 — Backend comparison models
