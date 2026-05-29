## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add TypeScript interfaces for the SBOM comparison API response, an API client function to call the comparison endpoint, and a React Query hook to manage the comparison request lifecycle. These are the data-layer building blocks that the comparison page will consume.

## Files to Modify
- `src/api/models.ts` — Add TypeScript interfaces: SbomComparisonResult, AddedPackage, RemovedPackage, VersionChange, NewVulnerability, ResolvedVulnerability, LicenseChange
- `src/api/rest.ts` — Add `fetchSbomComparison(leftId: string, rightId: string)` function that calls `GET /api/v2/sbom/compare?left={leftId}&right={rightId}`

## Files to Create
- `src/hooks/useSbomComparison.ts` — React Query hook: `useSbomComparison(leftId: string | undefined, rightId: string | undefined)` that calls `fetchSbomComparison` and returns query result. Hook should be disabled when either ID is undefined.

## Implementation Notes
- Follow the existing TypeScript interface pattern in `src/api/models.ts` — interfaces use PascalCase names and camelCase property names.
- Follow the existing API function pattern in `src/api/rest.ts` — functions use the Axios instance from `src/api/client.ts`, return typed responses (e.g., `fetchSboms()` returns `Promise<SbomSummary[]>`).
- Follow the existing hook pattern in `src/hooks/useSboms.ts` and `src/hooks/useSbomById.ts` — hooks use `useQuery` from React Query (TanStack Query), with a query key array and enabled option for conditional fetching.
- The `useSbomComparison` hook should use `enabled: !!leftId && !!rightId` to prevent the query from running until both SBOM IDs are provided.
- Interface field mapping from backend snake_case to frontend camelCase:
  - `added_packages` -> `addedPackages`
  - `removed_packages` -> `removedPackages`
  - `version_changes` -> `versionChanges`
  - `new_vulnerabilities` -> `newVulnerabilities`
  - `resolved_vulnerabilities` -> `resolvedVulnerabilities`
  - `license_changes` -> `licenseChanges`
  - `advisory_count` -> `advisoryCount`
  - `left_version` -> `leftVersion`
  - `right_version` -> `rightVersion`
  - `advisory_id` -> `advisoryId`
  - `affected_package` -> `affectedPackage`
  - `previously_affected_package` -> `previouslyAffectedPackage`
  - `left_license` -> `leftLicense`
  - `right_license` -> `rightLicense`
- Check whether the Axios instance in `src/api/client.ts` has response interceptors that handle snake_case to camelCase transformation automatically. If not, the `fetchSbomComparison` function may need to handle the transformation.
- **Backend API contracts:**
  - `GET /api/v2/sbom/compare?left={id1}&right={id2}` — response shape: `{ added_packages: AddedPackage[], removed_packages: RemovedPackage[], version_changes: VersionChange[], new_vulnerabilities: NewVulnerability[], resolved_vulnerabilities: ResolvedVulnerability[], license_changes: LicenseChange[] }` (see `modules/fundamental/src/sbom/endpoints/compare.rs` in trustify-backend)
  - Verify these contracts against the backend repo during implementation using the implement-task cross-repo API verification step.

## Reuse Candidates
- `src/api/models.ts` — existing TypeScript interfaces for API types; extend with comparison types following same patterns
- `src/api/rest.ts::fetchSboms` — existing API function demonstrating the Axios call pattern and response typing
- `src/hooks/useSboms.ts` — existing React Query hook demonstrating query key structure and useQuery usage
- `src/hooks/useSbomById.ts` — existing hook demonstrating single-entity fetching with conditional enabled flag

## Acceptance Criteria
- [ ] TypeScript interfaces for all comparison response types are defined in `src/api/models.ts`
- [ ] `fetchSbomComparison(leftId, rightId)` function is added to `src/api/rest.ts` and returns `Promise<SbomComparisonResult>`
- [ ] `useSbomComparison` hook is created in `src/hooks/useSbomComparison.ts` with proper query key and conditional enabling
- [ ] Hook does not fire the API call when either SBOM ID is undefined
- [ ] All types compile without errors

## Test Requirements
- [ ] Unit test for `useSbomComparison` hook: verify it does not call the API when leftId or rightId is undefined
- [ ] Unit test for `useSbomComparison` hook: verify it calls `fetchSbomComparison` with correct parameters when both IDs are provided (use MSW handler in `tests/mocks/handlers.ts`)
- [ ] Unit test: verify the hook returns the expected data shape from a mocked API response

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 4 — Add SBOM comparison endpoint (backend API must exist for contract verification)

[sdlc-workflow] Description digest: sha256:d58c2e8e454bbd259bf076290c94c6592852b867a1c9aff5ed6b6644c2db7282
