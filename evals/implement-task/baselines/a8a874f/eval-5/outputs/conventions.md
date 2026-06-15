# Discovered Conventions (from Sibling Analysis)

## Production Code Conventions

### Migration Pattern (from `migration/src/m0001_initial/mod.rs`)
- **Module structure:** Each migration lives in its own directory under `migration/src/` following the pattern `m<NNNN>_<descriptive_name>/mod.rs`
- **Trait implementation:** Every migration module implements `MigrationTrait` with `up()` and `down()` methods
- **Registration:** Migrations are registered in `migration/src/lib.rs` by adding them to the `vec![]` returned by the `migrations()` function
- **Naming:** Module names use snake_case with a numeric prefix (e.g., `m0001_initial`, `m0002_drop_advisory_status`)

### Entity Pattern (from `entity/src/advisory.rs`)
- **ORM framework:** SeaORM is used for database entities
- **Entity definition:** Each entity file defines a SeaORM `Entity` with column enums (e.g., `Advisory::Table`, `Advisory::Status`)
- **Column references:** Enum variants on the entity are used to reference table/column names in migrations and queries

### Error Handling
- **Pattern:** All handlers return `Result<T, AppError>` with `.context()` wrapping (from `common/src/error.rs`)

### Naming Conventions
- **Service methods:** Follow `verb_noun` pattern (e.g., `get_advisory`, `create_sbom`)
- **Module structure:** Each domain module follows `model/ + service/ + endpoints/` structure

### Database Operations
- **Schema changes:** Use SeaORM's `TableAlterStatement` for ALTER TABLE operations
- **Reversibility:** All migrations must have a reversible `down()` method

## Test Conventions

### Integration Test Pattern (from `tests/api/advisory.rs`, `tests/api/sbom.rs`)
- **Test location:** Integration tests reside in `tests/api/` and test against a real PostgreSQL test database
- **Assertion style:** Tests use `assert_eq!(resp.status(), StatusCode::OK)` pattern for HTTP status checks
- **Test naming:** Tests follow `test_<endpoint>_<scenario>` convention (e.g., `test_list_advisories_filtered`)
- **Response validation:** List endpoint tests validate `total_count`, `items.len()`, and at least one item's key fields
- **Error cases:** Endpoint tests include 404 tests with `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`

### Migration Test Pattern
- **Up migration:** Test that migration applies successfully and the target column no longer exists
- **Down migration (rollback):** Test that rollback re-adds the column with correct type (nullable string)
- **Query verification:** Test that existing queries (e.g., advisory list/get) still work after the column is dropped

## Repository-Level Conventions (from CONVENTIONS.md)
- No CONVENTIONS.md content was directly inspected (simulated environment), but the repo structure document notes:
  - Framework: Axum for HTTP, SeaORM for database
  - Response types: List endpoints return `PaginatedResults<T>`
  - Testing: Integration tests hit a real PostgreSQL test database
