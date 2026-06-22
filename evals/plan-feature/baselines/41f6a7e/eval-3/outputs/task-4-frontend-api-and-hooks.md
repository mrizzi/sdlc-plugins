# Task 4 — Add frontend API types, client function, and React Query hook for SBOM comparison

## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add the TypeScript interfaces for the SBOM comparison API response, the Axios-based API client function, and the React Query hook that the comparison page will use to fetch comparison data. This establishes the data layer before the UI is built.

## Files to Modify
- `src/api/models.ts` — add TypeScript interfaces for the comparison response types (SbomComparisonResult, PackageDiff, VersionChange, VulnerabilityDiff, LicenseChange)
- `src/api/rest.ts` — add `compareSboms(leftId: string, rightId: string)` function calling `GET /api/v2/sbom/compare`

## Files to Create
- `src/hooks/useSbomComparison.ts` — React Query hook wrapping the `compareSboms` API function, enabled only when both SBOM IDs are provided

## Implementation Notes
- Follow the existing API layer pattern: types in `src/api/models.ts`, client functions in `src/api/rest.ts`, hooks in `src/hooks/`.
- The `compareSboms` function should use the Axios client from `src/api/client.ts` with the path `/api/v2/sbom/compare` and query params `left` and `right`.
- The React Query hook should follow the pattern in `src/hooks/useSbomById.ts` — use `useQuery` with a query key like `["sbom-comparison", leftId, rightId]` and `enabled: !!leftId && !!rightId`.
- **Backend API contracts:**
  - `GET /api/v2/sbom/compare?left={id1}&right={id2}` — response shape:
    ```json
    {
      "added_packages": [{ "name": "string", "version": "string", "license": "string", "advisory_count": 0 }],
      "removed_packages": [{ "name": "string", "version": "string", "license": "string", "advisory_count": 0 }],
      "version_changes": [{ "name": "string", "left_version": "string", "right_version": "string", "direction": "upgrade | downgrade" }],
      "new_vulnerabilities": [{ "advisory_id": "string", "severity": "string", "title": "string", "affected_package": "string" }],
      "resolved_vulnerabilities": [{ "advisory_id": "string", "severity": "string", "title": "string", "previously_affected_package": "string" }],
      "license_changes": [{ "name": "string", "left_license": "string", "right_license": "string" }]
    }
    ```
  - Defined in backend at: `modules/fundamental/src/sbom/endpoints/compare.rs` and `modules/fundamental/src/sbom/model/comparison.rs`
  - Verify these contracts against the backend repo during implementation using the implement-task cross-repo API verification step.

## Reuse Candidates
- `src/api/client.ts` — Axios instance with base URL and auth interceptors
- `src/api/models.ts` — existing TypeScript interfaces showing the naming and structure pattern
- `src/api/rest.ts` — existing API functions (e.g., `fetchSboms()`) showing the client call pattern
- `src/hooks/useSbomById.ts` — existing React Query hook showing the `useQuery` pattern with conditional enabling
- `src/hooks/useSboms.ts` — existing SBOM list hook for reference

## Acceptance Criteria
- [ ] `SbomComparisonResult` TypeScript interface is defined in `src/api/models.ts` with all six diff category arrays
- [ ] `PackageDiff`, `VersionChange`, `VulnerabilityDiff`, and `LicenseChange` interfaces are defined
- [ ] `compareSboms(leftId, rightId)` function exists in `src/api/rest.ts` and calls the correct endpoint
- [ ] `useSbomComparison` hook returns `{ data, isLoading, error }` from React Query
- [ ] Hook is disabled (does not fire) when either SBOM ID is undefined or empty

## Test Requirements
- [ ] Unit test: `compareSboms` calls the correct URL with left/right query params
- [ ] Unit test: `useSbomComparison` hook does not fire when either ID is missing (enabled: false)
- [ ] Unit test: `useSbomComparison` hook returns parsed response data when both IDs are provided (use MSW mock)

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
