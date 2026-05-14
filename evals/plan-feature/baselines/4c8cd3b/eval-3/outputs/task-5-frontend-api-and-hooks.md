## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add TypeScript interfaces for the SBOM comparison API response, an API client function to call the comparison endpoint, and a React Query hook to manage comparison data fetching. This task establishes the data layer that the comparison page components will consume.

## Files to Create
- `src/hooks/useSbomComparison.ts` — React Query hook: `useSbomComparison(leftId, rightId)` that calls the comparison endpoint and returns the structured diff result

## Files to Modify
- `src/api/models.ts` — Add TypeScript interfaces: `SbomComparisonResult`, `PackageDiff`, `VersionChange`, `VulnerabilityDiff`, `LicenseDiff`
- `src/api/rest.ts` — Add `fetchSbomComparison(leftId: string, rightId: string): Promise<SbomComparisonResult>` function

## Implementation Notes
- Follow the existing API model pattern in `src/api/models.ts` — define interfaces with the same field names as the backend JSON response (snake_case from the API, but follow the existing project convention for interface field naming — check whether existing interfaces use camelCase or snake_case).
- TypeScript interfaces to add to `src/api/models.ts`:
  ```typescript
  interface SbomComparisonResult {
    added_packages: PackageDiff[];
    removed_packages: PackageDiff[];
    version_changes: VersionChange[];
    new_vulnerabilities: VulnerabilityDiff[];
    resolved_vulnerabilities: VulnerabilityDiff[];
    license_changes: LicenseDiff[];
  }
  interface PackageDiff { name: string; version: string; license: string | null; advisory_count: number; }
  interface VersionChange { name: string; left_version: string; right_version: string; direction: string; }
  interface VulnerabilityDiff { advisory_id: string; severity: string; title: string; affected_package: string; }
  interface LicenseDiff { name: string; left_license: string; right_license: string; }
  ```
- Follow the existing API client pattern in `src/api/rest.ts` — use the Axios instance from `src/api/client.ts` to make the GET request. Example: `export const fetchSbomComparison = (leftId: string, rightId: string) => client.get<SbomComparisonResult>(\`/api/v2/sbom/compare?left=\${leftId}&right=\${rightId}\`).then(r => r.data);`
- Follow the existing hook pattern in `src/hooks/useSboms.ts` — use `useQuery` from React Query with a query key like `["sbom-comparison", leftId, rightId]`. The hook should be disabled when either ID is missing (use `enabled: !!leftId && !!rightId`).
- The hook should only trigger the API call when explicitly requested (after the user clicks "Compare"), not on every render. Use `enabled: false` initially and provide a `refetch` function, or use a state flag.

**Backend API contracts:**
- `GET /api/v2/sbom/compare?left={id}&right={id}` — response shape: `SbomComparisonResult` as defined above (see `modules/fundamental/src/sbom/endpoints/compare.rs` in trustify-backend)
- Verify these contracts against the backend repo during implementation using the implement-task cross-repo API verification step.

## Reuse Candidates
- `src/api/rest.ts::fetchSboms` — reference for API client function pattern (Axios GET with typed response)
- `src/hooks/useSboms.ts` — reference for React Query `useQuery` hook pattern with query key structure
- `src/hooks/useSbomById.ts` — reference for single-entity query hook pattern with ID parameter
- `src/api/client.ts` — Axios instance with base URL and auth interceptors to reuse

## Acceptance Criteria
- [ ] TypeScript interfaces for `SbomComparisonResult`, `PackageDiff`, `VersionChange`, `VulnerabilityDiff`, `LicenseDiff` are defined in `src/api/models.ts`
- [ ] `fetchSbomComparison` function is exported from `src/api/rest.ts`
- [ ] `useSbomComparison` hook is exported from `src/hooks/useSbomComparison.ts`
- [ ] The hook correctly passes left and right SBOM IDs as query parameters
- [ ] The hook is disabled when either SBOM ID is not provided
- [ ] TypeScript compiles without errors

## Test Requirements
- [ ] Unit test: `useSbomComparison` returns comparison data when both IDs are provided (mock the API with MSW)
- [ ] Unit test: `useSbomComparison` does not fire a request when either ID is missing
- [ ] Add MSW handler to `tests/mocks/handlers.ts` for `GET /api/v2/sbom/compare` returning a mock `SbomComparisonResult`
- [ ] Add mock comparison fixture data to `tests/mocks/fixtures/` (e.g., `sbom-comparison.json`)

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 4 — Add GET /api/v2/sbom/compare endpoint (backend must define the API contract)
