## Repository
trustify-ui

## Target Branch
main

## Description
Add TypeScript interfaces for the SBOM comparison API response types, an API client function to call the comparison endpoint, and a React Query hook for data fetching. This task establishes the frontend API layer for the comparison feature, providing typed access to the `GET /api/v2/sbom/compare` endpoint created in the backend.

additional_fields: { "labels": ["ai-generated-jira"], "priority": "Critical", "fixVersions": "RHTPA 1.5.0" }

## Files to Create
- `src/hooks/useSbomCompare.ts` -- React Query hook that calls `compareSboms(leftId, rightId)` and returns the typed comparison result with loading/error states; query is disabled when either ID is undefined

## Files to Modify
- `src/api/models.ts` -- add TypeScript interfaces: `SbomComparisonResult`, `PackageDiff`, `VersionChange`, `VulnerabilityDiff`, `LicenseChange` matching the backend response shape
- `src/api/rest.ts` -- add `compareSboms(leftId: string, rightId: string): Promise<SbomComparisonResult>` function that calls `GET /api/v2/sbom/compare?left={leftId}&right={rightId}`

## Implementation Notes
Follow the existing API layer pattern:
- Types in `src/api/models.ts` follow the existing TypeScript interface conventions (reference the existing SBOM and advisory interfaces in the same file)
- API client function in `src/api/rest.ts` follows the pattern of existing functions like `fetchSboms()` and `fetchAdvisories()`, using the Axios instance from `src/api/client.ts`
- React Query hook in `src/hooks/` follows the pattern of `src/hooks/useSboms.ts` and `src/hooks/useSbomById.ts`

The `useSbomCompare` hook should:
1. Accept `leftId: string | undefined` and `rightId: string | undefined` parameters
2. Use `useQuery` with a query key like `["sbom-compare", leftId, rightId]`
3. Only enable the query when both IDs are defined (`enabled: !!leftId && !!rightId`)
4. Return the standard React Query result object with `data`, `isLoading`, `isError`

**Backend API contracts:**
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` -- response shape:
  ```json
  {
    "added_packages": [{ "name": "...", "version": "...", "license": "...", "advisory_count": 0 }],
    "removed_packages": [{ "name": "...", "version": "...", "license": "...", "advisory_count": 0 }],
    "version_changes": [{ "name": "...", "left_version": "...", "right_version": "...", "direction": "upgrade" }],
    "new_vulnerabilities": [{ "advisory_id": "...", "severity": "critical", "title": "...", "affected_package": "..." }],
    "resolved_vulnerabilities": [{ "advisory_id": "...", "severity": "...", "title": "...", "previously_affected_package": "..." }],
    "license_changes": [{ "name": "...", "left_license": "...", "right_license": "..." }]
  }
  ```
  (see `modules/fundamental/src/sbom/endpoints/compare.rs` in trustify-backend)

Verify these contracts against the backend repo during implementation using the implement-task cross-repo API verification step.

Per CONVENTIONS.md §API Layer: Axios client in `src/api/client.ts`; typed API functions in `src/api/rest.ts`; React Query hooks in `src/hooks/`.
Applies: task modifies `src/api/rest.ts` matching the convention's `.ts` module scope.

Per CONVENTIONS.md §State Management: React Query (TanStack Query) for server state; no Redux.
Applies: task creates `src/hooks/useSbomCompare.ts` matching the convention's `.ts` module scope.

Per CONVENTIONS.md §Naming: camelCase for hooks and utilities.
Applies: task creates `src/hooks/useSbomCompare.ts` matching the convention's `.ts` file scope.

## Reuse Candidates
- `src/api/models.ts` -- existing TypeScript interfaces for SBOM and advisory types; follow the same interface definition patterns
- `src/api/rest.ts::fetchSboms` -- existing API function; follow the same Axios call pattern for the comparison function
- `src/api/client.ts` -- Axios instance with base URL and auth interceptors; use for the comparison API call
- `src/hooks/useSboms.ts` -- existing React Query hook for SBOM list; follow the same `useQuery` pattern
- `src/hooks/useSbomById.ts` -- existing detail hook with ID parameter; reference for the enabled/disabled pattern based on parameter availability

## Acceptance Criteria
- [ ] TypeScript interfaces match the backend response shape for all six diff categories
- [ ] `compareSboms` function correctly calls `GET /api/v2/sbom/compare?left={leftId}&right={rightId}`
- [ ] `useSbomCompare` hook returns typed comparison result with loading and error states
- [ ] Query is disabled when either SBOM ID is undefined
- [ ] TypeScript compilation succeeds without errors

## Test Requirements
- [ ] Unit test: `compareSboms` constructs the correct URL with query parameters
- [ ] Unit test: `useSbomCompare` hook disables query when IDs are undefined
- [ ] Unit test: `useSbomCompare` hook returns correct data on successful fetch (using MSW mock handler)

## Verification Commands
- `npx tsc --noEmit` -- TypeScript compilation passes
- `npx vitest run src/hooks/useSbomCompare` -- hook unit tests pass

## Dependencies
- Depends on: Task 2 -- Implement SBOM comparison REST endpoint (backend API must exist for contract verification)
