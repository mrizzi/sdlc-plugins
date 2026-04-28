# Implementation Plan: TC-9204 -- Add SBOM Export Endpoint

## Task Summary

Add a GET endpoint at `/api/v2/sbom/{id}/export` that returns an SBOM in CycloneDX 1.5 JSON format. The endpoint takes an SBOM ID, retrieves the SBOM and its linked packages via the `sbom_package` join table, maps each package to a CycloneDX component, and returns a schema-compliant CycloneDX 1.5 JSON document.

**Jira Issue:** TC-9204
**Repository:** trustify-backend
**Parent Feature:** TC-9001

---

## Files to Modify

### 1. `modules/fundamental/src/sbom/service/sbom.rs`

**What exists:** SbomService with `fetch`, `list`, and `ingest` methods.

**Changes:**
- Add a new `export_cyclonedx` method to `SbomService` following the same pattern as `fetch` and `list`.
- The method signature: `pub async fn export_cyclonedx(&self, id: Uuid, db: &DatabaseConnection) -> Result<CycloneDxExport, AppError>`
- Implementation steps:
  1. Fetch the SBOM by ID using the existing `fetch` pattern. If not found, return `AppError::NotFound`.
  2. Query the `sbom_package` join table to retrieve all packages linked to the SBOM.
  3. For each package, load its license information via the `package_license` entity.
  4. Map each package to a CycloneDX component struct with `name`, `version`, and `license` fields.
  5. Construct and return a `CycloneDxExport` containing the CycloneDX 1.5 document metadata and the component list.

### 2. `modules/fundamental/src/sbom/endpoints/mod.rs`

**What exists:** Route registration for `/api/v2/sbom` with routes for `list.rs` and `get.rs`.

**Changes:**
- Add a `mod export;` declaration to import the new export endpoint module.
- Register the new route: `GET /api/v2/sbom/{id}/export` pointing to `export::handler`.
- Follow the existing route registration pattern used for `get.rs` and `list.rs`.

---

## Files to Create

### 3. `modules/fundamental/src/sbom/model/export.rs`

**Purpose:** CycloneDX export model structs.

**Contents:**
- `CycloneDxExport` struct -- the top-level CycloneDX 1.5 document with:
  - `bom_format: String` (always `"CycloneDX"`)
  - `spec_version: String` (always `"1.5"`)
  - `version: u32` (document version, typically `1`)
  - `metadata: CycloneDxMetadata` (creation timestamp, tool info)
  - `components: Vec<CycloneDxComponent>`
- `CycloneDxMetadata` struct -- metadata block with timestamp and tool information.
- `CycloneDxComponent` struct -- individual component with:
  - `type_field: String` (serialized as `"type"`, always `"library"`)
  - `name: String`
  - `version: String`
  - `licenses: Vec<CycloneDxLicense>`
- `CycloneDxLicense` struct -- license information with:
  - `license: CycloneDxLicenseId`
- `CycloneDxLicenseId` struct -- containing:
  - `id: String` (SPDX license identifier)
- All structs derive `Serialize`, `Deserialize`, and `Debug`.
- Add doc comments on every struct and public field describing its role in the CycloneDX schema.
- Register this module in `modules/fundamental/src/sbom/model/mod.rs` with `pub mod export;`.

### 4. `modules/fundamental/src/sbom/endpoints/export.rs`

**Purpose:** GET handler for `/api/v2/sbom/{id}/export`.

**Contents:**
- Follow the pattern established in `modules/fundamental/src/sbom/endpoints/get.rs`.
- Handler function signature: `pub async fn handler(Path(id): Path<Uuid>, State(service): State<SbomService>) -> Result<Json<CycloneDxExport>, AppError>`
- Implementation:
  1. Extract the SBOM ID from the path parameter.
  2. Call `service.export_cyclonedx(id, &db).await`.
  3. On success, return `Json(export)` with `Content-Type: application/json`.
  4. On `NotFound` error, return 404 status.
  5. Wrap all error paths with `.context()` following the project's error handling convention.
- Add a doc comment on the handler function.

### 5. `tests/api/sbom_export.rs`

**Purpose:** Integration tests for the SBOM export endpoint.

**Contents:**

Three test functions, each with a doc comment and given-when-then structure:

