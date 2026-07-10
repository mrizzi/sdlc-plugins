## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add TypeScript interfaces for the SBOM comparison API response, a client function to call the comparison endpoint, and a React Query hook for data fetching. This establishes the API layer that the comparison page (Task 5) will consume. The interfaces must match the backend response shape from the `GET /api/v2/sbom/compare` endpoint created in Task 3.

## Files to Modify
- `src/api/models.ts` — Add TypeScript interfaces: `SbomComparisonResult`, `AddedPackage`, `RemovedPackage`, `VersionChange`, `NewVulnerability`, `ResolvedVulnerability`, `LicenseChange`
- `src/api/rest.ts` — Add `fetchSbomComparison(leftId: string, rightId: string): Promise<SbomComparisonResult>` function

## Files to Create
- `src/hooks/useSbomComparison.ts` — React Query hook wrapping `fetchSbomComparison` with `useQuery`

## Implementation Notes
Follow the existing API layer pattern:
1. Add interfaces in `src/api/models.ts` following the naming and structure conventions used by existing interfaces in that file
2. Add the client function in `src/api/rest.ts` following the pattern of `fetchSboms()` and other existing functions that use the Axios instance from `src/api/client.ts`
3. Create the React Query hook in `src/hooks/useSbomComparison.ts` following the pattern of `src/hooks/useSbomById.ts` (single-resource query with parameters)

The hook should:
- Accept `leftId` and `rightId` as parameters
- Use a query key like `["sbomComparison", leftId, rightId]`
- Only enable the query when both IDs are provided (`enabled: !!leftId && !!rightId`)
- Return the standard `useQuery` result with typed `SbomComparisonResult` data

Per CONVENTIONS.md: use React Query (TanStack Query) for server state management; no Redux.
Applies: task creates `src/hooks/useSbomComparison.ts` matching the convention's `.ts` hook file scope.

Per CONVENTIONS.md: API layer follows Axios client in `client.ts`, typed functions in `rest.ts`, hooks in `hooks/`.
Applies: task modifies `src/api/rest.ts` and creates `src/hooks/useSbomComparison.ts` matching the convention's `.ts` API layer scope.

Per CONVENTIONS.md: naming convention uses camelCase for hooks and utilities.
Applies: task creates `src/hooks/useSbomComparison.ts` matching the convention's `.ts` file scope.

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
  (see `modules/fundamental/src/sbom/model/comparison.rs` in trustify-backend and `modules/fundamental/src/sbom/endpoints/compare.rs` for the endpoint definition)

Verify these contracts against the backend repo during implementation using the implement-task cross-repo API verification step.

## Reuse Candidates
- `src/api/rest.ts::fetchSboms` — Existing API client function; follow the same Axios call pattern for the comparison endpoint
- `src/hooks/useSbomById.ts` — Existing React Query hook for single-resource fetch; follow the same `useQuery` pattern with typed parameters
- `src/hooks/useSboms.ts` — Reference for query key naming and hook structure
- `src/api/client.ts` — Axios instance with base URL and auth interceptors; import and use for the comparison API call

## Acceptance Criteria
- [ ] `SbomComparisonResult` interface and all sub-interfaces are defined in `src/api/models.ts`
- [ ] `fetchSbomComparison` function calls `GET /api/v2/sbom/compare` with correct query parameters
- [ ] `useSbomComparison` hook returns typed `SbomComparisonResult` data
- [ ] Hook is disabled when either SBOM ID is not provided

## Test Requirements
- [ ] Unit test: `useSbomComparison` hook calls the correct endpoint with both IDs
- [ ] Unit test: hook is disabled when either ID is missing
- [ ] Add MSW handler for `GET /api/v2/sbom/compare` in `tests/mocks/handlers.ts`
- [ ] Add mock comparison fixture data in `tests/mocks/fixtures/`

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 3 — Add SBOM comparison endpoint and integration tests (backend endpoint must exist for API contract verification)
