# Convention Discovery for TC-9201

## Sibling Analysis Performed

Before planning any changes, the following existing files were inspected to discover conventions:

### 1. `modules/fundamental/src/advisory/endpoints/get.rs` (sibling endpoint)

Conventions discovered:
- Endpoint handlers are async functions with signature: `async fn handler(Path(id): Path<Id>, State(state): State<AppState>) -> Result<Json<T>, AppError>`
- Path parameters are extracted using Axum's `Path` extractor
- The handler calls into the corresponding service method, passing `&Transactional` context
- Errors are propagated with `.context("descriptive message")` wrapping (from `anyhow`)
- The return type is `Result<Json<ResponseStruct>, AppError>` -- Axum serializes the struct automatically
- 404 handling: when the service returns `None`, the handler returns `AppError::NotFound("resource description")`

### 2. `modules/fundamental/src/advisory/service/advisory.rs` (sibling service)

Conventions discovered:
- Service methods follow the pattern: `pub async fn method_name(&self, param: Type, tx: &Transactional<'_>) -> Result<T, anyhow::Error>`
- The service holds a reference to the database connection pool
- Queries use SeaORM's `Entity::find()` builder pattern with `.filter()`, `.all()`, `.one()` calls
- The `fetch` method returns `Option<AdvisoryDetails>`, the `list` method returns `PaginatedResults<AdvisorySummary>`
- Join queries use SeaORM's `.find_also_linked()` or direct relation joins
- All database errors are wrapped with `.context()` for meaningful error messages

### 3. `modules/fundamental/src/advisory/model/summary.rs` (sibling model)

Conventions discovered:
- Model structs derive `Clone, Debug, Serialize, Deserialize, utoipa::ToSchema`
- The `AdvisorySummary` struct includes a `severity: String` field -- this is the field we will use for aggregation
- Structs use `pub` visibility on all fields
- Module registration: each model file is declared in `model/mod.rs` with `pub mod filename;`

### 4. `modules/fundamental/src/advisory/endpoints/mod.rs` (route registration)

Conventions discovered:
- Routes are registered using `Router::new().route("/path", get(handler_fn))` pattern
- Each endpoint handler is imported from its own submodule
- New endpoint modules are declared with `mod module_name;` at the top of the file
- Routes are nested under the module's base path (e.g., `/api/v2/advisory`)

### 5. `common/src/error.rs` (error handling)

Conventions discovered:
- `AppError` is an enum implementing Axum's `IntoResponse` trait
- Variants include at least `NotFound(String)`, `Internal(anyhow::Error)`, and possibly `BadRequest(String)`
- The `From<anyhow::Error>` impl allows using `?` operator with `.context()` for automatic conversion
- HTTP status codes are mapped: `NotFound` -> 404, `Internal` -> 500

### 6. `tests/api/advisory.rs` (sibling test file)

Conventions discovered:
- Integration tests use `#[tokio::test]` attribute
- Tests set up a test server with `TestServer::new().await`
- HTTP requests are made with the test client: `server.get("/api/v2/advisory/...").await`
- Assertions follow `assert_eq!(resp.status(), StatusCode::OK)` pattern
- Response bodies are deserialized with `resp.json::<ResponseType>().await`
- Each test function is named descriptively: `test_<action>_<scenario>`

## Summary of Key Conventions

| Convention | Pattern | Source |
|---|---|---|
| Error handling | `Result<T, AppError>` with `.context()` wrapping | `common/src/error.rs`, all service/endpoint files |
| Module structure | `model/ + service/ + endpoints/` per domain | `advisory/`, `sbom/`, `package/` modules |
| Endpoint signature | `async fn(Path<Id>, State<AppState>) -> Result<Json<T>, AppError>` | `advisory/endpoints/get.rs` |
| Service signature | `pub async fn method(&self, id: Id, tx: &Transactional<'_>) -> Result<T, anyhow::Error>` | `advisory/service/advisory.rs` |
| Model derives | `Clone, Debug, Serialize, Deserialize, utoipa::ToSchema` | `advisory/model/summary.rs` |
| Route registration | `Router::new().route(path, get(handler))` in `endpoints/mod.rs` | `advisory/endpoints/mod.rs` |
| Test pattern | `#[tokio::test]`, `TestServer`, `assert_eq!(status, StatusCode)` | `tests/api/advisory.rs` |
| 404 handling | Return `AppError::NotFound` when entity not found | `advisory/endpoints/get.rs` |
