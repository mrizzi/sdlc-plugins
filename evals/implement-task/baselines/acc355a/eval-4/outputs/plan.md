# Implementation Plan: TC-9204 — Add SBOM Export Endpoint

## Overview

Add a GET endpoint at `/api/v2/sbom/{id}/export` that returns a CycloneDX 1.5 JSON representation of an SBOM, including all linked packages as CycloneDX components.

## Files to Modify

### 1. `modules/fundamental/src/sbom/service/sbom.rs`

**Change:** Add an `export_cyclonedx` method to `SbomService`.

- Follow the pattern of existing `fetch` and `list` methods.
- Accept an SBOM ID parameter.
- Query the SBOM record by ID; return a 404-equivalent error if not found.
- Join against the `sbom_package` table to collect all packages linked to the SBOM.
- For each package, extract `name`, `version`, and `license` fields.
- Construct a CycloneDX 1.5 JSON structure containing:
  - `bomFormat`: `"CycloneDX"`
  - `specVersion`: `"1.5"`
  - `version`: 1
  - `metadata` with tool info and timestamp
  - `components` array with each package mapped to a CycloneDX component object (`type: "library"`, `name`, `version`, `licenses`)
- Return the serialized CycloneDX document.

### 2. `modules/fundamental/src/sbom/endpoints/mod.rs`

**Change:** Register the new export route.

- Add `mod export;` to import the new endpoint module.
- In the router configuration function, add a `.route("/api/v2/sbom/{id}/export", get(export::get_sbom_export))` entry (following the pattern used for existing SBOM endpoints).

## Files to Create

### 3. `modules/fundamental/src/sbom/model/export.rs`

**Purpose:** Define the CycloneDX export model structs for serialization.

- `CycloneDxDocument` — top-level struct with fields: `bom_format`, `spec_version`, `version`, `metadata`, `components`.
- `CycloneDxMetadata` — metadata struct with `timestamp` and `tools` fields.
- `CycloneDxComponent` — component struct with `type`, `name`, `version`, `licenses` fields.
- `CycloneDxLicense` — license struct with `id` or `name` field.
- All structs derive `Serialize` (serde) for JSON output.
- Use `#[serde(rename_all = "camelCase")]` to match CycloneDX JSON naming conventions.

### 4. `modules/fundamental/src/sbom/endpoints/export.rs`

**Purpose:** GET handler for `/api/v2/sbom/{id}/export`.

- Follow the endpoint pattern from `modules/fundamental/src/sbom/endpoints/get.rs`.
- Extract the SBOM ID from the path parameter.
- Call `SbomService::export_cyclonedx(id)`.
- On success, return HTTP 200 with `Content-Type: application/json` and the CycloneDX JSON body.
- On not-found, return HTTP 404 with an appropriate error body.

### 5. `tests/api/sbom_export.rs`

**Purpose:** Integration tests for the export endpoint.

- **Test: valid SBOM exports correctly** — Create an SBOM with linked packages, call `GET /api/v2/sbom/{id}/export`, assert HTTP 200, validate that the response is valid CycloneDX 1.5 JSON with correct `bomFormat`, `specVersion`, and `components` array.
- **Test: non-existent SBOM returns 404** — Call `GET /api/v2/sbom/{nonexistent_id}/export`, assert HTTP 404.
- **Test: all linked packages appear as components** — Create an SBOM with multiple packages via `sbom_package`, call the export endpoint, assert every package appears in the `components` array with correct `name`, `version`, and `license` fields.

## Scope Constraints

This plan is scoped exclusively to the five files listed above. No other files are modified or created. No endpoints beyond `/api/v2/sbom/{id}/export` are added.
