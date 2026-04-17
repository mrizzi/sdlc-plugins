# Jira Tasks — TC-9004: Add License Compliance Report Endpoint

---

## Task 1 — Add license policy configuration and model types

## Repository
trustify-backend

## Description
Define the license compliance data model types (LicenseGroup, LicenseComplianceReport, LicensePolicy) and add support for loading a configurable license policy from a JSON file. The policy file specifies which licenses are allowed, denied, or flagged for review. This provides the foundation for the compliance report service in Task 2.

## Files to Create
- `modules/fundamental/src/license/mod.rs` — License module root, re-exports submodules
- `modules/fundamental/src/license/model/mod.rs` — Model submodule root
- `modules/fundamental/src/license/model/report.rs` — LicenseGroup and LicenseComplianceReport structs
- `modules/fundamental/src/license/model/policy.rs` — LicensePolicy struct and JSON deserialization logic
- `license-policy.json` — Default license policy configuration file at repository root

## Implementation Notes
- Follow the existing module pattern: each domain module has `model/ + service/ + endpoints/` structure (see `modules/fundamental/src/sbom/` for the canonical example)
- The `LicenseComplianceReport` struct should contain `groups: Vec<LicenseGroup>` where each `LicenseGroup` has `license: String`, `packages: Vec<PackageSummary>`, and `compliant: bool`
- The `LicensePolicy` should deserialize from JSON with fields like `allowed_licenses: Vec<String>`, `denied_licenses: Vec<String>` — a package is non-compliant if its license appears in `denied_licenses` or (if `allowed_licenses` is non-empty) does not appear in `allowed_licenses`
- Reuse the existing `PackageSummary` struct from `modules/fundamental/src/package/model/summary.rs` which already includes a `license` field
- Per CONVENTIONS.md Key Conventions: follow the `model/ + service/ + endpoints/` directory structure pattern. See `modules/fundamental/src/sbom/model/summary.rs` for the established struct pattern
- Per constraints.md section 2 (Commit Rules): commit messages must follow Conventional Commits, reference TC-9004 in the footer, and include the `Assisted-by: Claude Code` trailer
- Per constraints.md section 5 (Code Change Rules): do not modify files outside the scope of this task; inspect code before modifying it

## Reuse Candidates
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — already contains a `license` field; reuse as the package representation within license groups rather than creating a new struct
- `common/src/error.rs::AppError` — reuse for error handling in policy loading (e.g., file not found, invalid JSON)

## Acceptance Criteria
- [ ] LicenseGroup struct defined with fields: license (String), packages (Vec<PackageSummary>), compliant (bool)
- [ ] LicenseComplianceReport struct defined with field: groups (Vec<LicenseGroup>)
- [ ] LicensePolicy struct defined with allowed_licenses and denied_licenses fields
- [ ] LicensePolicy can be deserialized from a JSON file
- [ ] Default license-policy.json file exists at repository root with a reasonable default policy
- [ ] A policy evaluation function determines compliance for a given license string

## Test Requirements
- [ ] Unit test: LicensePolicy correctly identifies a denied license as non-compliant
- [ ] Unit test: LicensePolicy correctly identifies an allowed license as compliant
- [ ] Unit test: LicensePolicy with empty allowed_licenses list treats all non-denied licenses as compliant
- [ ] Unit test: LicensePolicy deserialization from valid JSON succeeds
- [ ] Unit test: LicensePolicy deserialization from invalid JSON returns appropriate error

## Documentation Updates
- `README.md` — Add section describing license policy configuration format and location

---

## Task 2 — Add license compliance report service with transitive dependency resolution

## Repository
trustify-backend

## Description
Implement the LicenseReportService that generates a license compliance report for a given SBOM. The service fetches all packages associated with the SBOM (including transitive dependencies by walking the full dependency tree via sbom_package relationships), groups them by license type, evaluates each group against the configured license policy, and returns a LicenseComplianceReport.

## Files to Create
- `modules/fundamental/src/license/service/mod.rs` — LicenseReportService with the generate_report method

## Files to Modify
- `modules/fundamental/src/license/mod.rs` — Register the service submodule
- `modules/fundamental/src/lib.rs` — Register the license module

