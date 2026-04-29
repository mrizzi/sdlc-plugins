# Task 2 — Frontend API types, client function, and React Query hook for SBOM comparison

## Repository
trustify-ui

## Description
Add the TypeScript types, API client function, and React Query hook needed to call the new `GET /api/v2/sbom/compare` backend endpoint. This establishes the data-fetching layer that the comparison page UI (Task 3) will consume. Also add MSW mock handlers and test fixtures so the comparison page can be tested without a running backend.

## Files to Modify
- `src/api/models.ts` — add TypeScript interfaces for the comparison response shape
- `src/api/rest.ts` — add `compareSboms(leftId: string, rightId: string)` API client function

## Files to Create
- `src/hooks/useSbomComparison.ts` — React Query hook wrapping `compareSboms()`; accepts `leftId` and `rightId` as parameters; only enabled when both IDs are provided
- `tests/mocks/fixtures/sbom-comparison.json` — mock comparison response fixture with representative data for all six diff categories
- `tests/mocks/handlers.ts` — extend existing MSW handlers to include `GET /api/v2/sbom/compare` (modify existing file)

## Implementation Notes

### TypeScript interfaces
Add the following interfaces to `src/api/models.ts`:
```typescript
interface AddedPackage {
  name: string;
  version: string;
  license: string;
  advisory_count: number;
}

interface RemovedPackage {
  name: string;
  version: string;
  license: string;
  advisory_count: number;
}

interface VersionChange {
  name: string;
  left_version: string;
  right_version: string;
  direction: "upgrade" | "downgrade";
}

interface NewVulnerability {
  advisory_id: string;
  severity: string;
  title: string;
  affected_package: string;
}

interface ResolvedVulnerability {
  advisory_id: string;
  severity: string;
  title: string;
  previously_affected_package: string;
}

interface LicenseChange {
  name: string;
  left_license: string;
  right_license: string;
}

interface SbomComparisonResult {
  added_packages: AddedPackage[];
  removed_packages: RemovedPackage[];
  version_changes: VersionChange[];
  new_vulnerabilities: NewVulnerability[];
  resolved_vulnerabilities: ResolvedVulnerability[];
  license_changes: LicenseChange[];
}
```

### API client function
Add to `src/api/rest.ts` following the pattern of existing functions (e.g., `fetchSboms()`):
```typescript
export const compareSboms = (leftId: string, rightId: string): Promise<SbomComparisonResult> =>
  client.get(`/api/v2/sbom/compare`, { params: { left: leftId, right: rightId } }).then(res => res.data);
```

Use the existing Axios instance from `src/api/client.ts` which includes base URL and auth interceptors.

### React Query hook
Create `src/hooks/useSbomComparison.ts` following the pattern of `src/hooks/useSbomById.ts`:
- Accept `leftId: string | undefined` and `rightId: string | undefined`
- Use `useQuery` with a query key like `["sbom-comparison", leftId, rightId]`
- Set `enabled: !!leftId && !!rightId` so the query does not fire until both IDs are selected
- Return the standard React Query result object

### MSW handler
Extend `tests/mocks/handlers.ts` to add a handler for `GET /api/v2/sbom/compare` that returns the fixture data from `tests/mocks/fixtures/sbom-comparison.json`. Follow the same handler pattern used for existing endpoints.

### Backend API contracts
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — response shape: `SbomComparisonResult` as defined above (see backend Task 1: `modules/fundamental/src/sbom/endpoints/compare.rs`)
- Verify these contracts against the backend repo during implementation using the implement-task cross-repo API verification step.

### Relevant constraints
- Per constraints doc section 2 (Commit Rules): commits must reference TC-9003 in the footer, follow Conventional Commits format, and include the `Assisted-by: Claude Code` trailer.
- Per constraints doc section 5 (Code Change Rules): changes must be scoped to listed files; follow existing patterns in `src/api/rest.ts` and `src/hooks/`.

## Reuse Candidates
- `src/api/client.ts` — existing Axios instance with base URL and auth interceptors; use for the compareSboms function
- `src/api/rest.ts::fetchSboms` — reference for API client function pattern (Axios GET with params)
- `src/hooks/useSbomById.ts` — reference for single-resource React Query hook pattern with `enabled` guard
- `src/hooks/useSboms.ts` — reference for list-based React Query hook pattern
- `tests/mocks/handlers.ts` — existing MSW handler registration; extend with comparison endpoint handler
- `tests/mocks/fixtures/sboms.json` — reference for fixture data format conventions

## Acceptance Criteria
- [ ] `SbomComparisonResult` and all nested interfaces are exported from `src/api/models.ts`
- [ ] `compareSboms(leftId, rightId)` function is exported from `src/api/rest.ts` and calls the correct endpoint with query parameters
- [ ] `useSbomComparison` hook returns React Query result; does not fire when either ID is undefined
- [ ] `useSbomComparison` hook fires the API call when both IDs are provided
- [ ] MSW handler for `GET /api/v2/sbom/compare` returns fixture data in the correct shape
- [ ] Mock fixture includes at least one entry in each of the six diff categories

## Test Requirements
- [ ] Unit test: `useSbomComparison` with both IDs provided returns data matching the mock fixture
- [ ] Unit test: `useSbomComparison` with one ID undefined does not trigger a network request
- [ ] Unit test: `compareSboms` calls the correct endpoint URL with `left` and `right` query parameters
- [ ] Tests use MSW handlers and follow patterns in `tests/setup.ts`

## Dependencies
- Depends on: Task 1 — Backend SBOM comparison endpoint and diffing service (defines the API contract this task implements the client for)
