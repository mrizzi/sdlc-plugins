# Conventions Discovered from Sibling Analysis

## Production Code Conventions

### Migration Pattern (from `m0001_initial/mod.rs`)
- **Module structure**: Each migration lives in its own directory under `migration/src/` following the `m<NNNN>_<description>/mod.rs` naming pattern.
- **Trait implementation**: Every migration struct implements `MigrationName` (returns the migration directory name as a string) and `MigrationTrait` (provides `up` and `down` async methods).
- **Struct naming**: The migration struct is simply named `Migration` (not prefixed with the migration name), referenced externally as `<module>::Migration`.
- **Async trait**: Uses `#[async_trait::async_trait]` attribute on the `MigrationTrait` impl block.
- **Error handling**: Migration methods return `Result<(), DbErr>` -- propagation via `?` operator, no custom error wrapping.
- **Schema operations**: Uses SeaORM's `SchemaManager` with builder-pattern statements (`Table::alter()`, `Table::create()`, etc.) rather than raw SQL.
- **Iden enums**: Defines local `#[derive(Iden)]` enums for type-safe table and column references within each migration.
- **Registration**: Migrations are registered in `migration/src/lib.rs` via a `vec![]` of `Box<dyn MigrationTrait>`, maintaining chronological order.

### General Code Conventions (from repository structure)
- **Framework**: Axum for HTTP, SeaORM for database ORM and migrations.
- **Module pattern**: Each domain module follows `model/ + service/ + endpoints/` structure.
- **Error handling**: All handlers return `Result<T, AppError>` with `.context()` wrapping.
- **Naming**: Service methods follow `verb_noun` pattern (e.g., `get_advisory`, `create_sbom`).
- **Response types**: List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`.

### Entity Conventions (from `entity/src/advisory.rs` and siblings)
- **SeaORM entities**: Each database table has a corresponding entity file in `entity/src/`.
- **Column mapping**: Entity structs map directly to table columns -- the `advisory` entity no longer includes `status`, confirming the column is safe to drop.

## Test Conventions (from `tests/api/`)
- **Test location**: Integration tests reside in `tests/api/` with one file per domain (e.g., `advisory.rs`, `sbom.rs`).
- **Test database**: Tests hit a real PostgreSQL test database (not mocked).
- **Assertion style**: Tests use `assert_eq!(resp.status(), StatusCode::OK)` pattern followed by body deserialization and field-level assertions.
- **Test naming**: Tests follow `test_<endpoint>_<scenario>` pattern (e.g., `test_list_advisories_filtered`).

## CONVENTIONS.md
- A `CONVENTIONS.md` file exists at the repository root. In a real implementation, this would be read to extract:
  - CI check commands (formatting, linting, compilation checks)
  - Code generation commands (if any)
  - Additional project-specific conventions
  - These commands would be run during Step 9 (Self-Verification) before committing.
