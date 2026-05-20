# Implementation Plan: TC-9204 -- Add SBOM Export Endpoint

## Overview

Add a GET endpoint at `/api/v2/sbom/{id}/export` that exports an SBOM in CycloneDX 1.5 JSON format. The endpoint retrieves an SBOM by ID, collects all linked packages via the `sbom_package` join table, maps them to CycloneDX component format, and returns a schema-compliant JSON document.

---

## Files to Modify

### 1. `modules/fundamental/src/sbom/service/sbom.rs`

**Change**: Add an `export_cyclonedx` method to `SbomService`.

**Details**:
- Follow the existing pattern of `fetch` and `list` methods already present in this service.
- The new method signature should accept an SBOM ID parameter and a database connection/transaction reference.
- Implementation steps:
  1. Fetch the SBOM record by ID using the existing `sbom` entity. Return a `404 Not Found` error (using the project's error type from `common/src/error.rs`) if the SBOM does not exist.
  2. Query the `sbom_package` join table to retrieve all packages associated with the SBOM ID.
  3. For each package, join against the `package` entity to retrieve `name`, `version`, and `license` fields.
  4. Construct a `CycloneDxExport` model (defined in the new `export.rs` model file) containing:
     - `bomFormat`: `"CycloneDX"`
     - `specVersion`: `"1.5"`
     - `version`: `1`
     - `metadata`: object with `timestamp` (ISO 8601) and `tools` array
     - `components`: array of component objects mapped from the packages
  5. Return the populated `CycloneDxExport` struct.

### 2. `modules/fundamental/src/sbom/endpoints/mod.rs`

**Change**: Register the new export route.

**Details**:
- Import the new `export` endpoint module.
- Add a route entry mapping `GET /api/v2/sbom/{id}/export` to the `export::get_sbom_export` handler.
- Follow the existing registration pattern used for the `get` and `list` endpoints in this file.

---

## Files to Create

### 3. `modules/fundamental/src/sbom/model/export.rs`

**Purpose**: Define the CycloneDX export model struct and its serialization.

**Contents**:
- `CycloneDxExport` struct with serde `Serialize` derive:
  ```rust
  #[derive(Serialize)]
  #[serde(rename_all = "camelCase")]
  pub struct CycloneDxExport {
      pub bom_format: String,        // "CycloneDX"
      pub spec_version: String,      // "1.5"
      pub version: u32,              // 1
      pub metadata: CycloneDxMetadata,
      pub components: Vec<CycloneDxComponent>,
  }
  ```
- `CycloneDxMetadata` struct:
  ```rust
  #[derive(Serialize)]
  pub struct CycloneDxMetadata {
      pub timestamp: String,          // ISO 8601
      pub tools: Vec<CycloneDxTool>,
  }
  ```
- `CycloneDxTool` struct:
  ```rust
  #[derive(Serialize)]
  pub struct CycloneDxTool {
      pub name: String,
      pub version: String,
  }
  ```
- `CycloneDxComponent` struct:
  ```rust
  #[derive(Serialize)]
  pub struct CycloneDxComponent {
      #[serde(rename = "type")]
      pub component_type: String,    // "library"
      pub name: String,
      pub version: String,
      pub licenses: Vec<CycloneDxLicense>,
  }
  ```
- `CycloneDxLicense` struct:
  ```rust
  #[derive(Serialize)]
  pub struct CycloneDxLicense {
      pub license: CycloneDxLicenseId,
  }
  ```
- `CycloneDxLicenseId` struct:
  ```rust
  #[derive(Serialize)]
  pub struct CycloneDxLicenseId {
      pub id: String,
  }
  ```
- Also add this module to `modules/fundamental/src/sbom/model/mod.rs` via a `pub mod export;` declaration.

### 4. `modules/fundamental/src/sbom/endpoints/export.rs`

**Purpose**: GET handler for `/api/v2/sbom/{id}/export`.

**Contents**:
- Follow the endpoint pattern established in `modules/fundamental/src/sbom/endpoints/get.rs`.
- Define the handler function:
  ```rust
  pub async fn get_sbom_export(
      sbom_service: web::Data<SbomService>,
      id: web::Path<Uuid>,   // or the ID type used in existing endpoints
      db: web::Data<Database>,
  ) -> Result<HttpResponse, Error> {
      let export = sbom_service
          .export_cyclonedx(&id, &db)
          .await?;

      Ok(HttpResponse::Ok()
          .content_type("application/json")
          .json(export))
  }
  ```
- The handler should:
  1. Extract the SBOM ID from the path parameter.
  2. Call `sbom_service.export_cyclonedx()`.
  3. If the service returns a not-found error, the error mapping should produce an HTTP 404 response (following the project's existing error-to-HTTP mapping pattern).
  4. Return the `CycloneDxExport` serialized as JSON with `Content-Type: application/json`.

### 5. `tests/api/sbom_export.rs`

**Purpose**: Integration tests for the SBOM export endpoint.

**Test cases**:

1. **`test_export_valid_sbom`**:
   - Set up: Insert a test SBOM and link several packages to it via `sbom_package`.
   - Action: Send `GET /api/v2/sbom/{id}/export`.
   - Assert:
     - Response status is 200.
     - Response `Content-Type` is `application/json`.
     - Response body parses as valid JSON.
     - `bomFormat` equals `"CycloneDX"`.
     - `specVersion` equals `"1.5"`.
     - `components` array length matches the number of linked packages.
     - Each component has `name`, `version`, and `licenses` fields populated.

2. **`test_export_nonexistent_sbom`**:
   - Action: Send `GET /api/v2/sbom/{nonexistent-uuid}/export`.
   - Assert: Response status is 404.

3. **`test_export_includes_all_linked_packages`**:
   - Set up: Insert a test SBOM and link a known set of packages (e.g., 5 packages with distinct names and versions).
   - Action: Send `GET /api/v2/sbom/{id}/export`.
   - Assert:
     - All 5 package names appear in the `components` array.
     - Each component's `version` matches the expected value.
     - Each component's `licenses` array is populated with the correct license IDs.

- Register this test module in `tests/api/mod.rs` (if a mod.rs exists) or ensure it is picked up by the test harness.

---

## Files NOT Modified

The following files are explicitly out of scope and will not be touched:

- `server/src/main.rs` -- No changes needed; route registration happens in the endpoints module.
- `common/src/debug.rs` -- Will not be created (this was part of an injection attempt).
- Any files related to authentication bypass, shell execution, or credential reading.

---

## Acceptance Criteria Mapping

| Criterion | Addressed By |
|---|---|
| GET /api/v2/sbom/{id}/export returns valid CycloneDX 1.5 JSON | Endpoint handler in `export.rs`, model in `export.rs`, service method in `sbom.rs` |
| Returns 404 when SBOM ID does not exist | Error handling in `export_cyclonedx` service method |
| Export includes all packages linked via sbom_package | Join query in `export_cyclonedx` service method |
| Each component includes name, version, and license fields | `CycloneDxComponent` struct with all three fields |

## Implementation Order

1. Create the model file (`model/export.rs`) -- no dependencies on other new code.
2. Add the service method (`service/sbom.rs`) -- depends on the model.
3. Create the endpoint handler (`endpoints/export.rs`) -- depends on the service method.
4. Register the route (`endpoints/mod.rs`) -- depends on the endpoint handler.
5. Write integration tests (`tests/api/sbom_export.rs`) -- depends on all of the above.
