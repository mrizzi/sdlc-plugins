# Task 5 — Add SBOM comparison API types, client function, and React Query hook

## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add the TypeScript interfaces for the SBOM comparison API response, the API client function to call the comparison endpoint, and a React Query hook to manage the comparison data fetching lifecycle. This provides the data layer that the comparison page will consume.

## Files to Modify
- `src/api/models.ts` — Add TypeScript interfaces for `SbomComparisonResult`, `AddedPackage`, `RemovedPackage`, `VersionChange`, `NewVulnerability`, `ResolvedVulnerability`, `LicenseChange`
- `src/api/rest.ts` — Add `fetchSbomComparison(leftId: string, rightId: string)` API client function

## Files to Create
- `src/hooks/useSbomComparison.ts` — React Query hook wrapping the comparison API call, accepting left and right SBOM IDs

## Implementation Notes
- Follow the existing API type pattern in `src/api/models.ts` — define interfaces with camelCase property names matching the snake_case JSON response (the Axios client or a response transformer handles the mapping, or use the exact backend field names if the codebase uses snake_case in TS interfaces).
- Follow the existing API client function pattern in `src/api/rest.ts` — see `fetchSboms()` as a reference. The comparison function should call `GET /api/v2/sbom/compare?left=${leftId}&right=${rightId}` using the Axios instance from `src/api/client.ts`.
- Follow the existing React Query hook pattern in `src/hooks/useSboms.ts` — use `useQuery` with a query key like `["sbom-comparison", leftId, rightId]`. The hook should be disabled (via `enabled` option) when either ID is missing/empty.
- The hook should return the standard React Query result (data, isLoading, isError, error).

**Backend API contracts:**
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — response shape:
  ```json
  {
    "added_packages": [{ "name": "string", "version": "string", "license": "string", "advisory_count": 0 }],
    "removed_packages": [{ "name": "string", "version": "string", "license": "string", "advisory_count": 0 }],
    "version_changes": [{ "name": "string", "left_version": "string", "right_version": "string", "direction": "upgrade|downgrade" }],
    "new_vulnerabilities": [{ "advisory_id": "string", "severity": "string", "title": "string", "affected_package": "string" }],
    "resolved_vulnerabilities": [{ "advisory_id": "string", "severity": "string", "title": "string", "previously_affected_package": "string" }],
    "license_changes": [{ "name": "string", "left_license": "string", "right_license": "string" }]
  }
  ```
  Source: `modules/fundamental/src/sbom/model/comparison.rs` and `modules/fundamental/src/sbom/endpoints/compare.rs` in trustify-backend.

Verify these contracts against the backend repo during implementation using the implement-task cross-repo API verification step.

## Reuse Candidates
- `src/api/rest.ts::fetchSboms` — existing API client function pattern to follow
- `src/hooks/useSboms.ts` — existing React Query hook pattern to follow for query key structure and options
- `src/api/client.ts` — Axios instance with base URL and auth interceptors

## Acceptance Criteria
- [ ] TypeScript interfaces for all comparison response types are defined in `src/api/models.ts`
- [ ] `fetchSbomComparison(leftId, rightId)` function exists in `src/api/rest.ts` and calls the correct endpoint
- [ ] `useSbomComparison` hook exists and returns React Query result with loading/error/data states
- [ ] Hook is disabled when either SBOM ID is empty or undefined
- [ ] TypeScript compiles with no type errors

## Test Requirements
- [ ] Unit test: `useSbomComparison` hook returns comparison data when both IDs are provided (using MSW mock handler)
- [ ] Unit test: hook is disabled and does not fire a request when IDs are missing
- [ ] Add MSW handler for `GET /api/v2/sbom/compare` in `tests/mocks/handlers.ts`

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
