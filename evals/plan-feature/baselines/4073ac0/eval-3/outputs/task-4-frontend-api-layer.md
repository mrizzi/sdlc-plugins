## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add the frontend API layer for the SBOM comparison feature: TypeScript interfaces for the comparison response, an Axios client function to call the comparison endpoint, and a React Query hook to manage the query lifecycle. This task is API-plumbing only with no UI components.

## Files to Create
- `src/hooks/useSbomComparison.ts` — React Query hook that calls `fetchSbomComparison()` with `left` and `right` SBOM IDs, enabled only when both IDs are provided

## Files to Modify
- `src/api/models.ts` — Add TypeScript interfaces: `SbomComparison`, `AddedPackage`, `RemovedPackage`, `VersionChange`, `NewVulnerability`, `ResolvedVulnerability`, `LicenseChange`
- `src/api/rest.ts` — Add `fetchSbomComparison(leftId: string, rightId: string): Promise<SbomComparison>` function

## API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — CONSUME: Frontend client function for the new backend comparison endpoint

## Implementation Notes
- Follow the existing interface pattern in `src/api/models.ts` — use TypeScript interfaces (not types) with snake_case field names matching the backend JSON response.
- Follow the existing API function pattern in `src/api/rest.ts` — use the shared Axios instance from `src/api/client.ts`, return typed promises. See `fetchSboms()` as a reference.
- Follow the existing hook pattern in `src/hooks/useSboms.ts` — use `useQuery` from React Query with a descriptive query key like `["sbomComparison", leftId, rightId]`. The hook should accept `leftId` and `rightId` parameters and set `enabled: !!leftId && !!rightId` to prevent fetching until both are selected.
- The `SbomComparison` interface must match the backend response shape from `figma-context.md`:
  - `added_packages: AddedPackage[]`
  - `removed_packages: RemovedPackage[]`
  - `version_changes: VersionChange[]`
  - `new_vulnerabilities: NewVulnerability[]`
  - `resolved_vulnerabilities: ResolvedVulnerability[]`
  - `license_changes: LicenseChange[]`

## Reuse Candidates
- `src/api/client.ts` — shared Axios instance with base URL and auth interceptors
- `src/api/rest.ts::fetchSboms` — pattern for API client functions
- `src/hooks/useSboms.ts` — pattern for React Query hooks with `useQuery`
- `src/api/models.ts` — existing interface definitions for response types

## Dependencies
- Depends on: Task 3 — Backend comparison endpoint (API contract must be available)

## Acceptance Criteria
- [ ] `SbomComparison` interface and sub-interfaces are defined in `models.ts` matching the backend response shape
- [ ] `fetchSbomComparison()` calls `GET /api/v2/sbom/compare` with `left` and `right` query parameters
- [ ] `useSbomComparison` hook returns React Query result with `data`, `isLoading`, `isError` fields
- [ ] Hook does not fire the query when either SBOM ID is missing (enabled guard)

## Test Requirements
- [ ] Unit test: `useSbomComparison` hook fires query when both IDs are provided
- [ ] Unit test: `useSbomComparison` hook does not fire query when one ID is missing
- [ ] Unit test: `fetchSbomComparison` constructs the correct URL with query parameters
