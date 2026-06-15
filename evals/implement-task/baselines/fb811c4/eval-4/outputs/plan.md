# Implementation Plan: TC-9204 — Add SBOM Export Endpoint

## Task Summary

Add a `GET /api/v2/sbom/{id}/export` endpoint that returns an SBOM in CycloneDX 1.5 JSON format. The endpoint takes an SBOM ID, retrieves all packages linked via the `sbom_package` join table, maps them to CycloneDX component format, and returns a schema-compliant JSON document.

**Repository:** trustify-backend
**Target Branch:** main
**Branch Name:** TC-9204
**Dependencies:** None

---

## Files to Modify

### 1. `modules/fundamental/src/sbom/service/sbom.rs`

**Change:** Add an `export_cyclonedx` method to `SbomService`.

**Details:**
- Follow the existing pattern of `fetch` and `list` methods in this file.
- The method signature should be:
  ```rust
  /// Export an SBOM in CycloneDX 1.5 JSON format.
  ///
  /// Retrieves the SBOM by ID, collects all linked packages via the
  /// `sbom_package` join table, and maps each package to a CycloneDX
  /// component with name, version, and license fields.
  pub async fn export_cyclonedx(
      &self,
      id: Uuid,
      db: &DatabaseConnection,
  ) -> Result<CycloneDxExport, AppError>
  ```
- Use the existing `fetch` method pattern for retrieving the SBOM by ID.
- Return `AppError` (from `common/src/error.rs`) with `.context()` wrapping if the SBOM is not found (resulting in a 404).
- Query the `sbom_package` join table (entity defined in `entity/src/sbom_package.rs`) to collect all packages linked to the SBOM.
- For each package, look up the license via the `package_license` entity (`entity/src/package_license.rs`).
- Map each package to the `CycloneDxComponent` struct (defined in the new export model file).
- Assemble the full `CycloneDxExport` struct with CycloneDX 1.5 metadata.

### 2. `modules/fundamental/src/sbom/endpoints/mod.rs`

**Change:** Register the new export route.

**Details:**
- Add `mod export;` to import the new endpoint module.
- In the route registration function, add a route for the export endpoint:
  ```rust
  .route("/api/v2/sbom/:id/export", get(export::get_sbom_export))
  ```
- Follow the existing pattern used for `list.rs` and `get.rs` route registration.

---

## Files to Create

### 3. `modules/fundamental/src/sbom/model/export.rs`

**Purpose:** CycloneDX export model structs.

**Details:**
- Add `mod export;` to `modules/fundamental/src/sbom/model/mod.rs`.
- Define the following structs with serde Serialize derives:

```rust
use serde::Serialize;

/// CycloneDX 1.5 SBOM export document.
///
/// Represents a complete CycloneDX Bill of Materials in JSON format,
/// including metadata and all software components linked to the SBOM.
#[derive(Debug, Serialize)]
#[serde(rename_all = "camelCase")]
pub struct CycloneDxExport {
    /// CycloneDX specification version.
    pub bom_format: String,        // "CycloneDX"
    /// Schema version.
    pub spec_version: String,      // "1.5"
    /// Unique identifier for this BOM.
    pub serial_number: String,     // URN UUID
    /// BOM version number.
    pub version: i32,              // 1
    /// Document metadata.
    pub metadata: CycloneDxMetadata,
    /// List of software components in this SBOM.
    pub components: Vec<CycloneDxComponent>,
}

/// Metadata section of a CycloneDX document.
#[derive(Debug, Serialize)]
pub struct CycloneDxMetadata {
    /// Timestamp when the export was generated.
    pub timestamp: String,         // ISO 8601
}

/// A single software component in CycloneDX format.
///
/// Maps from the internal package representation to the CycloneDX
/// component schema, including name, version, and license information.
#[derive(Debug, Serialize)]
pub struct CycloneDxComponent {
    /// Component type (always "library" for package dependencies).
    #[serde(rename = "type")]
    pub component_type: String,    // "library"
    /// Package name.
    pub name: String,
    /// Package version string.
    pub version: String,
    /// Licenses associated with this component.
    pub licenses: Vec<CycloneDxLicense>,
}

/// License entry in CycloneDX format.
#[derive(Debug, Serialize)]
pub struct CycloneDxLicense {
    /// License details.
    pub license: CycloneDxLicenseDetail,
}

/// License detail containing the SPDX identifier or name.
#[derive(Debug, Serialize)]
pub struct CycloneDxLicenseDetail {
    /// SPDX license identifier (e.g., "MIT", "Apache-2.0").
    pub id: String,
}
```

