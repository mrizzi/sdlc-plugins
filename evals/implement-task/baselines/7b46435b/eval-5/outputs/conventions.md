# Conventions Discovered from Sibling Analysis

## Production Code Conventions

### Migration module conventions (from `migration/src/m0001_initial/mod.rs`)

- **Module structure**: each migration lives in its own directory under `migration/src/` following the naming pattern `m<NNNN>_<snake_case_description>/mod.rs`
- **Migration numbering**: sequential four-digit prefix (m0001, m0002, ...) to ensure ordering
- **Trait implementation**: each migration module defines a `pub struct Migration;` and implements `MigrationTrait` for it
- **Method signatures**: `up` and `down` are async methods taking `&self` and `&SchemaManager` and returning `Result<(), DbErr>`
- **Table operations**: use SeaORM's `TableAlterStatement` via `manager.alter_table(...)` for DDL changes
- **Column definitions**: use `ColumnDef::new(Entity::Column)` with chained type and constraint methods (e.g., `.string().null()`)
- **Registration**: migrations are registered in `migration/src/lib.rs` by adding a `mod` declaration and appending `Box::new(module::Migration)` to the `vec![]` returned by the `migrations()` function

### Framework and architecture conventions (from repository-level patterns)

- **Framework**: Axum for HTTP, SeaORM for database ORM and migrations
- **Module pattern**: each domain module follows `model/ + service/ + endpoints/` structure
- **Error handling**: all handlers return `Result<T, AppError>` with `.context()` wrapping via the `AppError` enum in `common/src/error.rs`
- **Endpoint registration**: each module's `endpoints/mod.rs` registers routes; `server/main.rs` mounts all modules
- **Response types**: list endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`
- **Query helpers**: shared filtering, pagination, and sorting via `common/src/db/query.rs`
- **Entity definitions**: SeaORM entity structs in `entity/src/`, one file per entity (e.g., `advisory.rs`, `sbom.rs`)

### Naming conventions

- **Crate/module names**: snake_case (e.g., `m0001_initial`, `sbom_advisory`)
- **Struct names**: PascalCase (e.g., `Migration`, `AdvisorySummary`, `SbomDetails`)
- **Service methods**: verb_noun pattern (e.g., `fetch`, `list`, `ingest`, `search`)
- **Endpoint files**: named by HTTP verb/action (e.g., `list.rs`, `get.rs`)

## Test Conventions (from `tests/api/advisory.rs` and siblings)

- **Test location**: integration tests in `tests/api/` directory, organized by entity (e.g., `advisory.rs`, `sbom.rs`, `search.rs`)
- **Test database**: tests hit a real PostgreSQL test database (not mocks)
- **Assertion style**: `assert_eq!(resp.status(), StatusCode::OK)` pattern followed by body deserialization
- **Test naming**: tests follow `test_<endpoint>_<scenario>` pattern (e.g., `test_list_advisories_filtered`)
- **Response validation**: list endpoint tests validate `total_count`, `items.len()`, and at least one item's key fields
- **Error cases**: endpoint tests include 404 tests with `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`
- **Caching**: `tower-http` caching middleware; cache configuration in endpoint route builders

## CONVENTIONS.md

The repository contains a `CONVENTIONS.md` at the root. Would read it for:
- CI check commands for Step 9 verification
- Code generation commands
- Any additional naming rules or patterns not captured by sibling analysis
