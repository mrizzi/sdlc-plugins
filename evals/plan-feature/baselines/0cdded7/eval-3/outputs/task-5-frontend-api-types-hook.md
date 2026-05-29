# Task 5 — Add frontend API types, client function, and React Query hook for SBOM comparison

## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add TypeScript interfaces for the SBOM comparison API response, an Axios client function to call the comparison endpoint, and a React Query hook to manage the comparison request lifecycle. These form the data layer for the comparison page (Task 6).

## Files to Modify
- `src/api/models.ts` — add TypeScript interfaces for `SbomComparisonResult`, `AddedPackage`, `RemovedPackage`, `VersionChange`, `NewVulnerability`, `ResolvedVulnerability`, `LicenseChange`
- `src/api/rest.ts` — add `compareSboms(leftId: string, rightId: string): Promise<SbomComparisonResult>` function calling `GET /api/v2/sbom/compare?left={leftId}&right={rightId}`

## Files to Create
- `src/hooks/useSbomComparison.ts` — React Query hook `useSbomComparison(leftId: string | undefined, rightId: string | undefined)` that calls `compareSboms` when both IDs are provided

## Implementation Notes
- Follow the existing type definition pattern in `src/api/models.ts` for interface naming and field conventions.
- Follow the API function pattern in `src/api/rest.ts` — use the shared Axios instance from `src/api/client.ts`, return typed responses.
- Follow the React Query hook pattern in `src/hooks/useSboms.ts` and `src/hooks/useSbomById.ts` — use `useQuery` with a descriptive query key (e.g., `["sbom-comparison", leftId, rightId]`), set `enabled: Boolean(leftId && rightId)` to prevent firing without both IDs.
- TypeScript interfaces should use `camelCase` property names matching the snake_case JSON fields via automatic deserialization (or explicit mapping if the project uses one). Check `src/api/models.ts` for the existing convention on casing.

**Backend API contracts:**
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — response shape:
  ```json
  {
    "added_packages": [{ "name": "string", "version": "string", "license": "string", "advisory_count": 0 }],
    "removed_packages": [{ "name": "string", "version": "string", "license": "string", "advisory_count": 0 }],
    "version_changes": [{ "name": "string", "left_version": "string", "right_version": "string", "direction": "upgrade|downgrade" }],
    "new_vulnerabilities": [{ "advisory_id": "string", "severity": "critical|high|medium|low", "title": "string", "affected_package": "string" }],
    "resolved_vulnerabilities": [{ "advisory_id": "string", "severity": "string", "title": "string", "previously_affected_package": "string" }],
    "license_changes": [{ "name": "string", "left_license": "string", "right_license": "string" }]
  }
  ```
  (See `modules/fundamental/src/sbom/model/comparison.rs` in trustify-backend)

Verify these contracts against the backend repo during implementation using the implement-task cross-repo API verification step.

## Reuse Candidates
- `src/api/models.ts` — existing TypeScript interfaces for API response types (follow same style)
- `src/api/rest.ts::fetchSboms()` — API client function pattern using Axios
- `src/hooks/useSboms.ts` — React Query hook pattern for list queries
- `src/hooks/useSbomById.ts` — React Query hook pattern for single-item queries with ID parameter
- `src/api/client.ts` — Axios instance with base URL and auth interceptors

## Acceptance Criteria
- [ ] TypeScript interfaces for all six diff categories are defined in `src/api/models.ts`
- [ ] `compareSboms()` function exists in `src/api/rest.ts` and calls the correct endpoint with query params
- [ ] `useSbomComparison` hook exists and uses React Query `useQuery` with proper query key
- [ ] Hook is disabled (does not fire) when either SBOM ID is undefined
- [ ] TypeScript compiles without errors

## Test Requirements
- [ ] Unit test for `useSbomComparison` hook: verify it calls the correct API endpoint with MSW mock
- [ ] Unit test: verify the hook does not fire when IDs are undefined
- [ ] Unit test: verify the hook returns correct typed data on success

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main

[sdlc-workflow] Description digest: sha256:028ec6abe059815e55400f82d63e56ce79b2ed6551675592e7876d6428937d3a
