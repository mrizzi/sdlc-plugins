# Discovered Conventions (from sibling analysis)

## Production Code Conventions

### Module Structure
- Every domain module follows the `model/ + service/ + endpoints/` structure under `modules/fundamental/src/<domain>/`
- Each sub-directory has a `mod.rs` that re-exports or registers its children
- Model modules contain response structs (e.g., `summary.rs`, `details.rs`)
- Service modules contain the primary service struct with methods (e.g., `SbomService`, `AdvisoryService`)
- Endpoint modules contain route handlers and a `mod.rs` that registers routes

### Error Handling
- All endpoint handlers return `Result<T, AppError>` where `AppError` is defined in `common/src/error.rs`
- Errors are wrapped using `.context()` for contextual error messages
- `AppError` implements `IntoResponse` for Axum compatibility

### Endpoint Patterns
- Route registration uses `Router::new().route("/path", get(handler))` in each module's `endpoints/mod.rs`
- Path parameters are extracted via `Path<Id>` (Axum extractor)
- Handlers call a service method, then return the result directly (Axum's `Json` extractor handles serialization)
- List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`
- Single-resource endpoints return the model struct directly wrapped in JSON

### Service Patterns
- Service structs have methods like `fetch`, `list`, `search`
- Method signatures follow: `&self, id: Id, tx: &Transactional<'_>` for single-resource lookups
- Services use SeaORM for database queries

### Naming Conventions
- Service methods follow `verb_noun` pattern (e.g., `fetch`, `list`, `search`, `severity_summary`)
- Model structs use PascalCase descriptive names (e.g., `SbomSummary`, `AdvisoryDetails`, `AdvisorySummary`)
- Endpoint handler files are named after the HTTP action (e.g., `get.rs`, `list.rs`)
- Route paths follow `/api/v2/<resource>` or `/api/v2/<resource>/{id}` pattern

### Response Types
- Structs derive `Serialize` (and likely `Deserialize`) for JSON serialization
- Summary structs contain a `severity` field (observed on `AdvisorySummary`)
- Detail structs contain extended information beyond summary

### Database / ORM
- Framework: SeaORM
- Join tables use a `<parent>_<child>` naming pattern (e.g., `sbom_advisory`, `sbom_package`)
- Entities defined in `entity/src/` with one file per entity

### Import Organization
- External crate imports first, then internal module imports
- SeaORM entity imports for database operations
- Axum imports for endpoint handlers (`axum::extract::Path`, `axum::Json`, `axum::routing::get`)

## Test Conventions

### Test Organization
- Integration tests live in `tests/api/` directory
- Each domain has its own test file (e.g., `sbom.rs`, `advisory.rs`, `search.rs`)
- Tests hit a real PostgreSQL test database (integration test style)

### Assertion Style
- Status code assertions use `assert_eq!(resp.status(), StatusCode::OK)` pattern
- Response bodies are deserialized then field-checked
- 404 tests use `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`

### Test Naming
- Tests follow `test_<endpoint>_<scenario>` pattern (inferred from the convention of test files per endpoint)

### Parameterized Tests
- No evidence of parameterized test usage (`#[rstest]` etc.) in the sibling test files described -- individual test functions are used for each scenario

### Test Structure
- Tests make HTTP requests to the running test server
- Tests validate status code first, then body content
- Error cases (404) are explicitly covered in sibling test files

## Framework Conventions

### HTTP Framework
- Axum for HTTP routing and request handling
- `tower-http` for middleware (caching)

### Database
- SeaORM for ORM
- PostgreSQL as the backing database

### Shared Utilities
- `common/src/db/query.rs` provides shared query builder helpers (filtering, pagination, sorting)
- `common/src/db/limiter.rs` provides connection pool limiting
- `common/src/model/paginated.rs` provides `PaginatedResults<T>` wrapper
- `common/src/error.rs` provides `AppError` enum
