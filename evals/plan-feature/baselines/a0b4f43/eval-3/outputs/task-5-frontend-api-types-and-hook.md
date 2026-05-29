## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add TypeScript interfaces for the SBOM comparison API response, an API client function to call the comparison endpoint, and a React Query hook to manage the comparison data fetching. This provides the data layer that the comparison page UI will consume.

## Files to Modify
- `src/api/models.ts` — Add TypeScript interfaces: SbomComparisonResult, AddedPackage, RemovedPackage, VersionChange, NewVulnerability, ResolvedVulnerability, LicenseChange
- `src/api/rest.ts` — Add `fetchSbomComparison(leftId: string, rightId: string)` function that calls `GET /api/v2/sbom/compare?left={leftId}&right={rightId}`

## Files to Create
- `src/hooks/useSbomComparison.ts` — React Query hook: `useSbomComparison(leftId, rightId)` that calls `fetchSbomComparison` and returns query result with typed data

## Implementation Notes
- Follow the existing API layer pattern: typed interfaces in `src/api/models.ts`, API functions in `src/api/rest.ts`, React Query hooks in `src/hooks/`.
- Model the TypeScript interfaces to match the backend response shape exactly:
  ```
  SbomComparisonResult {
    added_packages: AddedPackage[]
    removed_packages: RemovedPackage[]
    version_changes: VersionChange[]
    new_vulnerabilities: NewVulnerability[]
    resolved_vulnerabilities: ResolvedVulnerability[]
    license_changes: LicenseChange[]
  }
  ```
- The API client function should use the existing Axios instance from `src/api/client.ts` which already handles base URL and auth interceptors.
- Follow the pattern of existing hooks like `useSboms.ts` and `useSbomById.ts` for React Query configuration (query keys, enabled conditions, etc.).
- The hook should only be enabled when both `leftId` and `rightId` are provided (non-empty strings), using `enabled: !!leftId && !!rightId` in the useQuery options.
- Use `useQuery` (not `useMutation`) since this is a data-fetching operation triggered by parameter changes, not a user action like form submission.

**Backend API contracts:**
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — response shape: `SbomComparisonResult` with six arrays (added_packages, removed_packages, version_changes, new_vulnerabilities, resolved_vulnerabilities, license_changes). See `modules/fundamental/src/sbom/endpoints/compare.rs` in trustify-backend.
- `GET /api/v2/sbom` — existing endpoint used by `useSboms` hook for SBOM list data. Response shape: `PaginatedResults<SbomSummary>`. See `modules/fundamental/src/sbom/endpoints/list.rs` in trustify-backend.

Verify these contracts against the backend repo during implementation using the implement-task cross-repo API verification step.

## Reuse Candidates
- `src/api/client.ts` — Axios instance with base URL and auth interceptors; use for the comparison API call
- `src/api/rest.ts::fetchSboms` — Existing API function; follow its pattern for the new fetchSbomComparison function
- `src/hooks/useSboms.ts` — Existing React Query hook; follow its pattern for query key naming, error handling, and options
- `src/hooks/useSbomById.ts` — Existing hook that takes an ID parameter; follow its pattern for the enabled condition

## Acceptance Criteria
- [ ] TypeScript interfaces for all six diff categories are defined in `models.ts` and match the backend response shape
- [ ] `fetchSbomComparison` function calls the correct endpoint with left and right IDs as query parameters
- [ ] `useSbomComparison` hook returns typed `SbomComparisonResult` data
- [ ] Hook is disabled when either ID is missing (does not fire API call)
- [ ] Hook uses the existing Axios client for authentication and base URL handling

## Test Requirements
- [ ] Unit test for `fetchSbomComparison`: verify it calls the correct URL with query parameters using MSW handler
- [ ] Unit test for `useSbomComparison` hook: verify it returns data when both IDs are provided and does not fetch when an ID is missing

## Dependencies
- Depends on: Task 2 — Create feature branch TC-9003 from main (trustify-ui)
- Depends on: Task 4 — Add SBOM comparison endpoint and integration tests (trustify-backend)