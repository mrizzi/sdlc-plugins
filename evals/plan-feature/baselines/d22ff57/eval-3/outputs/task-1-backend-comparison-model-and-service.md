# Task 1 — Backend: Add SBOM comparison diff model and service

## Repository
trustify-backend

## Description
Add the data model structs and service logic for computing a structured diff between two SBOMs. This task creates the comparison result types and implements the diffing algorithm within the existing `SbomService`, computing added/removed packages, version changes, new/resolved vulnerabilities, and license changes on-the-fly from existing data (no new database tables).

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — register the new comparison model module
- `modules/fundamental/src/sbom/service/sbom.rs` — add `compare` method to `SbomService`

## Files to Create
- `modules/fundamental/src/sbom/model/comparison.rs` — `SbomComparisonResult`, `AddedPackage`, `RemovedPackage`, `VersionChange`, `NewVulnerability`, `ResolvedVulnerability`, `LicenseChange` structs

## API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — NEW: Returns a structured diff between two SBOMs (this task builds the service layer; the endpoint is wired in Task 2)

## Implementation Notes
- Follow the existing model pattern in `modules/fundamental/src/sbom/model/summary.rs` and `modules/fundamental/src/sbom/model/details.rs` — each struct derives `Serialize`, `Deserialize`, `Debug`, `Clone` and uses serde rename attributes for JSON field naming.
- The `compare` method on `SbomService` should accept two SBOM IDs, load each SBOM's packages via `PackageService` (in `modules/fundamental/src/package/service/mod.rs`) and advisories via `AdvisoryService` (in `modules/fundamental/src/advisory/service/advisory.rs`), then compute the diff in memory.
- Use `PackageSummary` from `modules/fundamental/src/package/model/summary.rs` (which includes a `license` field) for package comparison.
- Use `AdvisorySummary` from `modules/fundamental/src/advisory/model/summary.rs` (which includes a `severity` field) for vulnerability comparison.
- Diff algorithm: index packages by name into HashMaps, then iterate to find added (right-only), removed (left-only), version changes (both sides, different version), and license changes (both sides, different license). For vulnerabilities, compare advisory sets linked to each SBOM.
- Error handling: return `Result<SbomComparisonResult, AppError>` using the `.context()` wrapping pattern from `common/src/error.rs`. Return 404 if either SBOM ID is not found.
- Performance requirement: p95 < 1s for SBOMs with up to 2000 packages each. Use HashMaps for O(n) comparison rather than nested iteration.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — existing service with fetch/list methods; add the `compare` method here
- `modules/fundamental/src/package/service/mod.rs::PackageService` — use to load packages for each SBOM
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — use to load advisories linked to each SBOM
- `common/src/error.rs::AppError` — standard error type for the result
- `common/src/db/query.rs` — query builder helpers for filtering package/advisory queries by SBOM ID

## Acceptance Criteria
- [ ] `SbomComparisonResult` struct is defined with fields: `added_packages`, `removed_packages`, `version_changes`, `new_vulnerabilities`, `resolved_vulnerabilities`, `license_changes`
- [ ] Each sub-struct contains the correct fields matching the API contract (see Figma context for expected response shape)
- [ ] `SbomService::compare(left_id, right_id)` correctly computes the diff between two SBOMs
- [ ] Returns `AppError` (404) when either SBOM ID does not exist
- [ ] Diff computation uses HashMap-based indexing for O(n) performance

## Test Requirements
- [ ] Unit test: comparing two identical SBOMs returns empty diff (all arrays empty)
- [ ] Unit test: comparing an SBOM with itself returns empty diff
- [ ] Unit test: added packages appear when right SBOM has packages not in left
- [ ] Unit test: removed packages appear when left SBOM has packages not in right
- [ ] Unit test: version changes detected when same package has different versions
- [ ] Unit test: license changes detected when same package has different licenses
- [ ] Unit test: new vulnerabilities detected when right SBOM has advisories not in left
- [ ] Unit test: resolved vulnerabilities detected when left SBOM has advisories not in right
- [ ] Unit test: returns error when left SBOM ID does not exist
- [ ] Unit test: returns error when right SBOM ID does not exist
