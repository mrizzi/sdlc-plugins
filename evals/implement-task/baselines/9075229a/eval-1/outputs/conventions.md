# Discovered Conventions (from sibling analysis)

## Production Code Conventions

### Module structure
- Each domain module follows a strict `model/ + service/ + endpoints/` three-directory structure.
- Models are split into separate files per concept (e.g., `summary.rs`, `details.rs`) and registered via `pub mod` in `model/mod.rs`.
- Services live in a dedicated file named after the domain entity (e.g., `advisory.rs` in `service/`), re-exported through `service/mod.rs`.
- Endpoints live in separate files per operation (e.g., `get.rs`, `list.rs`) and are registered in `endpoints/mod.rs`.

### Framework usage
- **HTTP framework**: Axum (path extraction via `Path<Id>`, JSON responses via `Json` extractor).
- **ORM**: SeaORM for database access with entity definitions in `entity/src/`.
- **Caching**: `tower-http` caching middleware configured in endpoint route builders.

### Error handling
- All handlers return `Result<T, AppError>`.
- Errors are wrapped with `.context()` for descriptive messages.
- `AppError` enum is defined in `common/src/error.rs` and implements `IntoResponse`.

### Naming conventions
- Service methods follow `verb_noun` pattern (e.g., `fetch`, `list`, `search`).
- Endpoint handler functions are named after the HTTP verb and resource (e.g., `get`, `list`).
- Model structs use PascalCase domain names (e.g., `AdvisorySummary`, `SbomDetails`).
- File names use snake_case matching the struct or concept name.

### Endpoint registration
- Routes are registered in each module's `endpoints/mod.rs` using `Router::new().route("/path", get(handler))`.
- `server/main.rs` mounts all module routers; modules auto-register.

### Response types
- List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`.
- Single-item endpoints return the struct directly, serialized by Axum's `Json` extractor.

### Service method signatures
- Service methods take `&self` as the receiver.
- Methods that access the database take a `tx: &Transactional<'_>` parameter.
- Methods that look up by ID take an `Id` parameter (e.g., `sbom_id: Id`).

### Import organization
- External crate imports first, then local module imports.
- SeaORM entity imports reference `entity::` paths.

### Query patterns
- Shared query builder helpers (filtering, pagination, sorting) live in `common/src/db/query.rs`.
- Join tables (e.g., `sbom_advisory`, `sbom_package`) are used for many-to-many relationships.

## Test Conventions

### Assertion style
- Endpoint tests use `assert_eq!(resp.status(), StatusCode::OK)` for status code checks.
- Body is deserialized from JSON and fields are checked with `assert_eq!`.

### Response validation
- Status code is always validated first.
- For list endpoints: `total_count`, `items.len()`, and at least one item's key fields are checked.
- For single-item endpoints: key fields are asserted individually.

### Error cases
- All endpoint test suites include a 404 test with `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`.

### Test naming
- Tests follow `test_<endpoint>_<scenario>` pattern (e.g., `test_list_advisories_filtered`).

### Test organization
- Integration tests are in `tests/api/`, one file per domain entity.
- Tests hit a real PostgreSQL test database.

### Test setup
- Test fixtures create entities via service methods or direct database insertion.
- Each test function handles its own setup (no shared `beforeAll` equivalent).

### Documentation
- Test functions should include a doc comment (`///`) explaining what is verified (AI-generated standard).
- Non-trivial tests use `// Given`, `// When`, `// Then` section comments.
