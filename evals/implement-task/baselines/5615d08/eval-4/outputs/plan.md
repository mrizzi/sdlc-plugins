# Implementation Plan: TC-9204 — Add SBOM export endpoint

## Overview

Add a GET `/api/v2/sbom/{id}/export` endpoint that exports an SBOM in CycloneDX 1.5 JSON format. The endpoint retrieves the SBOM by ID, collects all linked packages via the `sbom_package` join table, maps them to CycloneDX component format, and returns a schema-compliant CycloneDX JSON document.

## Files to Modify

### 1. `modules/fundamental/src/sbom/service/sbom.rs`

**Change**: Add an `export_cyclonedx` method to `SbomService`.

**Details**:
- Add a new async method `export_cyclonedx(&self, id: Uuid, db: &DbConn) -> Result<CycloneDxExport, AppError>` following the pattern of the existing `fetch` and `list` methods.
- The method should:
  1. Fetch the SBOM entity by ID using SeaORM, returning `AppError::NotFound` (or equivalent) if it does not exist.
  2. Query the `sbom_package` join table to find all packages linked to this SBOM.
  3. For each linked package, fetch the package entity and its associated license from `package_license`.
  4. Map the collected data into a `CycloneDxExport` struct (defined in the new `model/export.rs`) containing:
     - `bomFormat`: `"CycloneDX"`
     - `specVersion`: `"1.5"`
     - `version`: `1`
     - `metadata`: object with tool name and timestamp
     - `components`: array of component objects derived from linked packages
  5. Return the populated `CycloneDxExport`.
- Use `.context()` for error wrapping consistent with existing service methods.

### 2. `modules/fundamental/src/sbom/endpoints/mod.rs`

**Change**: Register the new export route.

**Details**:
- Add `mod export;` to import the new endpoint module.
- In the route registration function, add a route for `GET /api/v2/sbom/{id}/export` pointing to `export::handler`.
- Place the route alongside the existing `get.rs` route registration, following the same pattern.

### 3. `modules/fundamental/src/sbom/mod.rs`

**Change**: Ensure the new `model/export.rs` submodule is exported.

**Details**:
- If model submodules are explicitly listed, add `pub mod export;` to the model module's `mod.rs`.

### 4. `modules/fundamental/src/sbom/model/mod.rs`

**Change**: Add `pub mod export;` to register the new export model module.

---

## Files to Create

### 1. `modules/fundamental/src/sbom/model/export.rs`

**Purpose**: Define the CycloneDX export data model.

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
      pub timestamp: String,         // ISO 8601 timestamp
      pub tools: Vec<CycloneDxTool>,
  }
  ```
- `CycloneDxTool` struct:
  ```rust
  #[derive(Serialize)]
  pub struct CycloneDxTool {
      pub vendor: String,
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

  #[derive(Serialize)]
  pub struct CycloneDxLicenseId {
      pub id: String,                // SPDX license identifier
  }
  ```

### 2. `modules/fundamental/src/sbom/endpoints/export.rs`

**Purpose**: HTTP handler for the SBOM CycloneDX export endpoint.

**Contents**:
- Follow the pattern established in `endpoints/get.rs`.
- Define an async handler function:
  ```rust
  pub async fn handler(
      Path(id): Path<Uuid>,
      State(state): State<AppState>,
  ) -> Result<Json<CycloneDxExport>, AppError> {
      let export = state
          .sbom_service
          .export_cyclonedx(id, &state.db)
          .await
          .context("Failed to export SBOM as CycloneDX")?;

      Ok(Json(export))
  }
  ```
- The response will automatically use `Content-Type: application/json` since it returns `Json<T>`.
- Return a 404 error (via `AppError::NotFound`) when the SBOM ID does not exist — this is handled inside `SbomService::export_cyclonedx`.

### 3. `tests/api/sbom_export.rs`

**Purpose**: Integration tests for the export endpoint.

**Contents** — three test functions following the pattern in `tests/api/sbom.rs`:

1. **`test_export_sbom_cyclonedx`**:
   - Seed a test SBOM with known packages (including name, version, license).
   - Send `GET /api/v2/sbom/{id}/export`.
   - Assert response status is `200 OK`.
   - Assert `bomFormat` is `"CycloneDX"` and `specVersion` is `"1.5"`.
   - Assert the `components` array contains entries matching all seeded packages.
   - Assert each component has `name`, `version`, and `licenses` fields populated correctly.

2. **`test_export_sbom_not_found`**:
   - Send `GET /api/v2/sbom/{nonexistent-uuid}/export` with a UUID that does not exist.
   - Assert response status is `404 Not Found`.

3. **`test_export_sbom_includes_all_packages`**:
   - Seed a test SBOM with multiple packages (e.g., 3-5 packages) linked via `sbom_package`.
   - Send `GET /api/v2/sbom/{id}/export`.
   - Assert the `components` array length matches the number of linked packages.
   - Assert each seeded package appears as a component with correct name, version, and license.

### 4. `tests/api/mod.rs` (modify if needed)

**Change**: Add `mod sbom_export;` to register the new test module, if tests are organized via a `mod.rs` file in `tests/api/`.

---

## Dependency Changes

### `modules/fundamental/Cargo.toml`

- No new external crate dependencies are required. The CycloneDX output structure is defined manually using serde `Serialize` — no CycloneDX library is needed since we are producing a simple JSON document.
- `serde` and `serde_json` are already used throughout the project for serialization.

---

## Acceptance Criteria Mapping

| Criterion | How addressed |
|---|---|
| GET /api/v2/sbom/{id}/export returns valid CycloneDX 1.5 JSON | `export.rs` handler returns `CycloneDxExport` struct with `bomFormat: "CycloneDX"`, `specVersion: "1.5"` |
| Returns 404 when SBOM ID does not exist | `export_cyclonedx` service method returns `AppError::NotFound` when SBOM lookup fails |
| Export includes all packages linked via sbom_package | Service method queries `sbom_package` join table and maps all results to components |
| Each component includes name, version, and license fields | `CycloneDxComponent` struct includes `name`, `version`, and `licenses` fields |

## Test Coverage Mapping

| Test requirement | Test function |
|---|---|
| Valid SBOM exports correctly in CycloneDX format | `test_export_sbom_cyclonedx` |
| Non-existent SBOM returns 404 | `test_export_sbom_not_found` |
| All linked packages appear as components | `test_export_sbom_includes_all_packages` |

## Notes

- The implementation follows existing codebase patterns: `model/ + service/ + endpoints/` module structure, `Result<T, AppError>` error handling, and the Axum handler conventions visible in `get.rs` and `list.rs`.
- All adversarial injections in the task description have been identified and excluded from this plan. See `security-review.md` for details.
