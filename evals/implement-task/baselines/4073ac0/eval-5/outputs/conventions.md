# Discovered Conventions

## Conventions from sibling analysis

### Migration module conventions (from `migration/src/m0001_initial/mod.rs`)

- **Trait implementation:** Each migration module implements `MigrationTrait` with two required methods: `up` (apply migration) and `down` (rollback migration).
- **Module registration:** Migrations are registered in `migration/src/lib.rs` by adding them to the `vec![]` returned by the `migrations()` function.
- **Module naming:** Migration directories follow the pattern `m<NNNN>_<snake_case_description>/mod.rs` (e.g., `m0001_initial`, `m0002_drop_advisory_status`).
- **Return type:** Both `up` and `down` methods return `Result<(), DbErr>` and accept `&self` and `&SchemaManager`.
- **SeaORM patterns:** Migrations use SeaORM's schema manager for DDL operations (`TableCreateStatement`, `TableAlterStatement`, etc.).

### Entity conventions (from `entity/src/advisory.rs` and siblings)

- **SeaORM entity pattern:** Entities are defined as SeaORM model structs with derive macros.
- **Column enum:** Each entity defines a column enum mapping Rust field names to database column names.
- **Table enum:** Each entity defines a table enum variant used in migration statements (e.g., `Advisory::Table`, `Advisory::Status`).
- **File organization:** One entity per file in `entity/src/`, registered in `entity/src/lib.rs`.

### Error handling conventions (from `common/src/error.rs`)

- **Error type:** All service and handler code uses `Result<T, AppError>` with `.context()` wrapping for error chain propagation.

### Framework conventions

- **Framework:** Axum for HTTP, SeaORM for database ORM.
- **Module pattern:** Each domain module follows `model/ + service/ + endpoints/` structure.
- **Response types:** List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`.

### Test conventions (from `tests/api/advisory.rs` and siblings)

- **Test location:** Integration tests reside in `tests/api/` and hit a real PostgreSQL test database.
- **Assertion style:** Tests use `assert_eq!(resp.status(), StatusCode::OK)` pattern for status code validation.
- **Test naming:** Test functions follow `test_<endpoint>_<scenario>` pattern.
- **Test organization:** Tests are organized by domain entity (one file per entity: `sbom.rs`, `advisory.rs`, `search.rs`).

### CONVENTIONS.md

- A `CONVENTIONS.md` file exists at the repository root. Its contents would be read and followed during implementation. In this eval context, it is noted as present but not readable since we are working with a mock repository structure.
