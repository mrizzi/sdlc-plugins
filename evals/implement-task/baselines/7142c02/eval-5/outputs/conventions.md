# Discovered Conventions from Sibling Analysis

## Source: Repository Structure and Key Conventions

The following conventions were discovered by analyzing the repository structure (`repo-backend.md`), the project's Key Conventions section, and the sibling migration file `migration/src/m0001_initial/mod.rs`.

---

## Production Code Conventions

### Migration Pattern (from `migration/src/m0001_initial/mod.rs`)

- **Structure**: Each migration lives in its own subdirectory under `migration/src/` named with a sequential prefix (e.g., `m0001_initial`, `m0002_drop_advisory_status`)
- **File**: Single `mod.rs` file per migration directory
- **Trait**: Implements `MigrationTrait` with `up` (apply) and `down` (rollback) methods
- **Naming**: Uses `#[derive(DeriveMigrationName)]` on a `Migration` struct for automatic name derivation
- **Registration**: Migrations are registered in `migration/src/lib.rs` via `Box::new(module::Migration)` entries in a `vec![]`
- **Identifiers**: Uses local `#[derive(Iden)]` enum for table/column identifiers within each migration (avoids coupling to entity crate)
- **Async**: Migration methods are async via `#[async_trait::async_trait]`

### Entity Pattern (from `entity/src/advisory.rs` and siblings)

- **ORM**: SeaORM entities with `DeriveEntityModel`
- **Location**: Entity files in `entity/src/` with one file per database table
- **Naming**: Entity file names match table names (e.g., `advisory.rs` for the `advisory` table)

### Module Pattern (from `modules/fundamental/src/`)

- **Structure**: Each domain module follows `model/ + service/ + endpoints/` three-directory structure
- **Error handling**: All handlers return `Result<T, AppError>` with `.context()` for error wrapping
- **Response types**: List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`
- **Query helpers**: Shared filtering, pagination, and sorting via `common/src/db/query.rs`

### Naming Conventions

- **Services**: Methods follow `verb_noun` pattern (e.g., `get_advisory`, `create_sbom`, `list_advisories`)
- **Modules**: Lowercase, underscore-separated directory names matching domain concepts
- **Endpoints**: Route registration in each module's `endpoints/mod.rs`; handler files named by HTTP operation (`list.rs`, `get.rs`)

### Error Handling

- All handlers use `Result<T, AppError>` return type
- Errors are wrapped with `.context()` for additional information
- `AppError` enum is defined in `common/src/error.rs` and implements `IntoResponse`

### Framework Stack

- **HTTP**: Axum
- **ORM**: SeaORM
- **Database**: PostgreSQL
- **Caching**: tower-http caching middleware

---

## Test Conventions (from `tests/api/` sibling analysis)

### Test Organization

- **Location**: Integration tests in `tests/api/` directory
- **File naming**: One test file per domain entity (e.g., `sbom.rs`, `advisory.rs`, `search.rs`)
- **Test type**: Integration tests against a real PostgreSQL test database (not mocks)

### Assertion Patterns

- **Status codes**: `assert_eq!(resp.status(), StatusCode::OK)` pattern
- **Response bodies**: Deserialization followed by field-level assertions
- **Value-based**: Prefer asserting on actual values over length-only checks

### Test Naming

- Tests follow `test_<endpoint_or_subject>_<scenario>` pattern
- Examples from the domain: `test_list_advisories_filtered`, `test_get_advisory_by_id`

### Test Structure

- Async tests using `#[tokio::test]`
- Given-When-Then section comments for non-trivial tests
- Documentation comments (`///`) on every test function

---

## Convention Conflicts

No convention conflicts were detected between the task description/Implementation Notes and the discovered conventions. The task's Implementation Notes align with the migration pattern found in `m0001_initial/mod.rs`.
