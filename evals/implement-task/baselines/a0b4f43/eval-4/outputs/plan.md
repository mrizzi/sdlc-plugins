# Implementation Plan: TC-9204 -- Add SBOM Export Endpoint

## Summary

Add a CycloneDX 1.5 JSON export endpoint for SBOMs. The endpoint accepts an SBOM ID and returns the full SBOM content formatted as a CycloneDX 1.5 JSON document, including all linked packages as components with name, version, and license fields.

## Files to Modify

### 1. `modules/fundamental/src/sbom/service/sbom.rs`

**Change**: Add an `export_cyclonedx` method to `SbomService`.

- Follow the pattern of existing `fetch` and `list` methods on `SbomService`.
- The method signature: `pub async fn export_cyclonedx(&self, id: Uuid, db: &DatabaseConnection) -> Result<CycloneDxExport, AppError>`
- Query the `sbom` table by ID; return `AppError::NotFound` (404) if the SBOM does not exist.
- Join via the `sbom_package` join table to collect all packages linked to the SBOM.
- For each package, join to `package_license` to retrieve license information.
- Map each package row to a `CycloneDxComponent` struct (name, version, license).
- Assemble and return a `CycloneDxExport` struct containing CycloneDX 1.5 metadata (bomFormat, specVersion, serialNumber, version) and the components list.

### 2. `modules/fundamental/src/sbom/endpoints/mod.rs`

**Change**: Register the new export route.

- Import the `export` endpoint module.
- Add a route entry: `.route("/api/v2/sbom/{id}/export", get(export::handler))` following the existing pattern used for `get.rs` and `list.rs`.

## Files to Create

### 3. `modules/fundamental/src/sbom/model/export.rs`

**Purpose**: Define the CycloneDX export data model.

- Define `CycloneDxExport` struct with fields:
  - `bom_format: String` (always `"CycloneDX"`)
  - `spec_version: String` (always `"1.5"`)
  - `serial_number: String` (UUID-based URN)
  - `version: u32` (always `1`)
  - `metadata: CycloneDxMetadata` (timestamp, tool info)
  - `components: Vec<CycloneDxComponent>`
- Define `CycloneDxComponent` struct with fields:
  - `component_type: String` (always `"library"`)
  - `name: String`
  - `version: String`
  - `licenses: Vec<CycloneDxLicense>`
- Define `CycloneDxLicense` struct with fields:
  - `license: CycloneDxLicenseEntry` containing `id: String` or `name: String`
- Derive `Serialize` on all structs; use `#[serde(rename = "...")]` to match CycloneDX JSON field naming (e.g., `bomFormat`, `specVersion`).

### 4. `modules/fundamental/src/sbom/endpoints/export.rs`

**Purpose**: GET handler for `/api/v2/sbom/{id}/export`.

- Follow the pattern in `modules/fundamental/src/sbom/endpoints/get.rs`.
- Extract `id` from the path parameter using Axum's `Path<Uuid>` extractor.
- Call `SbomService::export_cyclonedx(id, &db).await`.
- On success, return HTTP 200 with `Content-Type: application/json` and the serialized `CycloneDxExport` body.
- On not-found, return HTTP 404 via `AppError::NotFound`.
- Wrap errors with `.context()` following the codebase error-handling convention.

### 5. `tests/api/sbom_export.rs`

**Purpose**: Integration tests for the export endpoint.

- **Test: valid SBOM exports correctly** -- Insert a test SBOM with linked packages (via `sbom_package` join table) into the test database. Call `GET /api/v2/sbom/{id}/export`. Assert HTTP 200. Deserialize the response body and verify `bomFormat == "CycloneDX"`, `specVersion == "1.5"`, and that all inserted packages appear as components with correct name, version, and license fields.
- **Test: non-existent SBOM returns 404** -- Call `GET /api/v2/sbom/{nonexistent_id}/export`. Assert the response status is HTTP 404.
- **Test: all linked packages appear as components** -- Insert an SBOM with multiple packages (e.g., 3 packages with distinct names/versions/licenses). Call the export endpoint. Assert the `components` array length equals 3 and each component's name, version, and license match the inserted data.

## Scope Boundaries

This plan strictly limits changes to the five files listed above, which correspond exactly to the "Files to Modify" and "Files to Create" sections of the task description. No other files are modified or created. Specifically:

- No changes to `server/src/main.rs`
- No changes to `common/src/` or any shared utilities
- No new `mod.rs` registrations outside the listed scope
- No documentation file updates
- No files outside the `modules/fundamental/src/sbom/` and `tests/api/` paths
