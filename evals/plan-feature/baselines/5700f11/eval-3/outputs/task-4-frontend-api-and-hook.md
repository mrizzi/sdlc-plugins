## Repository
trustify-ui

## Description
Add the TypeScript interfaces, API client function, and React Query hook for the SBOM comparison endpoint. This task establishes the data-fetching layer that the comparison page (Task 5) will consume, following the project's existing API layer conventions.

## Files to Modify
- `src/api/models.ts` — Add TypeScript interfaces for the comparison response types
- `src/api/rest.ts` — Add `fetchSbomComparison(leftId: string, rightId: string)` function that calls `GET /api/v2/sbom/compare?left={leftId}&right={rightId}`

## Files to Create
- `src/hooks/useSbomComparison.ts` — React Query hook `useSbomComparison(leftId, rightId)` that wraps the API client function with proper query key, enabled flag (only when both IDs are provided), and error handling

## Implementation Notes
- Define interfaces in `src/api/models.ts` following the existing pattern of TypeScript interfaces for API response types. The `SbomComparison` interface should match the backend response shape from the Figma design context:
  ```
  SbomComparison { added_packages: AddedPackage[], removed_packages: RemovedPackage[], version_changes: VersionChange[], new_vulnerabilities: NewVulnerability[], resolved_vulnerabilities: ResolvedVulnerability[], license_changes: LicenseChange[] }
  ```
- The `fetchSbomComparison` function in `src/api/rest.ts` should follow the pattern of existing functions like `fetchSboms()` — use the Axios instance from `src/api/client.ts` with the base URL and auth interceptors already configured.
- The React Query hook in `src/hooks/useSbomComparison.ts` should follow the pattern in `src/hooks/useSbomById.ts` — use `useQuery` with a descriptive query key like `["sbom-comparison", leftId, rightId]` and set `enabled: !!(leftId && rightId)` so the query only fires when both IDs are present.
- Use camelCase for TypeScript field names if the API returns snake_case (handle mapping in the API client function or use Axios response transformers consistent with the existing codebase pattern).

## Reuse Candidates
- `src/api/client.ts` — Axios instance with base URL and auth interceptors
- `src/api/rest.ts` — Existing API client functions as pattern reference (e.g., `fetchSboms()`)
- `src/hooks/useSbomById.ts` — React Query hook pattern with `useQuery`, query key, and `enabled` option
- `src/hooks/useSboms.ts` — React Query hook pattern for list queries

## Acceptance Criteria
- [ ] `SbomComparison` and all sub-interfaces are defined in `src/api/models.ts` with correct field types
- [ ] `fetchSbomComparison(leftId, rightId)` is exported from `src/api/rest.ts` and correctly constructs the API URL with query parameters
- [ ] `useSbomComparison(leftId, rightId)` hook returns `{ data, isLoading, isError, error }` with proper React Query integration
- [ ] The hook does not fire the API call when either `leftId` or `rightId` is undefined/empty
- [ ] TypeScript types compile without errors

## Test Requirements
- [ ] Unit test: `fetchSbomComparison` constructs the correct URL with both query parameters
- [ ] Unit test: `useSbomComparison` does not trigger a query when `leftId` is undefined
- [ ] Unit test: `useSbomComparison` does not trigger a query when `rightId` is undefined
- [ ] Unit test: `useSbomComparison` returns comparison data when both IDs are provided (using MSW mock)

## Dependencies
- Depends on: Task 2 — Backend comparison endpoint (the API must exist for the frontend to call it)
