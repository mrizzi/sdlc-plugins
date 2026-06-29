## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Add the SBOM comparison model types and service logic that computes a structured diff between two SBOMs. This task introduces the data structures for the comparison result (added/removed packages, version changes, new/resolved vulnerabilities, license changes) and the service method that queries existing package, advisory, and license data to produce the diff on-the-fly without new database tables.

## Jira Metadata
- **Priority**: Critical
- **Fix Versions**: RHTPA 1.5.0

## Files to Create
- `modules/fundamental/src/sbom/model/comparison.rs` — Structs for the comparison response: `SbomComparison`, `AddedPackage`, `RemovedPackage`, `VersionChange`, `NewVulnerability`, `ResolvedVulnerability`, `LicenseChange`
- `modules/fundamental/src/sbom/service/compare.rs` — `SbomService::compare()` method that computes the diff between two SBOMs

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod comparison;` to expose the new model module
- `modules/fundamental/src/sbom/service/mod.rs` — Add `pub mod compare;` to expose the new service module

## API Changes
- None — this task adds internal service logic only; the endpoint is added in Task 3

## Implementation Notes
- Follow the existing module pattern in `modules/fundamental/src/sbom/`: model structs in `model/`, service logic in `service/`.
- The `SbomComparison` struct should derive `Serialize`, `Deserialize`, `Debug`, `Clone` as other model types do (see `modules/fundamental/src/sbom/model/summary.rs` for the pattern).
- The comparison service method should accept two SBOM IDs and a database connection, then:
  1. Use `PackageService` (`modules/fundamental/src/package/service/mod.rs`) to fetch packages for each SBOM via the `sbom_package` join table (`entity/src/sbom_package.rs`).
  2. Compute set differences for added/removed packages.
  3. Compare versions for packages present in both SBOMs to detect version changes and direction (upgrade/downgrade).
  4. Use `AdvisoryService` (`modules/fundamental/src/advisory/service/advisory.rs`) to fetch advisories for each SBOM via the `sbom_advisory` join table (`entity/src/sbom_advisory.rs`), then compute new/resolved vulnerabilities.
  5. Use `package_license` entity (`entity/src/package_license.rs`) to detect license changes.
- Return `Result<SbomComparison, AppError>` using the error type from `common/src/error.rs`.
- The response JSON shape must match the Figma design contract:
  ```json
  {
    "added_packages": [{ "name": "...", "version": "...", "license": "...", "advisory_count": 0 }],
    "removed_packages": [...],
    "version_changes": [{ "name": "...", "left_version": "...", "right_version": "...", "direction": "upgrade" }],
    "new_vulnerabilities": [{ "advisory_id": "...", "severity": "critical", "title": "...", "affected_package": "..." }],
    "resolved_vulnerabilities": [{ "advisory_id": "...", "severity": "...", "title": "...", "previously_affected_package": "..." }],
    "license_changes": [{ "name": "...", "left_license": "...", "right_license": "..." }]
  }
  ```
- Per CONVENTIONS.md §Error handling: all service methods return `Result<T, AppError>` with `.context()` wrapping. Applies: task creates `modules/fundamental/src/sbom/service/compare.rs` matching the convention's `.rs` service file scope.
- Per CONVENTIONS.md §Module pattern: each domain module follows `model/ + service/ + endpoints/` structure. Applies: task creates `modules/fundamental/src/sbom/model/comparison.rs` and `modules/fundamental/src/sbom/service/compare.rs` matching the convention's module structure scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — Reference for struct derive macros and serialization patterns
- `modules/fundamental/src/sbom/model/details.rs::SbomDetails` — Reference for detailed model structure
- `modules/fundamental/src/package/service/mod.rs::PackageService` — Fetch packages for an SBOM
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — Fetch advisories for an SBOM
- `common/src/error.rs::AppError` — Error type for service methods
- `entity/src/sbom_package.rs` — SBOM-Package join table for querying packages per SBOM
- `entity/src/sbom_advisory.rs` — SBOM-Advisory join table for querying advisories per SBOM
- `entity/src/package_license.rs` — Package-License mapping for detecting license changes

## Acceptance Criteria
- [ ] `SbomComparison` struct and all sub-structs are defined with proper serialization
- [ ] `SbomService::compare(left_id, right_id)` returns a correctly computed diff
- [ ] Added packages: packages in right SBOM but not in left
- [ ] Removed packages: packages in left SBOM but not in right
- [ ] Version changes: packages in both with different versions, including upgrade/downgrade direction
- [ ] New vulnerabilities: advisories affecting right SBOM but not left
- [ ] Resolved vulnerabilities: advisories affecting left SBOM but not right
- [ ] License changes: packages whose license differs between the two SBOMs
- [ ] No new database tables or migrations are introduced

## Test Requirements
- [ ] Unit test for `SbomService::compare()` with two SBOMs sharing some packages — verifies correct added/removed/changed categorization
- [ ] Unit test for version change direction detection (upgrade vs downgrade)
- [ ] Unit test for vulnerability diff (new and resolved)
- [ ] Unit test for license change detection
- [ ] Unit test for comparing an SBOM with itself — all diff sections should be empty
- [ ] Unit test for comparing SBOMs with no overlapping packages — all packages show as added/removed

## Dependencies
- Depends on: Task 1 — Create feature branch for trustify-backend

[sdlc-workflow] Description digest: sha256-md:193672f459621eb437d668d288ea31f00d363a2bfb1f776e3f94afaf76297771
