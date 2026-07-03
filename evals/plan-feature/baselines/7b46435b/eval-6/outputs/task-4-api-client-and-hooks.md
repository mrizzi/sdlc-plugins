## Repository
trustify-ui

## Target Branch
main

## Description
Create the frontend API integration layer for the remediation dashboard. This task adds TypeScript interfaces for the remediation API response types, Axios client functions to call the backend endpoints, and React Query hooks for data fetching. This establishes the data layer that the dashboard page (Task 5) will consume.

Parent Epic: TC-9006: trustify-ui

additional_fields: { "labels": ["ai-generated-jira"], "priority": {"name": "Major"}, "fixVersions": [{"name": "RHTPA 1.5.0"}] }

## Files to Create
- `src/hooks/useRemediationSummary.ts` -- React Query hook wrapping `useQuery` for `GET /api/v2/remediation/summary`, returns `RemediationSummary` data with loading/error states
- `src/hooks/useRemediationByProduct.ts` -- React Query hook wrapping `useQuery` for `GET /api/v2/remediation/by-product` with pagination parameters (offset, limit)

## Files to Modify
- `src/api/models.ts` -- add `RemediationSummary` and `ProductRemediation` TypeScript interfaces alongside existing types
- `src/api/rest.ts` -- add `fetchRemediationSummary()` and `fetchRemediationByProduct(params: { offset: number; limit: number })` API client functions using Axios instance

## Implementation Notes
Follow the existing API layer patterns established in the codebase:
- Add interfaces to `src/api/models.ts` alongside existing types (`SbomSummary`, `AdvisorySummary`, etc.)
- Add client functions to `src/api/rest.ts` using the Axios instance from `src/api/client.ts`, following the pattern of `fetchSboms()` and `fetchAdvisories()`
- Create hooks in `src/hooks/` following the pattern of `src/hooks/useSboms.ts` and `src/hooks/useAdvisories.ts`

The `useRemediationSummary` hook should use `useQuery` with query key `["remediation", "summary"]`. The `useRemediationByProduct` hook should accept pagination parameters and pass them as query params, using query key `["remediation", "by-product", { offset, limit }]`.

**Backend API contracts:**
- `GET /api/v2/remediation/summary` -- response shape: `{ critical: { open: number, inProgress: number, resolved: number }, high: { open: number, inProgress: number, resolved: number }, medium: { open: number, inProgress: number, resolved: number }, low: { open: number, inProgress: number, resolved: number }, totals: { open: number, inProgress: number, resolved: number, total: number } }` (see `modules/fundamental/src/remediation/endpoints/summary.rs` in trustify-backend)
- `GET /api/v2/remediation/by-product?offset={offset}&limit={limit}` -- response shape: `{ items: ProductRemediation[], total: number }` where `ProductRemediation` is `{ name: string, total: number, open: number, inProgress: number, resolved: number }` (see `modules/fundamental/src/remediation/endpoints/by_product.rs` in trustify-backend)

Verify these contracts against the backend repo during implementation using the implement-task cross-repo API verification step.

Per CONVENTIONS.md: use React Query (TanStack Query) hooks pattern with `useQuery` for server state management.
Applies: task creates `src/hooks/useRemediationSummary.ts` matching the convention's `.ts` hook file scope.

Per CONVENTIONS.md: API client functions use Axios instance from `src/api/client.ts` with typed responses.
Applies: task modifies `src/api/rest.ts` matching the convention's `.ts` API file scope.

Per CONVENTIONS.md: camelCase naming for hooks and utilities.
Applies: task creates `src/hooks/useRemediationSummary.ts` matching the convention's `.ts` naming scope.

## Reuse Candidates
- `src/api/rest.ts::fetchSboms()` -- established pattern for API client functions with Axios
- `src/api/rest.ts::fetchAdvisories()` -- API client function pattern with typed responses
- `src/hooks/useSboms.ts` -- React Query hook pattern for list data fetching
- `src/hooks/useSbomById.ts` -- React Query hook pattern for single-item data fetching
- `src/hooks/useAdvisories.ts` -- React Query hook pattern for advisory data
- `src/api/models.ts` -- existing TypeScript interface definitions for API response types
- `src/api/client.ts` -- Axios instance with base URL and auth interceptors

## Acceptance Criteria
- [ ] `RemediationSummary` TypeScript interface defined in `src/api/models.ts` matching backend response shape
- [ ] `ProductRemediation` TypeScript interface defined in `src/api/models.ts` matching backend response shape
- [ ] `fetchRemediationSummary()` function calls `GET /api/v2/remediation/summary` and returns typed `RemediationSummary`
- [ ] `fetchRemediationByProduct(params)` function supports `offset` and `limit` pagination parameters
- [ ] `useRemediationSummary` hook returns React Query result with loading, error, and data states
- [ ] `useRemediationByProduct` hook returns paginated React Query result with refetch on param change

## Test Requirements
- [ ] Unit test: `fetchRemediationSummary` calls the correct API endpoint path
- [ ] Unit test: `fetchRemediationByProduct` passes pagination params as query parameters
- [ ] Unit test: `useRemediationSummary` hook returns expected loading, error, and success states using MSW handlers
- [ ] Unit test: `useRemediationByProduct` hook handles pagination state correctly

## Verification Commands
- `npm run type-check` -- TypeScript compilation succeeds with no errors
- `npm run test -- --filter remediation` -- unit tests pass

## Dependencies
- Depends on: Task 2 -- Implement remediation REST endpoints (API contract must be defined)
