## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add TypeScript interfaces for the SBOM comparison API response types, an API client function that calls the comparison endpoint, and a React Query hook that manages the comparison data fetching lifecycle. This provides the data layer that the comparison page UI will consume.

## Files to Modify
- `src/api/models.ts` — Add interfaces: SbomComparisonResult, AddedPackage, RemovedPackage, VersionChange, NewVulnerability, ResolvedVulnerability, LicenseChange
- `src/api/rest.ts` — Add `fetchSbomComparison(leftId: string, rightId: string): Promise<SbomComparisonResult>` function

## Files to Create
- `src/hooks/useSbomComparison.ts` — React Query hook: `useSbomComparison(leftId: string | undefined, rightId: string | undefined)` that returns the comparison result; query is disabled when either ID is undefined

## Implementation Notes
- Follow the existing interface patterns in `src/api/models.ts` for type definitions. The existing interfaces use TypeScript `interface` declarations with optional fields where applicable.
  Per CONVENTIONS.md §API layer: typed API functions in `src/api/rest.ts` and React Query hooks in `src/hooks/`.
  Applies: task modifies `src/api/rest.ts` matching the convention's TypeScript API layer scope.
- The SbomComparisonResult interface must match the backend response shape:
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
- Follow the `fetchSboms()` pattern in `src/api/rest.ts` for the API client function. Use the Axios instance from `src/api/client.ts` with the endpoint path `/api/v2/sbom/compare`.
- Follow the `useSbomById.ts` pattern in `src/hooks/` for the React Query hook structure. Use a query key like `["sbom-comparison", leftId, rightId]` and set `enabled: !!leftId && !!rightId` to prevent fetching until both IDs are selected.
  Per CONVENTIONS.md §Naming: camelCase for hooks (useSbomComparison), camelCase for utility functions (fetchSbomComparison).
  Applies: task creates `src/hooks/useSbomComparison.ts` matching the convention's TypeScript hook file scope.

**Backend API contracts:**
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — response shape: `SbomComparisonResult` as defined above (see `modules/fundamental/src/sbom/endpoints/compare.rs` in trustify-backend)
- Verify these contracts against the backend repo during implementation using the implement-task cross-repo API verification step.

## Reuse Candidates
- `src/api/models.ts` — existing TypeScript interfaces for API types; extend with comparison types following same patterns
- `src/api/rest.ts::fetchSboms` — existing API function pattern; replicate for `fetchSbomComparison`
- `src/api/client.ts` — Axios instance with base URL and auth interceptors; use for the comparison API call
- `src/hooks/useSbomById.ts` — existing React Query hook with single-entity fetch pattern; follow for `useSbomComparison`
- `src/hooks/useSboms.ts` — existing React Query hook for list fetch; reference for query key patterns

## Acceptance Criteria
- [ ] SbomComparisonResult interface and all sub-type interfaces are defined in models.ts
- [ ] fetchSbomComparison function calls GET /api/v2/sbom/compare with left and right query params
- [ ] useSbomComparison hook returns query result with data, isLoading, isError states
- [ ] Hook query is disabled when either leftId or rightId is undefined
- [ ] TypeScript compilation succeeds with no type errors

## Test Requirements
- [ ] Unit test: useSbomComparison hook fetches data when both IDs are provided
- [ ] Unit test: useSbomComparison hook does not fetch when either ID is undefined
- [ ] Unit test: fetchSbomComparison constructs correct URL with query parameters

## Verification Commands
- `npx tsc --noEmit` — TypeScript compilation succeeds with no errors

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 3 — Add SBOM comparison REST endpoint (cross-repo: defines the API contract this task consumes)
