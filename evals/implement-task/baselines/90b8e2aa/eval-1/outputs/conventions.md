# Discovered Conventions for TC-9201

## Convention Conformance Analysis (from sibling analysis)

Conventions discovered by inspecting sibling files in the trustify-backend repository. These serve as binding references during implementation.

### Production Code Conventions

#### Model Conventions (from `modules/fundamental/src/advisory/model/`)

Sibling files analyzed: `summary.rs`, `details.rs`

- **Module registration**: Each model file is registered via `pub mod <name>;` in the parent `mod.rs`
- **Derive macros**: Model structs use `#[derive(Clone, Debug, Serialize, Deserialize)]` at minimum; response-only structs may omit `Deserialize`
- **Serialization**: All response structs derive `serde::Serialize` for Axum `Json<T>` compatibility
- **Field naming**: Struct fields use snake_case in Rust; `#[serde(rename_all = "camelCase")]` is used when JSON output requires camelCase
- **Documentation**: Structs have `///` doc comments describing their purpose

#### Service Conventions (from `modules/fundamental/src/advisory/service/advisory.rs`)

Sibling methods analyzed: `fetch`, `list`, `search`

- **Method signature**: Service methods take `&self` as receiver, accept entity-specific ID types, and take `tx: &Transactional<'_>` as the last parameter for transaction propagation
- **Return type**: All methods return `Result<T, AppError>` where `T` is the domain type
- **Error handling**: Errors are wrapped using `.context("descriptive message")` (anyhow-style), producing `AppError` variants
- **Naming**: Service methods follow `verb_noun` pattern (e.g., `fetch`, `list`, `search`) -- the new method follows this as `severity_summary`
- **Query pattern**: Methods use SeaORM entity queries with `.find()`, `.filter()`, `.all()` or `.one()`, operating through the transactional connection

#### Endpoint Conventions (from `modules/fundamental/src/advisory/endpoints/`)

Sibling files analyzed: `get.rs`, `list.rs`, `mod.rs`

- **Handler signature**: Handlers are async functions taking Axum extractors (`Path<T>`, `Query<T>`, `State<T>`) and returning `Result<Json<T>, AppError>`
- **Path parameter extraction**: Uses `Path(id): Path<Id>` pattern for single path parameters
- **Service invocation**: Handlers obtain the service from application state, call the service method, and return the result wrapped in `Json()`
- **Route registration**: `mod.rs` registers routes via `Router::new().route("/path", get(handler_function))` chaining
- **Error responses**: 404 is returned by the service layer when an entity is not found; the handler does not need explicit 404 logic beyond propagating the `AppError`
- **Module declaration**: Each endpoint file is declared as `mod <name>;` in the parent `mod.rs`

#### Error Handling Conventions (from `common/src/error.rs`)

- **Error type**: `AppError` enum implements `IntoResponse` for Axum
- **Context wrapping**: All fallible operations use `.context("message")` to add context before converting to `AppError`
- **HTTP status mapping**: `AppError` variants map to HTTP status codes (e.g., NotFound -> 404, Internal -> 500)

#### Module Structure Conventions

- **Domain module layout**: Every domain module follows the `model/ + service/ + endpoints/` tripartite structure
- **File organization**: Each concern gets its own file (e.g., `summary.rs` for the summary model, `get.rs` for the get endpoint)
- **Re-exports**: Parent `mod.rs` files re-export key types for external consumption

### Test Conventions (from sibling test analysis)

Sibling test files analyzed: `tests/api/sbom.rs`, `tests/api/advisory.rs`

- **Assertion style**: Integration tests use `assert_eq!(resp.status(), StatusCode::OK)` for success cases and `assert_eq!(resp.status(), StatusCode::NOT_FOUND)` for 404 cases
- **Response validation**: Tests deserialize the response body and assert on specific field values, not just structure presence
- **Test naming**: Tests follow `test_<endpoint>_<scenario>` pattern (e.g., `test_get_advisory_by_id`, `test_list_sboms_filtered`)
- **Test setup**: Tests use a shared test database setup with fixture data seeded before assertions
- **HTTP client**: Tests use an HTTP test client (likely `reqwest` or Axum's test utilities) to make requests against the running test server
- **Error case coverage**: Every endpoint test suite includes at least one 404 test with a non-existent ID
- **Body deserialization**: Response bodies are deserialized into the expected struct type using `serde_json::from_slice` or equivalent
- **Parameterized tests**: Would check if sibling tests use `#[rstest]` with `#[case]` -- if not used in siblings, would not introduce parameterized tests
- **Documentation**: Per SKILL.md requirements, every test function gets a `///` doc comment regardless of whether siblings have them (AI-generated standard)

### Cross-section Reference Consistency

Verified file path references across task description sections:

| Entity | Files to Modify | Implementation Notes | Consistent |
|---|---|---|---|
| AdvisoryService | `modules/fundamental/src/advisory/service/advisory.rs` | `modules/fundamental/src/advisory/service/advisory.rs` | Yes |
| Endpoint registration | `modules/fundamental/src/advisory/endpoints/mod.rs` | `modules/fundamental/src/advisory/endpoints/mod.rs` | Yes |
| Model registration | `modules/fundamental/src/advisory/model/mod.rs` | (not referenced separately) | Yes |
| AdvisorySummary.severity | (not in Files to Modify) | `modules/fundamental/src/advisory/model/summary.rs` | Yes (read-only reference) |
| sbom_advisory join table | (not in Files to Modify) | `entity/src/sbom_advisory.rs` | Yes (read-only reference) |
| Endpoint pattern reference | (not in Files to Modify) | `modules/fundamental/src/advisory/endpoints/get.rs` | Yes (read-only reference) |
| AppError | (not in Files to Modify) | `common/src/error.rs` | Yes (read-only reference) |

No cross-section inconsistencies detected.
