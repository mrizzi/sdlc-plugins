## Repository
trustify-ui

## Description
Add TypeScript interfaces for the SBOM comparison API response and create the API client function and React Query hook that the comparison page will use. This establishes the data-fetching layer so the UI components (Task 5) can consume comparison data through the standard hook pattern used throughout the application.

## Files to Modify
- `src/api/models.ts` -- Add TypeScript interfaces for the comparison response: `SbomComparison`, `AddedPackage`, `RemovedPackage`, `VersionChange`, `VulnerabilityDiff`, `ResolvedVulnerability`, `LicenseChange`
- `src/api/rest.ts` -- Add `fetchSbomComparison(leftId: string, rightId: string)` function that calls `GET /api/v2/sbom/compare?left={leftId}&right={rightId}`

## Files to Create
- `src/hooks/useSbomComparison.ts` -- React Query hook: `useSbomComparison(leftId: string | undefined, rightId: string | undefined)` that returns the comparison data, loading state, and error

## Implementation Notes
- Define interfaces in `src/api/models.ts` following the existing patterns (e.g., the interfaces already in that file for SBOM and Advisory types). The field names must match the backend JSON contract exactly:
  ```typescript
  interface SbomComparison {
    added_packages: AddedPackage[];
    removed_packages: RemovedPackage[];
    version_changes: VersionChange[];
    new_vulnerabilities: VulnerabilityDiff[];
    resolved_vulnerabilities: ResolvedVulnerability[];
    license_changes: LicenseChange[];
  }
  ```
- In `src/api/rest.ts`, add the fetch function following the pattern of existing functions like `fetchSboms()`. Use the Axios client from `src/api/client.ts`:
  ```typescript
  export const fetchSbomComparison = (leftId: string, rightId: string): Promise<SbomComparison> =>
    client.get(`/api/v2/sbom/compare`, { params: { left: leftId, right: rightId } }).then(res => res.data);
  ```
- In the React Query hook (`src/hooks/useSbomComparison.ts`), follow the pattern from `src/hooks/useSbomById.ts`:
  - Use `useQuery` with a query key like `["sbom-comparison", leftId, rightId]`
  - Only enable the query when both `leftId` and `rightId` are defined (`enabled: !!leftId && !!rightId`)
  - Return the standard React Query result object

## Reuse Candidates
- `src/api/client.ts` -- Axios instance with base URL and auth interceptors
- `src/api/rest.ts` -- Existing API functions as pattern reference (e.g., `fetchSboms`)
- `src/hooks/useSbomById.ts` -- React Query hook pattern with conditional enabling
- `src/hooks/useSboms.ts` -- React Query hook pattern for list data

## Acceptance Criteria
- [ ] `SbomComparison` and all child interfaces are defined in `src/api/models.ts` with field names matching the backend JSON contract
- [ ] `fetchSbomComparison` function exists in `src/api/rest.ts` and calls the correct endpoint with query parameters
- [ ] `useSbomComparison` hook exists in `src/hooks/useSbomComparison.ts` and returns React Query result
- [ ] Hook is disabled when either SBOM ID is undefined (does not fire an API request)
- [ ] All types are properly exported

## Test Requirements
- [ ] Unit test: `useSbomComparison` does not fetch when `leftId` is undefined
- [ ] Unit test: `useSbomComparison` does not fetch when `rightId` is undefined
- [ ] Unit test: `useSbomComparison` fetches and returns parsed comparison data when both IDs are provided (using MSW mock)

## Dependencies
- Depends on: Task 3 -- Add comparison REST endpoint and integration tests (the backend endpoint must exist for the frontend to call it)