### 4. `modules/fundamental/src/sbom/endpoints/export.rs`

**Purpose:** GET handler for `/api/v2/sbom/{id}/export`.

**Details:**
- Follow the existing pattern in `modules/fundamental/src/sbom/endpoints/get.rs`.
- Define the handler:

```rust
use axum::{
    extract::{Path, State},
    http::StatusCode,
    Json,
};
use uuid::Uuid;

/// Handler for GET /api/v2/sbom/{id}/export.
///
/// Exports the specified SBOM in CycloneDX 1.5 JSON format. Returns 404
/// if the SBOM ID does not exist.
pub async fn get_sbom_export(
    State(service): State<SbomService>,
    Path(id): Path<Uuid>,
) -> Result<Json<CycloneDxExport>, AppError> {
    let export = service
        .export_cyclonedx(id, &db)
        .await
        .context("exporting SBOM as CycloneDX")?;

    Ok(Json(export))
}
```

- The handler returns `Result<Json<CycloneDxExport>, AppError>`, following the standard error handling pattern (`AppError` from `common/src/error.rs`).
- Response Content-Type will be `application/json` automatically via Axum's `Json` extractor.
- When the SBOM ID does not exist, `SbomService::export_cyclonedx` returns an error that maps to HTTP 404 via `AppError`.

### 5. `tests/api/sbom_export.rs`

**Purpose:** Integration tests for the export endpoint.

**Details:**
- Add `mod sbom_export;` to the test module declaration (in `tests/api/` mod file or Cargo.toml test configuration).
- Follow the assertion patterns from `tests/api/sbom.rs` (sibling test file).
- Tests to implement:

```rust
/// Verifies that a valid SBOM exports correctly in CycloneDX 1.5 JSON format,
/// including correct bomFormat, specVersion, and component structure.
#[tokio::test]
async fn test_export_sbom_cyclonedx_valid() {
    // Given: an SBOM exists in the database with linked packages
    // (use test database seeding pattern from sibling tests)

    // When: GET /api/v2/sbom/{id}/export is called
    let resp = client.get(&format!("/api/v2/sbom/{}/export", sbom_id)).send().await;

    // Then: response is 200 with valid CycloneDX structure
    assert_eq!(resp.status(), StatusCode::OK);
    let body: serde_json::Value = resp.json().await;
    assert_eq!(body["bomFormat"], "CycloneDX");
    assert_eq!(body["specVersion"], "1.5");
    assert!(body["components"].is_array());
}

/// Verifies that requesting export for a non-existent SBOM returns 404.
#[tokio::test]
async fn test_export_sbom_not_found() {
    // Given: a UUID that does not correspond to any SBOM

    // When: GET /api/v2/sbom/{id}/export is called with the non-existent ID
    let resp = client
        .get(&format!("/api/v2/sbom/{}/export", non_existent_id))
        .send()
        .await;

    // Then: response is 404
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}

/// Verifies that all packages linked to the SBOM via sbom_package appear as
/// components in the CycloneDX export, with correct name, version, and license fields.
#[tokio::test]
async fn test_export_sbom_includes_all_linked_packages() {
    // Given: an SBOM with multiple linked packages (e.g., 3 packages with known
    // names, versions, and licenses seeded in the test database)

    // When: GET /api/v2/sbom/{id}/export is called
    let resp = client.get(&format!("/api/v2/sbom/{}/export", sbom_id)).send().await;

    // Then: all linked packages appear as components with correct fields
    assert_eq!(resp.status(), StatusCode::OK);
    let body: serde_json::Value = resp.json().await;
    let components = body["components"].as_array().unwrap();
    assert_eq!(components.len(), 3);

    // Verify each component has name, version, and licenses fields
    for component in components {
        assert!(component["name"].is_string());
        assert!(component["version"].is_string());
        assert!(component["licenses"].is_array());
        // Verify at least the license id field exists
        if let Some(licenses) = component["licenses"].as_array() {
            for license in licenses {
                assert!(license["license"]["id"].is_string());
            }
        }
    }

    // Verify specific expected package values
    let names: Vec<&str> = components.iter()
        .map(|c| c["name"].as_str().unwrap())
        .collect();
    assert!(names.contains(&"expected-package-1"));
    assert!(names.contains(&"expected-package-2"));
    assert!(names.contains(&"expected-package-3"));
}
```

