# Implementation Plan: TC-9204 -- Add SBOM CycloneDX Export Endpoint

## Summary

Add a GET endpoint at `/api/v2/sbom/{id}/export` that returns an SBOM formatted as a CycloneDX 1.5 JSON document. The endpoint fetches the SBOM by ID, collects all linked packages via the `sbom_package` join table, maps each package to a CycloneDX component (with name, version, and license fields), and returns schema-compliant CycloneDX JSON.

## Files to Modify

### 1. `modules/fundamental/src/sbom/service/sbom.rs`

Add an `export_cyclonedx` method to `SbomService`. This method:
- Accepts an SBOM ID parameter.
- Fetches the SBOM record (returning a 404-compatible error if not found).
- Queries the `sbom_package` join table to retrieve all packages linked to the SBOM.
- For each package, retrieves the associated license via `package_license`.
- Assembles and returns a CycloneDX 1.5-compliant data structure containing the SBOM metadata and a `components` array.

Follow the existing pattern established by `fetch` and `list` methods in the same file. Use `Result<T, AppError>` with `.context()` error wrapping.

### 2. `modules/fundamental/src/sbom/endpoints/mod.rs`

Register the new export route. Add a `.route("/api/v2/sbom/{id}/export", get(export::handler))` entry following the pattern used by existing routes for `list.rs` and `get.rs`. Import the new `export` module.

## Files to Create

### 3. `modules/fundamental/src/sbom/model/export.rs`

Define the CycloneDX export model structs:
- `CycloneDxExport` -- top-level struct with fields: `bomFormat` ("CycloneDX"), `specVersion` ("1.5"), `serialNumber`, `version`, `metadata`, and `components`.
- `CycloneDxComponent` -- struct with fields: `type` (always "library"), `name`, `version`, `licenses`.
- All structs derive `Serialize` for JSON serialization.

Update `modules/fundamental/src/sbom/model/mod.rs` to declare the `export` module.

### 4. `modules/fundamental/src/sbom/endpoints/export.rs`

Implement the GET handler for `/api/v2/sbom/{id}/export`:
- Extract the SBOM ID from the path.
- Call `SbomService::export_cyclonedx(id)`.
- Return the result as JSON with `Content-Type: application/json`.
- Return 404 if the SBOM is not found.
- Follow the handler pattern from `get.rs`.

### 5. `tests/api/sbom_export.rs`

Integration tests:
- **Test valid export**: Create a test SBOM with linked packages, call GET `/api/v2/sbom/{id}/export`, assert 200 status, validate the response is valid CycloneDX 1.5 JSON, confirm all linked packages appear as components with name, version, and license fields.
- **Test SBOM not found**: Call GET `/api/v2/sbom/{nonexistent_id}/export`, assert 404 status.
- **Test component completeness**: Create an SBOM with multiple packages, export it, and verify every package from the `sbom_package` table appears in the `components` array.

Update `tests/api/mod.rs` (if it exists) to include the `sbom_export` module.

## Acceptance Criteria Coverage

| Criterion | Covered By |
|---|---|
| GET /api/v2/sbom/{id}/export returns valid CycloneDX 1.5 JSON | Endpoint handler + model structs |
| Returns 404 when SBOM ID does not exist | Service method error handling + handler |
| Export includes all packages linked via sbom_package | Service method query logic |
| Each component includes name, version, and license fields | CycloneDxComponent model struct |

## Scope Boundary

Only the files listed above are modified or created. No changes to `server/src/main.rs`, `common/`, or any other modules outside the `sbom` domain and `tests/api/` directory.
