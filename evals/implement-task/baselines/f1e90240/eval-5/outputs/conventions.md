# Conventions Discovered from Sibling Analysis

## Production Code Conventions (from `migration/src/m0001_initial/mod.rs` sibling analysis)

### Migration structure
- Each migration lives in its own subdirectory under `migration/src/` named `m<NNNN>_<description>/mod.rs`
- Migration modules use a four-digit zero-padded numeric prefix (e.g., `m0001_`, `m0002_`) for chronological ordering
- Each module exports a `Migration` struct that implements SeaORM's `MigrationTrait`

### Imports and dependencies
- Migrations import `sea_orm_migration::prelude::*` for access to all migration utilities
- `async_trait::async_trait` is used for the async trait implementation on `MigrationTrait`

### Migration trait implementation
- Both `up` (apply) and `down` (rollback) methods are always implemented
- Return type is `Result<(), DbErr>` for both methods
- The `SchemaManager` parameter is used for all DDL operations
- `DeriveMigrationName` derive macro is used on the `Migration` struct for automatic naming

### Table and column references
- Local `#[derive(Iden)]` enums are defined within each migration module for table and column identifiers
- This keeps migrations self-contained, independent of changes to the entity crate
- Enum variants map to SQL identifiers (e.g., `Advisory::Table` maps to the `advisory` table name)

### Migration registration
- All migration modules are declared with `mod` statements in `migration/src/lib.rs`
- Migrations are registered in a `migrations()` function that returns `Vec<Box<dyn MigrationTrait>>`
- Each migration is wrapped in `Box::new(module::Migration)` and added to the vec in chronological order

## Framework Conventions (from repository-wide analysis)

### Error handling
- All handlers in `modules/*/endpoints/` return `Result<T, AppError>` with `.context()` wrapping
- `AppError` is defined in `common/src/error.rs` and implements `IntoResponse`

### Naming
- Service methods follow `verb_noun` pattern (e.g., `get_advisory`, `create_sbom`)
- Module directories follow `model/ + service/ + endpoints/` structure within each domain

### Testing
- Integration tests in `tests/api/` hit a real PostgreSQL test database
- Tests use `assert_eq!(resp.status(), StatusCode::OK)` pattern for response status validation
- Test files are organized by domain entity (e.g., `tests/api/advisory.rs`, `tests/api/sbom.rs`)

### Response patterns
- List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`
- Shared filtering, pagination, and sorting via `common/src/db/query.rs`

## Test Conventions (from `tests/api/advisory.rs` sibling analysis)

### Assertion style
- Endpoint tests use `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization
- List endpoint tests validate `total_count`, `items.len()`, and at least one item's key fields

### Error cases
- Endpoint tests include 404 tests with `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`

### Test naming
- Tests follow `test_<endpoint>_<scenario>` pattern (e.g., `test_list_advisories_filtered`)

### Test setup
- Tests use a real PostgreSQL test database with fixtures for setup
- Migration tests would verify both `up` and `down` execution against the test database
