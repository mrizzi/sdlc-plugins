# Conventions Discovered from Sibling Analysis

## Production Code Conventions

### Migration pattern (from `migration/src/m0001_initial/mod.rs`)

- **Module structure**: Each migration lives in its own subdirectory under `migration/src/` named with the pattern `m<NNNN>_<descriptive_name>/mod.rs`
- **Struct definition**: Each migration module defines a public `Migration` struct (unit struct)
- **Trait implementation**: Implements `MigrationTrait` from `sea_orm_migration::prelude::*` with three methods:
  - `name()` -> `&str`: returns the migration name (typically the module directory name)
  - `up()` -> `Result<(), DbErr>`: applies the migration forward
  - `down()` -> `Result<(), DbErr>`: rolls back the migration
- **Import convention**: Uses `use sea_orm_migration::prelude::*;` as the standard prelude import
- **Table operations**: Uses SeaORM's `Table::alter()`, `Table::create()`, `Table::drop()` builders via the `SchemaManager`
- **Column definitions**: Uses `ColumnDef::new(Entity::Column)` builder pattern for defining columns
- **Entity references**: References entity column enums directly (e.g., `Advisory::Table`, `Advisory::Status`) for type-safe table/column identification

### Migration registration (from `migration/src/lib.rs`)

- **Module declaration**: Each migration is declared as `mod m<NNNN>_<name>;` at the top of `lib.rs`
- **Registration**: Migrations are registered in a `migrations()` function that returns a `Vec<Box<dyn MigrationTrait>>`, with each entry as `Box::new(m<NNNN>_<name>::Migration)`
- **Ordering**: Migrations are listed in sequential order (m0001 before m0002, etc.)

### Error handling

- Migration methods return `Result<(), DbErr>` using the `?` operator for error propagation
- No custom error wrapping in migration code; SeaORM errors propagate directly

### Entity conventions (from `entity/src/advisory.rs`)

- SeaORM entity files define a column enum with variants for each database column
- The `advisory` entity uses `severity` (enum field) and no longer references `status`

## Framework and tooling

- **Framework**: Axum for HTTP, SeaORM for database ORM and migrations
- **Module pattern**: Domain modules follow `model/ + service/ + endpoints/` structure
- **Error handling in handlers**: All handlers return `Result<T, AppError>` with `.context()` wrapping
- **Response types**: List endpoints return `PaginatedResults<T>`

## Test Conventions (from `tests/api/advisory.rs` and sibling test files)

- **Assertion style**: Endpoint tests use `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization
- **Response validation**: List endpoint tests validate `total_count`, `items.len()`, and at least one item's key fields
- **Error cases**: Endpoint tests include a 404 test with `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`
- **Test naming**: Tests follow `test_<endpoint>_<scenario>` pattern (e.g., `test_list_advisories_filtered`)
- **Database testing**: Integration tests in `tests/api/` hit a real PostgreSQL test database
- **Doc comments**: New test functions should include `///` doc comments explaining what is verified (AI-generated standard)
- **Section comments**: Non-trivial tests should include `// Given`, `// When`, `// Then` section comments

## Naming Conventions

- **Service methods**: Follow `verb_noun` pattern (e.g., `get_advisory`, `create_sbom`)
- **Migration directories**: Follow `m<NNNN>_<snake_case_description>` pattern
- **File naming**: Snake case throughout (Rust convention)
