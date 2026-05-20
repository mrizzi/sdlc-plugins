# Task 5 — Add API types and client function for SBOM comparison

## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add TypeScript interfaces for the SBOM comparison API response and create the API client function and React Query hook. This provides the data-fetching foundation for the comparison page UI.

## Files to Modify
- `src/api/models.ts` — Add TypeScript interfaces for comparison response types
- `src/api/rest.ts` — Add `compareSboms(leftId: string, rightId: string)` API client function

## Files to Create
- `src/hooks/useSbomComparison.ts` — React Query hook wrapping the comparison API call

## Implementation Notes
- Follow the existing API type pattern in `src/api/models.ts` — add interfaces that match the backend response shape:
  - `SbomComparisonResult` with fields: `added_packages: PackageDiff[]`, `removed_packages: PackageDiff[]`, `version_changes: VersionChange[]`, `new_vulnerabilities: VulnerabilityDiff[]`, `resolved_vulnerabilities: VulnerabilityDiff[]`, `license_changes: LicenseChange[]`
  - `PackageDiff` with fields: `name: string`, `version: string`, `license: string`, `advisory_count: number`
  - `VersionChange` with fields: `name: string`, `left_version: string`, `right_version: string`, `direction: "upgrade" | "downgrade"`
  - `VulnerabilityDiff` with fields: `advisory_id: string`, `severity: string`, `title: string`, `affected_package: string` (or `previously_affected_package: string` for resolved)
  - `LicenseChange` with fields: `name: string`, `left_license: string`, `right_license: string`
- Follow the existing API client pattern in `src/api/rest.ts` — use the Axios instance from `src/api/client.ts` to make the GET request
- Follow the existing React Query hook pattern in `src/hooks/useSboms.ts` — the comparison hook should:
  - Accept `leftId` and `rightId` as parameters
  - Use `useQuery` with a query key like `["sbom-comparison", leftId, rightId]`
  - Set `enabled: !!(leftId && rightId)` so the query only runs when both IDs are provided
  - Return the standard React Query result object

### Backend API contracts
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — response shape: `SbomComparisonResult` (see `modules/fundamental/src/sbom/endpoints/compare.rs` in trustify-backend)
- Query parameters: `left` (UUID string, required), `right` (UUID string, required)
- Error responses: 400 for missing parameters, 404 for non-existent SBOM IDs

Verify these contracts against the backend repo during implementation using the implement-task cross-repo API verification step.

## Reuse Candidates
- `src/api/models.ts` — existing TypeScript interfaces to follow for naming and export patterns
- `src/api/rest.ts` — existing API client functions (e.g., `fetchSboms()`) to follow for Axios usage pattern
- `src/hooks/useSboms.ts` — existing React Query hook to follow for query key naming and hook structure
- `src/hooks/useSbomById.ts` — existing single-entity query hook to follow for parameterized queries
- `src/api/client.ts` — Axios instance with base URL and auth interceptors

## Acceptance Criteria
- [ ] TypeScript interfaces for all comparison response types added to `models.ts`
- [ ] `compareSboms(leftId, rightId)` function added to `rest.ts` using Axios client
- [ ] `useSbomComparison` hook created using React Query's `useQuery`
- [ ] Hook only fires the query when both SBOM IDs are provided
- [ ] All types are properly exported

## Test Requirements
- [ ] Unit test for `useSbomComparison` hook: verify it calls the correct endpoint with query parameters
- [ ] Unit test: verify the hook does not fire when either ID is missing (enabled: false)
- [ ] Add MSW handler for `GET /api/v2/sbom/compare` in `tests/mocks/handlers.ts` for use by other tests

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
