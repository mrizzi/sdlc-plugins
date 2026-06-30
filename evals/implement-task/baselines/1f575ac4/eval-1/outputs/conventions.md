# Conventions Discovered from Sibling Analysis

## 1. Error Handling Pattern: `Result<T, AppError>` with `.context()`

All service methods and endpoint handlers return `Result<T, AppError>` where `AppError` is defined in `common/src/error.rs` and implements Axum's `IntoResponse` trait.

Error wrapping uses the `.context()` method (from the `anyhow`-style error chain) to add descriptive messages when propagating errors:

```rust
// Pattern observed in service methods:
pub async fn fetch(&self, id: Id, tx: &Transactional<'_>) -> Result<AdvisoryDetails, AppError> {
    let advisory = entity::advisory::Entity::find_by_id(id)
        .one(tx.connection())
        .await
        .context("Failed to fetch advisory")?;
    // ...
}
```

This pattern ensures consistent error responses across all endpoints and provides meaningful error context for debugging.

## 2. Module Structure: `model/ + service/ + endpoints/`

Every domain module under `modules/fundamental/src/` follows a strict three-directory structure:

- **`model/`** -- Data structures (response types, domain objects). Contains `mod.rs` for module registration plus individual files per struct (e.g., `summary.rs`, `details.rs`). Structs derive `Serialize`, `Deserialize`, `Debug`, `Clone`, and `utoipa::ToSchema`.
- **`service/`** -- Business logic. Contains a primary service struct (e.g., `AdvisoryService`, `SbomService`) with async methods that accept `&self`, entity IDs, and a `&Transactional<'_>` parameter for database access.
- **`endpoints/`** -- HTTP handlers and route registration. Contains `mod.rs` for route registration via `Router::new().route(...)` and individual handler files. Handlers extract path params via `Path<Id>`, call service methods, and return `Json(T)`.

This pattern is consistently applied across the `sbom/`, `advisory/`, and `package/` modules.

## 3. Route Registration Pattern

Each module's `endpoints/mod.rs` builds a `Router` by chaining `.route("/path", get(handler))` calls. The `server/main.rs` mounts all module routers, meaning new routes are auto-discovered once registered in the module's `mod.rs`.

```rust
// Pattern from endpoints/mod.rs:
pub fn router() -> Router {
    Router::new()
        .route("/api/v2/advisory", get(list::list))
        .route("/api/v2/advisory/:id", get(get::get_advisory))
}
```

## 4. Endpoint Handler Pattern

Endpoint handlers follow a consistent async function signature:

```rust
pub async fn handler_name(
    Path(id): Path<Id>,
    State(service): State<AdvisoryService>,
) -> Result<Json<ResponseType>, AppError> {
    let result = service.method(id, &Transactional::default()).await?;
    Ok(Json(result))
}
```

Key elements: path parameter extraction via `Path<Id>`, service injection via `State`, `Result<Json<T>, AppError>` return type.

## 5. Integration Test Pattern

Tests in `tests/api/` use a real PostgreSQL test database and follow this pattern:

```rust
#[tokio::test]
async fn test_endpoint() {
    let app = test_app().await;
    let resp = app.get("/api/v2/...").await;
    assert_eq!(resp.status(), StatusCode::OK);
    let body: ResponseType = resp.json().await;
    assert_eq!(body.field, expected_value);
}
```

Tests use `assert_eq!(resp.status(), StatusCode::OK)` for status checks and deserialize response bodies for content validation.

## 6. Response Types for Collections

List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`, while single-entity and aggregation endpoints return the struct directly wrapped in `Json<T>`.
