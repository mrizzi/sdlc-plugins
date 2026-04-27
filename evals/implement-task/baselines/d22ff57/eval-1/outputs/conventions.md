# Discovered Conventions for TC-9201

## Conventions from Repository Structure and Sibling Analysis

### Module Structure

- **Domain module pattern:** Each domain module follows a `model/ + service/ + endpoints/` structure under `modules/fundamental/src/<domain>/`.
- **Model sub-modules:** Each model concept gets its own file (e.g., `summary.rs`, `details.rs`) registered via `pub mod` in `model/mod.rs`.
- **Service files:** Service logic resides in a dedicated file (e.g., `advisory.rs`, `sbom.rs`) within `service/`, registered in `service/mod.rs`.
- **Endpoint files:** Each endpoint handler lives in its own file (e.g., `list.rs`, `get.rs`) within `endpoints/`, with route registration in `endpoints/mod.rs`.

### Framework and Libraries

- **HTTP framework:** Axum for REST endpoints.
- **ORM:** SeaORM for database access.
- **Caching middleware:** `tower-http` caching middleware configured in endpoint route builders.

### Endpoint Conventions (from sibling: `advisory/endpoints/get.rs`, `sbom/endpoints/get.rs`)

- **Path extraction:** Use `Path<Id>` from Axum to extract path parameters.
- **Return type:** Handlers return `Result<Json<T>, AppError>` where `T` is the response struct.
- **Service invocation:** Handlers call the corresponding service method (e.g., `AdvisoryService::fetch`) and propagate errors with `.context()`.
- **Route registration:** Routes are registered in `endpoints/mod.rs` using `Router::new().route("/path", get(handler))` pattern.
- **JSON serialization:** Response structs are returned directly; Axum's `Json` extractor handles serialization.

### Service Conventions (from sibling: `advisory/service/advisory.rs`, `sbom/service/sbom.rs`)

- **Method signature pattern:** Service methods take `&self, id: Id, tx: &Transactional<'_>` as parameters.
- **Naming:** Service methods use `verb_noun` or short verb names (e.g., `fetch`, `list`, `search`).
- **Error handling:** Use `Result<T, AppError>` with `.context()` wrapping from the `anyhow` / `AppError` pattern in `common/src/error.rs`.

### Model Conventions (from sibling: `advisory/model/summary.rs`, `sbom/model/summary.rs`)

- **Struct naming:** Response structs use PascalCase with a descriptive suffix (e.g., `AdvisorySummary`, `SbomDetails`).
- **Derive macros:** Model structs derive `Serialize`, `Deserialize`, and likely `Debug`, `Clone`.
- **Field types:** Counts are represented as integer types (likely `u32` or `i64`).

### Error Handling

- **Error type:** All handlers and services use `AppError` from `common/src/error.rs`.
- **Error wrapping:** Use `.context("descriptive message")` to add context when propagating errors.
- **404 pattern:** Return appropriate 404 responses when entities are not found, consistent with existing SBOM endpoints.
- **`IntoResponse`:** `AppError` implements `IntoResponse` so Axum can convert it to HTTP responses.

### Testing Conventions (from sibling: `tests/api/advisory.rs`, `tests/api/sbom.rs`)

- **Integration tests:** Tests in `tests/api/` hit a real PostgreSQL test database.
- **Assertion style:** Use `assert_eq!(resp.status(), StatusCode::OK)` for status code checks.
- **Response validation:** Deserialize response body and check field values.
- **Error cases:** Include 404 tests with `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`.
- **Test naming:** Tests follow `test_<endpoint>_<scenario>` pattern (e.g., `test_list_advisories_filtered`).
- **Test location:** Integration tests for a domain's endpoints live in `tests/api/<domain>.rs`.

### API Design

- **URL pattern:** REST endpoints follow `/api/v2/<resource>` and `/api/v2/<resource>/{id}` patterns.
- **List responses:** List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`.
- **Single-item responses:** Detail/summary endpoints return the struct directly wrapped in `Json`.

### Import Organization

- **Standard library** imports first, then **external crate** imports, then **internal module** imports (typical Rust convention).

### Query and Database

- **Join tables:** Entity relationships use join tables (e.g., `sbom_advisory`, `sbom_package`) defined in `entity/src/`.
- **Query helpers:** Shared filtering, pagination, and sorting via `common/src/db/query.rs`.
- **Deduplication:** When counting across join tables, deduplicate by entity ID to avoid double-counting.
