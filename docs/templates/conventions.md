# Coding Conventions Template

<!-- TODO: Copy this template into your project and fill in the sections below.
     This document helps the AI assistant follow your project's coding standards
     when generating or modifying code. -->

## Language and Framework

<!-- TODO: Specify the primary languages and frameworks.
     Example:
     - Backend: Rust with Actix-web
     - Frontend: TypeScript with React and PatternFly
     - Infrastructure: Helm charts with YAML -->

## Code Style

<!-- TODO: Document formatting and style rules.
     Example:
     - Rust: follow `rustfmt` defaults, run `cargo fmt` before committing
     - TypeScript: ESLint + Prettier, run `npm run lint` before committing
     - Maximum line length: 100 characters -->

## Naming Conventions

<!-- TODO: Document naming patterns for your codebase.
     Example:
     - Rust structs: PascalCase (e.g., `SbomService`)
     - Rust functions: snake_case (e.g., `fetch_advisory`)
     - TypeScript components: PascalCase (e.g., `AdvisoryList`)
     - Database tables: snake_case (e.g., `sbom_packages`)
     - API endpoints: kebab-case (e.g., `/api/v1/sbom-packages`) -->

## File Organization

<!-- TODO: Describe where new files should be placed.
     Example:
     - New API endpoints go in `modules/<domain>/endpoints/`
     - New React components go in `client/src/app/pages/<feature>/`
     - Database migrations go in `migration/` with timestamp prefix -->

## Error Handling

<!-- TODO: Document error handling patterns.
     Example:
     - Use `Result<T, Error>` for all fallible operations
     - Map external errors with `.context("descriptive message")`
     - Return HTTP 4xx for client errors, 5xx for server errors -->

## Testing Conventions

<!-- TODO: Document testing patterns and requirements.
     Example:
     - Every public function must have at least one unit test
     - Integration tests use the `#[test_context]` macro
     - Frontend components need snapshot tests -->

## Commit Messages

<!-- TODO: Document your commit message format.
     Example:
     - Follow Conventional Commits: `type(scope): description`
     - Types: feat, fix, refactor, test, docs, chore
     - Always reference the Jira issue in the footer -->

## Dependencies

<!-- TODO: Document policies for adding dependencies.
     Example:
     - Prefer standard library over external crates when reasonable
     - All new npm packages require team review
     - Pin exact versions in Cargo.toml -->

## Performance Optimization

<!-- TODO: Document when and how to run performance optimization workflow.
     Example:
     - Run `/sdlc-workflow:performance-setup` once per repository to initialize configuration
     - Capture baseline before starting optimization work
     - Re-capture baseline after major feature additions or library upgrades
     - Target metrics for this repository:
       * LCP (p95): < 2500 ms
       * FCP (p95): < 1800 ms
       * DOM Interactive (p95): < 3500 ms
       * Bundle size: < 500 KB (main bundle)
     - Anti-pattern severity thresholds:
       * High: Impacts LCP by > 500ms or bundle size by > 100KB
       * Medium: Impacts LCP by 200-500ms or bundle size by 50-100KB
       * Low: Impacts LCP by < 200ms or bundle size by < 50KB
     - Baseline capture frequency: weekly, before/after optimization, before release
     - Performance budget enforcement: CI fails if LCP > 3000ms or bundle > 600KB -->
