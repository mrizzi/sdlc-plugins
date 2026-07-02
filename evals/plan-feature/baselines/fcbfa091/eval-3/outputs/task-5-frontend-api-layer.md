## additional_fields
```
{ "labels": ["ai-generated-jira"], "priority": {"name": "Critical"}, "fixVersions": [{"name": "RHTPA 1.5.0"}] }
```

## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add the frontend API layer for the SBOM comparison feature: TypeScript interfaces for the comparison response, an API client function, and a React Query hook. This provides the data-fetching foundation that the comparison page (Task 6) will consume.

## Files to Create
- `src/hooks/useSbomComparison.ts` — React Query hook wrapping `fetchSbomComparison` with `left` and `right` SBOM ID parameters; enabled only when both IDs are provided

## Files to Modify
- `src/api/models.ts` — Add TypeScript interfaces: `SbomComparisonResult`, `AddedPackage`, `RemovedPackage`, `VersionChange`, `NewVulnerability`, `ResolvedVulnerability`, `LicenseChange`
- `src/api/rest.ts` — Add `fetchSbomComparison(leftId: string, rightId: string): Promise<SbomComparisonResult>` function calling `GET /api/v2/sbom/compare?left={leftId}&right={rightId}`

## Implementation Notes
TypeScript interfaces must match the backend response shape exactly:

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

Sub-interfaces:
- `AddedPackage` / `RemovedPackage`: `name: string`, `version: string`, `license: string`, `advisory_count: number`
- `VersionChange`: `name: string`, `left_version: string`, `right_version: string`, `direction: "upgrade" | "downgrade"`
- `NewVulnerability`: `advisory_id: string`, `severity: string`, `title: string`, `affected_package: string`
- `ResolvedVulnerability`: `advisory_id: string`, `severity: string`, `title: string`, `previously_affected_package: string`
- `LicenseChange`: `name: string`, `left_license: string`, `right_license: string`

The API client function in `src/api/rest.ts` should follow the existing pattern of `fetchSboms()` and `fetchAdvisories()` — use the Axios instance from `src/api/client.ts` with typed response.

The React Query hook should follow the pattern in `src/hooks/useSboms.ts` and `src/hooks/useSbomById.ts`:
- Use `useQuery` with a query key like `["sbom-comparison", leftId, rightId]`
- Set `enabled: !!leftId && !!rightId` to prevent calls when IDs are missing

**Backend API contracts:**
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — response shape: `SbomComparisonResult` with six array fields as defined above (see `modules/fundamental/src/sbom/endpoints/compare.rs` in trustify-backend, created in Task 4)

Verify these contracts against the backend repo during implementation using the implement-task cross-repo API verification step.

Per CONVENTIONS.md §API layer: Axios client in `src/api/client.ts`; typed API functions in `src/api/rest.ts`; React Query hooks in `src/hooks/`.
Applies: task modifies `src/api/rest.ts` matching the convention's `.ts` scope.

Per CONVENTIONS.md §State management: React Query (TanStack Query) for server state; no Redux.
Applies: task creates `src/hooks/useSbomComparison.ts` matching the convention's `.ts` scope.

Per CONVENTIONS.md §Naming: camelCase for hooks and utilities.
Applies: task creates `src/hooks/useSbomComparison.ts` matching the convention's `.ts` scope.

## Reuse Candidates
- `src/api/rest.ts::fetchSboms` — Existing API client function pattern; follow the same Axios call and typing approach
- `src/api/client.ts` — Axios instance with base URL and auth interceptors; use for the comparison request
- `src/api/models.ts` — Existing TypeScript interfaces; follow naming and structure conventions
- `src/hooks/useSboms.ts` — Existing React Query hook pattern; follow for useQuery configuration
- `src/hooks/useSbomById.ts` — Existing single-entity hook pattern; reference for parameterized query key and enabled guard

## Acceptance Criteria
- [ ] TypeScript interfaces for all comparison response types are defined in `src/api/models.ts`
- [ ] `fetchSbomComparison()` function is added to `src/api/rest.ts` using the Axios client
- [ ] `useSbomComparison` hook is created in `src/hooks/` with proper query key and enabled guard
- [ ] Hook returns loading, error, and data states matching React Query conventions
- [ ] API function targets the correct endpoint path `GET /api/v2/sbom/compare`
- [ ] TypeScript types match the backend response shape exactly (snake_case field names)

## Test Requirements
- [ ] Unit test: `fetchSbomComparison` calls the correct endpoint with left and right query parameters
- [ ] Unit test: `useSbomComparison` hook is disabled when either SBOM ID is undefined/empty
- [ ] Unit test: `useSbomComparison` hook is enabled and fetches data when both SBOM IDs are provided
- [ ] Unit test: hook correctly returns typed `SbomComparisonResult` data

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 4 — Backend comparison endpoint (the endpoint must exist for the API client to target)
