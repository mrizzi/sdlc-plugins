# Task 4 -- Frontend API Types, Client Function, and React Query Hook

## Repository
trustify-ui

## Description
Add TypeScript interfaces for the SBOM comparison API response, an API client function to call the comparison endpoint, and a React Query hook to manage the comparison data fetching lifecycle. This provides the data layer that the comparison page UI will consume.

## Files to Modify
- `src/api/models.ts` -- add TypeScript interfaces for the comparison response (SbomComparisonResult, AddedPackage, RemovedPackage, VersionChange, NewVulnerability, ResolvedVulnerability, LicenseChange)
- `src/api/rest.ts` -- add `fetchSbomComparison(leftId: string, rightId: string)` function that calls `GET /api/v2/sbom/compare?left={leftId}&right={rightId}`

## Files to Create
- `src/hooks/useSbomComparison.ts` -- React Query hook wrapping the comparison API call, enabled only when both left and right IDs are provided

## Implementation Notes
- Follow the existing API type patterns in `src/api/models.ts` for interface naming and structure.
- Follow the existing API client function pattern in `src/api/rest.ts` (e.g., `fetchSboms()`) which uses the Axios instance from `src/api/client.ts`.
- Follow the existing React Query hook pattern in `src/hooks/useSboms.ts` and `src/hooks/useSbomById.ts` for hook structure (useQuery with typed return).
- The hook should accept `leftId` and `rightId` parameters and only enable the query when both are defined (use the `enabled` option in useQuery).
- Use a query key like `["sbom-comparison", leftId, rightId]` for proper cache management.

**Backend API contracts:**
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` -- response shape:
  ```typescript
  interface SbomComparisonResult {
    added_packages: AddedPackage[];
    removed_packages: RemovedPackage[];
    version_changes: VersionChange[];
    new_vulnerabilities: NewVulnerability[];
    resolved_vulnerabilities: ResolvedVulnerability[];
    license_changes: LicenseChange[];
  }
  ```
  Where:
  - `AddedPackage`: `{ name: string; version: string; license: string; advisory_count: number }`
  - `RemovedPackage`: `{ name: string; version: string; license: string; advisory_count: number }`
  - `VersionChange`: `{ name: string; left_version: string; right_version: string; direction: "upgrade" | "downgrade" }`
  - `NewVulnerability`: `{ advisory_id: string; severity: string; title: string; affected_package: string }`
  - `ResolvedVulnerability`: `{ advisory_id: string; severity: string; title: string; previously_affected_package: string }`
  - `LicenseChange`: `{ name: string; left_license: string; right_license: string }`

Verify these contracts against the backend repo during implementation using the implement-task cross-repo API verification step.

## Reuse Candidates
- `src/api/models.ts` -- existing TypeScript interfaces for API responses; follow naming convention
- `src/api/rest.ts::fetchSboms` -- existing API client function pattern to follow
- `src/api/client.ts` -- Axios instance with base URL and auth interceptors; import and use for the new endpoint call
- `src/hooks/useSboms.ts` -- React Query hook pattern for list queries
- `src/hooks/useSbomById.ts` -- React Query hook pattern with parameter-based enabling

## Acceptance Criteria
- [ ] TypeScript interfaces match the backend API response shape for all six diff categories
- [ ] API client function correctly constructs the query string with left and right parameters
- [ ] React Query hook returns typed data, loading, and error states
- [ ] Hook is disabled when either leftId or rightId is undefined
- [ ] Query key includes both SBOM IDs for correct cache invalidation

## Test Requirements
- [ ] Unit test: useSbomComparison hook returns comparison data when both IDs are provided
- [ ] Unit test: useSbomComparison hook does not fire a request when either ID is missing
- [ ] Add MSW handler in `tests/mocks/handlers.ts` for `GET /api/v2/sbom/compare` returning mock comparison data

## Dependencies
- Depends on: Task 2 -- Backend Comparison Endpoint (API contract must be finalized)
