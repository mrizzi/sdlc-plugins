## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Add model types to represent SBOM comparison results and implement the diff computation service that compares two SBOMs to identify added/removed packages, version changes, new/resolved vulnerabilities, and license changes. This service computes diffs on-the-fly from existing package and advisory data without requiring new database tables.

## Files to Create
- `modules/fundamental/src/sbom/model/comparison.rs` — Structs for comparison result: SbomComparisonResult, AddedPackage, RemovedPackage, VersionChange, NewVulnerability, ResolvedVulnerability, LicenseChange
- `modules/fundamental/src/sbom/service/comparison.rs` — Comparison service logic: load two SBOMs by ID, diff their package lists, correlate advisory impacts, detect license changes

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — Export the new comparison module
- `modules/fundamental/src/sbom/service/mod.rs` — Export the new comparison service module

## Implementation Notes
- Follow the existing model pattern in `modules/fundamental/src/sbom/model/summary.rs` (SbomSummary) and `modules/fundamental/src/sbom/model/details.rs` (SbomDetails) for struct definitions with serde Serialize/Deserialize derives.
- Follow the existing service pattern in `modules/fundamental/src/sbom/service/sbom.rs` (SbomService) for database query logic and error handling.
- Use SeaORM queries to fetch package lists for both SBOMs via the `sbom_package` join table (`entity/sbom_package.rs`).
- For vulnerability diff, query the `sbom_advisory` join table (`entity/sbom_advisory.rs`) to find advisories associated with each SBOM, then compute the set difference.
- For license changes, use the `package_license` entity (`entity/package_license.rs`) to compare license mappings between the two SBOMs.
- The `direction` field for version changes should be "upgrade" or "downgrade" based on version string comparison (use semver parsing if available, otherwise lexicographic).
- Use existing query helpers from `common/src/db/query.rs` for any filtering or pagination needs.
- Return errors using `AppError` from `common/src/error.rs` with `.context()` wrapping per the project's error handling convention.
- All handler return types must use `Result<T, AppError>` — per the backend key conventions (Framework: Axum for HTTP, SeaORM for database; Error handling: All handlers return `Result<T, AppError>` with `.context()` wrapping).
  Applies: task creates `modules/fundamental/src/sbom/service/comparison.rs` matching the convention's `.rs` service file scope.
- Per the backend key conventions (Module pattern): each domain module follows `model/ + service/ + endpoints/` structure. This task adds model and service sub-modules under the existing `sbom/` module.
  Applies: task creates `modules/fundamental/src/sbom/model/comparison.rs` and `modules/fundamental/src/sbom/service/comparison.rs` matching the convention's Rust module structure scope.
- The comparison result JSON shape must match the frontend contract specified in the feature description:
  ```json
  {
    "added_packages": [{ "name": "...", "version": "...", "license": "...", "advisory_count": 0 }],
    "removed_packages": [{ "name": "...", "version": "...", "license": "...", "advisory_count": 0 }],
    "version_changes": [{ "name": "...", "left_version": "...", "right_version": "...", "direction": "upgrade" }],
    "new_vulnerabilities": [{ "advisory_id": "...", "severity": "critical", "title": "...", "affected_package": "..." }],
    "resolved_vulnerabilities": [{ "advisory_id": "...", "severity": "...", "title": "...", "previously_affected_package": "..." }],
    "license_changes": [{ "name": "...", "left_license": "...", "right_license": "..." }]
  }
  ```
- Non-functional requirement: the diff computation must complete within p95 < 1s for SBOMs with up to 2000 packages each. Optimize queries accordingly (batch-load packages rather than N+1 queries).

## Reuse Candidates
- `common/src/db/query.rs` — shared query builder helpers (filtering, pagination, sorting) for constructing efficient queries
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — existing SBOM fetch logic to reuse for loading SBOM data by ID
- `entity/sbom_package.rs` — SBOM-Package join table entity for querying packages belonging to an SBOM
- `entity/sbom_advisory.rs` — SBOM-Advisory join table entity for querying advisories associated with an SBOM
- `entity/package_license.rs` — Package-License mapping entity for querying license data
- `common/src/model/paginated.rs::PaginatedResults` — response wrapper pattern (reference for struct design, though comparison results are not paginated)

## Acceptance Criteria
- [ ] SbomComparisonResult struct serializes to JSON matching the expected response shape
- [ ] Comparison service correctly identifies packages added in the right SBOM but absent from the left
- [ ] Comparison service correctly identifies packages removed (present in left, absent in right)
- [ ] Comparison service correctly identifies packages with version changes and classifies direction as upgrade or downgrade
- [ ] Comparison service correctly identifies new vulnerabilities (advisories affecting right SBOM but not left)
- [ ] Comparison service correctly identifies resolved vulnerabilities (advisories affecting left SBOM but not right)
- [ ] Comparison service correctly identifies license changes between the two SBOMs
- [ ] Service returns AppError with appropriate status for invalid or non-existent SBOM IDs

## Test Requirements
- [ ] Unit test for diff logic with known, controlled package lists verifying all six diff categories
- [ ] Unit test for empty diff result when comparing identical SBOMs
- [ ] Unit test for error case when a non-existent SBOM ID is provided
- [ ] Unit test for version change direction classification (upgrade vs downgrade)

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
