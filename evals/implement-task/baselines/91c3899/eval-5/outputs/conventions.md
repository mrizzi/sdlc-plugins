# Conventions Discovered from Sibling Analysis

## Migration Conventions (from `migration/src/m0001_initial/mod.rs`)

- **Module naming**: Migrations follow the pattern `m<NNNN>_<descriptive_name>` where NNNN is a zero-padded sequential number (e.g., `m0001_initial`, `m0002_drop_advisory_status`)
- **Directory structure**: Each migration is a directory-based module: `migration/src/<module_name>/mod.rs`
- **Trait implementation**: Every migration implements both `MigrationName` (for `name()`) and `MigrationTrait` (for `up()` and `down()`)
- **Name format**: The `name()` method returns the module directory name as a string (e.g., `"m0001_initial"`)
- **Column identifiers**: Migrations define a local `#[derive(Iden)]` enum for table and column references rather than importing from the entity crate, keeping migrations self-contained
- **Error handling**: All migration methods return `Result<(), DbErr>` using SeaORM's error type
- **Async trait**: Migrations use `#[async_trait::async_trait]` for async `up()` and `down()` methods
- **Registration**: Migrations are registered in `migration/src/lib.rs` via `Box::new(<module>::Migration)` entries in the `migrations()` function's `vec![]`, in chronological order
- **Rollback**: Every migration must implement `down()` to support rollback -- the down method reverses the up operation

## Entity Conventions (from `entity/src/advisory.rs` and siblings)

- **Framework**: SeaORM is used for all database entities
- **File naming**: One entity per file, named after the database table (e.g., `advisory.rs`, `sbom.rs`, `package.rs`)
- **Location**: All entity files are in `entity/src/`

## General Project Conventions (from repo structure)

- **Framework**: Axum for HTTP, SeaORM for database
- **Module pattern**: Each domain module follows `model/ + service/ + endpoints/` structure
- **Error handling**: All handlers return `Result<T, AppError>` with `.context()` wrapping
- **Endpoint registration**: Each module's `endpoints/mod.rs` registers routes; `server/main.rs` mounts all modules
- **Response types**: List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`
- **Query helpers**: Shared filtering, pagination, and sorting via `common/src/db/query.rs`
- **Testing**: Integration tests in `tests/api/` hit a real PostgreSQL test database; use `assert_eq!(resp.status(), StatusCode::OK)` pattern

## Test Conventions (from `tests/api/` siblings)

- **Assertion style**: Tests use `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization
- **Test database**: Tests run against a real PostgreSQL test database (not mocked)
- **Test location**: Integration tests are in `tests/api/` directory
- **Test naming**: Tests follow `test_<endpoint>_<scenario>` pattern (e.g., `test_list_advisories_filtered`)
- **Error cases**: Endpoint tests include tests for error status codes like `StatusCode::NOT_FOUND`

## Commit Conventions

- **Format**: Conventional Commits specification (`<type>[optional scope]: <description>`)
- **Types**: feat, fix, refactor, test, docs, chore
- **Scope**: Used when relevant (e.g., `feat(migration):`, `feat(api):`)
- **Footer**: Must reference the Jira issue ID (e.g., `Implements TC-9205`)
- **Trailer**: Must include `--trailer="Assisted-by: Claude Code"`
