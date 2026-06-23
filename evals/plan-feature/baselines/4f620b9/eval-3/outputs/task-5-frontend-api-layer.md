## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add the TypeScript interfaces for the SBOM comparison API response, the API client function to call the comparison endpoint, and a React Query hook to manage the comparison data fetching. This provides the data layer that the comparison page (Task 6) will consume.

## Files to Modify
- `src/api/models.ts` — Add TypeScript interfaces for comparison response types
- `src/api/rest.ts` — Add `compareSboms(leftId, rightId)` API client function

## Files to Create
- `src/hooks/useSbomComparison.ts` — React Query hook for fetching comparison results

## API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — NEW client function consuming the backend endpoint

## Implementation Notes
- Add interfaces to `src/api/models.ts`: `SbomComparisonResult`, `PackageDiff`, `VersionChange`, `VulnerabilityDiff`, `LicenseChange` matching the backend API response shape.
- The `SbomComparisonResult` interface should have fields: `added_packages: PackageDiff[]`, `removed_packages: PackageDiff[]`, `version_changes: VersionChange[]`, `new_vulnerabilities: VulnerabilityDiff[]`, `resolved_vulnerabilities: VulnerabilityDiff[]`, `license_changes: LicenseChange[]`.
- Add `compareSboms` function to `src/api/rest.ts` following the pattern of `fetchSboms()` and `fetchAdvisories()` — use the Axios instance from `src/api/client.ts`.
- The hook in `src/hooks/useSbomComparison.ts` should follow the pattern of `src/hooks/useSbomById.ts` — accept `leftId` and `rightId` parameters, return `useQuery` result. Use `enabled: !!leftId && !!rightId` to prevent fetching until both IDs are provided.
- Use query key pattern `['sbom-comparison', leftId, rightId]` for cache key.

**Backend API contracts:**
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — response shape:
  ```
  {
    added_packages: [{ name: string, version: string, license: string, advisory_count: number }],
    removed_packages: [{ name: string, version: string, license: string, advisory_count: number }],
    version_changes: [{ name: string, left_version: string, right_version: string, direction: "upgrade" | "downgrade" }],
    new_vulnerabilities: [{ advisory_id: string, severity: string, title: string, affected_package: string }],
    resolved_vulnerabilities: [{ advisory_id: string, severity: string, title: string, previously_affected_package: string }],
    license_changes: [{ name: string, left_license: string, right_license: string }]
  }
  ```
  (see `modules/fundamental/src/sbom/endpoints/compare.rs` in trustify-backend)

Verify these contracts against the backend repo during implementation using the implement-task cross-repo API verification step.

## Reuse Candidates
- `src/api/rest.ts::fetchSboms` — existing API client function as template for the new `compareSboms` function
- `src/hooks/useSbomById.ts` — existing React Query hook as template for `useSbomComparison`
- `src/api/client.ts` — Axios instance with base URL and auth interceptors

## Acceptance Criteria
- [ ] TypeScript interfaces match the backend API response shape exactly
- [ ] `compareSboms(leftId, rightId)` function calls the correct endpoint with query parameters
- [ ] `useSbomComparison` hook returns typed comparison data via React Query
- [ ] Hook does not fetch when either ID is undefined/null

## Test Requirements
- [ ] Unit test: `compareSboms` constructs correct URL with query parameters
- [ ] Unit test: `useSbomComparison` hook returns data when both IDs are provided (use MSW mock)
- [ ] Unit test: `useSbomComparison` hook does not fetch when an ID is missing

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 4 — Add SBOM comparison endpoint and integration tests

[sdlc-workflow] Description digest: sha256-md:a98aeca2b9314433ec7d6f18fb1c8f1768f447e22e60853f1cdea9c0a62515bc
