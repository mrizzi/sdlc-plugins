# Discovered Conventions

## From sibling analysis of the trustify-backend repository

### Production Code Conventions

#### Module Structure
- Each domain module follows a consistent `model/ + service/ + endpoints/` directory structure
- Module registration uses `mod.rs` files at each level
- The `model/` directory contains response structs (`summary.rs`, `details.rs`)
- The `service/` directory contains the service struct with domain methods (e.g., `SbomService`, `AdvisoryService`)
- The `endpoints/` directory contains route registration (`mod.rs`) and individual handler files (`get.rs`, `list.rs`)

#### Framework Patterns
- **HTTP Framework**: Axum — handlers use extractors like `Path<Id>` for path parameters
- **ORM**: SeaORM — database operations use entity modules from `entity/src/`
- **Response types**: Single-entity endpoints return the struct directly (Axum's `Json` handles serialization); list endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`
- **Error handling**: All handlers return `Result<T, AppError>` with `.context()` wrapping (pattern from `common/src/error.rs`)

#### Naming Conventions
- **Service methods**: follow `verb_noun` pattern (e.g., `fetch`, `list`, `search` on `AdvisoryService`)
- **Service method signatures**: methods take `&self`, domain-specific ID parameters, and `tx: &Transactional<'_>` for transaction context
- **Endpoint files**: named after the HTTP action (e.g., `get.rs`, `list.rs`)
- **Model files**: named after the domain concept (e.g., `summary.rs`, `details.rs`)
- **Entity files**: named after the database table concept (e.g., `sbom.rs`, `advisory.rs`, `sbom_advisory.rs` for join tables)

#### Route Registration
- Each module's `endpoints/mod.rs` registers routes using `Router::new().route("/path", get(handler))` pattern
- `server/main.rs` mounts all modules' routers — routes auto-mount via module registration
- API routes follow `api/v2/<entity>` pattern (e.g., `/api/v2/advisory`, `/api/v2/sbom`)

#### Error Handling
- All handlers use `Result<T, AppError>` return type
- Errors are wrapped with `.context()` providing human-readable messages
- `AppError` enum is defined in `common/src/error.rs` and implements `IntoResponse`
- 404 responses for missing entities follow a consistent pattern across SBOM and advisory endpoints

#### Import Organization
- Entity imports from `entity::` crate
- Common utilities from `common::` crate (error types, paginated results, query helpers)
- Cross-module service usage through service struct imports

#### Caching
- Uses `tower-http` caching middleware
- Cache configuration set in endpoint route builders

### Test Conventions

#### Test Location and Organization
- Integration tests live in `tests/api/` directory
- Tests are organized by domain entity (e.g., `sbom.rs`, `advisory.rs`, `search.rs`)
- Tests hit a real PostgreSQL test database (not mocked)

#### Assertion Style
- Tests use `assert_eq!(resp.status(), StatusCode::OK)` for status code checks
- Response body is deserialized and validated
- Error cases (404) use `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`

#### Test Naming
- Tests follow `test_<endpoint>_<scenario>` pattern (e.g., implied from sibling naming in `sbom.rs`, `advisory.rs`)

#### Test Structure
- Tests follow the given-when-then pattern with setup, action, and assertion phases
- Error cases are explicitly covered (404 for non-existent entities)

### CONVENTIONS.md
- A `CONVENTIONS.md` file exists at the repository root
- Its contents would be read and followed during implementation (CI commands, naming rules, directory structure)
- Verification commands from CONVENTIONS.md would be extracted and run in Step 9
