## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add TypeScript interfaces for the SBOM comparison API response, an Axios client function to call the comparison endpoint, and a React Query hook to manage the comparison data fetching lifecycle. This provides the data layer that the comparison page UI (Task 6) will consume.

## Files to Modify
- `src/api/models.ts` -- add TypeScript interfaces: `SbomComparison`, `AddedPackage`, `RemovedPackage`, `VersionChange`, `NewVulnerability`, `ResolvedVulnerability`, `LicenseChange`
- `src/api/rest.ts` -- add `compareSboms(leftId: string, rightId: string): Promise<SbomComparison>` function using the Axios client

## Files to Create
- `src/hooks/useSbomComparison.ts` -- React Query hook `useSbomComparison(leftId: string | undefined, rightId: string | undefined)` that calls `compareSboms()` and returns query result; only enabled when both IDs are defined

## Implementation Notes
- Follow the existing pattern in `src/api/models.ts` for interface definitions -- match the JSON field names from the backend response (snake_case in JSON, but TypeScript interfaces may use camelCase with field mapping in the client function).
- Follow the existing pattern in `src/api/rest.ts` for client functions -- use the shared Axios instance from `src/api/client.ts` with proper typing.
- Follow the existing hook pattern in `src/hooks/useSboms.ts` for the React Query hook structure -- use `useQuery` with a descriptive query key like `["sbom-comparison", leftId, rightId]`.
- The hook should set `enabled: !!leftId && !!rightId` to prevent fetching until both SBOM IDs are selected.
- Per CONVENTIONS.md §Mutation pattern: use React Query patterns with proper query key management. Applies: task creates `src/hooks/useSbomComparison.ts` matching the convention's `.ts` scope.

## Reuse Candidates
- `src/api/client.ts` -- shared Axios instance with base URL and auth interceptors; import and use for the comparison API call
- `src/api/rest.ts::fetchSboms` -- follow this function's pattern for typing and error handling
- `src/hooks/useSboms.ts` -- follow this hook's pattern for `useQuery` configuration and return type
- `src/hooks/useSbomById.ts` -- follow this hook's pattern for conditional fetching with `enabled` option

## Acceptance Criteria
- [ ] `SbomComparison` TypeScript interface matches the backend response shape (added_packages, removed_packages, version_changes, new_vulnerabilities, resolved_vulnerabilities, license_changes)
- [ ] `compareSboms()` calls `GET /api/v2/sbom/compare?left={id1}&right={id2}` and returns typed response
- [ ] `useSbomComparison` hook returns loading/error/data states via React Query
- [ ] Hook does not fire the API call until both `leftId` and `rightId` are defined

## Test Requirements
- [ ] Unit test: `compareSboms()` calls the correct endpoint URL with query parameters
- [ ] Unit test: `useSbomComparison` returns `isLoading: false` and does not fetch when either ID is undefined

## Verification Commands
- `npx tsc --noEmit` -- no TypeScript compilation errors
- `npx vitest run src/hooks/useSbomComparison` -- hook unit tests pass

## Dependencies
- Depends on: Task 2 -- Create feature branch (trustify-ui)
- Depends on: Task 4 -- Add SBOM comparison endpoint and integration tests (backend endpoint must exist for integration)

## Additional Fields
- priority: Critical
- fixVersions: RHTPA 1.5.0
- labels: ai-generated-jira
