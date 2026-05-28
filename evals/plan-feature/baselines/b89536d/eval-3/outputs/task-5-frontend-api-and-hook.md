# Task 5 — Add comparison API client function and React Query hook

## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add the TypeScript interfaces for the comparison API response, the API client function to call the backend comparison endpoint, and a React Query hook to manage the comparison data fetching lifecycle. This establishes the data layer that the comparison page (Task 6) will consume.

## Files to Modify
- `src/api/models.ts` — Add TypeScript interfaces: `SbomComparison`, `AddedPackage`, `RemovedPackage`, `VersionChange`, `NewVulnerability`, `ResolvedVulnerability`, `LicenseChange`
- `src/api/rest.ts` — Add `compareSboms(leftId: string, rightId: string): Promise<SbomComparison>` function using the Axios client

## Files to Create
- `src/hooks/useSbomComparison.ts` — React Query hook `useSbomComparison(leftId: string | undefined, rightId: string | undefined)` that calls `compareSboms` and returns query state; enabled only when both IDs are defined

## Implementation Notes
- Follow the existing API type pattern in `src/api/models.ts` — interfaces use PascalCase names and camelCase fields matching the JSON response shape (the backend returns snake_case; the Axios client or a transformer should handle the mapping, or use exact snake_case field names to match the API).
- Follow the existing API function pattern in `src/api/rest.ts` — functions like `fetchSboms()` use the Axios instance from `src/api/client.ts`. The new function should be: `export const compareSboms = (leftId: string, rightId: string) => client.get<SbomComparison>("/api/v2/sbom/compare", { params: { left: leftId, right: rightId } }).then(res => res.data);`
- Follow the existing React Query hook pattern in `src/hooks/useSboms.ts` and `src/hooks/useSbomById.ts` — use `useQuery` with a descriptive query key (e.g., `["sbom-comparison", leftId, rightId]`). Set `enabled: !!leftId && !!rightId` so the query only fires when both IDs are provided.
- The hook should return the standard React Query result object (`data`, `isLoading`, `isError`, `error`).

### Backend API contracts
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — response shape:
  ```json
  {
    "added_packages": [{ "name": "string", "version": "string", "license": "string", "advisory_count": 0 }],
    "removed_packages": [{ "name": "string", "version": "string", "license": "string", "advisory_count": 0 }],
    "version_changes": [{ "name": "string", "left_version": "string", "right_version": "string", "direction": "upgrade|downgrade" }],
    "new_vulnerabilities": [{ "advisory_id": "string", "severity": "critical|high|medium|low", "title": "string", "affected_package": "string" }],
    "resolved_vulnerabilities": [{ "advisory_id": "string", "severity": "string", "title": "string", "previously_affected_package": "string" }],
    "license_changes": [{ "name": "string", "left_license": "string", "right_license": "string" }]
  }
  ```
  (See `modules/fundamental/src/sbom/model/comparison.rs` in trustify-backend and `modules/fundamental/src/sbom/endpoints/compare.rs` for endpoint definition)

Verify these contracts against the backend repo during implementation using the implement-task cross-repo API verification step.

## Reuse Candidates
- `src/api/rest.ts::fetchSboms` — existing API client function demonstrating the Axios call pattern for SBOM endpoints
- `src/hooks/useSboms.ts` — existing React Query hook demonstrating the useQuery pattern with query key conventions
- `src/hooks/useSbomById.ts` — existing React Query hook for fetching a single SBOM by ID, demonstrating the enabled-flag pattern
- `src/api/client.ts` — Axios instance with base URL and auth interceptors

## Acceptance Criteria
- [ ] TypeScript interfaces for the comparison response are defined in `models.ts`
- [ ] `compareSboms` function is exported from `rest.ts` and calls the correct endpoint with query params
- [ ] `useSbomComparison` hook uses React Query and is only enabled when both IDs are defined
- [ ] Hook returns standard React Query state (`data`, `isLoading`, `isError`)
- [ ] TypeScript compiles without type errors

## Test Requirements
- [ ] Unit test for `useSbomComparison` hook: verify it calls `compareSboms` with correct parameters when both IDs are provided
- [ ] Unit test: verify hook does not fire when either ID is undefined
- [ ] Add MSW handler in `tests/mocks/handlers.ts` for `GET /api/v2/sbom/compare` returning mock comparison data

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
