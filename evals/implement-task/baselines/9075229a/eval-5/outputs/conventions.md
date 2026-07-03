# Conventions Discovered from Sibling Analysis

## Production Code Conventions

### Migration Pattern (from `migration/src/m0001_initial/mod.rs`)

- **Structure**: Each migration lives in its own subdirectory under `migration/src/` with a `mod.rs` file
- **Naming**: Migration directories follow the pattern `m<NNNN>_<snake_case_description>` (e.g., `m0001_initial`, `m0002_drop_advisory_status`)
- **Trait implementation**: Each migration module defines a struct and implements `MigrationTrait` with `up` and `down` async methods
- **Up method**: Performs the forward migration (create table, add column, drop column, etc.)
- **Down method**: Performs the rollback (reverse the `up` operation)
- **Manager usage**: Migrations use the `SchemaManager` passed as a parameter to execute DDL statements
- **Table operations**: Use SeaORM's `Table::alter()`, `Table::create()`, etc. builder pattern with `.to_owned()` at the end

### Migration Registration (from `migration/src/lib.rs`)

- **Registration pattern**: All migrations are listed in a `vec![]` inside the `migrations()` function
- **Ordering**: Migrations are listed in chronological order (m0001 first, then m0002, etc.)
- **Module declaration**: Each migration module is declared with `mod m<NNNN>_<name>;` at the top of `lib.rs`
- **Box wrapping**: Each migration is wrapped in `Box::new()` when added to the vec (e.g., `Box::new(m0001_initial::Migration)`)

### Entity Conventions (from `entity/src/advisory.rs`)

- **Framework**: SeaORM entities with `DeriveEntityModel` derive macro
- **Column enum**: Each entity has an enum listing its columns (e.g., `Advisory::Table`, `Advisory::Status`, `Advisory::Severity`)
- **Column references**: Migration code references columns via the entity's column enum (e.g., `Advisory::Status`)

### General Code Conventions (from repo structure and Key Conventions)

- **Framework**: Axum for HTTP, SeaORM for database
- **Module pattern**: Each domain module follows `model/ + service/ + endpoints/` structure
- **Error handling**: All handlers return `Result<T, AppError>` with `.context()` wrapping
- **Response types**: List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`

## Test Conventions

### Integration Tests (from `tests/api/`)

- **Location**: Integration tests live in `tests/api/` with one file per domain entity (e.g., `advisory.rs`, `sbom.rs`)
- **Database**: Tests hit a real PostgreSQL test database (not mocked)
- **Assertion style**: Use `assert_eq!(resp.status(), StatusCode::OK)` pattern for status code validation
- **Migration testing**: Migrations should be tested by running them against a test database and verifying they complete successfully, then testing rollback

### Migration-Specific Test Patterns

- **Forward migration test**: Run the migration, then verify the column no longer exists (query the table schema or attempt to select the dropped column and expect failure)
- **Rollback test**: Run the migration up, then run the migration down, and verify the column is re-added as a nullable string
- **Query compatibility**: After the migration runs, verify that existing advisory queries (those in `AdvisoryService`) still work without the dropped column

## CONVENTIONS.md

- A `CONVENTIONS.md` file exists at the repository root — its contents should be read and followed during implementation
- CI check commands should be extracted from `CONVENTIONS.md` and run before committing
