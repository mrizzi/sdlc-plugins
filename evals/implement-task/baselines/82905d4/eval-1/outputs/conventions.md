# Conventions Discovered from Sibling Analysis

The following conventions were identified from the task description's references to existing code patterns in the trustify-backend repository.

## 1. Error Handling Pattern

**Convention**: All handlers and service methods return `Result<T, AppError>` where `AppError` is defined in `common/src/error.rs`.

**Details**:
- Errors are wrapped using the `.context("descriptive message")` method (from the `anyhow` or similar error-chaining crate)
- `AppError` likely has variants for common HTTP status codes (e.g., `NotFound`, `InternalServerError`)
- The framework (Axum) automatically converts `AppError` into the appropriate HTTP response
- Pattern: `service.method().await.context("Error doing X")?;`

**Source**: Referenced in task description as the pattern from `common/src/error.rs`.

## 2. Module Structure: Three-Layer Layout

**Convention**: Each domain module follows a `model/ + service/ + endpoints/` three-layer architecture.

**Details**:
- `model/` — Data structures (request/response types, domain entities). Each model type in its own file, registered via `pub mod` in `model/mod.rs`.
- `service/` — Business logic. Service structs with methods that accept typed IDs and `&Transactional<'_>` for database access.
- `endpoints/` — HTTP handlers and route registration. Each endpoint in its own file, routes composed in `endpoints/mod.rs`.

**Example**: The `advisory` module has:
- `modules/fundamental/src/advisory/model/summary.rs` — `AdvisorySummary` struct
- `modules/fundamental/src/advisory/service/advisory.rs` — `AdvisoryService` with `fetch`, `list` methods
- `modules/fundamental/src/advisory/endpoints/get.rs` — GET handler
- `modules/fundamental/src/advisory/endpoints/mod.rs` — Route registration

## 3. Endpoint Handler Pattern

**Convention**: HTTP handlers follow a consistent signature pattern.

**Details**:
- **Path parameters**: Extracted via `Path<Id>` (Axum extractor)
- **Service injection**: Via `State<ServiceType>` (Axum state)
- **Return type**: `Result<Json<ResponseType>, AppError>`
- **Transaction**: Passed as `&Transactional::None` for read-only operations
- **Flow**: Extract params -> call service method -> return JSON

**Typical handler shape**:
```rust
pub async fn get_thing(
    State(service): State<ThingService>,
    Path(id): Path<Id>,
) -> Result<Json<ThingResponse>, AppError> {
    let result = service.fetch(id, &Transactional::None).await?;
    Ok(Json(result))
}
```

## 4. Service Method Pattern

**Convention**: Service methods follow a consistent signature and behavior pattern.

**Details**:
- **Signature**: `pub async fn method_name(&self, id: Id, tx: &Transactional<'_>) -> Result<T, AppError>`
- **Database access**: Via `self.db.connection(tx)` to get a database connection respecting the transaction context
- **Entity queries**: Via SeaORM's `Entity::find().filter(...).all(&db).await`
- **Error handling**: `.context("descriptive message")?` on all fallible operations
- **ID types**: Use the `Id` type from `trustify_common::id` (supports multiple ID formats)

## 5. Response Types

**Convention**: Different endpoint types use different response wrappers.

**Details**:
- **Single-entity endpoints** (GET by ID): Return `Json<T>` directly where `T` is the domain model
- **List endpoints**: Return `PaginatedResults<T>` from `common/src/model/paginated.rs`
- **Summary/aggregation endpoints**: Return `Json<T>` with a custom summary struct (this is the pattern for the new endpoint)
- All response types derive `Serialize`, `Deserialize`, and `ToSchema` (for OpenAPI docs)

## 6. Route Registration Pattern

**Convention**: Routes are composed in each module's `endpoints/mod.rs`.

**Details**:
- Individual endpoint handlers are in separate files (e.g., `get.rs`, `list.rs`)
- `mod.rs` declares sub-modules and builds the router: `Router::new().route("/path", get(handler))`
- Routes auto-mount: `server/src/main.rs` does not need manual updates when adding routes to existing modules
- The router composition uses Axum's `Router` with method routing (`get`, `post`, etc.)

## 7. Database Entity Pattern

**Convention**: SeaORM entities in `entity/src/` define database tables.

**Details**:
- Each entity file defines `Model`, `Entity`, `Column`, `Relation` types
- Join tables (like `sbom_advisory.rs`) connect related entities
- Queries use SeaORM's fluent API: `Entity::find().filter(Column::X.eq(value)).all(&db).await`
- Column enums enable type-safe filtering

## 8. OpenAPI Documentation Pattern

**Convention**: Endpoints are documented with utoipa annotations.

**Details**:
- `#[utoipa::path(...)]` attribute on handler functions
- `responses(...)` lists possible HTTP status codes and body types
- `params(...)` documents path and query parameters
- `tag = "module_name"` groups endpoints in the API docs
- Response structs derive `ToSchema`

## 9. Testing Conventions

**Convention**: Integration tests in `tests/api/` exercise endpoints against a real database.

**Details**:
- Tests use `#[tokio::test]` for async test execution
- A test harness provisions a PostgreSQL test database
- HTTP requests are made to the test server (likely via `reqwest` or the framework's test client)
- Assertions use `assert_eq!(resp.status(), StatusCode::OK)` pattern
- Response bodies are parsed as JSON and individual fields are asserted
- Each test is self-contained with its own test data

## 10. ID Type Convention

**Convention**: The `Id` type from `trustify_common::id` is used throughout for entity identifiers.

**Details**:
- Supports multiple identifier formats (likely UUID, numeric, or string-based)
- Used in path parameters, service method signatures, and entity lookups
- Extracted from HTTP paths via `Path<Id>`

## 11. Transaction Convention

**Convention**: The `Transactional<'_>` type controls database transaction behavior.

**Details**:
- Passed as a parameter to service methods: `tx: &Transactional<'_>`
- `Transactional::None` used for read-only operations at the handler level
- Enables callers to wrap multiple service calls in a single transaction when needed
- Service methods use `self.db.connection(tx)` to obtain a connection that respects the transaction context
