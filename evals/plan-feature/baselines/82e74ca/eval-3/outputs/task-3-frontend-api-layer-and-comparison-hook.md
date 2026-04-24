# Task 3 — Frontend API layer, types, and React Query hook for SBOM comparison

## Repository
trustify-ui

## Description
Add the TypeScript type definitions for the SBOM comparison API response, the API client function to call the backend comparison endpoint, and a React Query hook that frontend components will use to fetch comparison results. This task establishes the data-fetching layer that the comparison page (Task 4) will consume.

## Files to Modify
- `src/api/models.ts` — add TypeScript interfaces for the comparison response shape
- `src/api/rest.ts` — add `compareSboms(leftId: string, rightId: string)` API client function

## Files to Create
- `src/hooks/useSbomComparison.ts` — React Query hook wrapping the comparison API call

## API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — CONSUME: frontend calls this new backend endpoint

## Implementation Notes
- Add the following TypeScript interfaces to `src/api/models.ts`, matching the backend response shape exactly:
  - `SbomComparisonResult` with fields: `added_packages: AddedPackage[]`, `removed_packages: RemovedPackage[]`, `version_changes: VersionChange[]`, `new_vulnerabilities: NewVulnerability[]`, `resolved_vulnerabilities: ResolvedVulnerability[]`, `license_changes: LicenseChange[]`
  - `AddedPackage` with fields: `name: string`, `version: string`, `license: string`, `advisory_count: number`
  - `RemovedPackage` with fields: `name: string`, `version: string`, `license: string`, `advisory_count: number`
  - `VersionChange` with fields: `name: string`, `left_version: string`, `right_version: string`, `direction: "upgrade" | "downgrade"`
  - `NewVulnerability` with fields: `advisory_id: string`, `severity: string`, `title: string`, `affected_package: string`
  - `ResolvedVulnerability` with fields: `advisory_id: string`, `severity: string`, `title: string`, `previously_affected_package: string`
  - `LicenseChange` with fields: `name: string`, `left_license: string`, `right_license: string`
- The API client function in `src/api/rest.ts` should follow the pattern of existing functions (e.g., `fetchSboms()`). Use the Axios instance from `src/api/client.ts` and call `GET /api/v2/sbom/compare` with `left` and `right` as query parameters.
- The React Query hook `useSbomComparison` should follow the pattern in `src/hooks/useSboms.ts` and `src/hooks/useSbomById.ts` — use `useQuery` with a query key like `["sbom-comparison", leftId, rightId]`. The hook should accept `leftId` and `rightId` as parameters and enable the query only when both IDs are provided (use the `enabled` option).
- Use camelCase for TypeScript interface field names consistent with project conventions. The API returns snake_case — the Axios response interceptor or manual mapping may be needed. Check `src/api/client.ts` for existing conventions on case transformation.

**Backend API contracts:**
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — response shape:
  ```json
  {
    "added_packages": [{ "name": "...", "version": "...", "license": "...", "advisory_count": 0 }],
    "removed_packages": [{ "name": "...", "version": "...", "license": "...", "advisory_count": 0 }],
    "version_changes": [{ "name": "...", "left_version": "...", "right_version": "...", "direction": "upgrade" }],
    "new_vulnerabilities": [{ "advisory_id": "...", "severity": "critical", "title": "...", "affected_package": "..." }],
    "resolved_vulnerabilities": [{ "advisory_id": "...", "severity": "...", "title": "...", "previously_affected_package": "..." }],
    "license_changes": [{ "name": "...", "left_license": "...", "right_license": "..." }]
  }
  ```
  (See `modules/fundamental/src/sbom/model/comparison.rs` in trustify-backend for the struct definitions.)

Verify these contracts against the backend repo during implementation using the implement-task cross-repo API verification step.

## Reuse Candidates
- `src/api/rest.ts` — existing API functions (e.g., `fetchSboms()`) for client function pattern reference
- `src/api/client.ts` — existing Axios instance with base URL and auth interceptors
- `src/api/models.ts` — existing TypeScript interfaces for API types; add new interfaces alongside existing ones
- `src/hooks/useSboms.ts` — existing React Query hook for SBOM list; follow this pattern for query key and options
- `src/hooks/useSbomById.ts` — existing React Query hook for single SBOM fetch; follow this pattern for ID-parameterized queries

## Acceptance Criteria
- [ ] TypeScript interfaces for `SbomComparisonResult` and all sub-types are defined in `src/api/models.ts`
- [ ] `compareSboms(leftId, rightId)` function exists in `src/api/rest.ts` and calls `GET /api/v2/sbom/compare` with correct query parameters
- [ ] `useSbomComparison(leftId, rightId)` hook exists in `src/hooks/useSbomComparison.ts` and returns `useQuery` result
- [ ] Hook disables the query when either `leftId` or `rightId` is not provided (no API call made)
- [ ] TypeScript interfaces match the backend response shape exactly

## Test Requirements
- [ ] Unit test: `useSbomComparison` hook returns data when both IDs are provided and API responds successfully
- [ ] Unit test: `useSbomComparison` hook does not fire a request when `leftId` is undefined
- [ ] Unit test: `useSbomComparison` hook does not fire a request when `rightId` is undefined
- [ ] Unit test: `compareSboms()` API function calls the correct endpoint with correct query parameters

## Dependencies
- Depends on: Task 2 — Backend SBOM comparison endpoint (the API must exist for contract verification, though development can proceed in parallel using the documented response shape)
