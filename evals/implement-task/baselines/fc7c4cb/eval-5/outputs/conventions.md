# Discovered Conventions from Sibling Analysis

## Source: migration/src/m0001_initial/mod.rs (sibling migration)

### Migration module structure
- Each migration lives in its own subdirectory under `migration/src/` named `m<NNNN>_<description>/`
- Each migration directory contains a single `mod.rs` file
- Numbering is sequential: `m0001_`, `m0002_`, etc.

### Migration implementation pattern
- Import `sea_orm_migration::prelude::*`
- Define a unit struct `Migration` with `#[derive(DeriveMigrationName)]`
- Implement `MigrationTrait` for `Migration` with `async fn up()` and `async fn down()`
- Both methods accept `&SchemaManager` and return `Result<(), DbErr>`
- Use `#[async_trait::async_trait]` attribute on the impl block

### Table/column references
- Define an `#[derive(Iden)]` enum for type-safe table and column identifiers
- Enum variants map to SQL names (e.g., `Advisory::Table` maps to the `advisory` table, `Advisory::Status` maps to the `status` column)
- Only include the table and column identifiers needed for the specific migration

### Schema manipulation
- Use SeaORM's builder pattern for DDL operations: `Table::alter().table(...).drop_column(...).to_owned()`
- Pass built statements to `manager.alter_table()` or `manager.create_table()`
- Operations are awaited (async)

### Migration registration (migration/src/lib.rs)
- Each migration module is declared with `mod m<NNNN>_<description>;`
- All migrations are registered in a `migrations()` function returning `Vec<Box<dyn MigrationTrait>>`
- Migrations are listed in order: `Box::new(m<NNNN>_<description>::Migration)`

## Source: entity/src/advisory.rs (advisory entity)

### Entity conventions
- SeaORM entity definitions define the database schema as Rust types
- The `advisory` entity no longer includes a `status` field, confirming the column is deprecated
- The entity uses a `severity` enum field as the replacement for `status`

## Source: Key Conventions from repo-backend.md

### Framework and patterns
- **Framework**: Axum for HTTP, SeaORM for database ORM
- **Error handling**: All handlers return `Result<T, AppError>` with `.context()` wrapping
- **Module pattern**: Each domain module follows `model/ + service/ + endpoints/` structure
- **Testing**: Integration tests in `tests/api/` use a real PostgreSQL test database
- **Assertion style**: Tests use `assert_eq!(resp.status(), StatusCode::OK)` pattern

## Source: Test conventions (tests/api/advisory.rs sibling)

### Test patterns
- Tests are in `tests/api/` directory, one file per domain entity
- Integration tests hit a real PostgreSQL test database
- Assertion pattern: `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization
- Test naming likely follows `test_<endpoint>_<scenario>` pattern based on repo conventions

## Convention Conflicts

No conflicts detected between the task description/Implementation Notes and the
discovered conventions. The task explicitly references the patterns in `m0001_initial/mod.rs`
and the implementation follows them exactly.
