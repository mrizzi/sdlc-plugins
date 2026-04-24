## Repository
trustify-backend

## Description
Create the SBOM comparison model structs and diff computation service that compares two SBOMs and produces a structured diff containing added packages, removed packages, version changes, new vulnerabilities, resolved vulnerabilities, and license changes. This is the core business logic for the SBOM comparison feature (TC-9003). The service computes diffs on-the-fly from existing entity data without requiring new database tables. This task does not include the HTTP endpoint (handled in Task 2).

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod comparison;` to expose the new comparison model module
- `modules/fundamental/src/sbom/service/mod.rs` — Add `pub mod compare;` to expose the new comparison service module

## Files to Create
- `modules/fundamental/src/sbom/model/comparison.rs` — Structs for the comparison response: `SbomComparison`, `AddedPackage`, `RemovedPackage`, `VersionChange`, `NewVulnerability`, `ResolvedVulnerability`, `LicenseChange`
- `modules/fundamental/src/sbom/service/compare.rs` — Implements `SbomService::compare(left_id, right_id, db)` method that computes the structured diff between two SBOMs

## API Changes
- No HTTP API changes in this task — the model and service are internal. The endpoint is created in Task 2.

## Implementation Notes
- Follow the existing model pattern in `modules/fundamental/src/sbom/model/summary.rs` and `modules/fundamental/src/sbom/model/details.rs` — each struct should derive `Serialize`, `Deserialize`, `Debug`, `Clone` and use `utoipa::ToSchema` for OpenAPI generation.
- The `SbomComparison` struct must contain six `Vec` fields matching the API response shape from the feature spec: `added_packages: Vec<AddedPackage>`, `removed_packages: Vec<RemovedPackage>`, `version_changes: Vec<VersionChange>`, `new_vulnerabilities: Vec<NewVulnerability>`, `resolved_vulnerabilities: Vec<ResolvedVulnerability>`, `license_changes: Vec<LicenseChange>`.
- The comparison service method should follow the pattern in `modules/fundamental/src/sbom/service/sbom.rs` where `SbomService` methods accept a database connection and return `Result<T, AppError>`.
- Use the `PackageSummary` struct from `modules/fundamental/src/package/model/summary.rs` to access the `license` field on packages.
- Use the `AdvisorySummary` struct from `modules/fundamental/src/advisory/model/summary.rs` to access the `severity` field for vulnerability entries.
- Query packages for each SBOM via the `sbom_package` join entity in `entity/src/sbom_package.rs`, then compute set differences (by package name) for added/removed packages.
- Query advisories for each SBOM via the `sbom_advisory` join entity in `entity/src/sbom_advisory.rs`, then compute set differences for new/resolved vulnerabilities.
- Query license data from the `package_license` entity in `entity/src/package_license.rs` and compare across the two SBOMs for license changes.
- For version changes, find packages present in both SBOMs (matched by package name) with differing versions; set `direction` to `"upgrade"` or `"downgrade"` based on version comparison.
- Use `AppError` from `common/src/error.rs` with `.context()` wrapping for all fallible operations.
- No new database tables or migrations are needed — all data is computed on-the-fly from existing entities.
- Per the non-functional requirement, the comparison must handle SBOMs with up to 2000 packages each with p95 < 1s response time. Use efficient SQL queries (batch fetch packages/advisories per SBOM in two queries each) rather than N+1 queries.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — Existing service struct to extend with the `compare` method
- `modules/fundamental/src/package/service/mod.rs::PackageService` — Can be used to fetch package lists for each SBOM
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — Can be used to fetch advisories associated with each SBOM
- `entity/src/sbom_package.rs` — SBOM-Package join table entity for querying packages per SBOM
- `entity/src/sbom_advisory.rs` — SBOM-Advisory join table entity for querying advisories per SBOM
- `entity/src/package_license.rs` — Package-License mapping entity for license comparison
- `common/src/error.rs::AppError` — Standard error type for Result returns
- `common/src/db/query.rs` — Shared query builder helpers for filtering and pagination

## Acceptance Criteria
- [ ] `SbomComparison` struct is defined with all six diff sections matching the API contract from the feature spec
- [ ] Each sub-struct (`AddedPackage`, `RemovedPackage`, `VersionChange`, `NewVulnerability`, `ResolvedVulnerability`, `LicenseChange`) has fields matching the expected JSON response shape
- [ ] `SbomService::compare(left_id, right_id, db)` returns a correctly populated `SbomComparison` when given two valid SBOM IDs
- [ ] Added packages are those present in the right SBOM but absent from the left
- [ ] Removed packages are those present in the left SBOM but absent from the right
- [ ] Version changes identify packages in both SBOMs with differing versions and correctly determine upgrade vs. downgrade direction
- [ ] New vulnerabilities are advisories affecting the right SBOM but not the left
- [ ] Resolved vulnerabilities are advisories affecting the left SBOM but not the right
- [ ] License changes identify packages whose license differs between the two SBOMs
- [ ] Returns appropriate `AppError` when either SBOM ID is not found

## Test Requirements
- [ ] Unit test: `compare` returns empty diff when both SBOM IDs reference the same SBOM
- [ ] Unit test: `compare` correctly identifies added and removed packages when packages differ between SBOMs
- [ ] Unit test: `compare` correctly identifies version changes with upgrade/downgrade direction
- [ ] Unit test: `compare` returns `AppError::NotFound` when a non-existent SBOM ID is provided
- [ ] Unit test: `compare` correctly identifies new and resolved vulnerabilities
- [ ] Unit test: `compare` correctly identifies license changes between SBOMs

## Dependencies
- None — this is the foundational task for the backend comparison feature
