# Task 1 — Backend SBOM comparison endpoint and diffing service

## Repository
trustify-backend

## Description
Add a new `GET /api/v2/sbom/compare?left={id1}&right={id2}` endpoint that computes an on-the-fly diff between two SBOMs and returns a structured comparison result. This enables security analysts and compliance officers to see added/removed packages, version changes, new/resolved vulnerabilities, and license changes between two SBOM versions without manual comparison. The diff must be computed from existing package, advisory, and license data — no new database tables are introduced.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the new `/compare` route alongside existing SBOM routes
- `modules/fundamental/src/sbom/service/mod.rs` — add reference to the new comparison service module
- `server/src/main.rs` — no changes expected (routes are mounted via the fundamental module), but verify the compare route is included

## Files to Create
- `modules/fundamental/src/sbom/model/comparison.rs` — define `SbomComparisonResult`, `AddedPackage`, `RemovedPackage`, `VersionChange`, `NewVulnerability`, `ResolvedVulnerability`, `LicenseChange` structs with `Serialize`/`Deserialize` derives
- `modules/fundamental/src/sbom/service/comparison.rs` — implement `SbomComparisonService::compare(left_id, right_id)` that fetches both SBOMs' package lists and advisory associations, then computes the diff
- `modules/fundamental/src/sbom/endpoints/compare.rs` — implement the `GET /api/v2/sbom/compare` handler with `left` and `right` query parameters
- `tests/api/sbom_compare.rs` — integration tests for the comparison endpoint

## API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — NEW: returns `SbomComparisonResult` with fields: `added_packages`, `removed_packages`, `version_changes`, `new_vulnerabilities`, `resolved_vulnerabilities`, `license_changes`

## Implementation Notes

### Module structure
Follow the established `model/ + service/ + endpoints/` pattern used by existing domain modules (see `modules/fundamental/src/sbom/` for the reference structure). The comparison model, service, and endpoint each get their own file within the existing `sbom` module — no new top-level module is needed.

### Comparison model
Define the response structs in `modules/fundamental/src/sbom/model/comparison.rs`:
- `SbomComparisonResult` — top-level struct containing vectors for each diff category
- `AddedPackage` — fields: `name: String`, `version: String`, `license: String`, `advisory_count: u32`
- `RemovedPackage` — same fields as `AddedPackage`
- `VersionChange` — fields: `name: String`, `left_version: String`, `right_version: String`, `direction: String` (values: "upgrade" or "downgrade")
- `NewVulnerability` — fields: `advisory_id: String`, `severity: String`, `title: String`, `affected_package: String`
- `ResolvedVulnerability` — fields: `advisory_id: String`, `severity: String`, `title: String`, `previously_affected_package: String`
- `LicenseChange` — fields: `name: String`, `left_license: String`, `right_license: String`

Re-export from `modules/fundamental/src/sbom/model/mod.rs`.

### Comparison service
Implement in `modules/fundamental/src/sbom/service/comparison.rs`:
1. Fetch both SBOMs by ID using `SbomService::fetch()` (see `modules/fundamental/src/sbom/service/sbom.rs`)
2. For each SBOM, load associated packages via the `sbom_package` join table (see `entity/src/sbom_package.rs`) and their licenses via `package_license` (see `entity/src/package_license.rs`)
3. For each SBOM, load associated advisories via the `sbom_advisory` join table (see `entity/src/sbom_advisory.rs`)
4. Compute the diff:
   - Added packages: packages in right but not in left (match by package name)
   - Removed packages: packages in left but not in right
   - Version changes: packages in both but with different version strings; determine direction by comparing version strings (use semver parsing if available, otherwise lexicographic)
   - New vulnerabilities: advisories linked to right SBOM but not left SBOM
   - Resolved vulnerabilities: advisories linked to left SBOM but not right SBOM
   - License changes: packages in both SBOMs where the license field differs
5. Return `SbomComparisonResult`

