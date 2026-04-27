# Task 3 — Frontend: Add comparison API types, client function, and React Query hook

## Repository
trustify-ui

## Description
Add the TypeScript interfaces for the SBOM comparison API response, an Axios client function to call the comparison endpoint, and a React Query hook that manages the comparison query lifecycle (loading, error, data). This provides the data-fetching foundation that the comparison page UI (Task 4) will consume.

## Files to Modify
- `src/api/models.ts` — add TypeScript interfaces for the comparison response
- `src/api/rest.ts` — add `compareSboms(leftId: string, rightId: string)` function

## Files to Create
- `src/hooks/useSbomComparison.ts` — React Query hook wrapping the comparison API call

## Implementation Notes
- Add the following interfaces to `src/api/models.ts`, matching the backend API response shape:
  - `SbomComparisonResult` with fields: `added_packages: AddedPackage[]`, `removed_packages: RemovedPackage[]`, `version_changes: VersionChange[]`, `new_vulnerabilities: NewVulnerability[]`, `resolved_vulnerabilities: ResolvedVulnerability[]`, `license_changes: LicenseChange[]`
  - `AddedPackage` with fields: `name: string`, `version: string`, `license: string`, `advisory_count: number`
  - `RemovedPackage` with fields: `name: string`, `version: string`, `license: string`, `advisory_count: number`
  - `VersionChange` with fields: `name: string`, `left_version: string`, `right_version: string`, `direction: "upgrade" | "downgrade"`
  - `NewVulnerability` with fields: `advisory_id: string`, `severity: string`, `title: string`, `affected_package: string`
  - `ResolvedVulnerability` with fields: `advisory_id: string`, `severity: string`, `title: string`, `previously_affected_package: string`
  - `LicenseChange` with fields: `name: string`, `left_license: string`, `right_license: string`
- In `src/api/rest.ts`, add a function following the pattern of existing functions (e.g., `fetchSboms()`). Use the Axios instance from `src/api/client.ts`. The function should call `GET /api/v2/sbom/compare?left=${leftId}&right=${rightId}` and return the typed response.
- In `src/hooks/useSbomComparison.ts`, follow the pattern of `src/hooks/useSbomById.ts` — use `useQuery` from React Query (TanStack Query). The hook should accept `leftId` and `rightId` parameters and only enable the query when both are provided (use the `enabled` option).
- Per project conventions: camelCase for hooks and utilities, PascalCase for type interfaces.

**Backend API contracts:**
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — response shape: `SbomComparisonResult` as defined above (see `modules/fundamental/src/sbom/endpoints/compare.rs` in trustify-backend)
- Verify these contracts against the backend repo during implementation using the implement-task cross-repo API verification step.

## Reuse Candidates
- `src/api/models.ts` — existing interfaces for SBOM and advisory types; follow the same naming and export patterns
- `src/api/rest.ts` — existing API client functions (`fetchSboms`, etc.); follow the same Axios usage pattern
- `src/api/client.ts` — Axios instance with base URL and auth interceptors; import and use for the comparison call
- `src/hooks/useSbomById.ts` — existing React Query hook pattern with `useQuery`; replicate for comparison
- `src/hooks/useSboms.ts` — another React Query hook example; shows list query pattern

## Acceptance Criteria
- [ ] TypeScript interfaces for all comparison response types are defined and exported from `src/api/models.ts`
- [ ] `compareSboms(leftId, rightId)` function is exported from `src/api/rest.ts` and calls the correct endpoint
- [ ] `useSbomComparison(leftId, rightId)` hook is exported from `src/hooks/useSbomComparison.ts`
- [ ] Hook returns `{ data, isLoading, isError, error }` matching React Query conventions
- [ ] Hook is disabled (does not fire) when either `leftId` or `rightId` is undefined/empty

## Test Requirements
- [ ] Unit test: `compareSboms` calls the correct endpoint URL with left and right query params
- [ ] Unit test: `useSbomComparison` returns loading state initially when both IDs are provided
- [ ] Unit test: `useSbomComparison` does not fire query when leftId is missing
- [ ] Unit test: `useSbomComparison` does not fire query when rightId is missing
- [ ] Unit test: `useSbomComparison` returns data on successful API response (using MSW mock)

## Dependencies
- Depends on: Task 2 — Backend: Add SBOM comparison endpoint and integration tests
