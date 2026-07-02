# Conventions Discovered from Sibling Analysis

## Production Code Conventions

### Migration module conventions (from `migration/src/m0001_initial/mod.rs`)

- **Module naming**: migration directories follow the pattern `m<NNNN>_<snake_case_description>/` with a zero-padded four-digit sequence number (e.g., `m0001_initial`, `m0002_drop_advisory_status`)
- **File structure**: each migration module contains a single `mod.rs` file
- **Struct pattern**: a unit struct `Migration` (no fields) that implements `MigrationTrait`
- **Imports**: `use sea_orm_migration::prelude::*;` as the standard prelude import
- **Method signatures**: `async fn up(&self, manager: &SchemaManager) -> Result<(), DbErr>` and matching `down()` method
- **Table/column identifiers**: use SeaORM enum variants (e.g., `Advisory::Table`, `Advisory::Status`) rather than raw string table/column names
- **Schema operations**: use `manager.alter_table(...)`, `manager.create_table(...)` etc. with builder pattern ending in `.to_owned()`
- **Error handling**: methods return `Result<(), DbErr>` -- propagate errors with `?` operator, no manual error wrapping

### Migration registration conventions (from `migration/src/lib.rs`)

- **Module declaration**: `mod m<NNNN>_<description>;` at the top of `lib.rs`
- **Registration**: add `Box::new(m<NNNN>_<description>::Migration)` to the `vec![]` returned by `fn migrations() -> Vec<Box<dyn MigrationTrait>>`
- **Ordering**: migrations are listed in sequence order within the vec

### Entity conventions (from `entity/src/advisory.rs`)

- **SeaORM entities**: each entity file defines a `Model` struct with `#[derive(Clone, Debug, PartialEq, DeriveEntityModel)]` and a corresponding `Entity` with column enum variants
- **Column naming**: column enum variants use PascalCase matching the database column name in snake_case (e.g., `Severity` for `severity` column)

### General Rust conventions (from repository structure)

- **Framework**: Axum for HTTP, SeaORM for database ORM
- **Module pattern**: domain modules follow `model/ + service/ + endpoints/` structure
- **Error handling**: all handlers return `Result<T, AppError>` with `.context()` wrapping via the `anyhow` crate
- **Response types**: list endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`
- **Import organization**: standard library imports first, then external crates, then local modules

### Naming conventions

- **Service methods**: follow `verb_noun` pattern (e.g., `get_advisory`, `create_sbom`, `list_advisories`)
- **Endpoint files**: named after the HTTP action (e.g., `list.rs`, `get.rs`)
- **Module files**: `mod.rs` for re-exports and route registration

## Test Conventions

### Integration test conventions (from `tests/api/advisory.rs` and siblings)

- **Assertion style**: `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization
- **Response validation**: list endpoint tests validate `total_count`, `items.len()`, and at least one item's key fields
- **Error cases**: endpoint tests include a 404 test with `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`
- **Test naming**: tests follow `test_<endpoint>_<scenario>` pattern (e.g., `test_list_advisories_filtered`)
- **Database setup**: integration tests use a real PostgreSQL test database with migrations applied
- **Test organization**: tests grouped by domain entity in separate files under `tests/api/`

### Migration test conventions

- **Migration tests**: would verify `up()` applies cleanly and `down()` rolls back correctly
- **Column verification**: after running `up()`, query the table schema to confirm the column no longer exists; after `down()`, confirm the column was re-added
- **Query compatibility**: run existing advisory queries after migration to verify they still succeed without the dropped column

## Commit Message Conventions

- **Format**: Conventional Commits (`<type>[optional scope]: <description>`)
- **Types**: `feat`, `fix`, `refactor`, `test`, `docs`, `chore`
- **Scope**: use when relevant (e.g., `migration`, `api`, `advisory`)
- **Footer**: must reference Jira issue ID (`Implements TC-XXXX`)
- **Trailer**: include `--trailer="Assisted-by: Claude Code"`
