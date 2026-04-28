# Conventions Discovered from Sibling Analysis

## 1. Error Handling Pattern: `Result<T, AppError>` with `.context()`

All service methods and endpoint handlers return `Result<T, AppError>`. Errors from database operations and other fallible calls are propagated using the `.context("descriptive message")` method (from the `anyhow` or similar crate), which wraps the underlying error into an `AppError`. This is defined in `common/src/error.rs` and ensures consistent HTTP error responses across all endpoints.

**Example pattern observed in service methods:**
```rust
pub async fn fetch(&self, id: Id, tx: &Transactional<'_>) -> Result<AdvisoryDetails, AppError> {
    // ... database query ...
    .context("failed to fetch advisory")?;
}
```

**Example pattern observed in endpoint handlers:**
```rust
pub async fn handler(Path(id): Path<Id>, ...) -> Result<Json<T>, AppError> {
    let result = service.fetch(id, &tx).await.context("fetching advisory")?;
    Ok(Json(result))
}
```

## 2. Module Structure: `model/` + `service/` + `endpoints/`

Every domain module (sbom, advisory, package) follows a consistent three-subdirectory structure:

- **`model/`** — Data structs (DTOs/response types) with Serialize/Deserialize derives. Each struct gets its own file. A `mod.rs` re-exports all submodules with `pub mod`.
- **`service/`** — Business logic layer. Service structs contain methods that accept entity IDs and a `&Transactional<'_>` parameter for database access. Methods return `Result<ModelType, AppError>`.
- **`endpoints/`** — HTTP handlers. Each endpoint gets its own file (e.g., `get.rs`, `list.rs`). A `mod.rs` assembles all routes using Axum's `Router::new().route(...)` builder pattern.

This pattern is consistent across `sbom/`, `advisory/`, and `package/` modules within `modules/fundamental/src/`.

## 3. Endpoint Handler Pattern: Extract, Call, Return

Endpoint handlers follow a uniform three-step pattern:

1. **Extract** path/query parameters using Axum extractors (`Path<Id>`, `Query<Params>`)
2. **Call** the corresponding service method, propagating errors with `.context()`
3. **Return** the result wrapped in `Json(...)` (or `PaginatedResults` for list endpoints)

## 4. Route Registration Convention

Routes are registered in each module's `endpoints/mod.rs` using Axum's router builder:
```rust
Router::new()
    .route("/api/v2/<entity>", get(list::handler))
    .route("/api/v2/<entity>/:id", get(get::handler))
```
The `server/main.rs` mounts all module routers — individual modules do not need to modify the server entry point.

## 5. Response Types

- Single-entity endpoints return `Json<DetailStruct>`
- List endpoints return `PaginatedResults<SummaryStruct>` from `common/src/model/paginated.rs`
- New aggregate/summary endpoints (like this one) return a dedicated struct directly via `Json<T>`

## 6. Testing Convention

Integration tests live in `tests/api/` with one file per domain area. Tests hit a real PostgreSQL test database and assert on HTTP status codes using `assert_eq!(resp.status(), StatusCode::OK)` and similar patterns. Test names describe the scenario (e.g., `test_get_advisory_returns_404_for_unknown_id`).

## 7. Model Struct Conventions

Model structs derive at minimum `Serialize`, `Deserialize`, `Clone`, and `Debug`. Response structs intended for the OpenAPI spec also derive `utoipa::ToSchema`. Fields use snake_case and serde renames where needed for the JSON API contract.
