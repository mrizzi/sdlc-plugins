## Repository
trustify-ui

## Description
Add the TypeScript interfaces, API client function, and React Query hook needed for the SBOM comparison feature (TC-9003). This task creates the data-fetching layer that the comparison page UI (Task 5) will consume. It includes TypeScript types matching the backend response shape, an Axios-based API function, and a React Query hook with proper cache key management.

## Files to Modify
- `src/api/models.ts` — Add TypeScript interfaces for comparison response types: `SbomComparison`, `AddedPackage`, `RemovedPackage`, `VersionChange`, `NewVulnerability`, `ResolvedVulnerability`, `LicenseChange`
- `src/api/rest.ts` — Add `fetchSbomComparison(leftId: string, rightId: string)` API client function

## Files to Create
- `src/hooks/useSbomComparison.ts` — React Query hook: `useSbomComparison(leftId, rightId)` that calls the comparison endpoint and returns the typed response

## Implementation Notes
- Follow the existing TypeScript interface pattern in `src/api/models.ts` — interfaces should use camelCase field names matching the JSON response keys from the backend.
- Follow the existing API client function pattern in `src/api/rest.ts` — use the shared Axios instance from `src/api/client.ts` and return typed responses.
- Follow the existing React Query hook pattern in `src/hooks/useSboms.ts` and `src/hooks/useSbomById.ts` — use `useQuery` with a descriptive query key array.
- The hook should accept `leftId` and `rightId` as parameters and include both in the query key for proper cache invalidation: `["sbom-comparison", leftId, rightId]`.
- The hook should be disabled (via `enabled` option) when either `leftId` or `rightId` is undefined or empty — this prevents automatic fetching before the user selects both SBOMs.
- Use the Axios instance's base URL configuration from `src/api/client.ts` — no hardcoded URLs.

**Backend API contracts:**
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — response shape:
  ```typescript
  {
    added_packages: Array<{ name: string; version: string; license: string; advisory_count: number }>;
    removed_packages: Array<{ name: string; version: string; license: string; advisory_count: number }>;
    version_changes: Array<{ name: string; left_version: string; right_version: string; direction: "upgrade" | "downgrade" }>;
    new_vulnerabilities: Array<{ advisory_id: string; severity: string; title: string; affected_package: string }>;
    resolved_vulnerabilities: Array<{ advisory_id: string; severity: string; title: string; previously_affected_package: string }>;
    license_changes: Array<{ name: string; left_license: string; right_license: string }>;
  }
  ```
  (See `modules/fundamental/src/sbom/model/comparison.rs` in trustify-backend and `modules/fundamental/src/sbom/endpoints/compare.rs` for the backend source)

Verify these contracts against the backend repo during implementation using the implement-task cross-repo API verification step.

## Reuse Candidates
- `src/api/client.ts` — Axios instance with base URL and auth interceptors
- `src/api/rest.ts::fetchSboms()` — Reference for API function structure and error handling
- `src/hooks/useSboms.ts` — Reference for React Query hook pattern with `useQuery`
- `src/hooks/useSbomById.ts` — Reference for hook with parameter-based query key
- `src/api/models.ts` — Existing model interfaces to follow naming conventions

## Acceptance Criteria
- [ ] TypeScript interfaces for all comparison response types are defined in `src/api/models.ts`
- [ ] Interface field names and types match the backend JSON response shape exactly
- [ ] `fetchSbomComparison(leftId, rightId)` calls `GET /api/v2/sbom/compare?left={leftId}&right={rightId}` and returns typed `SbomComparison`
- [ ] `useSbomComparison` hook returns `{ data, isLoading, isError, error }` following the existing hook pattern
- [ ] Hook is disabled when either SBOM ID is missing (does not fire an API request)
- [ ] Query key includes both SBOM IDs for proper cache behavior

## Test Requirements
- [ ] Unit test: `fetchSbomComparison` makes a GET request to the correct URL with both query parameters
- [ ] Unit test: `useSbomComparison` returns loading state initially, then data on success
- [ ] Unit test: `useSbomComparison` does not fetch when `leftId` is undefined
- [ ] Unit test: `useSbomComparison` does not fetch when `rightId` is undefined

## Dependencies
- Depends on: Task 2 — Backend comparison endpoint (API contract must be available)