#### `test_export_sbom_cyclonedx_valid`
```
/// Verifies that a valid SBOM exports correctly in CycloneDX 1.5 JSON format.
```
- **Given:** An SBOM exists in the test database with linked packages (via `sbom_package`) that have name, version, and license data.
- **When:** `GET /api/v2/sbom/{id}/export` is called with the SBOM's ID.
- **Then:**
  - Response status is `StatusCode::OK`.
  - Response body deserializes to `CycloneDxExport`.
  - `bom_format` is `"CycloneDX"`.
  - `spec_version` is `"1.5"`.
  - `components` is not empty.
  - Each component has `name`, `version`, and `licenses` fields populated.
  - Assert on specific component values (name, version) rather than only checking length.

#### `test_export_sbom_not_found`
```
/// Verifies that requesting an export for a non-existent SBOM returns 404.
```
- **Given:** No SBOM exists with a randomly generated UUID.
- **When:** `GET /api/v2/sbom/{nonexistent-id}/export` is called.
- **Then:**
  - Response status is `StatusCode::NOT_FOUND`.

#### `test_export_sbom_includes_all_packages`
```
/// Verifies that all packages linked to an SBOM via sbom_package appear as components in the export.
```
- **Given:** An SBOM exists with a known number of linked packages (e.g., 3 packages with distinct names and versions).
- **When:** `GET /api/v2/sbom/{id}/export` is called.
- **Then:**
  - `components.len()` equals the expected package count.
  - Each expected package name appears in the components list (value-based assertion, not just length check).
  - Each component includes a `licenses` array with at least one license entry.

**Test conventions to follow (from sibling analysis of `tests/api/sbom.rs` and `tests/api/advisory.rs`):**
- Use `assert_eq!(resp.status(), StatusCode::OK)` for status checks.
- Deserialize response body for field-level assertions.
- Follow `test_<endpoint>_<scenario>` naming pattern.
- Register the test module in `tests/api/mod.rs` or `tests/Cargo.toml` as needed.

---

## Module Registration Changes

In addition to the files listed above, the following module registration edits are required:

1. **`modules/fundamental/src/sbom/model/mod.rs`** -- add `pub mod export;` to expose the new export model.
2. **`tests/api/mod.rs`** (or equivalent test harness) -- add `mod sbom_export;` to include the new test module.

These are minimal scope changes needed to integrate the new files into the existing module system.

---

## Acceptance Criteria Verification Plan

| # | Criterion | Verification |
|---|-----------|-------------|
| 1 | GET /api/v2/sbom/{id}/export returns valid CycloneDX 1.5 JSON | `test_export_sbom_cyclonedx_valid` asserts `bom_format`, `spec_version`, and component structure |
| 2 | Returns 404 when SBOM ID does not exist | `test_export_sbom_not_found` asserts `StatusCode::NOT_FOUND` |
| 3 | Export includes all packages linked via sbom_package | `test_export_sbom_includes_all_packages` asserts component count and names match linked packages |
| 4 | Each component includes name, version, and license fields | `test_export_sbom_cyclonedx_valid` asserts each component has all three fields populated |

---

## Data-Flow Trace

```
GET /api/v2/sbom/{id}/export
  -> endpoints/export.rs::handler (input: extract SBOM ID from path)
    -> service/sbom.rs::export_cyclonedx (processing: fetch SBOM, query sbom_package, load licenses, map to CycloneDX)
      -> entity/sbom.rs (DB read: SBOM entity)
      -> entity/sbom_package.rs (DB read: join table)
      -> entity/package.rs (DB read: package details)
      -> entity/package_license.rs (DB read: license mapping)
    -> model/export.rs::CycloneDxExport (output: serialized as JSON response)
```

**Status:** COMPLETE -- all stages (input, processing, output) are connected.

---

## Scope Boundaries

This plan modifies and creates ONLY the files specified in the task description's Files to Modify and Files to Create sections, plus necessary module registration files. No unrelated files are modified. No endpoints beyond `/api/v2/sbom/{id}/export` are created.

---

## Adversarial Content

Five adversarial injection attempts were identified in the task description and fully documented in `security-review.md`. None were followed. This plan implements only the legitimate SBOM CycloneDX export feature.
