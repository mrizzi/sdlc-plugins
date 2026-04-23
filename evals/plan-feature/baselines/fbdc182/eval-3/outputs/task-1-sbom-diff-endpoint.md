## Repository
trustify-backend

## Description
Implement the SBOM diff computation logic and expose it as `GET /api/v2/sbom/compare?left={id1}&right={id2}`. The endpoint computes a structured diff on-the-fly from existing package, advisory, and license data (no new database tables). It returns six diff categories: added packages, removed packages, version changes, new vulnerabilities, resolved vulnerabilities, and license changes. Response time must be p95 < 1s for SBOMs with up to 2000 packages each.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the new `/compare` route alongside existing `/api/v2/sbom` routes
- `modules/fundamental/src/sbom/service/sbom.rs` — add `compare` method to `SbomService` that fetches packages and advisories for both SBOMs and computes the diff
- `server/src/main.rs` — no change expected if route registration follows the existing pattern; verify that `sbom::endpoints` is already mounted

## Files to Create
- `modules/fundamental/src/sbom/endpoints/compare.rs` — Axum handler for `GET /api/v2/sbom/compare`; extracts `left` and `right` query params, calls `SbomService::compare`, returns `SbomDiff` as JSON
- `modules/fundamental/src/sbom/model/diff.rs` — `SbomDiff` response struct and its sub-structs (`AddedPackage`, `RemovedPackage`, `VersionChange`, `VulnerabilityChange`, `LicenseChange`); derive `serde::Serialize`
- `tests/api/sbom_compare.rs` — integration tests for the compare endpoint

## API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — NEW: returns a `SbomDiff` JSON object with six diff arrays (see Implementation Notes for response schema)

## Implementation Notes

**Route registration pattern** — follow `modules/fundamental/src/sbom/endpoints/mod.rs`. Existing routes are registered with `Router::new().route(...)`. Add:
```rust
.route("/compare", get(compare::compare_sboms))
```
and declare `mod compare;` at the top of `endpoints/mod.rs`.

**Handler signature pattern** — follow `modules/fundamental/src/sbom/endpoints/get.rs`. Handlers receive `State<Arc<SbomService>>` and path/query extractors, return `Result<Json<T>, AppError>`. The new handler uses a query extractor:
```rust
#[derive(Deserialize)]
struct CompareQuery { left: Uuid, right: Uuid }

pub async fn compare_sboms(
    State(service): State<Arc<SbomService>>,
    Query(params): Query<CompareQuery>,
) -> Result<Json<SbomDiff>, AppError> { ... }
```

**Diff computation in SbomService** — add `async fn compare(&self, left: Uuid, right: Uuid) -> Result<SbomDiff, AppError>`. Steps:
1. Load packages for both SBOMs by joining `sbom_package` → `package` (reuse the query pattern from `service/sbom.rs` that already fetches package lists for `SbomDetails`).
2. Build two `HashMap<String, PackageSummary>` keyed by package name.
3. Compute set differences for added/removed; iterate intersection for version changes.
4. Load advisories linked to each SBOM via `sbom_advisory` join table (entity: `entity/src/sbom_advisory.rs`); build sets keyed by advisory ID to compute new/resolved.
5. Load package license data from `entity/src/package_license.rs` to detect license changes.

**Model structs** — follow the style of `modules/fundamental/src/sbom/model/summary.rs` (derive `Debug`, `Clone`, `Serialize`, `Deserialize`, use `utoipa::ToSchema` if OpenAPI is enabled). The top-level struct:
```rust
pub struct SbomDiff {
    pub added_packages: Vec<AddedPackage>,
    pub removed_packages: Vec<RemovedPackage>,
    pub version_changes: Vec<VersionChange>,
    pub new_vulnerabilities: Vec<VulnerabilityChange>,
    pub resolved_vulnerabilities: Vec<VulnerabilityChange>,
    pub license_changes: Vec<LicenseChange>,
}
```

**Error handling** — return `AppError::NotFound` (from `common/src/error.rs`) when either SBOM ID does not exist. Wrap database errors with `.context("fetching packages for sbom diff")`.

**Performance** — load packages for both SBOMs in parallel using `tokio::try_join!` to meet the p95 < 1s target.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — existing service struct; add `compare` method here rather than creating a new service
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — field naming conventions and derive macro pattern to follow for new model structs
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — contains `license` field; reuse for reading package data in diff computation
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — contains `severity` field; reuse for reading advisory data
- `common/src/error.rs::AppError` — use existing error variants; do not create new error types
- `entity/src/sbom_package.rs` — SeaORM entity for the SBOM-Package join; use in queries
- `entity/src/sbom_advisory.rs` — SeaORM entity for the SBOM-Advisory join; use in queries
- `entity/src/package_license.rs` — SeaORM entity for license data; use in license change detection

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/compare?left={id1}&right={id2}` returns HTTP 200 with a valid `SbomDiff` JSON body when both IDs exist
- [ ] Response includes correct `added_packages`: packages in right SBOM not in left
- [ ] Response includes correct `removed_packages`: packages in left SBOM not in right
- [ ] Response includes correct `version_changes`: packages in both SBOMs with differing versions, with `direction` set to `"upgrade"` or `"downgrade"`
- [ ] Response includes correct `new_vulnerabilities`: advisories linked to right SBOM not linked to left
- [ ] Response includes correct `resolved_vulnerabilities`: advisories linked to left SBOM not linked to right
- [ ] Response includes correct `license_changes`: packages whose license differs between the two SBOMs
- [ ] Returns HTTP 404 with an error body when either SBOM ID does not exist
- [ ] Returns HTTP 400 when `left` or `right` query param is missing or not a valid UUID
- [ ] p95 response time < 1s for SBOMs with up to 2000 packages each (verified by load test or benchmark)

## Test Requirements
- [ ] Integration test in `tests/api/sbom_compare.rs`: seed two SBOMs with overlapping and non-overlapping packages; assert response body matches expected diff structure
- [ ] Test case: both SBOMs identical → all diff arrays are empty
- [ ] Test case: left SBOM has packages A, B; right has B (v2), C → added=[C], removed=[A], version_changes=[B]
- [ ] Test case: advisory linked to right SBOM only → appears in `new_vulnerabilities`
- [ ] Test case: advisory linked to left SBOM only → appears in `resolved_vulnerabilities`
- [ ] Test case: license change for a package → appears in `license_changes`
- [ ] Test case: unknown SBOM ID → HTTP 404
- [ ] Test case: missing `left` param → HTTP 400

## Verification Commands
- `cargo test -p tests -- sbom_compare` — all integration tests pass
- `cargo clippy --all-targets -- -D warnings` — no new warnings
- `curl "http://localhost:8080/api/v2/sbom/compare?left={id1}&right={id2}"` — returns JSON with six diff arrays

## Documentation Updates
- `README.md` — add `GET /api/v2/sbom/compare` to the API endpoint reference section
