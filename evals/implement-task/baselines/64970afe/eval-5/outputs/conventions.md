# Discovered Conventions from Sibling Analysis

## Production code conventions

### Migration module conventions (from `m0001_initial/mod.rs`)

- **Module structure**: Each migration lives in its own directory under `migration/src/` named `m<NNNN>_<descriptive_name>/mod.rs`
- **Naming**: Migration directories use snake_case with a sequential numeric prefix (e.g., `m0001_initial`, `m0002_drop_advisory_status`)
- **Struct**: Each migration module exports a `Migration` struct with `#[derive(DeriveMigrationName)]`
- **Trait implementation**: Implements `MigrationTrait` with `async fn up()` and `async fn down()` methods
- **Error handling**: Both `up()` and `down()` return `Result<(), DbErr>` -- errors propagate via `?` operator, no manual error wrapping
- **Self-contained Iden enums**: Migrations define their own `#[derive(Iden)] enum` for table/column references rather than importing from entity crates. This ensures migrations remain stable even as entity definitions evolve.
- **Async trait**: Uses `#[async_trait::async_trait]` attribute on the trait impl block

### Migration registration conventions (from `migration/src/lib.rs`)

- **Module declarations**: Listed sequentially by migration number at the top of `lib.rs`
- **Registration**: Migrations are collected in a `vec![]` inside a `migrations()` function, using `Box::new(<module>::Migration)` syntax
- **Ordering**: Migrations appear in the vec in the same sequential order as their numeric prefix

### Entity conventions (from `entity/src/advisory.rs` and siblings)

- **Framework**: SeaORM entities with derive macros
- **Column enum**: Each entity has a column enum with variants matching database column names
- **Table reference**: Entities use `#[derive(Iden)]` or SeaORM's `DeriveEntityModel` for table/column references

### General Rust conventions (from repository structure)

- **Error handling**: All handlers use `Result<T, AppError>` with `.context()` wrapping (from `common/src/error.rs`)
- **Module pattern**: Domain modules follow `model/ + service/ + endpoints/` structure
- **Response types**: List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`
- **Documentation**: Public symbols should have `///` doc comments

## Test conventions (from `tests/api/` siblings)

### Assertion style

- Endpoint tests use `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization
- Value-based assertions preferred over length-only checks

### Response validation

- List endpoint tests validate `total_count`, `items.len()`, and at least one item's key fields
- Error cases include 404 tests with `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`

### Test naming

- Tests follow `test_<endpoint>_<scenario>` pattern (e.g., `test_list_advisories_filtered`)

### Test setup

- Integration tests hit a real PostgreSQL test database
- Migrations run as part of test database setup

### Test organization

- Tests grouped by domain entity in `tests/api/` (e.g., `sbom.rs`, `advisory.rs`, `search.rs`)

## Framework and tooling conventions

- **HTTP framework**: Axum
- **ORM**: SeaORM
- **Testing**: `cargo test` with PostgreSQL test database
- **Caching**: `tower-http` caching middleware
- **Endpoint registration**: Each module's `endpoints/mod.rs` registers routes; `server/main.rs` mounts all modules
