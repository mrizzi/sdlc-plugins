# Task 4 — Frontend API client and React Query hook for SBOM comparison

## Repository
trustify-ui

## Description
Add the TypeScript interfaces, API client function, and React Query hook needed to call the backend SBOM comparison endpoint. This provides the data-fetching layer that the comparison page UI (Task 5) will consume.

## Files to Modify
- `src/api/models.ts` — add TypeScript interfaces for the comparison response
- `src/api/rest.ts` — add `compareSboms()` API client function

## Files to Create
- `src/hooks/useSbomComparison.ts` — React Query hook wrapping the comparison API call

## API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — CONSUMED: frontend calls this new backend endpoint

## Implementation Notes
- **TypeScript interfaces** in `src/api/models.ts` — add interfaces matching the backend response shape:
  ```
  SbomComparisonResult {
    added_packages: PackageDiff[]
    removed_packages: PackageDiff[]
    version_changes: VersionChange[]
    new_vulnerabilities: VulnerabilityDiff[]
    resolved_vulnerabilities: VulnerabilityDiff[]
    license_changes: LicenseChange[]
  }
  ```
  Plus sub-types: `PackageDiff` (name, version, license, advisory_count), `VersionChange` (name, left_version, right_version, direction), `VulnerabilityDiff` (advisory_id, severity, title, affected_package/previously_affected_package), `LicenseChange` (name, left_license, right_license).
- **API client function** in `src/api/rest.ts` — follow the pattern of existing functions like `fetchSboms()`. Use the Axios instance from `src/api/client.ts`. Function signature: `compareSboms(leftId: string, rightId: string): Promise<SbomComparisonResult>`.
- **React Query hook** in `src/hooks/useSbomComparison.ts` — follow the pattern in `src/hooks/useSboms.ts` and `src/hooks/useSbomById.ts`. Use `useQuery` with a query key like `["sbom-comparison", leftId, rightId]`. The hook should:
  - Accept `leftId` and `rightId` parameters
  - Only enable the query when both IDs are provided (use `enabled: !!leftId && !!rightId`)
  - Return the standard React Query result object

- **Backend API contracts:**
  - `GET /api/v2/sbom/compare?left={id1}&right={id2}` — response shape: `SbomComparisonResult` as defined above (see `modules/fundamental/src/sbom/model/comparison.rs` in trustify-backend)
  - Verify these contracts against the backend repo during implementation using the implement-task cross-repo API verification step.

## Reuse Candidates
- `src/api/rest.ts::fetchSboms` — existing API client function pattern to follow for `compareSboms`
- `src/api/client.ts` — Axios instance with base URL and auth interceptors
- `src/hooks/useSboms.ts` — React Query hook pattern to follow for `useSbomComparison`
- `src/hooks/useSbomById.ts` — React Query hook pattern for single-resource queries with dynamic ID parameter
- `src/api/models.ts` — existing TypeScript interface definitions to extend

## Acceptance Criteria
- [ ] `SbomComparisonResult` and all sub-type interfaces are defined in `src/api/models.ts`
- [ ] `compareSboms(leftId, rightId)` function is exported from `src/api/rest.ts`
- [ ] `useSbomComparison` hook is exported from `src/hooks/useSbomComparison.ts`
- [ ] Hook is disabled when either ID is missing (no unnecessary API calls)
- [ ] Hook uses appropriate query key for caching (`["sbom-comparison", leftId, rightId]`)

## Test Requirements
- [ ] Unit test: `compareSboms` calls the correct endpoint with query parameters
- [ ] Unit test: `useSbomComparison` returns loading state when query is in flight
- [ ] Unit test: `useSbomComparison` returns data when query succeeds
- [ ] Unit test: `useSbomComparison` is disabled when leftId or rightId is undefined

## Dependencies
- Depends on: Task 1 — Backend comparison model and service (for API contract definition)
