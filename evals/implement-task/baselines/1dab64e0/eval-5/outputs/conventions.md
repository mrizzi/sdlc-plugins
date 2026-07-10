# Conventions Discovered from Sibling Analysis

## Migration Conventions (from `migration/src/m0001_initial/mod.rs`)

- **File naming**: Migrations follow the pattern `m<NNNN>_<snake_case_description>/mod.rs` where NNNN is a zero-padded sequential number
- **Struct naming**: Each migration module exports a `Migration` struct (no prefix/suffix)
- **Trait implementation**: Migrations implement `MigrationTrait` from `sea_orm_migration::prelude::*` with async `up` and `down` methods
- **Migration name**: The `MigrationName` trait returns a string matching the directory name (e.g., `"m0001_initial"`)
- **Iden enums**: Table and column identifiers are defined using `#[derive(Iden)]` enums local to each migration module
- **Registration**: Migrations are registered in `migration/src/lib.rs` via `Box::new(<module>::Migration)` in the `migrations()` function's `vec![]`
- **Rollback support**: Every migration must implement a `down` method that reverses the `up` operation

## General Code Conventions (from repository structure and Key Conventions)

- **Framework**: Axum for HTTP, SeaORM for database ORM and migrations
- **Module pattern**: Each domain module follows `model/ + service/ + endpoints/` structure
- **Error handling**: All handlers return `Result<T, AppError>` with `.context()` wrapping for error enrichment
- **Naming**: Service methods follow `verb_noun` pattern (e.g., `get_advisory`, `create_sbom`)
- **Entity definitions**: SeaORM entity models live in `entity/src/<entity_name>.rs`
- **Import organization**: `use sea_orm_migration::prelude::*` for migration modules (wildcard import for SeaORM prelude)

## Test Conventions (from `tests/api/`)

- **Test location**: Integration tests live in `tests/api/<domain>.rs` (e.g., `tests/api/advisory.rs`)
- **Assertion style**: Tests use `assert_eq!(resp.status(), StatusCode::OK)` pattern for status code verification
- **Database**: Integration tests hit a real PostgreSQL test database
- **Test scope for migrations**: Migration tests would verify that the migration runs successfully (up), that the rollback works (down), and that existing queries still function after the migration
