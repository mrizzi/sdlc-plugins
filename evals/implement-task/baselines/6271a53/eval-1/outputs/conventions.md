# Convention Conformance Analysis

## Sibling Analysis

The following conventions were discovered by examining existing files in the advisory module and common utilities.

---

### 1. Error Handling: `Result<T, AppError>` with `.context()` Wrapping

**Pattern** (from `common/src/error.rs` and `advisory/service/advisory.rs`):
- All endpoint handlers return `Result<T, AppError>`
- Service methods return `Result<T, anyhow::Error>` which converts into `AppError` at the handler boundary
- Errors are wrapped with `.context("descriptive message")` (anyhow-style) to provide actionable error context
- 404s are returned for missing resources via `AppError::NotFound("resource description")`

**Example from existing code**:
```rust
let sbom = self.db
    .find_by_id(sbom_id)
    .one(&tx)
    .await?
    .context("SBOM not found")?;
```

**Conformance for TC-9201**: The new service method must use `.context()` for error wrapping and return 404 when the SBOM ID does not exist.

---

### 2. Module Structure: `model/` + `service/` + `endpoints/` Pattern

**Pattern** (from `advisory/`, `sbom/`, `package/` modules):
Every domain module under `modules/fundamental/src/` follows a strict three-directory structure:

```
<domain>/
  mod.rs
  model/
    mod.rs
    summary.rs
    details.rs
  service/
    mod.rs
    <domain>.rs
  endpoints/
    mod.rs
    list.rs
    get.rs
```

- `model/mod.rs` re-exports sub-modules via `pub mod <name>;`
- `service/mod.rs` re-exports the service struct
- `endpoints/mod.rs` registers routes and re-exports handlers

**Conformance for TC-9201**: New files slot into the existing `advisory/` module: model goes in `model/severity_summary.rs`, endpoint in `endpoints/severity_summary.rs`, service method added to `service/advisory.rs`.

---

### 3. Naming Conventions

**Pattern**:
- File names use `snake_case` and match the concept they represent
- Model files: named after the struct concept (`summary.rs`, `details.rs`)
- Service files: named after the domain entity (`advisory.rs`, `sbom.rs`)
- Endpoint files: named after the HTTP verb or action (`list.rs`, `get.rs`)
- Structs: `PascalCase` matching the file name concept (`AdvisorySummary`, `SbomDetails`)

**Conformance for TC-9201**: New files named `severity_summary.rs`, struct named `SeveritySummary`.

---

### 4. Endpoint Handler Pattern

**Pattern** (from `advisory/endpoints/get.rs`):
- Extract path parameters via Axum's `Path<Id>` extractor
- Accept shared state (service) via `State` or `Extension` extractor
- Accept transaction context via `Transactional<'_>` extractor
- Call the corresponding service method
- Return `Result<Json<T>, AppError>`
- Use `.context("descriptive message")` for error wrapping

**Signature pattern**:
```rust
pub async fn get(
    Path(id): Path<Id>,
    State(service): State<AdvisoryService>,
    tx: Transactional<'_>,
) -> Result<Json<T>, AppError> {
    let result = service
        .get_advisory(id, &tx)
        .await?
        .context("advisory not found")?;
    Ok(Json(result))
}
```

**Conformance for TC-9201**: The new `severity_summary` handler must follow this exact pattern.

---

### 5. Route Registration Pattern

**Pattern** (from `advisory/endpoints/mod.rs`):
- Routes are registered using `Router::new().route("/path", get(handler))`
- Each module's `endpoints/mod.rs` builds a `Router` that is merged into the parent
- Route paths follow REST conventions with nested resources

**Conformance for TC-9201**: Add `.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::severity_summary))` in the advisory endpoints module.

---

### 6. Service Method Pattern

**Pattern** (from `advisory/service/advisory.rs`):
- Methods on `AdvisoryService` take `&self`
- Entity ID parameters use the `Id` type
- Transaction context passed as `tx: &Transactional<'_>`
- Methods return `Result<T, anyhow::Error>`
- Database queries use SeaORM entity query builders

**Signature pattern**:
```rust
pub async fn get_severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, anyhow::Error> {
    // ...
}
```

**Conformance for TC-9201**: Follow this exact pattern for the new service method.

---

### 7. Model/Struct Pattern

**Pattern** (from `advisory/model/summary.rs`):
- Response structs derive `Serialize`, `Deserialize`, `Debug`, `Clone`
- Also derive `utoipa::ToSchema` for OpenAPI documentation
- Fields use Rust standard types (`i64`, `String`, etc.)
- Structs are `pub` with `pub` fields

**Conformance for TC-9201**: The `SeveritySummary` struct must derive the same traits as `AdvisorySummary`.

---

### 8. Test Pattern

**Pattern** (from `tests/api/advisory.rs`, `tests/api/sbom.rs`):
- Integration tests use a test harness that spins up a real PostgreSQL database
- Tests make HTTP requests to the running server
- Tests assert on response status codes and JSON bodies
- Test functions are `#[tokio::test]` async functions
- Test data is set up via service calls or fixtures

**Conformance for TC-9201**: Integration tests should follow this pattern with setup, HTTP request, and assertion phases.

---

### 9. Module Registration Pattern

**Pattern** (from `advisory/model/mod.rs`):
- Each `mod.rs` declares sub-modules with `pub mod <name>;`
- This is the sole mechanism for making modules visible to the rest of the crate

**Conformance for TC-9201**: Add `pub mod severity_summary;` to `advisory/model/mod.rs`.
