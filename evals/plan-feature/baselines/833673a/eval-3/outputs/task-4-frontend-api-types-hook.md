## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add the TypeScript interfaces for the SBOM comparison API response, the API client function to call the comparison endpoint, and a React Query hook to manage the comparison query. This establishes the data-fetching layer that the comparison page UI will consume.

## Files to Modify
- `src/api/models.ts` — Add TypeScript interfaces: `SbomComparisonResult`, `AddedPackage`, `RemovedPackage`, `VersionChange`, `NewVulnerability`, `ResolvedVulnerability`, `LicenseChange`
- `src/api/rest.ts` — Add `fetchSbomComparison(leftId: string, rightId: string): Promise<SbomComparisonResult>` function

## Files to Create
- `src/hooks/useSbomComparison.ts` — React Query hook: `useSbomComparison(leftId: string | undefined, rightId: string | undefined)` that calls `fetchSbomComparison` and is enabled only when both IDs are provided

## Implementation Notes
Add TypeScript interfaces in `src/api/models.ts` alongside existing interfaces. The response shape matches the backend `SbomComparisonResult`:

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

The API client function in `src/api/rest.ts` should follow the pattern of existing functions like `fetchSboms()` — use the Axios instance from `src/api/client.ts`.

The React Query hook in `src/hooks/useSbomComparison.ts` should follow the pattern of `src/hooks/useSboms.ts` and `src/hooks/useSbomById.ts` — use `useQuery` with a query key and the `enabled` option to conditionally fetch.

**Backend API contracts:**
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — response shape: `SbomComparisonResult` with six array fields (see above). Defined in `modules/fundamental/src/sbom/endpoints/compare.rs` in the backend repo.

Verify these contracts against the backend repo during implementation using the implement-task cross-repo API verification step.

## Reuse Candidates
- `src/api/models.ts` — Existing TypeScript interfaces for API response types; follow the same naming and export patterns
- `src/api/rest.ts` — Existing API client functions (e.g., `fetchSboms`, `fetchAdvisories`) using the shared Axios instance
- `src/api/client.ts` — Axios instance with base URL and auth interceptors
- `src/hooks/useSboms.ts` — React Query hook pattern to follow for `useSbomComparison`
- `src/hooks/useSbomById.ts` — React Query hook pattern with conditional `enabled` option

## Acceptance Criteria
- [ ] TypeScript interfaces for all six diff category structs are exported from `src/api/models.ts`
- [ ] `fetchSbomComparison` function calls `GET /api/v2/sbom/compare` with `left` and `right` query parameters
- [ ] `useSbomComparison` hook returns React Query result and is disabled when either ID is undefined
- [ ] All types compile without errors

## Test Requirements
- [ ] Unit test: `useSbomComparison` hook does not fetch when `leftId` is undefined
- [ ] Unit test: `useSbomComparison` hook does not fetch when `rightId` is undefined
- [ ] Unit test: `useSbomComparison` hook fetches when both IDs are provided

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main

[sdlc-workflow] Description digest: sha256-md:6180ca340d2ad2e248c3ea816d8d48086f2ae5e3a9340fa42e0371182714d5b9
