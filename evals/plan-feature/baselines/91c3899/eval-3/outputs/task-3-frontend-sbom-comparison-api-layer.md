# Task 3 — Add SBOM comparison API layer

## Repository
trustify-ui

## Target Branch
main

## Description
Add the TypeScript interfaces for the SBOM comparison API response, the API client function to call the comparison endpoint, and the React Query hook for data fetching. This provides the data layer that the comparison page UI (Task 4) will consume.

## Files to Create
- `src/hooks/useSbomComparison.ts` — React Query hook wrapping the comparison API call; accepts left and right SBOM IDs, returns query result with comparison data

## Files to Modify
- `src/api/models.ts` — Add TypeScript interfaces: SbomComparisonResult, AddedPackage, RemovedPackage, VersionChange, NewVulnerability, ResolvedVulnerability, LicenseChange
- `src/api/rest.ts` — Add `fetchSbomComparison(leftId: string, rightId: string): Promise<SbomComparisonResult>` function

## Implementation Notes
- Follow the existing API layer pattern: types in `src/api/models.ts`, client functions in `src/api/rest.ts`, hooks in `src/hooks/`.
- See `src/hooks/useSboms.ts` for the React Query hook pattern: use `useQuery` with a query key array and the API client function as the query function.
- The hook should accept `leftId` and `rightId` parameters and only enable the query when both are non-empty (use the `enabled` option).
- Use the existing Axios instance from `src/api/client.ts` for the HTTP call.
- Per CONVENTIONS.md §API layer: Axios client in `src/api/client.ts`; typed API functions in `src/api/rest.ts`; React Query hooks in `src/hooks/`.
  Applies: task modifies `src/api/rest.ts` and creates `src/hooks/useSbomComparison.ts` matching the convention's API layer file scope.
- Per CONVENTIONS.md §State management: React Query (TanStack Query) for server state; no Redux.
  Applies: task creates `src/hooks/useSbomComparison.ts` matching the convention's hook file scope.
- Per CONVENTIONS.md §Naming: camelCase for hooks and utilities.
  Applies: task creates `src/hooks/useSbomComparison.ts` matching the convention's TypeScript file scope.

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
  Defined in `modules/fundamental/src/sbom/model/comparison.rs` (trustify-backend).

Verify these contracts against the backend repo during implementation using the implement-task cross-repo API verification step.

## Reuse Candidates
- `src/api/client.ts` — Axios instance with base URL and auth interceptors; use for the comparison API call
- `src/api/rest.ts::fetchSboms` — existing API client function demonstrating the pattern for GET requests with query parameters
- `src/hooks/useSboms.ts` — existing React Query hook demonstrating the useQuery pattern with query keys
- `src/api/models.ts` — existing TypeScript interfaces to follow the same naming and typing conventions

## Acceptance Criteria
- [ ] SbomComparisonResult and all sub-interfaces are defined in models.ts with correct field names and types
- [ ] fetchSbomComparison function calls GET /api/v2/sbom/compare with left and right query parameters
- [ ] useSbomComparison hook returns a React Query result with typed comparison data
- [ ] The hook is disabled (does not fire) when either SBOM ID is empty or undefined

## Test Requirements
- [ ] Unit test: useSbomComparison hook fires the API call when both IDs are provided (mock with MSW)
- [ ] Unit test: useSbomComparison hook does not fire when one ID is missing
- [ ] Unit test: fetchSbomComparison constructs the correct URL with query parameters

## Dependencies
- Depends on: Task 2 — Add SBOM comparison REST endpoint
