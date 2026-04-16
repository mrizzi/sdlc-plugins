# Repository Structure: trustify-ui

A React/TypeScript frontend for the Trusted Profile Analyzer platform. Uses PatternFly
as the component library, React Router for navigation, and React Query for data fetching.

## Directory Tree

```
trustify-ui/
├── package.json
├── tsconfig.json
├── vite.config.ts
├── README.md
├── CONVENTIONS.md
├── public/
│   └── index.html
├── src/
│   ├── main.tsx                         # App entry point
│   ├── App.tsx                          # Root component, router setup
│   ├── api/
│   │   ├── client.ts                    # Axios instance with base URL and auth interceptors
│   │   ├── models.ts                    # TypeScript interfaces for API response types
│   │   └── rest.ts                      # API client functions: fetchSboms(), fetchAdvisories(), etc.
│   ├── hooks/
│   │   ├── useSboms.ts                  # React Query hook: useQuery for SBOM list
│   │   ├── useSbomById.ts              # React Query hook: useQuery for SBOM detail
│   │   ├── useAdvisories.ts             # React Query hook: useQuery for advisory list
│   │   └── useDeleteSbomMutation.ts     # React Query mutation hook for SBOM deletion
│   ├── pages/
│   │   ├── SbomListPage/
│   │   │   ├── SbomListPage.tsx         # SBOM list page with table and filters
│   │   │   └── SbomListPage.test.tsx
│   │   ├── SbomDetailPage/
│   │   │   ├── SbomDetailPage.tsx       # SBOM detail page with tabs
│   │   │   ├── SbomDetailPage.test.tsx
│   │   │   └── components/
│   │   │       ├── PackageTable.tsx      # Package list table component
│   │   │       ├── AdvisoryList.tsx      # Advisory list for an SBOM
│   │   │       └── SbomMetadata.tsx      # SBOM metadata display
│   │   ├── AdvisoryListPage/
│   │   │   ├── AdvisoryListPage.tsx      # Advisory list page
│   │   │   └── AdvisoryListPage.test.tsx
│   │   └── SearchPage/
│   │       ├── SearchPage.tsx            # Global search page
│   │       └── SearchPage.test.tsx
│   ├── components/
│   │   ├── SeverityBadge.tsx             # Severity level badge (Critical/High/Medium/Low)
│   │   ├── FilterToolbar.tsx             # Reusable filter toolbar with PatternFly
│   │   ├── EmptyStateCard.tsx            # Empty state placeholder
│   │   └── LoadingSpinner.tsx            # Loading indicator
│   ├── routes.tsx                        # Route definitions: path → page component
│   └── utils/
│       ├── formatDate.ts                 # Date formatting helpers
│       └── severityUtils.ts             # Severity level ordering, color mapping
├── tests/
│   ├── setup.ts                          # Test setup: MSW handlers, render helpers
│   ├── mocks/
│   │   ├── handlers.ts                   # MSW request handlers
│   │   └── fixtures/
│   │       ├── sboms.json                # Mock SBOM data
│   │       └── advisories.json           # Mock advisory data
│   └── e2e/
│       └── sbom-list.spec.ts             # Playwright E2E tests
└── .env.development                      # Dev environment variables (API base URL)
```

## Key Conventions

- **Framework**: React 18 + TypeScript + Vite
- **Component library**: PatternFly 5 — all UI components use PF5 equivalents
- **State management**: React Query (TanStack Query) for server state; no Redux
- **Routing**: React Router v6 with lazy-loaded page components
- **API layer**: Axios client in `src/api/client.ts`; typed API functions in `src/api/rest.ts`; React Query hooks in `src/hooks/`
- **Page structure**: Each page gets its own directory under `src/pages/` with a main component, optional test file, and `components/` subdirectory for page-specific components
- **Shared components**: Reusable components live in `src/components/`
- **Testing**: Vitest + React Testing Library for unit tests; Playwright for E2E; MSW for API mocking
- **Naming**: PascalCase for components, camelCase for hooks and utilities, kebab-case for directories
- **Mutation pattern**: React Query mutations use `onSuccess` with `queryClient.invalidateQueries()` for cache invalidation + toast notification; never use `window.location.reload()`
