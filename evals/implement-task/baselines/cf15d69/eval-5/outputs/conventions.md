# Conventions Discovered from Sibling Analysis

## Production Code Conventions

### Migration pattern (from `m0001_initial/mod.rs`)

- **Module structure**: Each migration lives in its own directory under `migration/src/` with a single `mod.rs` file (e.g., `migration/src/m0001_initial/mod.rs`)
- **Naming**: Migration directories follow the pattern `m<NNNN>_<descriptive_name>` where NNNN is a zero-padded sequential number
- **Struct naming**: The migration struct is named `Migration` (unqualified) -- each module's namespace provides disambiguation
- **Trait implementation**: Each migration struct implements `MigrationName` (for the `name()` method) and `MigrationTrait` (for `up()` and `down()` methods)
- **Name method**: Returns a string matching the module directory name (e.g., `"m0001_initial"`)
- **Imports**: Use `sea_orm_migration::prelude::*` for SeaORM migration utilities
- **Iden enums**: Table and column identifiers are defined as local `#[derive(Iden)]` enums within the migration module, keeping migrations self-contained and independent of the current entity definitions

### Migration registration (from `migration/src/lib.rs`)

- **Module declarations**: `mod` statements for each migration are ordered chronologically at the top of `lib.rs`
- **Registration**: Migrations are registered in a `migrations()` method that returns `Vec<Box<dyn MigrationTrait>>`, with entries in chronological order
- **Boxing pattern**: Each migration is added as `Box::new(module_name::Migration)`

### Entity conventions (from `entity/src/advisory.rs` and siblings)

- **Framework**: SeaORM entities with derive macros
- **Column mapping**: Each entity field maps to a database column; removed columns should have no corresponding field in the entity struct
- **Enum variants**: Table and column names use SeaORM's `Iden` derive macro for type-safe references

### General project conventions (from repo Key Conventions)

- **Framework**: Axum for HTTP, SeaORM for database
- **Module pattern**: Each domain module follows `model/ + service/ + endpoints/` structure
- **Error handling**: All handlers return `Result<T, AppError>` with `.context()` wrapping
- **Response types**: List endpoints return `PaginatedResults<T>`
- **Testing**: Integration tests in `tests/api/` hit a real PostgreSQL test database
- **Assertion style**: Tests use `assert_eq!(resp.status(), StatusCode::OK)` pattern

## Test Conventions

### Integration test patterns (from `tests/api/advisory.rs` and siblings)

- **Location**: Integration tests live in `tests/api/` with one file per domain (e.g., `advisory.rs`, `sbom.rs`)
- **Database**: Tests run against a real PostgreSQL test database (not mocked)
- **Assertion style**: Use `assert_eq!` with `StatusCode` variants for HTTP response validation, followed by body deserialization and field assertions
- **Test naming**: Tests follow `test_<endpoint>_<scenario>` pattern (e.g., `test_list_advisories_filtered`)
- **Response validation**: List endpoint tests validate `total_count`, `items.len()`, and key fields on individual items
- **Error cases**: Tests include cases for not-found and invalid input scenarios
- **Documentation**: Each test function should have a `///` doc comment (per skill requirement, even if existing tests do not have them)

## Convention Conflicts

No conflicts detected between the task description / Implementation Notes and the discovered conventions. The task aligns with established migration patterns.
