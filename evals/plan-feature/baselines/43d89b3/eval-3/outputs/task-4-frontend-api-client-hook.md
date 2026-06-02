## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add TypeScript interfaces for the SBOM comparison API response, an API client function to call the comparison endpoint, and a React Query hook to manage the comparison data fetching. This provides the data layer for the SBOM comparison page.

## Files to Modify
- `src/api/models.ts` — Add TypeScript interfaces: SbomComparisonResult, AddedPackage, RemovedPackage, VersionChange, NewVulnerability, ResolvedVulnerability, LicenseChange
- `src/api/rest.ts` — Add `fetchSbomComparison(leftId: string, rightId: string): Promise<SbomComparisonResult>` function

## Files to Create
- `src/hooks/useSbomComparison.ts` — React Query hook `useSbomComparison(leftId?: string, rightId?: string)` that calls fetchSbomComparison and returns query state

## Implementation Notes
For TypeScript interfaces in `src/api/models.ts`, match the backend API response shape exactly:
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

For the API client function in `src/api/rest.ts`, follow the existing pattern of `fetchSboms()` and other API functions — use the Axios instance from `src/api/client.ts` with typed responses.

For the React Query hook in `src/hooks/useSbomComparison.ts`, follow the pattern in `src/hooks/useSboms.ts` and `src/hooks/useSbomById.ts`:
- Use `useQuery` from TanStack Query
- Set `enabled: !!leftId && !!rightId` to prevent fetching when either selector is empty
- Use a query key like `["sbom-comparison", leftId, rightId]` for proper caching and refetching

**Backend API contracts:**
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — response shape: `SbomComparisonResult` with six diff category arrays (see Task 2 for full field definitions). Defined in `modules/fundamental/src/sbom/endpoints/compare.rs`.

Verify these contracts against the backend repo during implementation using the implement-task cross-repo API verification step.

## Reuse Candidates
- `src/api/rest.ts::fetchSboms` — Existing API function; follow the same Axios call pattern with typed response
- `src/api/client.ts` — Axios instance with base URL and auth interceptors; use for the comparison API call
- `src/hooks/useSboms.ts` — Existing React Query hook; follow the same useQuery pattern with query key and enabled flag
- `src/hooks/useSbomById.ts` — Existing single-entity query hook; reference for parameter-dependent query patterns

## Acceptance Criteria
- [ ] TypeScript interfaces for all comparison response types are defined in `src/api/models.ts`
- [ ] `fetchSbomComparison` function calls `GET /api/v2/sbom/compare` with correct query parameters
- [ ] `useSbomComparison` hook returns query state (data, isLoading, isError)
- [ ] Hook is disabled when either leftId or rightId is undefined/empty
- [ ] All types match the backend API response shape exactly

## Test Requirements
- [ ] Unit test: verify `useSbomComparison` hook calls the correct API endpoint with both IDs
- [ ] Unit test: verify hook is disabled when leftId is undefined
- [ ] Unit test: verify hook is disabled when rightId is undefined
- [ ] Unit test: verify successful data fetch returns correctly typed SbomComparisonResult

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 3 — Add comparison REST endpoint and integration tests
