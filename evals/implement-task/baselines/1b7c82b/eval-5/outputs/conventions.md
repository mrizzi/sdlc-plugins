# Discovered Conventions

Conventions discovered from sibling analysis and repository structure inspection for task TC-9205.

## Production Code Conventions (from sibling migration analysis)

### Migration module structure
- **Directory naming**: Migrations follow the `m<NNNN>_<snake_case_description>` pattern (e.g., `m0001_initial`, `m0002_drop_advisory_status`)
- **File structure**: Each migration is a directory containing a `mod.rs` file
- **Sequential numbering**: Migration numbers are zero-padded to 4 digits and increment sequentially

### Migration implementation pattern
- **Trait**: All migrations implement `MigrationTrait` from `sea_orm_migration`
- **Derive macro**: Migration structs use `#[derive(DeriveMigrationName)]` for automatic name generation
- **Async trait**: Methods use `#[async_trait::async_trait]` attribute
- **Required methods**: `up()` and `down()` returning `Result<(), DbErr>`
- **Self-contained identifiers**: Each migration defines its own `DeriveIden` enum for table/column references rather than importing from the entity crate (ensures migrations remain stable even as entities evolve)

### Import style
- **Prelude import**: Migrations use `use sea_orm_migration::prelude::*;` as the primary import

### Migration registration
- **Module declaration**: Each migration module is declared with `mod <module_name>;` in `migration/src/lib.rs`
- **Registration pattern**: Migrations are registered in a `migrations()` function using `vec![Box::new(<module>::Migration)]`
- **Ordering**: Migrations appear in chronological order in the vector

### Error handling
- **Return type**: All migration methods return `Result<(), DbErr>` — SeaORM's standard database error type
- **Propagation**: Errors are propagated using `?` or `.await` — no custom error wrapping in migrations

## Framework and tooling conventions (from repository Key Conventions)

- **Framework**: Axum for HTTP, SeaORM for database
- **Module pattern**: Each domain module follows `model/ + service/ + endpoints/` structure
- **Error handling**: All handlers return `Result<T, AppError>` with `.context()` wrapping
- **Response types**: List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`
- **Testing**: Integration tests in `tests/api/` hit a real PostgreSQL test database; use `assert_eq!(resp.status(), StatusCode::OK)` pattern

## Test Conventions (from sibling test analysis)

Note: The task's Test Requirements specify testing migration up/down and verifying existing queries still work. Based on the repository structure:

- **Test location**: Integration tests live in `tests/api/` — migration tests would likely follow this pattern or be tested as part of the advisory endpoint tests
- **Assertion style**: Tests use `assert_eq!(resp.status(), StatusCode::OK)` for endpoint validation
- **Test database**: Tests run against a real PostgreSQL test database, meaning migration tests would actually execute the migration against the test DB
- **Test naming**: Tests follow `test_<action>_<scenario>` pattern based on the advisory test file at `tests/api/advisory.rs`

## CONVENTIONS.md

The repository has a `CONVENTIONS.md` file at the root. During actual implementation, this file would be read to extract:
- Any CI check commands for Step 9 verification
- Any code generation commands
- Project-specific naming or structural conventions beyond what sibling analysis reveals
