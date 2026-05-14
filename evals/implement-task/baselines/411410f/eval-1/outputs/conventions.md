# Discovered Conventions for TC-9201

## Source: Sibling analysis of trustify-backend repository structure

### Production Code Conventions

#### Module structure
- Every domain module follows the `model/ + service/ + endpoints/` structure (observed in `sbom/`, `advisory/`, `package/`).
- Each sub-directory has a `mod.rs` that re-exports or registers sub-modules.

#### Model conventions
- Model structs live in `modules/fundamental/src/<domain>/model/`.
- Each model concept gets its own file (e.g., `summary.rs`, `details.rs`).
- The parent `mod.rs` declares `pub mod <module_name>;` for each sub-module file.
- Structs derive `Serialize` and `Deserialize` (from serde) for JSON serialization.

#### Service conventions
- Service structs live in `modules/fundamental/src/<domain>/service/`.
- The service file (e.g., `advisory.rs`) contains the primary service struct (e.g., `AdvisoryService`).
- Service methods follow the `verb_noun` pattern (e.g., `fetch`, `list`, `search`).
- Service methods accept `&self`, an entity ID or query parameters, and `tx: &Transactional<'_>` for database transaction context.
- Services return `Result<T, AppError>` with `.context()` wrapping for error propagation.

#### Endpoint conventions
- Endpoint handlers live in `modules/fundamental/src/<domain>/endpoints/`.
- Each endpoint gets its own file (e.g., `list.rs`, `get.rs`).
- The parent `endpoints/mod.rs` registers routes using `Router::new().route("/path", get(handler))`.
- Handlers extract path parameters via `Path<Id>` (Axum extractor).
- Handlers call the corresponding service method and return the result directly — Axum's `Json` extractor handles serialization.
- All handlers return `Result<T, AppError>` for consistent error handling.
- List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`.

#### Error handling
- All errors use the `AppError` enum from `common/src/error.rs`.
- Errors are wrapped with `.context()` to provide descriptive messages.
- `AppError` implements `IntoResponse` for automatic HTTP error response conversion.
- 404 responses are returned when an entity is not found, consistent with existing SBOM and advisory endpoints.

#### Framework and ORM
- HTTP framework: Axum.
- ORM: SeaORM for database interactions.
- Join tables (e.g., `sbom_advisory.rs` in `entity/src/`) map many-to-many relationships.

#### Naming conventions
- Files use `snake_case` naming.
- Structs use `PascalCase` (e.g., `SbomSummary`, `AdvisoryDetails`).
- Module files match the concept they contain (e.g., `severity_summary.rs` for `SeveritySummary`).

#### Import organization
- Standard library imports first, then external crates, then local modules (Rust convention).

#### Route registration
- Routes are registered in each module's `endpoints/mod.rs`.
- `server/src/main.rs` mounts all modules — no changes needed for new endpoints within existing modules.

### Test Conventions

#### Test location
- Integration tests live in `tests/api/` with one file per domain (e.g., `sbom.rs`, `advisory.rs`, `search.rs`).
- Tests hit a real PostgreSQL test database.

#### Assertion style
- Status code assertions: `assert_eq!(resp.status(), StatusCode::OK)`.
- Body deserialization follows status assertion.
- 404 assertions: `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`.

#### Test naming
- Tests follow `test_<endpoint>_<scenario>` pattern (e.g., `test_list_advisories_filtered`).

#### Test structure
- Tests use the given-when-then pattern with section comments for non-trivial tests.
- Each test function has a documentation comment (`///`) explaining what it verifies.

### CONVENTIONS.md
- A `CONVENTIONS.md` file exists at the repository root — its contents should be read and followed during implementation.
- Verification commands from CONVENTIONS.md should be extracted and run during CI checks step.
