# Coding Conventions

<!-- This file documents project-specific coding standards for {{repository-name}}.
     It helps the AI assistant follow your project's patterns when generating
     or modifying code. Fill in each section with your project's conventions. -->

## Language and Framework

<!-- Specify the primary languages and frameworks.
     Example:
     - Backend: Rust with Actix-web
     - Frontend: TypeScript with React and PatternFly
     - Infrastructure: Helm charts with YAML -->

{{language-and-framework}}

## Code Style

<!-- Document formatting and style rules.
     Example:
     - Rust: follow `rustfmt` defaults, run `cargo fmt` before committing
     - TypeScript: ESLint + Prettier, run `npm run lint` before committing
     - Maximum line length: 100 characters -->

{{code-style}}

## Naming Conventions

<!-- Document naming patterns for your codebase.
     Example:
     - Rust structs: PascalCase (e.g., `SbomService`)
     - Rust functions: snake_case (e.g., `fetch_advisory`)
     - TypeScript components: PascalCase (e.g., `AdvisoryList`)
     - Database tables: snake_case (e.g., `sbom_packages`)
     - API endpoints: kebab-case (e.g., `/api/v1/sbom-packages`) -->

{{naming-conventions}}

## File Organization

<!-- Describe where new files should be placed.
     Example:
     - New API endpoints go in `modules/<domain>/endpoints/`
     - New React components go in `client/src/app/pages/<feature>/`
     - Database migrations go in `migration/` with timestamp prefix -->

{{file-organization}}

## Error Handling

<!-- Document error handling patterns.
     Example:
     - Use `Result<T, Error>` for all fallible operations
     - Map external errors with `.context("descriptive message")`
     - Return HTTP 4xx for client errors, 5xx for server errors -->

{{error-handling}}

## Testing Conventions

<!-- Document testing patterns and requirements.
     Example:
     - Every public function must have at least one unit test
     - Integration tests use the `#[test_context]` macro
     - Frontend components need snapshot tests -->

{{testing-conventions}}

## Commit Messages

<!-- Document your commit message format.
     Example:
     - Follow Conventional Commits: `type(scope): description`
     - Types: feat, fix, refactor, test, docs, chore
     - Always reference the Jira issue in the footer -->

{{commit-messages}}

## Shared Modules and Reuse

<!-- Document shared utilities, helpers, and common abstractions that should be
     reused instead of duplicating logic. This helps AI assistants find existing
     code before writing new implementations.
     Example:
     - Utility directory: `src/utils/` — common helpers (string formatting, date parsing)
     - Shared HTTP client: `src/common/http.ts` — use `apiClient` for all API calls
     - Error types: `modules/error/` — use `AppError` and existing error variants
     - Shared components: `client/src/components/` — reuse PatternFly wrappers
     - Database helpers: `src/db/helpers.rs` — use `paginate()` for paginated queries -->

{{shared-modules-and-reuse}}

## Documentation

<!-- Document where documentation lives and when it should be updated.
     Example:
     - README: `README.md` at repo root — update when setup steps or project overview changes
     - API docs: `docs/api/` — update when public endpoints are added or modified
     - Architecture: `docs/architecture.md` — update when major structural changes are made
     - Formats: Markdown for all docs, OpenAPI 3.0 for API specs
     - Triggers: update docs when public APIs, configuration, CLI commands, or setup steps change -->

{{documentation}}

## Dependencies

<!-- Document policies for adding dependencies.
     Example:
     - Prefer standard library over external crates when reasonable
     - All new npm packages require team review
     - Pin exact versions in Cargo.toml -->

{{dependencies}}

## Performance Optimization

<!-- Document performance optimization conventions for your project.
     This section guides performance workflow usage and metrics expectations.
     See the Performance Workflow documentation for details on the performance
     optimization workflow (setup, baseline, analyze, plan, implement, verify).
     
     Example:
     - Baseline capture frequency: Before major releases, after library upgrades
     - Target metrics: LCP < 2500ms (p95), FCP < 1800ms (p95), TTI < 3500ms (p95)
     - Anti-pattern severity thresholds: Follow default thresholds in performance-metrics-guide.md
     - Commit message type: Use `perf(scope): description` for performance optimizations
     - Performance documentation: Quick reference style (tables, bullets, minimal prose)
     - Regression threshold: 5% degradation in non-target scenarios triggers investigation -->

{{performance-optimization}}