### Endpoint handler
Implement in `modules/fundamental/src/sbom/endpoints/compare.rs`:
- Use Axum query parameter extraction for `left` and `right` (both required UUID/ID params)
- Return `Result<Json<SbomComparisonResult>, AppError>` following the error handling pattern in `common/src/error.rs`
- Return `400 Bad Request` if either parameter is missing
- Return `404 Not Found` if either SBOM does not exist
- Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` alongside existing routes

### Error handling
Follow the `Result<T, AppError>` pattern with `.context()` wrapping as used throughout the codebase (see `common/src/error.rs`).

### Performance
The comparison must meet p95 < 1s for SBOMs with up to 2000 packages each. Optimize database queries — fetch both SBOMs' packages in bulk rather than one-at-a-time. Consider using a single query per SBOM that joins package + license + advisory data.

### Relevant constraints
- Per constraints doc section 2 (Commit Rules): commits must reference TC-9003 in the footer, follow Conventional Commits format, and include the `Assisted-by: Claude Code` trailer.
- Per constraints doc section 3 (PR Rules): branch must be named after the Jira issue ID.
- Per constraints doc section 5 (Code Change Rules): changes must be scoped to listed files; inspect code before modifying; follow patterns referenced in implementation notes.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — existing service for fetching SBOMs by ID; reuse for loading left and right SBOMs
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — existing struct; reference its fields when building comparison model
- `modules/fundamental/src/sbom/model/details.rs::SbomDetails` — existing struct for detailed SBOM data
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — includes severity field; reference for vulnerability diff fields
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — includes license field; reference for package diff and license change fields
- `common/src/db/query.rs` — shared query builder helpers for filtering and pagination
- `common/src/model/paginated.rs::PaginatedResults` — reference for response wrapper patterns (comparison uses a flat struct, not paginated, but follow the serialization pattern)
- `entity/src/sbom_package.rs` — SBOM-Package join table entity; use for loading packages per SBOM
- `entity/src/sbom_advisory.rs` — SBOM-Advisory join table entity; use for loading advisories per SBOM
- `entity/src/package_license.rs` — Package-License mapping entity; use for loading license data

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/compare?left={id1}&right={id2}` returns 200 with a JSON body containing `added_packages`, `removed_packages`, `version_changes`, `new_vulnerabilities`, `resolved_vulnerabilities`, `license_changes` arrays
- [ ] Missing `left` or `right` query parameter returns 400 Bad Request
- [ ] Non-existent SBOM ID returns 404 Not Found
- [ ] Added packages correctly identifies packages in right SBOM but not in left
- [ ] Removed packages correctly identifies packages in left SBOM but not in right
- [ ] Version changes correctly identifies packages present in both SBOMs with different versions and reports upgrade/downgrade direction
- [ ] New vulnerabilities lists advisories affecting right SBOM but not left SBOM, including severity
- [ ] Resolved vulnerabilities lists advisories affecting left SBOM but not right SBOM
- [ ] License changes lists packages whose license differs between the two SBOMs
- [ ] No new database tables or migrations are introduced
- [ ] Endpoint response time is under 1 second (p95) for SBOMs with up to 2000 packages each

## Test Requirements
- [ ] Integration test: compare two SBOMs with known package differences — verify `added_packages` and `removed_packages` contain the correct entries
- [ ] Integration test: compare two SBOMs where a shared package has different versions — verify `version_changes` contains the correct entry with correct direction
- [ ] Integration test: compare two SBOMs with different advisory associations — verify `new_vulnerabilities` and `resolved_vulnerabilities` are correct
- [ ] Integration test: compare two SBOMs where a shared package has a different license — verify `license_changes` contains the correct entry
- [ ] Integration test: request with missing `left` parameter returns 400
- [ ] Integration test: request with non-existent SBOM ID returns 404
- [ ] Integration test: compare an SBOM with itself — all diff arrays should be empty
- [ ] Tests follow the existing test pattern in `tests/api/sbom.rs` using `assert_eq!(resp.status(), StatusCode::OK)`

## Dependencies
- None (this is the first task; frontend tasks depend on this)
