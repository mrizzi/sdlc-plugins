# Discovered Conventions (from Sibling Analysis)

## Production Code Conventions

### Migration pattern (from `m0001_initial/mod.rs`)
- **Module structure**: Each migration lives in its own directory under `migration/src/` with a single `mod.rs` file
- **Naming**: Modules are named `m<NNNN>_<descriptive_name>` with zero-padded sequential numbering (e.g., `m0001_initial`, `m0002_drop_advisory_status`)
- **Struct**: Each migration module exports a `pub struct Migration;` with no fields
- **Trait implementation**: Implements `MigrationName` (returning the module name as a string) and `MigrationTrait` (with async `up` and `down` methods)
- **Self-contained identifiers**: Column and table identifiers are defined as local `#[derive(Iden)] enum` types within the migration module, not imported from the entity crate. This ensures migrations remain stable even as entities evolve.
- **Registration**: Migrations are registered in `migration/src/lib.rs` via `Box::new(<module>::Migration)` entries in a `vec![]` returned by the `migrations()` function

### Error handling (from service and endpoint modules)
- **Return type**: All handlers and service methods return `Result<T, AppError>` using the shared `AppError` enum from `common/src/error.rs`
- **Context wrapping**: Errors are enriched with `.context()` calls for debugging

### Module structure (from `modules/fundamental/src/`)
- **Domain organization**: Each domain module follows `model/ + service/ + endpoints/` structure
- **Model pattern**: Summary and Details structs separated into individual files under `model/`
- **Service pattern**: Service structs in `service/` contain business logic methods (fetch, list, search, ingest)
- **Endpoint pattern**: Route registration in `endpoints/mod.rs`; individual endpoint handlers in separate files (list.rs, get.rs)

### Naming (from across modules)
- **Service methods**: Follow `verb_noun` pattern (e.g., `fetch`, `list`, `search`, `ingest`)
- **Files**: Named after their primary responsibility in lowercase (e.g., `summary.rs`, `details.rs`, `list.rs`, `get.rs`)

### Response types (from endpoint modules)
- **List endpoints**: Return `PaginatedResults<T>` from `common/src/model/paginated.rs`
- **Query helpers**: Use shared filtering, pagination, and sorting from `common/src/db/query.rs`

## Test Conventions

### Integration tests (from `tests/api/`)
- **Location**: Integration tests live in `tests/api/` with one file per domain (e.g., `sbom.rs`, `advisory.rs`, `search.rs`)
- **Database**: Tests run against a real PostgreSQL test database (not mocked)
- **Assertion style**: Use `assert_eq!(resp.status(), StatusCode::OK)` pattern for status code verification, followed by body deserialization and field-level assertions
- **Naming**: Test files named after the domain entity they test

### Migration-specific testing
- Migration tests would verify both `up` (column dropped) and `down` (column re-added) directions
- Should verify that existing queries (e.g., advisory list/fetch) continue to work after the column is dropped
- Test naming should follow `test_<migration_name>_<scenario>` pattern consistent with the project's `test_<action>_<scenario>` convention

## Framework and Toolchain
- **Web framework**: Axum
- **ORM**: SeaORM (for both entities and migrations)
- **Language**: Rust
- **Database**: PostgreSQL
- **Caching**: tower-http middleware
