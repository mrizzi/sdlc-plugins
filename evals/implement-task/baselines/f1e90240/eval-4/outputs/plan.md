# Implementation Plan: TC-9204 — Add SBOM Export Endpoint

## Overview

Add a GET /api/v2/sbom/{id}/export endpoint that returns an SBOM in CycloneDX 1.5 JSON format. The endpoint takes an SBOM ID, retrieves all linked packages via the sbom_package join table, maps them to CycloneDX component format, and returns a schema-compliant JSON document.

## Repository

trustify-backend

## Target Branch

main

## Branch Name

TC-9204

---

## Files to Modify

### 1. `modules/fundamental/src/sbom/service/sbom.rs`

**Change:** Add an `export_cyclonedx` method to `SbomService`.

**Details:**
- Follow the pattern of the existing `fetch` and `list` methods in the same file.
- The method accepts an SBOM ID parameter and a database connection/pool reference.
- Query the `sbom` table to find the SBOM by ID. If not found, return an error that maps to HTTP 404 (using the `AppError` pattern from `common/src/error.rs`).
- Query the `sbom_package` join table to retrieve all packages linked to this SBOM.
- For each package, join with the `package_license` table to retrieve license information.
- Map each package to the `CycloneDxComponent` struct (defined in the new export model).
- Assemble the full `CycloneDxBom` struct with:
  - `bomFormat`: "CycloneDX"
  - `specVersion`: "1.5"
  - `version`: 1
  - `components`: the list of mapped components
- Return `Result<CycloneDxBom, AppError>` following the existing error handling pattern with `.context()` wrapping.

### 2. `modules/fundamental/src/sbom/endpoints/mod.rs`

**Change:** Register the new export route.

**Details:**
- Add `mod export;` to import the new export handler module.
- In the route registration function, add a route for `GET /api/v2/sbom/{id}/export` pointing to `export::get_sbom_export`.
- Follow the same route registration pattern used by `get.rs` and `list.rs` in this module.

---

## Files to Create

### 1. `modules/fundamental/src/sbom/model/export.rs`

**Purpose:** Define CycloneDX export model structs.

**Contents:**
- `CycloneDxBom` struct with fields:
  - `bom_format: String` (serialized as `"bomFormat"`)
  - `spec_version: String` (serialized as `"specVersion"`)
  - `version: u32`
  - `components: Vec<CycloneDxComponent>`
- `CycloneDxComponent` struct with fields:
  - `type_field: String` (serialized as `"type"`, value: `"library"`)
  - `name: String`
  - `version: String`
  - `licenses: Vec<CycloneDxLicense>`
- `CycloneDxLicense` struct with fields:
  - `license: CycloneDxLicenseExpression`
- `CycloneDxLicenseExpression` struct with fields:
  - `id: String` (SPDX license identifier)
- All structs derive `Serialize` (serde) for JSON serialization.
- Add documentation comments on each struct and field explaining their role in the CycloneDX 1.5 schema.
- Register this module in `modules/fundamental/src/sbom/model/mod.rs` with `pub mod export;`.

### 2. `modules/fundamental/src/sbom/endpoints/export.rs`

**Purpose:** GET handler for /api/v2/sbom/{id}/export.

