# Implementation Plan: TC-9204 - Add SBOM Export Endpoint

## Overview

Add a GET endpoint at `/api/v2/sbom/{id}/export` that exports an SBOM in CycloneDX 1.5 JSON format. The endpoint takes an SBOM ID, retrieves the SBOM and its linked packages via the `sbom_package` join table, and returns a CycloneDX-compliant JSON document.

## Repository

trustify-backend (Rust, Axum + SeaORM)

## Target Branch

main

## Files to Modify

### 1. `modules/fundamental/src/sbom/service/sbom.rs`

**What to change:** Add an `export_cyclonedx` method to `SbomService`.

**Details:**
- Follow the pattern of existing `fetch` and `list` methods in the same file.
- The method signature should be:
  ```rust
  /// Exports an SBOM in CycloneDX 1.5 JSON format.
  pub async fn export_cyclonedx(&self, id: Uuid, db: &DatabaseConnection) -> Result<CycloneDxExport, AppError>
  ```
- Implementation steps:
  1. Fetch the SBOM by ID using the existing `fetch` pattern. Return 404 (`AppError::NotFound`) if the SBOM does not exist.
  2. Query the `sbom_package` join table to retrieve all packages linked to this SBOM.
  3. For each package, retrieve its license information via the `package_license` entity.
  4. Map each package to a CycloneDX `Component` with `name`, `version`, and `license` fields.
  5. Construct and return a `CycloneDxExport` struct containing the BOM metadata and components list.
- Use `.context()` for error wrapping, consistent with the codebase's error handling convention.

### 2. `modules/fundamental/src/sbom/endpoints/mod.rs`

**What to change:** Register the new export route.

**Details:**
- Add a route entry for `GET /api/v2/sbom/{id}/export` pointing to the export handler.
- Follow the same registration pattern used for the existing `get.rs` handler (GET `/api/v2/sbom/{id}`).
- Add `mod export;` to bring the new endpoint module into scope.

## Files to Create

### 3. `modules/fundamental/src/sbom/model/export.rs`

**Purpose:** Define the CycloneDX export model structs.

**Details:**
- Define `CycloneDxExport` struct with fields:
  - `bom_format: String` (always "CycloneDX")
  - `spec_version: String` (always "1.5")
  - `version: i32` (BOM version, default 1)
  - `serial_number: String` (UUID-based URN)
  - `metadata: CycloneDxMetadata` (timestamp, tool info)
  - `components: Vec<CycloneDxComponent>`
- Define `CycloneDxComponent` struct with fields:
  - `type_field: String` (serialized as "type", always "library")
  - `name: String`
  - `version: String`
  - `licenses: Vec<CycloneDxLicense>`
- Define `CycloneDxLicense` struct with fields:
  - `license: CycloneDxLicenseEntry` (containing `id` or `name`)
- Define `CycloneDxMetadata` struct with timestamp and tool fields.
- All structs derive `Serialize` (serde) for JSON output.
- Add doc comments on every struct and public field.
- Register this module in `modules/fundamental/src/sbom/model/mod.rs` with `pub mod export;`.

### 4. `modules/fundamental/src/sbom/endpoints/export.rs`

**Purpose:** GET handler for `/api/v2/sbom/{id}/export`.

**Details:**
- Follow the pattern in `modules/fundamental/src/sbom/endpoints/get.rs`.
- Handler signature:
  ```rust
  /// Exports an SBOM as a CycloneDX 1.5 JSON document.
  pub async fn export_sbom(
      Path(id): Path<Uuid>,
      State(service): State<SbomService>,
      db: DatabaseConnection,
  ) -> Result<Json<CycloneDxExport>, AppError>
  ```
- Implementation:
  1. Call `service.export_cyclonedx(id, &db).await`.
  2. On success, return `Json(export)` with `Content-Type: application/json`.
  3. On error (SBOM not found), let the `AppError` propagate (returns 404 automatically via `IntoResponse`).
- Use `Result<T, AppError>` with `.context()` wrapping for error handling, consistent with sibling handlers.

### 5. `tests/api/sbom_export.rs`

**Purpose:** Integration tests for the export endpoint.

**Details:**
- Follow the test conventions in `tests/api/sbom.rs` (assertion style, setup, naming).
- Test functions:

  ```rust
  /// Verifies that a valid SBOM exports correctly in CycloneDX 1.5 JSON format.
  #[tokio::test]
  async fn test_export_sbom_valid() {
      // Given an SBOM with linked packages in the test database
      // When requesting GET /api/v2/sbom/{id}/export
      // Then the response status is 200
      // And the response body contains valid CycloneDX JSON with bomFormat, specVersion, components
      // And all linked packages appear as components with name, version, and license fields
  }

  /// Verifies that exporting a non-existent SBOM returns 404.
  #[tokio::test]
  async fn test_export_sbom_not_found() {
      // Given a non-existent SBOM ID
      // When requesting GET /api/v2/sbom/{non_existent_id}/export
      // Then the response status is 404
  }

  /// Verifies that all packages linked via sbom_package appear as components in the export.
  #[tokio::test]
  async fn test_export_sbom_includes_all_packages() {
      // Given an SBOM with multiple linked packages
      // When requesting GET /api/v2/sbom/{id}/export
      // Then components list contains an entry for each linked package
      // And each component has name, version, and license fields with correct values
  }
  ```

- Register this test file in `tests/Cargo.toml` if needed, following the pattern for existing test files.
- Use `assert_eq!(resp.status(), StatusCode::OK)` and `assert_eq!(resp.status(), StatusCode::NOT_FOUND)` patterns consistent with sibling tests.
- Assert on actual field values, not just collection length.

## Module Registration

- Add `pub mod export;` to `modules/fundamental/src/sbom/model/mod.rs`
- The endpoint module is already registered via `mod export;` in `modules/fundamental/src/sbom/endpoints/mod.rs` (covered in File 2 above)

## Acceptance Criteria Verification

| Criterion | How Verified |
|---|---|
| GET /api/v2/sbom/{id}/export returns valid CycloneDX 1.5 JSON | `test_export_sbom_valid` asserts bomFormat="CycloneDX", specVersion="1.5", and component structure |
| Returns 404 when SBOM ID does not exist | `test_export_sbom_not_found` asserts 404 status |
| Export includes all packages linked via sbom_package | `test_export_sbom_includes_all_packages` asserts component count and values match linked packages |
| Each component includes name, version, and license fields | All test cases verify these fields are present and correct |

## Data-Flow Trace

- `GET /api/v2/sbom/{id}/export` -> `export_sbom` handler (parse path param) -> `SbomService::export_cyclonedx` (fetch SBOM, query packages, map to CycloneDX) -> JSON response -- COMPLETE

## Notes

- No changes to `server/src/main.rs` are needed -- the sbom module's `endpoints/mod.rs` handles route registration, which is already mounted by the server.
- No changes to `common/` are needed -- existing error types and model patterns are sufficient.
- No new dependencies should be required; serde serialization is already available in the project.
