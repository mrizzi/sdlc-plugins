## Repository
trustify-ui

## Description
Add TypeScript interfaces for the SBOM comparison API response, a `compareSboms()` API client function, and a `useSbomComparison` React Query hook. This provides the data layer for the frontend comparison page.

## Files to Modify
- `src/api/models.ts` — add TypeScript interfaces: `SbomComparisonResult`, `AddedPackage`, `RemovedPackage`, `VersionChange`, `NewVulnerability`, `ResolvedVulnerability`, `LicenseChange`
- `src/api/rest.ts` — add `compareSboms(leftId: string, rightId: string): Promise<SbomComparisonResult>` function using the Axios client

## Files to Create
- `src/hooks/useSbomComparison.ts` — React Query hook wrapping `compareSboms()` with `useQuery`, enabled only when both IDs are provided

## Implementation Notes
- Follow the existing API client pattern in `src/api/rest.ts` — functions like `fetchSboms()` use the Axios instance from `src/api/client.ts` and return typed responses.
- Follow the existing React Query hook pattern in `src/hooks/useSboms.ts` and `src/hooks/useSbomById.ts` for query key naming, enabled conditionals, and error handling.
- TypeScript interfaces should match the backend `SbomComparisonResult` response shape exactly.
- The hook should accept `leftId` and `rightId` parameters and only execute the query when both are defined.

## Reuse Candidates
- `src/api/rest.ts::fetchSboms` — API client function pattern
- `src/api/client.ts` — Axios instance with base URL and auth interceptors
- `src/api/models.ts` — existing TypeScript interface patterns
- `src/hooks/useSbomById.ts` — React Query hook pattern with conditional enabling

## Acceptance Criteria
- [ ] TypeScript interfaces match the backend comparison response shape
- [ ] `compareSboms()` function calls `GET /api/v2/sbom/compare?left={id1}&right={id2}`
- [ ] `useSbomComparison` hook wraps the API call with React Query
- [ ] Hook only executes when both SBOM IDs are provided

## Test Requirements
- [ ] Unit test: `compareSboms()` makes correct API call with left and right params
- [ ] Unit test: `useSbomComparison` hook returns loading/data/error states correctly
- [ ] Unit test: hook does not fire query when either ID is undefined

## Dependencies
- Depends on: Task 3 — SBOM comparison endpoint (backend endpoint must exist for frontend to call)
