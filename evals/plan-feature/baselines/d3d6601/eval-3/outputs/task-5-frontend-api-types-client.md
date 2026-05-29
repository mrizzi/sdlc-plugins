## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add TypeScript interfaces for the SBOM comparison API response and a client function that calls the new backend comparison endpoint. This provides the data layer that the React Query hook and comparison page will consume.

## Files to Modify
- `src/api/models.ts` — add TypeScript interfaces for the comparison response shape
- `src/api/rest.ts` — add `fetchSbomComparison(leftId: string, rightId: string)` function

## Implementation Notes
- Add the following interfaces to `src/api/models.ts`, following the naming and style conventions of existing interfaces in that file:
  - `SbomComparison` — top-level response with fields: `added_packages: PackageDiff[]`, `removed_packages: PackageDiff[]`, `version_changes: VersionChange[]`, `new_vulnerabilities: VulnerabilityDiff[]`, `resolved_vulnerabilities: VulnerabilityDiff[]`, `license_changes: LicenseChange[]`
  - `PackageDiff` — fields: `name: string`, `version: string`, `license: string`, `advisory_count: number`
  - `VersionChange` — fields: `name: string`, `left_version: string`, `right_version: string`, `direction: "upgrade" | "downgrade"`
  - `VulnerabilityDiff` — fields: `advisory_id: string`, `severity: string`, `title: string`, `affected_package: string`
  - `LicenseChange` — fields: `name: string`, `left_license: string`, `right_license: string`
- Add the `fetchSbomComparison` function to `src/api/rest.ts` following the pattern of existing functions like `fetchSboms()` — use the Axios client from `src/api/client.ts` and return a typed `Promise<SbomComparison>`.
- **Backend API contracts:**
  - `GET /api/v2/sbom/compare?left={id1}&right={id2}` — response shape: `SbomComparison` as defined above (see `modules/fundamental/src/sbom/endpoints/compare.rs` in trustify-backend)
  - Verify these contracts against the backend repo during implementation using the implement-task cross-repo API verification step.

## Reuse Candidates
- `src/api/models.ts` — existing API model interfaces; follow the same export style and naming conventions
- `src/api/rest.ts::fetchSboms` — follow the same Axios GET pattern for the comparison function
- `src/api/client.ts` — Axios instance with base URL and auth interceptors (import and use directly)

## Acceptance Criteria
- [ ] `SbomComparison` and all sub-interfaces are exported from `src/api/models.ts`
- [ ] `fetchSbomComparison` function is exported from `src/api/rest.ts`
- [ ] `fetchSbomComparison` calls `GET /api/v2/sbom/compare` with left and right query parameters
- [ ] Function returns a typed `Promise<SbomComparison>`

## Test Requirements
- [ ] Unit test: verify `fetchSbomComparison` calls the correct URL with correct query parameters (using MSW mock handler)
- [ ] Unit test: verify the response is correctly typed

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 4 — Add GET /api/v2/sbom/compare endpoint and integration tests

[sdlc-workflow] Description digest: sha256:0e5253da872c408fb34236b655477b0e9374c1c1bf329c72d600f11d26c78b9d
