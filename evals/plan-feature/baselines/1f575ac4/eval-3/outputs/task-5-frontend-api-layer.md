## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add the TypeScript interfaces, API client function, and React Query hook for the SBOM comparison endpoint. This provides the data-fetching layer that the comparison page will consume.

## Files to Modify
- `src/api/models.ts` — add TypeScript interfaces for the comparison response
- `src/api/rest.ts` — add `fetchSbomComparison()` API client function

## Files to Create
- `src/hooks/useSbomComparison.ts` — React Query hook for the comparison endpoint

## Implementation Notes
- Add TypeScript interfaces in `src/api/models.ts` matching the backend response shape:
  - `SbomComparisonResult` with fields: `added_packages: AddedPackage[]`, `removed_packages: RemovedPackage[]`, `version_changes: VersionChange[]`, `new_vulnerabilities: NewVulnerability[]`, `resolved_vulnerabilities: ResolvedVulnerability[]`, `license_changes: LicenseChange[]`
  - `AddedPackage` / `RemovedPackage`: `name: string`, `version: string`, `license: string`, `advisory_count: number`
  - `VersionChange`: `name: string`, `left_version: string`, `right_version: string`, `direction: "upgrade" | "downgrade"`
  - `NewVulnerability` / `ResolvedVulnerability`: `advisory_id: string`, `severity: string`, `title: string`, `affected_package: string` (or `previously_affected_package` for resolved)
  - `LicenseChange`: `name: string`, `left_license: string`, `right_license: string`
- Add `fetchSbomComparison(leftId: string, rightId: string)` in `src/api/rest.ts` following the pattern of existing functions like `fetchSboms()`. Use the Axios client from `src/api/client.ts`.
- Create `useSbomComparison` hook in `src/hooks/useSbomComparison.ts` following the pattern in `src/hooks/useSboms.ts` and `src/hooks/useSbomById.ts`. Use `useQuery` with the query key `["sbom-comparison", leftId, rightId]`. The hook should be disabled when either ID is undefined (use the `enabled` option).
- Follow the existing mutation pattern from `src/hooks/useDeleteSbomMutation.ts` for reference on React Query patterns used in this project.

**Backend API contracts:**
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — response shape: `SbomComparisonResult` (see Task 2 for full struct definition). Defined in `modules/fundamental/src/sbom/endpoints/compare.rs` in the backend.

Verify these contracts against the backend repo during implementation using the implement-task cross-repo API verification step.

## Reuse Candidates
- `src/api/models.ts` — existing TypeScript interfaces for API types; extend with comparison types
- `src/api/rest.ts` — existing API client functions (`fetchSboms`, etc.); follow the same pattern
- `src/api/client.ts` — Axios instance with auth interceptors; use for the comparison API call
- `src/hooks/useSboms.ts` — React Query hook pattern to follow for `useSbomComparison`
- `src/hooks/useSbomById.ts` — hook pattern with single-entity query key

## Acceptance Criteria
- [ ] TypeScript interfaces for `SbomComparisonResult` and all sub-types are defined in `models.ts`
- [ ] `fetchSbomComparison()` function calls the correct endpoint with query parameters
- [ ] `useSbomComparison` hook returns loading, error, and data states
- [ ] Hook is disabled when either SBOM ID is not provided

## Test Requirements
- [ ] Unit test: verify `useSbomComparison` hook returns expected data shape when API responds successfully
- [ ] Unit test: verify hook is disabled when IDs are undefined
- [ ] Add MSW handler in `tests/mocks/handlers.ts` for `GET /api/v2/sbom/compare`
- [ ] Add comparison fixture data in `tests/mocks/fixtures/`

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003
