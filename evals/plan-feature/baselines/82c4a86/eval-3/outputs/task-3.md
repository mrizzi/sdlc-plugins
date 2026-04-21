# Task 3 — Add comparison API client and React Query hook

## Repository
trustify-ui

## Description
Add the TypeScript interfaces for the SBOM comparison API response, the API client function to call the backend comparison endpoint, and a React Query hook to manage the comparison query lifecycle. This provides the data layer that the comparison page UI (Task 4) will consume.

## Files to Modify
- `src/api/models.ts` — add TypeScript interfaces for comparison response types
- `src/api/rest.ts` — add `fetchSbomComparison(leftId, rightId)` function

## Files to Create
- `src/hooks/useSbomComparison.ts` — React Query hook wrapping the comparison API call

## Implementation Notes
- Add interfaces in `src/api/models.ts` following the existing pattern (see `SbomSummary`, `AdvisorySummary` interfaces in that file). The comparison response shape from the backend is:
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
- Add sub-interfaces for each diff category matching the backend JSON shape (see figma-context.md for field names).
- In `src/api/rest.ts`, add `fetchSbomComparison` using the existing Axios instance from `src/api/client.ts`. Follow the pattern of existing functions like `fetchSboms()`.
- The React Query hook in `useSbomComparison.ts` should follow the existing hook pattern (see `src/hooks/useSboms.ts` and `src/hooks/useSbomById.ts`). Use `useQuery` with a query key like `["sbom-comparison", leftId, rightId]`. The query should be disabled when either ID is missing (use the `enabled` option).
- Per constraints (5.4): reuse the Axios client instance from `src/api/client.ts` — do not create a new HTTP client.

**Backend API contracts:**
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — response shape: `SbomComparisonResult` as defined above (see `modules/fundamental/src/sbom/endpoints/compare.rs` in trustify-backend)
- Verify these contracts against the backend repo during implementation using the implement-task cross-repo API verification step.

## Reuse Candidates
- `src/api/client.ts` — Axios instance with base URL and auth interceptors, used by all API functions
- `src/api/rest.ts::fetchSboms` — existing API function pattern to follow
- `src/hooks/useSboms.ts` — existing React Query hook pattern (useQuery with query key convention)
- `src/hooks/useSbomById.ts` — demonstrates single-entity query with ID parameter and `enabled` option

## Acceptance Criteria
- [ ] TypeScript interfaces for all comparison response types are defined in `src/api/models.ts`
- [ ] `fetchSbomComparison(leftId, rightId)` function exists in `src/api/rest.ts` and calls `GET /api/v2/sbom/compare?left={leftId}&right={rightId}`
- [ ] `useSbomComparison` hook returns `{ data, isLoading, isError, error }` following React Query conventions
- [ ] Hook is disabled (does not fire) when either `leftId` or `rightId` is undefined
- [ ] TypeScript compilation passes with no type errors

## Test Requirements
- [ ] Unit test: `useSbomComparison` returns comparison data when both IDs are provided (mock API with MSW)
- [ ] Unit test: `useSbomComparison` does not fire query when one ID is missing
- [ ] Unit test: `useSbomComparison` surfaces error state when API returns 404

## Verification Commands
- `npx tsc --noEmit` — TypeScript compilation passes
- `npx vitest run src/hooks/useSbomComparison` — hook tests pass

## Dependencies
- Depends on: Task 2 — Add SBOM comparison REST endpoint (backend must define the API contract before frontend implements against it)
