# Conventions Discovered from Sibling Analysis

## Production Code Conventions

### Migration Pattern (from `migration/src/m0001_initial/mod.rs`)

- **Struct definition**: Each migration is a public unit struct named `Migration` inside its own module directory (e.g., `m0001_initial/mod.rs`)
- **Module naming**: Migration modules follow the pattern `m<NNNN>_<snake_case_description>` (e.g., `m0001_initial`, `m0002_drop_advisory_status`)
- **Trait implementation**: Each migration implements `MigrationTrait` from `sea_orm_migration::prelude::*`
- **Name method**: The `MigrationName` trait returns the module name as a string (e.g., `"m0002_drop_advisory_status"`)
- **Up/Down methods**: Both `up` and `down` are async methods returning `Result<(), DbErr>`, using the `SchemaManager` parameter
- **Schema operations**: Use SeaORM's builder pattern for schema changes (`Table::alter()`, `Table::create()`, etc.)
- **Column definitions**: Use `ColumnDef::new(Iden)` with chained type and constraint methods (`.string()`, `.null()`, `.not_null()`, etc.)
- **Imports**: Use `sea_orm_migration::prelude::*` for all migration types and traits

### Migration Registration (from `migration/src/lib.rs`)

- **Module declarations**: Each migration module is declared with `mod m<NNNN>_<name>;` at the top of `lib.rs`
- **Migrator struct**: A `Migrator` struct implements `MigratorTrait`
- **Registration pattern**: Migrations are returned in a `Vec<Box<dyn MigrationTrait>>` from the `migrations()` method, ordered chronologically
- **Ordering**: Migrations are listed in sequence order (m0001 before m0002, etc.)

### Entity Pattern (from `entity/src/advisory.rs`)

- **SeaORM entities**: Each entity defines a `Model` struct with `DeriveEntityModel` and an `Entity` enum with `DeriveEntityModel`
- **Column enum**: Entity columns are represented as an enum implementing `Iden` (e.g., `Advisory::Table`, `Advisory::Status`, `Advisory::Severity`)
- **Entity module pattern**: One entity per file under `entity/src/`

### General Code Conventions (from repo structure)

- **Framework**: Axum for HTTP, SeaORM for database
- **Module pattern**: Each domain follows `model/ + service/ + endpoints/` structure
- **Error handling**: All handlers return `Result<T, AppError>` with `.context()` wrapping
- **Response types**: List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`
- **Naming**: Service methods follow `verb_noun` pattern (e.g., `get_advisory`, `create_sbom`)

## Test Conventions

### Integration Tests (from `tests/api/advisory.rs` and siblings)

- **Assertion style**: Use `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization
- **Response validation**: List endpoint tests validate `total_count`, `items.len()`, and at least one item's key fields
- **Error cases**: All endpoint tests include a 404 test with `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`
- **Test naming**: Tests follow `test_<endpoint>_<scenario>` pattern (e.g., `test_list_advisories_filtered`)
- **Database setup**: Integration tests hit a real PostgreSQL test database
- **Test organization**: Tests are organized by entity/endpoint in `tests/api/`

### Migration Tests

- **Pattern**: Migration tests would follow the integration test conventions, running against a test database
- **Naming**: `test_<migration_name>_<scenario>` (e.g., `test_m0002_drop_advisory_status_up`, `test_m0002_drop_advisory_status_down`)
- **Assertion**: Verify column existence/absence by querying the information_schema or attempting to select the column
