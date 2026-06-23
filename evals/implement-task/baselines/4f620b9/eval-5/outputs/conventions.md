# Discovered Conventions from Sibling Analysis

## Production Code Conventions

### Migration Pattern (from `migration/src/m0001_initial/mod.rs`)

- **Structure**: Each migration lives in its own subdirectory under `migration/src/` with a `mod.rs` file.
- **Naming**: Migration directories follow the pattern `m<NNNN>_<snake_case_description>` (e.g., `m0001_initial`, `m0002_drop_advisory_status`).
- **Struct**: Each migration defines a `pub struct Migration` with `#[derive(DeriveMigrationName)]`.
- **Trait implementation**: Implements `MigrationTrait` with `async fn up()` and `async fn down()` methods, both returning `Result<(), DbErr>`.
- **Async trait**: Uses `#[async_trait::async_trait]` attribute on the trait implementation.
- **Imports**: Uses `use sea_orm_migration::prelude::*;` for all SeaORM migration types.
- **Local identifiers**: Defines a local `#[derive(DeriveIden)]` enum for table and column identifiers rather than importing from the entity crate. This makes migrations self-contained and resilient to future entity changes.

### Migration Registry (from `migration/src/lib.rs`)

- **Module declarations**: Each migration module is declared with `mod m<NNNN>_<name>;` in chronological order.
- **Registration**: Migrations are registered in the `migrations()` function, which returns `Vec<Box<dyn MigrationTrait>>`.
- **Ordering**: Migrations are listed in chronological order in the `vec![]` (oldest first).

### Error Handling (from `common/src/error.rs` and module conventions)

- All handlers return `Result<T, AppError>` with `.context()` wrapping for error enrichment.
- Framework: Axum for HTTP, SeaORM for database ORM.

### Module Structure (from `modules/fundamental/src/`)

- Each domain module follows the `model/ + service/ + endpoints/` directory structure.
- Endpoint modules register routes via `endpoints/mod.rs`.
- `server/main.rs` mounts all module route registrations.

### Naming Conventions

- Service methods follow `verb_noun` pattern (e.g., `get_advisory`, `create_sbom`, `list_sboms`).
- Response types for list endpoints use `PaginatedResults<T>` from `common/src/model/paginated.rs`.

### API Conventions

- Endpoint paths follow REST conventions with plural nouns (e.g., `/api/v2/advisory`, `/api/v2/sbom`).
- Shared filtering, pagination, and sorting via `common/src/db/query.rs`.

## Test Conventions (from `tests/api/`)

- **Framework**: Integration tests in `tests/api/` run against a real PostgreSQL test database.
- **Assertion style**: Use `assert_eq!(resp.status(), StatusCode::OK)` pattern for status code verification, followed by body deserialization.
- **Test file organization**: One test file per domain area (e.g., `tests/api/advisory.rs` for advisory endpoints, `tests/api/sbom.rs` for SBOM endpoints).
- **Test naming**: Tests follow the `test_<endpoint>_<scenario>` pattern (e.g., `test_list_advisories_filtered`).

## Documentation Conventions

- Repository root contains `README.md` and `CONVENTIONS.md`.
- Architecture documentation in `docs/architecture.md`.
- API documentation in `docs/api.md`.

## Commit Conventions

- Conventional Commits format: `<type>(<scope>): <description>`.
- Footer must include `Implements <JIRA-ID>`.
- Trailer must include `Assisted-by: Claude Code`.
