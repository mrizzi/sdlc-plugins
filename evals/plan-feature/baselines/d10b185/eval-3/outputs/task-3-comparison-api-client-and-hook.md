# Task 3 — Add comparison API client, TypeScript types, and React Query hook

## Repository
trustify-ui

## Target Branch
main

## Description
Add the frontend API layer for the SBOM comparison feature: TypeScript interfaces for the comparison response shape, an API client function to call the backend comparison endpoint, and a React Query hook that components can use to trigger and cache comparison results. This task establishes the data-fetching foundation that the comparison page (Task 4) will consume.

## Files to Modify
- `src/api/models.ts` — Add TypeScript interfaces for the comparison response: `SbomComparison`, `AddedPackage`, `RemovedPackage`, `VersionChange`, `NewVulnerability`, `ResolvedVulnerability`, `LicenseChange`
- `src/api/rest.ts` — Add `fetchSbomComparison(leftId: string, rightId: string): Promise<SbomComparison>` API client function

## Files to Create
- `src/hooks/useSbomComparison.ts` — React Query hook `useSbomComparison(leftId: string | undefined, rightId: string | undefined)` that calls `fetchSbomComparison` and returns query state

## Implementation Notes
- **TypeScript interfaces**: Define in `src/api/models.ts` alongside existing interfaces. Follow the naming convention of existing interfaces in that file (e.g., `SbomSummary`, `AdvisoryDetails`). The `SbomComparison` interface must match the backend response shape:
  ```typescript
  interface SbomComparison {
    added_packages: AddedPackage[];
    removed_packages: RemovedPackage[];
    version_changes: VersionChange[];
    new_vulnerabilities: NewVulnerability[];
    resolved_vulnerabilities: ResolvedVulnerability[];
    license_changes: LicenseChange[];
  }
  ```
- **API client function**: Add to `src/api/rest.ts` following the pattern of existing functions like `fetchSboms()`. Use the Axios instance from `src/api/client.ts`. The function calls `GET /api/v2/sbom/compare?left={leftId}&right={rightId}`.
- **React Query hook**: Follow the pattern in `src/hooks/useSboms.ts` and `src/hooks/useSbomById.ts`. Use `useQuery` with a query key like `["sbomComparison", leftId, rightId]`. The hook should be `enabled` only when both `leftId` and `rightId` are defined, so the query does not fire until the user clicks Compare.
- Per frontend conventions: React Query for server state (no Redux), camelCase for hooks, Axios client for HTTP calls.

**Backend API contracts:**
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — response shape: `SbomComparison` with fields `added_packages`, `removed_packages`, `version_changes`, `new_vulnerabilities`, `resolved_vulnerabilities`, `license_changes` (see `modules/fundamental/src/sbom/endpoints/compare.rs` in trustify-backend)
- Verify these contracts against the backend repo during implementation using the implement-task cross-repo API verification step.

## Reuse Candidates
- `src/api/rest.ts::fetchSboms` — existing API client function pattern to follow for the new `fetchSbomComparison`
- `src/api/client.ts` — Axios instance with base URL and auth interceptors, used by all API functions
- `src/api/models.ts` — existing TypeScript interfaces to follow for naming and structure conventions
- `src/hooks/useSboms.ts` — React Query hook pattern to follow for `useSbomComparison`
- `src/hooks/useSbomById.ts` — React Query hook pattern for single-entity queries with conditional enabling

## Acceptance Criteria
- [ ] `SbomComparison` and all sub-interfaces are defined in `src/api/models.ts` matching the backend response shape
- [ ] `fetchSbomComparison(leftId, rightId)` function exists in `src/api/rest.ts` and calls the correct endpoint
- [ ] `useSbomComparison` hook returns React Query state (data, isLoading, isError) and only fires when both IDs are provided
- [ ] Hook uses a descriptive query key that includes both SBOM IDs for proper cache invalidation

## Test Requirements
- [ ] Unit test: `fetchSbomComparison` calls the correct URL with query parameters (mock Axios)
- [ ] Unit test: `useSbomComparison` hook does not fire query when either ID is undefined
- [ ] Unit test: `useSbomComparison` hook fires query and returns data when both IDs are provided (MSW mock)

## Dependencies
- Depends on: Task 2 — Add SBOM comparison REST endpoint with integration tests
