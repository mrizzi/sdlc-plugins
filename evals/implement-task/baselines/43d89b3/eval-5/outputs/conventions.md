# Discovered Conventions from Sibling Analysis

## Production Code Conventions

### Migration pattern (from `migration/src/m0001_initial/mod.rs`)
- **Struct naming:** Each migration module exports a public struct named `Migration` with `#[derive(DeriveMigrationName)]`
- **Trait implementation:** Implements `MigrationTrait` with `#[async_trait::async_trait]` attribute
- **Method signatures:** Both `up` and `down` return `Result<(), DbErr>` and take `&self` and `&SchemaManager`
- **Import style:** Uses `use sea_orm_migration::prelude::*;` as the single import
- **Identifier enums:** Table and column identifiers are defined as local `#[derive(DeriveIden)]` enums within each migration module, making migrations self-contained
- **Directory structure:** Each migration is a directory (`m0001_initial/`) containing a `mod.rs` file
- **Naming convention:** Migration directories follow `m<NNNN>_<descriptive_name>` pattern (zero-padded 4-digit sequence number)

### Migration registration (from `migration/src/lib.rs`)
- **Module declarations:** Each migration module is declared with `mod m<NNNN>_<name>;` at the top of `lib.rs`
- **Registration:** Migrations are registered in a `migrations()` function that returns `Vec<Box<dyn MigrationTrait>>`
- **Ordering:** Migrations are listed in chronological order (ascending sequence number)
- **Boxing pattern:** Each migration is registered as `Box::new(<module>::Migration)`

### Entity conventions (from `entity/src/advisory.rs` and siblings)
- **Framework:** SeaORM entities with derive macros
- **Column identifiers:** Each entity defines a `DeriveIden` enum for table and column names
- **File organization:** One entity per file in `entity/src/`

### Error handling (from modules throughout the codebase)
- **Return types:** All handlers use `Result<T, AppError>` with `.context()` wrapping
- **Error type:** Centralized `AppError` enum from `common/src/error.rs` implementing `IntoResponse`

### Module structure
- **Domain modules:** Each domain follows `model/ + service/ + endpoints/` structure
- **Endpoint registration:** Each module's `endpoints/mod.rs` registers routes; `server/main.rs` mounts all modules

## Test Conventions

### Integration tests (from `tests/api/advisory.rs` and siblings)
- **Assertion style:** `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization
- **Test location:** Integration tests live in `tests/api/` organized by domain
- **Database:** Tests run against a real PostgreSQL test database
- **Naming:** Not fully confirmed without reading test files, but likely follows `test_<endpoint>_<scenario>` pattern based on project conventions

## Documentation Conventions
- **Doc comments:** Use `///` for Rust doc comments on public items
- **Module-level docs:** Use `//!` for module-level documentation at the top of the file
