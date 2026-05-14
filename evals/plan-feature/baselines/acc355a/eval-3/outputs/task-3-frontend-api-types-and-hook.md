# Task 3 — Add API types, client function, and React Query hook for SBOM comparison

## Repository
trustify-ui

## Target Branch
main

## Description
Add the TypeScript interfaces for the SBOM comparison API response, an API client function to call the backend comparison endpoint, and a React Query hook to manage the comparison data fetching lifecycle. This establishes the data layer that the comparison page UI (Task 4) will consume.

## Files to Modify
- `src/api/models.ts` — Add TypeScript interfaces for `SbomComparisonResult`, `AddedPackage`, `RemovedPackage`, `VersionChange`, `NewVulnerability`, `ResolvedVulnerability`, `LicenseChange`
- `src/api/rest.ts` — Add `fetchSbomComparison(leftId: string, rightId: string)` function

## Files to Create
- `src/hooks/useSbomComparison.ts` — React Query hook wrapping the comparison API call, enabled only when both SBOM IDs are provided

## Implementation Notes
- Follow the existing interface pattern in `src/api/models.ts` for naming and field conventions. Use snake_case field names to match the backend JSON response (the existing codebase uses snake_case in API models).
- The `fetchSbomComparison` function in `src/api/rest.ts` should follow the pattern of existing functions like `fetchSboms()` and `fetchAdvisories()` — use the shared Axios instance from `src/api/client.ts`.
- The React Query hook should follow the pattern in `src/hooks/useSbomById.ts`:
  - Accept `leftId` and `rightId` parameters
  - Use a query key like `["sbom-comparison", leftId, rightId]`
  - Set `enabled: !!(leftId && rightId)` so the query only fires when both IDs are present
  - Return the standard React Query result object (`data`, `isLoading`, `isError`, `error`)

**Backend API contracts:**
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
  (See backend endpoint in `modules/fundamental/src/sbom/endpoints/compare.rs`)

Verify these contracts against the backend repo during implementation using the implement-task cross-repo API verification step.

## Reuse Candidates
- `src/api/client.ts` — shared Axios instance with base URL and auth interceptors
- `src/api/rest.ts::fetchSboms` — follow the same pattern for the new `fetchSbomComparison` function
- `src/hooks/useSbomById.ts` — follow the same React Query hook pattern (query key structure, enabled flag, return type)
- `src/api/models.ts` — follow existing interface naming and field conventions

## Acceptance Criteria
- [ ] TypeScript interfaces exist for all six diff section item types and the top-level `SbomComparisonResult`
- [ ] `fetchSbomComparison(leftId, rightId)` function exists in `rest.ts` and calls the correct endpoint
- [ ] `useSbomComparison` hook exists and returns React Query state (data, isLoading, isError)
- [ ] Hook is disabled (does not fire) when either SBOM ID is undefined or empty
- [ ] All types are exported and usable by consumer components

## Test Requirements
- [ ] Unit test: `useSbomComparison` does not fetch when `leftId` is undefined
- [ ] Unit test: `useSbomComparison` does not fetch when `rightId` is undefined
- [ ] Unit test: `useSbomComparison` fetches and returns data when both IDs are provided (use MSW mock handler)
- [ ] Unit test: `useSbomComparison` returns error state when the API returns 404

## Dependencies
- Depends on: Task 2 — Add SBOM comparison REST endpoint and integration tests
