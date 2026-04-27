# Task 4 — API types, client function, and React Query hook for SBOM comparison

## Repository
trustify-ui

## Description
Add TypeScript interfaces for the SBOM comparison API response, an Axios-based API client function to call the comparison endpoint, and a React Query hook that components can use to trigger and consume comparison results. This establishes the data-fetching layer that the comparison UI (Task 5) will consume.

## Files to Modify
- `src/api/models.ts` — add TypeScript interfaces for the comparison response types
- `src/api/rest.ts` — add `compareSboms(leftId: string, rightId: string)` function

## Files to Create
- `src/hooks/useSbomComparison.ts` — React Query hook wrapping the comparison API call

## Implementation Notes
- **TypeScript interfaces** — add the following types to `src/api/models.ts`, matching the backend response shape exactly:
  ```typescript
  interface AddedPackage { name: string; version: string; license: string; advisory_count: number; }
  interface RemovedPackage { name: string; version: string; license: string; advisory_count: number; }
  interface VersionChange { name: string; left_version: string; right_version: string; direction: "upgrade" | "downgrade"; }
  interface NewVulnerability { advisory_id: string; severity: "critical" | "high" | "medium" | "low"; title: string; affected_package: string; }
  interface ResolvedVulnerability { advisory_id: string; severity: string; title: string; previously_affected_package: string; }
  interface LicenseChange { name: string; left_license: string; right_license: string; }
  interface SbomComparisonResult {
    added_packages: AddedPackage[];
    removed_packages: RemovedPackage[];
    version_changes: VersionChange[];
    new_vulnerabilities: NewVulnerability[];
    resolved_vulnerabilities: ResolvedVulnerability[];
    license_changes: LicenseChange[];
  }
  ```
- **API client function** — follow the pattern of existing functions in `src/api/rest.ts` (e.g., `fetchSboms()`, `fetchAdvisories()`). Use the Axios client instance from `src/api/client.ts`. The function signature: `compareSboms(leftId: string, rightId: string): Promise<SbomComparisonResult>`. Send parameters as query params: `GET /api/v2/sbom/compare?left={leftId}&right={rightId}`.
- **React Query hook** — follow the pattern of existing hooks in `src/hooks/` (e.g., `useSboms.ts`, `useSbomById.ts`). Use `useQuery` from TanStack Query. The hook should:
  - Accept `leftId: string | undefined` and `rightId: string | undefined` as parameters
  - Set `enabled: !!leftId && !!rightId` so the query only fires when both IDs are provided
  - Use a query key like `["sbom-comparison", leftId, rightId]`
  - Return the standard `useQuery` result (data, isLoading, isError, error)

### Backend API contracts
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — response shape: `SbomComparisonResult` as defined above (see `modules/fundamental/src/sbom/endpoints/compare.rs` in trustify-backend)
- `GET /api/v2/sbom` — existing endpoint returning SBOM list, used by SBOM selectors (see `modules/fundamental/src/sbom/endpoints/list.rs` in trustify-backend)

Verify these contracts against the backend repo during implementation using the implement-task cross-repo API verification step.

## Reuse Candidates
- `src/api/rest.ts::fetchSboms` — existing API function pattern to follow for the new `compareSboms` function
- `src/api/client.ts` — Axios instance with base URL and auth interceptors; reuse for the comparison call
- `src/hooks/useSboms.ts` — existing React Query hook pattern to follow for `useSbomComparison`
- `src/hooks/useSbomById.ts` — existing single-entity query hook pattern; reference for query key conventions and enabled flag
- `src/api/models.ts` — existing TypeScript interfaces; follow naming and export conventions

## Acceptance Criteria
- [ ] TypeScript interfaces for all comparison response types are exported from `src/api/models.ts`
- [ ] `compareSboms(leftId, rightId)` function exists in `src/api/rest.ts` and calls the correct endpoint
- [ ] `useSbomComparison` hook is exported from `src/hooks/useSbomComparison.ts`
- [ ] Hook only fires the query when both SBOM IDs are provided (enabled flag)
- [ ] Hook returns standard React Query result shape (data, isLoading, isError)
- [ ] All TypeScript types compile without errors

## Test Requirements
- [ ] Unit test: `compareSboms` sends correct GET request with left/right query params (use MSW handler)
- [ ] Unit test: `useSbomComparison` does not fire when IDs are undefined
- [ ] Unit test: `useSbomComparison` returns comparison data when both IDs are provided

## Verification Commands
- `npx tsc --noEmit` — TypeScript compilation passes
- `npx vitest run --reporter=verbose` — unit tests pass

## Dependencies
- Depends on: Task 2 — SBOM comparison REST endpoint (backend must define the API contract)
