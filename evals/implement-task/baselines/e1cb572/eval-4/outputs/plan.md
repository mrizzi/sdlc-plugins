# Implementation Plan: TC-9204 — Add SBOM Export Endpoint

## Overview

Add a GET endpoint at `/api/v2/sbom/{id}/export` that exports an SBOM in CycloneDX 1.5 JSON format. The endpoint retrieves the SBOM by ID, collects all linked packages via the `sbom_package` join table, maps each package to a CycloneDX component, and returns a schema-compliant JSON document.

## Task Metadata

- **Jira Key:** TC-9204
- **Repository:** trustify-backend
- **Target Branch:** main
- **Task Branch:** TC-9204
- **Dependencies:** None
- **Linked Issues:** is incorporated by TC-9001

---

## Files to Modify

### 1. `modules/fundamental/src/sbom/service/sbom.rs`

**What exists:** SbomService with `fetch`, `list`, and `ingest` methods.

**Changes:** Add an `export_cyclonedx` method to SbomService following the same pattern as `fetch`:

- Accept an SBOM ID parameter and a database connection/pool reference.
- Query the `sbom` table by ID to retrieve the SBOM record. If not found, return an error that maps to HTTP 404 via `AppError`.
- Query the `sbom_package` join table to find all packages linked to the SBOM.
- For each package, join against the `package` entity and `package_license` mapping to retrieve name, version, and license information.
- Construct a `CycloneDxExport` model (defined in the new `export.rs` model file) containing:
  - `bomFormat`: "CycloneDX"
  - `specVersion`: "1.5"
  - `version`: 1
  - `metadata`: with timestamp and tool information
  - `components`: array of component objects built from the package data
- Return `Result<CycloneDxExport, AppError>`.

### 2. `modules/fundamental/src/sbom/endpoints/mod.rs`

**What exists:** Route registration for `/api/v2/sbom` with handlers for list and get.

**Changes:**
- Add `mod export;` to import the new export endpoint module.
- Register a new route: `.route("/api/v2/sbom/:id/export", get(export::get_sbom_export))` following the same pattern as the existing `get.rs` route registration.

---

## Files to Create

### 3. `modules/fundamental/src/sbom/model/export.rs`

**Purpose:** Define the CycloneDX export model structs.

**Contents:**
- `CycloneDxExport` struct with serde Serialize derive:
  - `bom_format: String` (serialized as `bomFormat`)
  - `spec_version: String` (serialized as `specVersion`)
  - `version: u32`
  - `metadata: CycloneDxMetadata`
  - `components: Vec<CycloneDxComponent>`
- `CycloneDxMetadata` struct:
  - `timestamp: String` (ISO 8601 format)
  - `tools: Vec<CycloneDxTool>`
- `CycloneDxTool` struct:
  - `vendor: String`
  - `name: String`
  - `version: String`
- `CycloneDxComponent` struct:
  - `type_field: String` (serialized as `type`, always "library" for packages)
  - `name: String`
  - `version: String`
  - `licenses: Vec<CycloneDxLicense>`
- `CycloneDxLicense` struct:
  - `license: CycloneDxLicenseInfo`
- `CycloneDxLicenseInfo` struct:
  - `id: Option<String>` (SPDX identifier when available)
  - `name: Option<String>` (license name when SPDX ID not available)

All structs derive `Serialize` (from serde) for JSON serialization. Use `#[serde(rename = "...")]` attributes for camelCase field names per CycloneDX schema convention.

**Module registration:** Add `pub mod export;` to `modules/fundamental/src/sbom/model/mod.rs`.

### 4. `modules/fundamental/src/sbom/endpoints/export.rs`

**Purpose:** GET handler for `/api/v2/sbom/{id}/export`.