## Implementation Notes
- Follow the service pattern established in `modules/fundamental/src/sbom/service/sbom.rs` — the SbomService shows how to accept a database connection and entity ID, query related entities, and return a structured result
- Use SeaORM to query the `sbom_package` join table (`entity/src/sbom_package.rs`) to get all packages for an SBOM, then join to `package_license` (`entity/src/package_license.rs`) to get license data
- For transitive dependency resolution: walk the `sbom_package` relationship table which links SBOMs to all their packages (including transitives captured during ingestion). The SBOM ingestion process (`modules/ingestor/src/graph/sbom/mod.rs`) already parses and stores the full dependency tree
- Group packages by their license string, then evaluate each group against the LicensePolicy loaded from the JSON config
- Use `common/src/db/query.rs` query helpers for database operations where applicable
- Return `Result<LicenseComplianceReport, AppError>` following the error handling pattern with `.context()` wrapping (see `common/src/error.rs`)
- Per CONVENTIONS.md Key Conventions: all service methods return `Result<T, AppError>` with `.context()` wrapping
- Performance target from NFRs: p95 < 500ms for SBOMs with up to 1000 packages — use efficient batch queries rather than N+1 patterns

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — reference for service structure, database connection handling, and query patterns
- `modules/fundamental/src/package/service/mod.rs::PackageService` — reference for package-related queries
- `entity/src/sbom_package.rs` — existing SBOM-Package join entity for dependency resolution
- `entity/src/package_license.rs` — existing Package-License mapping entity
- `common/src/db/query.rs` — shared query builder helpers for filtering and pagination

## Acceptance Criteria
- [ ] LicenseReportService.generate_report(sbom_id) returns a LicenseComplianceReport
- [ ] Report groups all packages by license type
- [ ] Transitive dependency licenses are included (full dependency tree)
- [ ] Each license group has a correct compliant flag based on the configured policy
- [ ] Non-existent SBOM ID returns an appropriate error
- [ ] No new database tables are created (aggregates from existing data per NFR)

## Test Requirements
- [ ] Unit test: service correctly groups packages by license type
- [ ] Unit test: service marks denied licenses as non-compliant
- [ ] Unit test: service includes transitive dependency packages
- [ ] Unit test: service returns error for non-existent SBOM ID
- [ ] Unit test: service handles SBOM with no packages (empty report)

## Verification Commands
- `cargo test --package fundamental -- license` — all license service tests pass

## Dependencies
- Depends on: Task 1 — Add license policy configuration and model types

---

## Task 3 — Add GET /api/v2/sbom/{id}/license-report endpoint

## Repository
trustify-backend

## Description
Add the REST endpoint `GET /api/v2/sbom/{id}/license-report` that calls the LicenseReportService to generate a compliance report for the specified SBOM and returns it as JSON. Register the route in the SBOM endpoint module and mount it in the server.

## Files to Create
- `modules/fundamental/src/license/endpoints/mod.rs` — Route registration for the license report endpoint
- `modules/fundamental/src/license/endpoints/report.rs` — GET handler for `/api/v2/sbom/{id}/license-report`

## Files to Modify
- `modules/fundamental/src/license/mod.rs` — Register the endpoints submodule
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Mount the license-report sub-route under the SBOM route namespace, or alternatively register in `server/src/main.rs`
- `server/src/main.rs` — Mount the license report routes if not nested under SBOM routes

## API Changes
- `GET /api/v2/sbom/{id}/license-report` — NEW: Returns a LicenseComplianceReport JSON object with structure `{ groups: [{ license: "MIT", packages: [...], compliant: true }] }`

