# Conventions Discovered from Sibling Analysis

## Source: Repository Structure and Key Conventions (repo-backend.md)

### Production Code Conventions

- **Framework**: Axum for HTTP, SeaORM for database ORM
- **Module pattern**: Each domain module follows `model/ + service/ + endpoints/` structure
- **Error handling**: All handlers return `Result<T, AppError>` with `.context()` wrapping
- **Endpoint registration**: Each module's `endpoints/mod.rs` registers routes; `server/main.rs` mounts all modules
- **Response types**: List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`
- **Query helpers**: Shared filtering, pagination, and sorting via `common/src/db/query.rs`

### Migration Conventions (from sibling: `migration/src/m0001_initial/mod.rs`)

- **Directory structure**: Each migration lives in its own module directory under `migration/src/`, named with a sequential prefix `m<NNNN>_<descriptive_name>/`
- **File structure**: Each migration module has a `mod.rs` file implementing `MigrationTrait`
- **Trait implementation**: Migrations implement `MigrationTrait` with `up()` and `down()` methods
- **Registration**: Migrations are registered in `migration/src/lib.rs` by adding them to the `vec![]` returned by the `migrations()` function
- **Module declaration**: Each migration module is declared with `mod m<NNNN>_<name>;` in `migration/src/lib.rs`
- **Naming convention**: Migration directories use snake_case with a sequential numeric prefix (e.g., `m0001_initial`, `m0002_drop_advisory_status`)

### Entity Conventions (from sibling: `entity/src/advisory.rs`)

- **SeaORM entity pattern**: Entities define column enums that map to database table columns
- **Column references**: Column variants are used in migration statements (e.g., `Advisory::Table`, `Advisory::Status`)
- **Entity verification**: The `advisory.rs` entity no longer references the `status` column, confirming it has been removed from the entity model in a prior change

### Test Conventions

- **Location**: Integration tests in `tests/api/` directory
- **Database**: Tests hit a real PostgreSQL test database
- **Assertion style**: Use `assert_eq!(resp.status(), StatusCode::OK)` pattern
- **Test files**: Named after the domain they test (e.g., `advisory.rs` for advisory endpoint tests)

### CONVENTIONS.md

- A `CONVENTIONS.md` file exists at the repository root (`trustify-backend/CONVENTIONS.md`)
- Its contents should be read and followed during implementation
- Any CI check commands listed within should be extracted and run during verification

### Documentation

- `README.md` exists at the repository root
- API docs at `docs/api.md`
- Architecture docs at `docs/architecture.md`
