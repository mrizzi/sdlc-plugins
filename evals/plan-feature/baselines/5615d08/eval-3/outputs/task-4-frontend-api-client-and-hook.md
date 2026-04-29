## Repository
trustify-ui

## Description
Add the TypeScript types, API client function, and React Query hook for the SBOM comparison endpoint. This provides the data-fetching layer that the comparison page UI will consume, following the existing API layer conventions in the frontend codebase.

## Files to Modify
- `src/api/models.ts` — Add TypeScript interfaces for the comparison response: `SbomComparison`, `PackageDiff`, `VersionChange`, `VulnerabilityDiff`, `LicenseChange`
- `src/api/rest.ts` — Add `fetchSbomComparison(leftId: string, rightId: string)` function that calls `GET /api/v2/sbom/compare?left={leftId}&right={rightId}`

## Files to Create
- `src/hooks/useSbomComparison.ts` — React Query hook `useSbomComparison(leftId: string | undefined, rightId: string | undefined)` that calls `fetchSbomComparison` and returns the query result. The hook should be disabled (via `enabled` option) when either ID is undefined.

## Implementation Notes
- In `src/api/models.ts`, add interfaces matching the backend response shape. Follow the naming conventions of existing interfaces in that file (e.g., `SbomSummary`, `AdvisorySummary`):
  ```
  SbomComparison { added_packages: PackageDiff[], removed_packages: PackageDiff[], version_changes: VersionChange[], new_vulnerabilities: VulnerabilityDiff[], resolved_vulnerabilities: VulnerabilityDiff[], license_changes: LicenseChange[] }
  PackageDiff { name: string, version: string, license: string, advisory_count: number }
  VersionChange { name: string, left_version: string, right_version: string, direction: "upgrade" | "downgrade" }
  VulnerabilityDiff { advisory_id: string, severity: string, title: string, affected_package: string }
  LicenseChange { name: string, left_license: string, right_license: string }
  ```
- In `src/api/rest.ts`, follow the pattern of existing functions like `fetchSboms()`. Use the Axios instance from `src/api/client.ts`. The function should be: `export const fetchSbomComparison = (leftId: string, rightId: string): Promise<SbomComparison> => client.get('/api/v2/sbom/compare', { params: { left: leftId, right: rightId } }).then(res => res.data);`
- In `src/hooks/useSbomComparison.ts`, follow the pattern in `src/hooks/useSbomById.ts`. Use `useQuery` from React Query with a query key like `["sbom-comparison", leftId, rightId]`. Set `enabled: !!leftId && !!rightId` so the query only fires when both IDs are present.

## Reuse Candidates
- `src/api/client.ts` — Reuse the existing Axios instance with auth interceptors
- `src/api/rest.ts` — Follow the pattern of `fetchSboms()` and other existing API functions
- `src/hooks/useSbomById.ts` — Follow the same `useQuery` pattern for the new hook
- `src/api/models.ts` — Extend with new interfaces following existing naming conventions

## Acceptance Criteria
- [ ] `SbomComparison` and related interfaces are exported from `src/api/models.ts`
- [ ] `fetchSbomComparison` function is exported from `src/api/rest.ts` and correctly calls the comparison endpoint with query parameters
- [ ] `useSbomComparison` hook returns a React Query result with the comparison data
- [ ] Hook is disabled when either `leftId` or `rightId` is undefined
- [ ] TypeScript compiles without errors

## Test Requirements
- [ ] Unit test: `useSbomComparison` hook returns data when both IDs are provided (mock API response with MSW)
- [ ] Unit test: `useSbomComparison` hook does not fire request when leftId is undefined
- [ ] Unit test: `useSbomComparison` hook does not fire request when rightId is undefined

## Dependencies
- Depends on: Task 2 — SBOM comparison endpoint (the backend endpoint this client calls)