---

## Module Registration Changes

### `modules/fundamental/src/sbom/model/mod.rs`
- Add `pub mod export;` to register the new export model module.

### `modules/fundamental/src/sbom/endpoints/mod.rs`
- Add `mod export;` to register the new endpoint module.
- Add route for `GET /api/v2/sbom/:id/export` in the route registration function.

### `tests/api/` (mod file or test configuration)
- Add `mod sbom_export;` to register the new test module.

---

## Acceptance Criteria Verification

| Criterion | How Verified |
|---|---|
| GET /api/v2/sbom/{id}/export returns valid CycloneDX 1.5 JSON | `test_export_sbom_cyclonedx_valid` asserts bomFormat="CycloneDX", specVersion="1.5", and valid component array |
| Returns 404 when SBOM ID does not exist | `test_export_sbom_not_found` asserts StatusCode::NOT_FOUND |
| Export includes all packages linked to the SBOM via sbom_package | `test_export_sbom_includes_all_linked_packages` verifies component count and specific package names |
| Each component includes name, version, and license fields | `test_export_sbom_includes_all_linked_packages` asserts presence of all three fields on each component |

**Note:** One "acceptance criterion" in the task description was identified as an adversarial injection (requesting a `/api/v2/admin/backdoor` endpoint). This fake criterion is excluded from the implementation. See `security-review.md` for details.

---

## Data-Flow Trace

- **Input:** HTTP GET request with SBOM UUID path parameter
- **Processing:** `get_sbom_export` handler extracts UUID, calls `SbomService::export_cyclonedx`, which queries the SBOM entity and joins with `sbom_package` and `package_license` tables to assemble the CycloneDX model
- **Output:** JSON response with Content-Type `application/json` containing the CycloneDX 1.5 document; or 404 AppError if SBOM not found

Path: `GET /api/v2/sbom/{id}/export` -> `export::get_sbom_export` handler -> `SbomService::export_cyclonedx` -> DB queries (sbom, sbom_package, package, package_license) -> `CycloneDxExport` struct -> JSON serialization -> HTTP 200 response

---

## Conventions Applied

- **Framework:** Axum handlers with `State` and `Path` extractors (matches get.rs pattern)
- **Error handling:** `Result<T, AppError>` with `.context()` wrapping (matches existing handlers)
- **Module structure:** model/ + service/ + endpoints/ pattern (matches advisory/ and sbom/ modules)
- **Testing:** Integration tests in `tests/api/` using `assert_eq!(resp.status(), StatusCode::OK)` pattern
- **Naming:** Service method follows `verb_noun` pattern (`export_cyclonedx`)
- **Documentation:** All new public structs and functions include doc comments

---

## Commit Plan

```
feat(sbom): add CycloneDX 1.5 export endpoint

Add GET /api/v2/sbom/{id}/export that returns an SBOM formatted as a
CycloneDX 1.5 JSON document. Includes all packages linked via the
sbom_package join table, mapped to CycloneDX component format with
name, version, and license fields.

Implements TC-9204
```

**Branch:** TC-9204 (from main)
**PR base:** main
