## Repository
trustify-ui

## Target Branch
main

## Parent Epic
TC-9006: trustify-ui

## Description
Add TypeScript interfaces for remediation API responses and client functions for the new remediation endpoints. Create React Query hooks that wrap the API calls for use in dashboard components, following the existing hook patterns in the codebase.

## Files to Modify
- `src/api/models.ts` — Add RemediationSummary and ProductRemediation TypeScript interfaces
- `src/api/rest.ts` — Add API client functions getRemediationSummary() and getRemediationByProduct()

## Files to Create
- `src/hooks/useRemediationSummary.ts` — React Query hook wrapping getRemediationSummary() with caching and refetch configuration
- `src/hooks/useRemediationByProduct.ts` — React Query hook wrapping getRemediationByProduct() with pagination support

## Implementation Notes
TypeScript interfaces should mirror the backend model structs:

- `RemediationSummary`: severity x status count matrix with total count
- `ProductRemediation`: product id, name, total, open, inProgress, resolved counts
- `PaginatedResponse<T>`: generic paginated wrapper matching backend PaginatedResults

API client functions:
- `getRemediationSummary(filters?)`: GET /api/v2/remediation/summary with optional filter params
- `getRemediationByProduct(filters?, pagination?)`: GET /api/v2/remediation/by-product with filter and pagination params
- Follow the existing client function patterns in `src/api/rest.ts`

React Query hooks:
- Use `useQuery` with appropriate query keys including filter parameters
- Configure staleTime for dashboard data (remediation data changes infrequently)
- Support refetch on window focus for real-time updates

Per CONVENTIONS.md §Mutation Pattern: use React Query with queryClient.invalidateQueries(). Applies: task creates src/hooks/useRemediationSummary.ts matching the convention's .ts hook scope.

## Acceptance Criteria
- [ ] RemediationSummary and ProductRemediation TypeScript interfaces match backend models
- [ ] getRemediationSummary() calls GET /api/v2/remediation/summary with optional filters
- [ ] getRemediationByProduct() calls GET /api/v2/remediation/by-product with pagination
- [ ] useRemediationSummary hook provides loading, error, and data states
- [ ] useRemediationByProduct hook supports pagination parameters
- [ ] All types are properly exported for use in dashboard components

## Test Requirements
- [ ] TypeScript compilation passes with no type errors
- [ ] Hook returns correct loading/error/data states in unit test

## Dependencies
- Depends on: Task 2 (backend endpoints must be defined so API contracts are known)

## Additional Fields
- priority: Major
- fixVersions: RHTPA 1.5.0
- labels: ai-generated-jira
