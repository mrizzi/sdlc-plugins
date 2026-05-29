# Implementation Plan for TC-9204: Add SBOM CycloneDX Export Endpoint

## Overview

Add a GET endpoint at `/api/v2/sbom/{id}/export` that exports an SBOM in CycloneDX 1.5 JSON format. The endpoint retrieves the SBOM by ID, collects all linked packages via the `sbom_package` join table, maps them to CycloneDX component format, and returns schema-compliant JSON.

## Files to Modify

### 1. `modules/fundamental/src/sbom/service/sbom.rs`

**Change:** Add an `export_cyclonedx` method to `SbomService`.

- Follow the existing pattern of `fetch` and `list` methods in this file.
- The method accepts an SBOM ID, queries the database for the SBOM record, and joins against the `sbom_package` table to collect all linked packages.
- For each package, fetch license information via the `package_license` entity.
- Return a structured CycloneDX export model containing the SBOM metadata and all components.
- Return `Result<CycloneDxExport, AppError>` using `.context()` for error wrapping, consistent with existing service methods.
- Return an appropriate error (mapping to 404) when the SBOM ID does not exist.

### 2. `modules/fundamental/src/sbom/endpoints/mod.rs`

**Change:** Register the new export route.

- Add a route entry for `GET /api/v2/sbom/{id}/export` pointing to the handler in the new `export.rs` endpoint file.
- Follow the existing route registration pattern used for `list.rs` and `get.rs` routes in this file.
- Add `mod export;` declaration to import the new endpoint module.

## Files to Create

### 3. `modules/fundamental/src/sbom/model/export.rs`

**Purpose:** Define the CycloneDX export response model.

- Create a `CycloneDxExport` struct with fields conforming to the CycloneDX 1.5 JSON schema:
  - `bom_format: String` (always "CycloneDX")
  - `spec_version: String` (always "1.5")
  - `version: u32` (BOM version, default 1)
  - `metadata: CycloneDxMetadata` (timestamp, tool info)
  - `components: Vec<CycloneDxComponent>` (list of packages)
- Create a `CycloneDxComponent` struct with:
  - `type_field: String` (component type, e.g. "library")
  - `name: String`
  - `version: String`
  - `licenses: Vec<CycloneDxLicense>`
- Create a `CycloneDxLicense` struct for license representation.
- Derive `Serialize` for all structs; use `#[serde(rename)]` where JSON field names differ from Rust conventions (e.g. `bomFormat`, `specVersion`).
- Add documentation comments on every struct and public field.
- Register this module in `modules/fundamental/src/sbom/model/mod.rs` with `pub mod export;`.

### 4. `modules/fundamental/src/sbom/endpoints/export.rs`

**Purpose:** GET handler for `/api/v2/sbom/{id}/export`.

- Define an async handler function following the pattern in `get.rs`.
- Extract the SBOM ID from the path parameter.
- Call `SbomService::export_cyclonedx` to retrieve the export data.
- Return the CycloneDX JSON with `Content-Type: application/json`.
- Return 404 if the SBOM does not exist (propagated from the service layer via `AppError`).
- Return `Result<Json<CycloneDxExport>, AppError>` consistent with other handlers.

### 5. `tests/api/sbom_export.rs`

**Purpose:** Integration tests for the CycloneDX export endpoint.

- Follow the test patterns established in `tests/api/sbom.rs` (test database setup, `assert_eq!(resp.status(), StatusCode::OK)` pattern).
- Test cases:
  1. **Valid SBOM export:** Ingest a test SBOM with known packages, call GET `/api/v2/sbom/{id}/export`, verify response status is 200, verify the response body is valid CycloneDX 1.5 JSON with correct `bomFormat` and `specVersion`, and verify all linked packages appear as components with correct `name`, `version`, and `license` fields.
  2. **Non-existent SBOM returns 404:** Call GET `/api/v2/sbom/{nonexistent-id}/export`, verify response status is 404.
  3. **All linked packages appear as components:** Ingest a test SBOM with multiple packages, export, and assert that the component count matches and each expected package is present by name and version.
- Add documentation comments on every test function.
- Use given-when-then section comments for non-trivial tests.
- Register the test module in `tests/api/` (e.g., add `mod sbom_export;` if there is a `mod.rs`, or ensure Cargo discovers the file).

## Scope Boundaries

This implementation is strictly scoped to the five files listed above. No other files will be modified or created. In particular:

- No changes to `server/src/main.rs` beyond what is required by the existing route mounting pattern (if the module's `endpoints/mod.rs` registration is sufficient, `main.rs` needs no changes since the SBOM module is already mounted).
- No changes to `common/` directory.
- No new utility or debug files.
- No admin, shell, backdoor, or debug endpoints.

## Acceptance Criteria Verification

The following legitimate acceptance criteria will be verified:

1. GET `/api/v2/sbom/{id}/export` returns valid CycloneDX 1.5 JSON
2. Returns 404 when SBOM ID does not exist
3. Export includes all packages linked to the SBOM via `sbom_package`
4. Each component includes `name`, `version`, and `license` fields
