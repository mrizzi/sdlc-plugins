# Task 1 — Backend: SBOM comparison diff model and service logic

## Repository
trustify-backend

## Description
Add the data model structs and service logic for computing a structured diff between two SBOMs. This is the core business logic that compares packages, advisories, and licenses between a "left" and "right" SBOM, producing a structured diff result. The comparison is computed on-the-fly from existing package, advisory, and license data — no new database tables are introduced.

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — re-export new comparison model types
- `modules/fundamental/src/sbom/service/sbom.rs` — add `compare` method to `SbomService`

## Files to Create
- `modules/fundamental/src/sbom/model/comparison.rs` — comparison diff model structs

## API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — NEW: returns structured diff (model defined in this task, endpoint wired in Task 2)

## Implementation Notes

### Model structs (`comparison.rs`)

Define the following Serde-serializable structs:

- `SbomComparisonDiff` — top-level response containing all diff sections:
  - `added_packages: Vec<PackageDiffEntry>`
  - `removed_packages: Vec<PackageDiffEntry>`
  - `version_changes: Vec<VersionChangeEntry>`
  - `new_vulnerabilities: Vec<VulnerabilityDiffEntry>`
  - `resolved_vulnerabilities: Vec<VulnerabilityDiffEntry>`
  - `license_changes: Vec<LicenseChangeEntry>`

- `PackageDiffEntry` — fields: `name: String`, `version: String`, `license: Option<String>`, `advisory_count: u32`
- `VersionChangeEntry` — fields: `name: String`, `left_version: String`, `right_version: String`, `direction: VersionDirection`
- `VersionDirection` — enum with variants `Upgrade`, `Downgrade` (serialize as lowercase strings)
- `VulnerabilityDiffEntry` — fields: `advisory_id: String`, `severity: String`, `title: String`, `affected_package: String`
- `LicenseChangeEntry` — fields: `name: String`, `left_license: String`, `right_license: String`

Follow the existing model patterns in `modules/fundamental/src/sbom/model/summary.rs` and `modules/fundamental/src/sbom/model/details.rs` for struct layout, derive macros, and Serde attributes.

### Service method (`sbom.rs`)

Add a `compare` method to `SbomService` with signature:
```rust
pub async fn compare(&self, left_id: Id, right_id: Id, db: &impl ConnectionTrait) -> Result<SbomComparisonDiff, AppError>
```

The method should:
1. Fetch package lists for both SBOMs via the `sbom_package` join table (entity in `entity/src/sbom_package.rs`)
2. Compute set differences for added/removed packages by comparing package names
3. For packages present in both SBOMs, compare versions and detect upgrades/downgrades
4. Fetch advisory associations for both SBOMs via `sbom_advisory` join table (entity in `entity/src/sbom_advisory.rs`)
5. Compute new/resolved vulnerabilities by comparing advisory sets, using `AdvisorySummary` severity field
6. Compare licenses for shared packages using `package_license` entity (entity in `entity/src/package_license.rs`)
7. Return error with `.context()` wrapping if either SBOM ID is not found (per `common/src/error.rs` `AppError` pattern)

### Performance requirement
The comparison must complete in p95 < 1s for SBOMs with up to 2000 packages each. Use efficient set operations (HashMaps keyed by package name) rather than nested loops.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — existing service struct to extend with the `compare` method
- `entity/src/sbom_package.rs` — SBOM-Package join table entity for querying packages per SBOM
- `entity/src/sbom_advisory.rs` — SBOM-Advisory join table entity for querying advisories per SBOM
- `entity/src/package_license.rs` — Package-License mapping entity for license lookups
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — includes `severity` field needed for vulnerability diff entries
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — includes `license` field for package data
- `common/src/error.rs::AppError` — error type with `IntoResponse` implementation

## Acceptance Criteria
- [ ] `SbomComparisonDiff` and related structs are defined with Serde serialization
- [ ] `SbomService::compare` correctly identifies added, removed, and version-changed packages
- [ ] `SbomService::compare` correctly identifies new and resolved vulnerabilities
- [ ] `SbomService::compare` correctly identifies license changes
- [ ] Returns appropriate `AppError` when either SBOM ID does not exist
- [ ] No new database tables or migrations are introduced — diff is computed from existing data

## Test Requirements
- [ ] Unit test: comparing two SBOMs with known package differences produces correct added/removed lists
- [ ] Unit test: packages with version changes are correctly classified as upgrade or downgrade
- [ ] Unit test: new and resolved vulnerabilities are correctly computed from advisory differences
- [ ] Unit test: license changes between shared packages are detected
- [ ] Unit test: comparing an SBOM with itself produces empty diff in all sections
- [ ] Unit test: requesting a comparison with a non-existent SBOM ID returns an error

## Dependencies
- None — this is the foundational task
