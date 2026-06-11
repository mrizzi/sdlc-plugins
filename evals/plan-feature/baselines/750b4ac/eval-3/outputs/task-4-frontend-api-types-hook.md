# Task 4 — Add comparison API types, client function, and React Query hook

## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add TypeScript interfaces for the SBOM comparison API response, an Axios client function to call the comparison endpoint, and a React Query hook to manage the comparison request lifecycle. This task provides the data-fetching foundation that the comparison page (Task 5) will consume.

## Files to Modify
- `src/api/models.ts` — add TypeScript interfaces for comparison response types
- `src/api/rest.ts` — add `compareSboms(leftId, rightId)` client function

## Files to Create
- `src/hooks/useSbomComparison.ts` — React Query hook wrapping the comparison API call

## Implementation Notes
- Follow the existing API layer pattern: interfaces in `src/api/models.ts`, client functions in `src/api/rest.ts`, hooks in `src/hooks/`.
- The comparison response interfaces should match the backend contract exactly:
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
- The client function should use the existing Axios instance from `src/api/client.ts` and call `GET /api/v2/sbom/compare?left={leftId}&right={rightId}`.
- The React Query hook should follow the established pattern (see `src/hooks/useSboms.ts` and `src/hooks/useSbomById.ts`): use `useQuery` with a query key that includes both SBOM IDs, and set `enabled: false` by default so the query only runs when explicitly triggered (the user must click "Compare").
- Use the mutation pattern from `src/hooks/useDeleteSbomMutation.ts` as reference for cache invalidation patterns, though this hook uses `useQuery` with manual triggering rather than `useMutation`.

**Backend API contracts:**
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — response shape:
  ```json
  {
    "added_packages": [{ "name": "str", "version": "str", "license": "str", "advisory_count": 0 }],
    "removed_packages": [{ "name": "str", "version": "str", "license": "str", "advisory_count": 0 }],
    "version_changes": [{ "name": "str", "left_version": "str", "right_version": "str", "direction": "upgrade|downgrade" }],
    "new_vulnerabilities": [{ "advisory_id": "str", "severity": "str", "title": "str", "affected_package": "str" }],
    "resolved_vulnerabilities": [{ "advisory_id": "str", "severity": "str", "title": "str", "previously_affected_package": "str" }],
    "license_changes": [{ "name": "str", "left_license": "str", "right_license": "str" }]
  }
  ```
  (Defined in backend: `modules/fundamental/src/sbom/model/comparison.rs`)

Verify these contracts against the backend repo during implementation using the implement-task cross-repo API verification step.

## Reuse Candidates
- `src/api/client.ts` — Axios instance with base URL and auth interceptors
- `src/api/models.ts` — existing TypeScript interfaces to follow as pattern
- `src/api/rest.ts` — existing API client functions (fetchSboms, fetchAdvisories) as pattern
- `src/hooks/useSboms.ts` — React Query hook pattern for list queries
- `src/hooks/useSbomById.ts` — React Query hook pattern for single-entity queries

## Acceptance Criteria
- [ ] TypeScript interfaces for all comparison response types are defined in `src/api/models.ts`
- [ ] `compareSboms(leftId: string, rightId: string)` function is exported from `src/api/rest.ts`
- [ ] `useSbomComparison` hook is implemented with React Query, accepting left and right SBOM IDs
- [ ] Hook query is disabled by default and can be manually triggered
- [ ] All types match the backend API contract exactly

## Test Requirements
- [ ] Unit test: `useSbomComparison` hook returns loading/error/data states correctly using MSW mock
- [ ] Unit test: hook does not fire automatically when IDs are provided (enabled: false behavior)
- [ ] Unit test: hook returns comparison data when manually triggered

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 3 — Add SBOM comparison endpoint and integration tests

[sdlc-workflow] Description digest: sha256-md:70782c51d2f39668ffd648e6f7f745e52303323389790dec970d7d9cee377949
