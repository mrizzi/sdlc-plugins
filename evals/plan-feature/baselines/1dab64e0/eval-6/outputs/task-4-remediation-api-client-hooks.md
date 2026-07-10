**Summary:** Add remediation API client, types, and React Query hooks
**Issue Type:** Task
**Parent Epic:** TC-9006: trustify-ui

## Repository
trustify-ui

## Target Branch
main

## Description
Add the TypeScript interfaces for remediation API responses, API client functions for calling the backend remediation endpoints, and React Query hooks for data fetching. This establishes the data layer that the dashboard page components will consume.

## Files to Modify
- `src/api/models.ts` — Add TypeScript interfaces for RemediationSummary, SeverityStatusCounts, StatusCounts, and ProductRemediation
- `src/api/rest.ts` — Add fetchRemediationSummary() and fetchRemediationByProduct() API client functions

## Files to Create
- `src/hooks/useRemediationSummary.ts` — React Query hook for fetching remediation summary data
- `src/hooks/useRemediationByProduct.ts` — React Query hook for fetching per-product remediation data with filter parameters

## Implementation Notes
Per CONVENTIONS.md §API layer: typed API functions live in `src/api/rest.ts`; React Query hooks live in `src/hooks/`.
Applies: task modifies `src/api/rest.ts` matching the convention's `.ts` API layer scope.

Per CONVENTIONS.md §State management: use React Query (TanStack Query) for server state; no Redux.
Applies: task creates `src/hooks/useRemediationSummary.ts` matching the convention's `.ts` hook scope.

Per CONVENTIONS.md §Naming: camelCase for hooks and utilities.
Applies: task creates `src/hooks/useRemediationByProduct.ts` matching the convention's `.ts` naming scope.

**Backend API contracts:**
- `GET /api/v2/remediation/summary` — response shape: `{ by_severity: Array<{ severity: string, open: number, in_progress: number, resolved: number }>, totals: { open: number, in_progress: number, resolved: number } }` (see `modules/fundamental/src/remediation/endpoints/summary.rs` in trustify-backend)
- `GET /api/v2/remediation/by-product?offset={offset}&limit={limit}` — response shape: `{ items: Array<{ product_name: string, total: number, open: number, in_progress: number, resolved: number }>, total: number }` (see `modules/fundamental/src/remediation/endpoints/by_product.rs` in trustify-backend)

Verify these contracts against the backend repo during implementation using the implement-task cross-repo API verification step.

Follow the existing API client pattern in `src/api/rest.ts` (e.g., `fetchSboms()`, `fetchAdvisories()`) using the Axios instance from `src/api/client.ts`.

The React Query hooks should follow the pattern in `src/hooks/useSboms.ts`:
- Use `useQuery` with a descriptive query key (e.g., `["remediation", "summary"]`)
- Accept optional filter parameters (severity, product, status) for the by-product hook
- Return the standard React Query result object (data, isLoading, isError)

## Reuse Candidates
- `src/api/rest.ts::fetchSboms` — API client function pattern using the shared Axios instance
- `src/api/models.ts` — TypeScript interface definition patterns for API response types
- `src/hooks/useSboms.ts` — React Query useQuery hook pattern with query key and fetch function
- `src/api/client.ts` — Axios instance with base URL and auth interceptors; use for all API calls

## Acceptance Criteria
- [ ] TypeScript interfaces accurately model the backend API response shapes
- [ ] `fetchRemediationSummary()` calls `GET /api/v2/remediation/summary` via the shared Axios client
- [ ] `fetchRemediationByProduct()` calls `GET /api/v2/remediation/by-product` with pagination and filter params
- [ ] React Query hooks wrap the fetch functions with appropriate query keys and options
- [ ] All type exports are available for import by page components

## Test Requirements
- [ ] Unit test: `fetchRemediationSummary` makes correct API call path and returns typed response
- [ ] Unit test: `fetchRemediationByProduct` passes pagination parameters (offset, limit) correctly
- [ ] Unit test: React Query hooks return loading/error/data states correctly using MSW mock handlers

## Dependencies
- Depends on: Task 2 — Add remediation REST API endpoints
