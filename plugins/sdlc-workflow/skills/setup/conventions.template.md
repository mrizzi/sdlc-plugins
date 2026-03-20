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

## Dependencies

<!-- Document policies for adding dependencies.
     Example:
     - Prefer standard library over external crates when reasonable
     - All new npm packages require team review
     - Pin exact versions in Cargo.toml -->

{{dependencies}}
