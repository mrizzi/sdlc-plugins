# Conventions Discovered from Sibling Analysis

## Production Code Conventions

### Migration Pattern (from `migration/src/m0001_initial/mod.rs`)

- **Module structure:** Each migration lives in its own subdirectory under `migration/src/` named `m<NNNN>_<descriptive_name>/mod.rs`.
- **Trait implementation:** Every migration module implements `MigrationTrait` with two required methods: `up` (apply migration) and `down` (rollback migration).
- **SeaORM usage:** Migrations use SeaORM's schema manager (`SchemaManager`) to execute table alterations, creation, and drops. Table operations are built using fluent API methods such as `Table::alter()`, `Table::create()`, etc.
- **Column operations:** Column additions and removals use `TableAlterStatement` via `manager.alter_table(...)`. Columns are defined with `ColumnDef::new(...)` specifying type and constraints (e.g., `.string().null()`).
- **Enum references:** Columns and tables are referenced via enum variants from the entity module (e.g., `Advisory::Table`, `Advisory::Status`), not raw strings.
- **Registration:** Migrations are registered in `migration/src/lib.rs` by adding `Box::new(m<NNNN>_<name>::Migration)` to the `vec![]` returned by the `migrations()` function.
- **Async:** Both `up` and `down` methods are async.

### Entity Pattern (from `entity/src/advisory.rs`)

- **SeaORM entity:** Entities are defined as SeaORM structs with `#[derive(DeriveEntityModel)]` and column definitions annotated with `#[sea_orm(column_type = "...")]`.
- **Column enum:** Each entity has an associated `Column` enum listing all database columns. The `advisory.rs` entity no longer includes a `Status` variant in its column enum (confirming the `status` column is already removed from the entity model).

### General Rust Conventions

- **Framework:** Axum for HTTP, SeaORM for database ORM.
- **Error handling:** All handlers and service methods return `Result<T, AppError>` with `.context()` wrapping for error messages.
- **Module pattern:** Domain modules follow `model/ + service/ + endpoints/` structure.
- **Naming:** Service methods follow `verb_noun` pattern (e.g., `get_advisory`, `create_sbom`).
- **Imports:** Organized with `use` statements at the top, grouped by crate (std, external, internal).

## Test Conventions

### Integration Test Pattern (from `tests/api/advisory.rs`)

- **Assertion style:** Tests use `assert_eq!(resp.status(), StatusCode::OK)` for status code checks, followed by body deserialization.
- **Response validation:** List endpoint tests validate `total_count`, `items.len()`, and at least one item's key fields.
- **Error cases:** All endpoint tests include a 404 test with `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`.
- **Test naming:** Tests follow `test_<endpoint>_<scenario>` pattern (e.g., `test_list_advisories_filtered`).
- **Database:** Integration tests use a real PostgreSQL test database.
- **Test documentation:** Doc comments on test functions explaining what each test verifies.

## CONVENTIONS.md

The repository contains a `CONVENTIONS.md` file at the root. Its conventions would be read and followed during implementation, including any CI check commands listed therein.