## Implementation Notes
- Follow the endpoint pattern in `modules/fundamental/src/sbom/endpoints/get.rs` — shows how to extract a path parameter (SBOM ID), call a service, and return a JSON response
- Route registration follows the pattern in `modules/fundamental/src/sbom/endpoints/mod.rs` — each endpoint module has a `configure` or router function that registers routes
- The handler should extract the SBOM ID from the path, call `LicenseReportService::generate_report(sbom_id)`, and return the result serialized as JSON
- Error handling: return `AppError` for not-found or internal errors, matching the pattern in `common/src/error.rs`
- Per CONVENTIONS.md Key Conventions: endpoint registration goes in `endpoints/mod.rs`; server mounting goes in `server/src/main.rs`
- Per CONVENTIONS.md Key Conventions: all handlers return `Result<T, AppError>` with `.context()` wrapping

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — canonical example of a GET endpoint with path parameter extraction
- `modules/fundamental/src/sbom/endpoints/mod.rs` — route registration pattern
- `common/src/error.rs::AppError` — error type for handler error responses

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/license-report` returns 200 with a valid LicenseComplianceReport JSON body
- [ ] Response JSON structure matches `{ groups: [{ license: string, packages: [...], compliant: boolean }] }`
- [ ] Returns appropriate error (404) for non-existent SBOM ID
- [ ] Endpoint is accessible via the mounted route configuration

## Test Requirements
- [ ] Integration test: GET request returns 200 with correct report structure for an SBOM with known packages and licenses
- [ ] Integration test: GET request returns 404 for non-existent SBOM ID
- [ ] Integration test: report correctly flags non-compliant licenses based on configured policy
- [ ] Integration test: report includes transitive dependency packages

## Verification Commands
- `cargo test --package fundamental -- license::endpoints` — endpoint tests pass
- `curl http://localhost:8080/api/v2/sbom/{id}/license-report` — returns valid JSON response (manual verification)

## Documentation Updates
- `README.md` — Document the new endpoint path, HTTP method, request parameters, and response schema

## Dependencies
- Depends on: Task 2 — Add license compliance report service with transitive dependency resolution

---

## Task 4 — Add integration tests for the license compliance report endpoint

## Repository
trustify-backend

## Description
Add comprehensive integration tests for the license compliance report endpoint. Tests should cover the full request lifecycle: setting up test data (SBOM with packages and licenses), calling the endpoint, and verifying the response structure and compliance logic. Follow the existing integration test patterns in `tests/api/`.

## Files to Create
- `tests/api/license_report.rs` — Integration tests for the license report endpoint

## Files to Modify
- `tests/Cargo.toml` — Add any necessary test dependencies if not already present

## Implementation Notes
- Follow the integration test pattern in `tests/api/sbom.rs` — shows how to set up a test database, create test data, make HTTP requests to endpoints, and assert on response status and body
- Use `assert_eq!(resp.status(), StatusCode::OK)` pattern per CONVENTIONS.md Key Conventions
- Test scenarios should include:
  - SBOM with all compliant licenses (all groups have `compliant: true`)
  - SBOM with some non-compliant licenses (mixed report)
  - SBOM with only non-compliant licenses
  - SBOM with transitive dependencies contributing additional licenses
  - Empty SBOM (no packages) returning an empty groups array
  - Non-existent SBOM returning 404
- Set up test license policy data that matches the test scenarios
- Per constraints.md section 5.9-5.10: prefer parameterized tests if sibling tests use them; check `tests/api/sbom.rs` for existing patterns first
- Per constraints.md section 5.11: add a doc comment to every test function
- Per constraints.md section 5.12-5.13: add given-when-then inline comments to non-trivial test functions

## Reuse Candidates
- `tests/api/sbom.rs` — integration test structure, test database setup, HTTP request helpers
- `tests/api/advisory.rs` — additional reference for integration test patterns

## Acceptance Criteria
- [ ] Integration tests cover compliant, non-compliant, mixed, empty, and not-found scenarios
- [ ] All tests pass against a PostgreSQL test database
- [ ] Tests follow existing integration test patterns in the repository
- [ ] Every test function has a doc comment
- [ ] Non-trivial test functions have given-when-then inline comments

## Test Requirements
- [ ] Test: SBOM with all MIT-licensed packages returns all groups as compliant
- [ ] Test: SBOM with a denied license returns that group as non-compliant
- [ ] Test: SBOM with no packages returns empty groups array
- [ ] Test: Non-existent SBOM ID returns 404 status
- [ ] Test: Transitive dependencies appear in the license report
- [ ] Test: Mixed scenario with some compliant and some non-compliant licenses

## Verification Commands
- `cargo test --test api -- license_report` — all integration tests pass

## Dependencies
- Depends on: Task 3 — Add GET /api/v2/sbom/{id}/license-report endpoint