**Contents:**
- Follow the pattern from `modules/fundamental/src/sbom/endpoints/get.rs`.
- Define an async handler function `get_sbom_export` that:
  - Extracts the SBOM ID from the path parameter (using Axum's `Path` extractor).
  - Calls `SbomService::export_cyclonedx(id, &db)`.
  - On success, returns `(StatusCode::OK, Json(bom))` with `Content-Type: application/json`.
  - On not-found, returns a 404 response (via the `AppError` mapping).
  - Uses `Result<T, AppError>` return type with `.context()` for error wrapping, consistent with sibling handlers.
- Add documentation comments on the handler function.

### 3. `tests/api/sbom_export.rs`

**Purpose:** Integration tests for the export endpoint.

**Contents:**
- Follow the test patterns from `tests/api/sbom.rs` (sibling test file).
- Use `assert_eq!(resp.status(), StatusCode::OK)` pattern for status checks.
- Register this test module in `tests/api/mod.rs` (if a mod.rs exists) or ensure it is picked up by the test harness.

**Test functions:**

1. `test_export_sbom_cyclonedx_valid`
   - Doc comment: "Verifies that a valid SBOM exports correctly in CycloneDX 1.5 JSON format."
   - Given: An SBOM exists in the test database with linked packages (via sbom_package).
   - When: GET /api/v2/sbom/{id}/export is called.
   - Then:
     - Response status is 200 OK.
     - Response body deserializes to valid JSON.
     - `bomFormat` equals "CycloneDX".
     - `specVersion` equals "1.5".
     - `components` array is non-empty.
     - Each component has `name`, `version`, and `licenses` fields.
     - Assert on specific component values (name, version) matching the test data, not just array length.

2. `test_export_sbom_not_found`
   - Doc comment: "Verifies that requesting an export for a non-existent SBOM returns 404."
   - Given: No SBOM exists with the given ID.
   - When: GET /api/v2/sbom/{non-existent-id}/export is called.
   - Then: Response status is 404 NOT_FOUND.

3. `test_export_sbom_includes_all_linked_packages`
   - Doc comment: "Verifies that all packages linked to the SBOM via sbom_package appear as components in the export."
   - Given: An SBOM exists with N known packages linked via sbom_package.
   - When: GET /api/v2/sbom/{id}/export is called.
   - Then:
     - The `components` array contains exactly N entries.
     - Each expected package name appears in the components list.
     - Each component includes the correct version and license fields matching the test data.

---

## Module Registration Changes

In addition to the files listed above, the following existing module files need minor registration additions:

- `modules/fundamental/src/sbom/model/mod.rs` — add `pub mod export;` to expose the new export model.

This file is within the scope of the task (it is part of the sbom module being extended) and the change is a single line addition required for the new model to be importable.

---

## Data Flow

```
GET /api/v2/sbom/{id}/export
  -> export.rs handler (extract path param)
    -> SbomService::export_cyclonedx(id)
      -> Query sbom table (find by ID, or 404)
      -> Query sbom_package join table (get linked package IDs)
      -> Query package + package_license tables (get package details with licenses)
      -> Map to CycloneDxComponent structs
      -> Assemble CycloneDxBom
    <- Return JSON response with Content-Type: application/json
```

---

## Acceptance Criteria Verification

| Criterion | How Verified |
|---|---|
| GET /api/v2/sbom/{id}/export returns valid CycloneDX 1.5 JSON | test_export_sbom_cyclonedx_valid asserts bomFormat, specVersion, and component structure |
| Returns 404 when SBOM ID does not exist | test_export_sbom_not_found asserts 404 status |
| Export includes all packages linked via sbom_package | test_export_sbom_includes_all_linked_packages asserts component count and values |
| Each component includes name, version, and license fields | test_export_sbom_cyclonedx_valid asserts field presence on each component |

---

## Conventions to Follow

Based on the repository structure and key conventions documented in repo-backend.md:

- **Framework:** Axum for HTTP handlers, SeaORM for database queries.
- **Error handling:** All handlers return `Result<T, AppError>` with `.context()` wrapping.
- **Module structure:** Follow the `model/ + service/ + endpoints/` pattern used by sbom, advisory, and package modules.
- **Endpoint registration:** Register routes in `endpoints/mod.rs`; server/main.rs mounts modules.
- **Test style:** Integration tests in `tests/api/` using `assert_eq!(resp.status(), StatusCode::OK)` pattern with body deserialization.
- **Naming:** Service methods follow `verb_noun` pattern (e.g., `export_cyclonedx`).

---

## Commit Message

```
feat(sbom): add CycloneDX 1.5 export endpoint

Add GET /api/v2/sbom/{id}/export that returns the SBOM content
formatted as a CycloneDX 1.5 JSON document, including all linked
packages as components with name, version, and license fields.

Implements TC-9204
```