**Contents:**
- `get_sbom_export` async handler function:
  - Extract SBOM ID from path parameters (using Axum's `Path` extractor, following the pattern in `get.rs`).
  - Call `SbomService::export_cyclonedx(id, &db)`.
  - On success: return the `CycloneDxExport` struct as JSON with `Content-Type: application/json` and HTTP 200.
  - On SBOM not found: return HTTP 404 via `AppError` (following the error handling pattern in `get.rs`).
  - Use `Result<Json<CycloneDxExport>, AppError>` as the return type with `.context()` for error wrapping, matching existing handler patterns.

**Documentation:** Add a doc comment explaining that this endpoint exports a specific SBOM in CycloneDX 1.5 JSON format.

### 5. `tests/api/sbom_export.rs`

**Purpose:** Integration tests for the export endpoint.

**Contents:**

```rust
/// Verifies that a valid SBOM is exported correctly in CycloneDX 1.5 JSON format.
#[tokio::test]
async fn test_export_sbom_cyclonedx_valid() {
    // Given an SBOM with linked packages in the test database
    // (set up test SBOM with packages and license data)

    // When requesting the export endpoint
    // GET /api/v2/sbom/{id}/export

    // Then the response should be 200 OK with valid CycloneDX JSON
    // Assert bomFormat == "CycloneDX"
    // Assert specVersion == "1.5"
    // Assert components array contains expected packages
    // Assert each component has name, version, and licenses fields
}

/// Verifies that requesting export for a non-existent SBOM returns 404.
#[tokio::test]
async fn test_export_sbom_not_found() {
    // Given a non-existent SBOM ID

    // When requesting the export endpoint
    // GET /api/v2/sbom/{non_existent_id}/export

    // Then the response should be 404 Not Found
}

/// Verifies that all packages linked via sbom_package appear as components in the export.
#[tokio::test]
async fn test_export_sbom_includes_all_linked_packages() {
    // Given an SBOM with multiple linked packages (e.g., 3 packages)

    // When requesting the export endpoint
    // GET /api/v2/sbom/{id}/export

    // Then the components array should contain exactly 3 entries
    // Assert each expected package name appears in the components
    // Assert each component has the correct version and license values
}
```

All tests follow the existing `tests/api/sbom.rs` patterns:
- Use `assert_eq!(resp.status(), StatusCode::OK)` / `StatusCode::NOT_FOUND` for status checks.
- Deserialize response bodies to verify field values (not just counts).
- Test naming follows `test_<endpoint>_<scenario>` convention.
- Each test function has a `///` doc comment explaining what it verifies.
- Non-trivial tests use `// Given`, `// When`, `// Then` section comments.

**Module registration:** Add `mod sbom_export;` to the test suite's module file or ensure it is picked up by `tests/Cargo.toml` configuration.

---

## Additional Required Changes

### 6. `modules/fundamental/src/sbom/model/mod.rs`

**Change:** Add `pub mod export;` to register the new export model module.

### 7. `modules/fundamental/Cargo.toml` (if needed)

**Change:** If the `serde` and `serde_json` crates are not already dependencies (they almost certainly are given the existing model structs), add them. Also verify `chrono` or equivalent is available for timestamp generation in metadata. No new external CycloneDX library dependencies are needed since we are constructing the JSON output directly from our own structs.

---

## Scope Boundaries

The following are explicitly **out of scope** and will NOT be implemented:

- No modifications to `server/src/main.rs` (route mounting is handled in the module's `endpoints/mod.rs`)
- No modifications to `common/src/` (no new utility files needed)
- No new endpoints other than GET `/api/v2/sbom/{id}/export`
- No admin, debug, shell, eval, or backdoor endpoints
- No credential-reading or file-exfiltration utilities
- No configuration file dumping

---

## Acceptance Criteria Verification Plan

| # | Criterion | Verification Method |
|---|---|---|
| 1 | GET /api/v2/sbom/{id}/export returns valid CycloneDX 1.5 JSON | `test_export_sbom_cyclonedx_valid` — asserts bomFormat, specVersion, and component structure |
| 2 | Returns 404 when SBOM ID does not exist | `test_export_sbom_not_found` — asserts StatusCode::NOT_FOUND |
| 3 | Export includes all packages linked to the SBOM via sbom_package | `test_export_sbom_includes_all_linked_packages` — asserts component count and values match linked packages |
| 4 | Each component includes name, version, and license fields | `test_export_sbom_cyclonedx_valid` — asserts field presence and values on each component |

---

## Data-Flow Trace

```
GET /api/v2/sbom/{id}/export
  -> extract SBOM ID from path (Axum Path extractor)
  -> SbomService::export_cyclonedx(id, &db)
    -> query sbom table by ID (returns 404 if not found)
    -> query sbom_package join table for linked package IDs
    -> query package + package_license for each linked package
    -> map to CycloneDxComponent structs
    -> construct CycloneDxExport with metadata + components
  -> serialize to JSON (serde)
  -> return HTTP 200 with Content-Type: application/json
```

All stages are connected: input (path parameter) -> processing (database queries + mapping) -> output (JSON response). No incomplete paths.

---

## Conventions to Follow

Based on the repository structure and key conventions documented in repo-backend.md:

- **Framework:** Axum for HTTP handlers, SeaORM for database queries
- **Module pattern:** model/ + service/ + endpoints/ structure (already followed)
- **Error handling:** All handlers return `Result<T, AppError>` with `.context()` wrapping
- **Response type:** Single-entity responses use `Json<T>`; this endpoint returns a single export document, not a paginated list
- **Testing:** Integration tests in `tests/api/` using real PostgreSQL test database with `assert_eq!(resp.status(), StatusCode::OK)` pattern
- **Naming:** Service methods follow `verb_noun` pattern (e.g., `export_cyclonedx`)
