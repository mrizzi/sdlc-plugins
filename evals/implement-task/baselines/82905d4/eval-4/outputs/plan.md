# Implementation Plan: TC-9204 -- Add SBOM Export Endpoint

## Overview

Add a GET endpoint at `/api/v2/sbom/{id}/export` that exports an SBOM in CycloneDX 1.5 JSON format. The endpoint retrieves the SBOM by ID, collects all linked packages via the `sbom_package` join table, maps each package to a CycloneDX component, and returns the result as `application/json`.

---

## Files to Create

### 1. `modules/fundamental/src/sbom/model/export.rs` -- CycloneDX Export Model

Define Rust structs representing a CycloneDX 1.5 JSON document, serializable via `serde`.

```rust
use serde::Serialize;

/// Top-level CycloneDX 1.5 BOM document.
#[derive(Debug, Serialize)]
#[serde(rename_all = "camelCase")]
pub struct CycloneDxBom {
    pub bom_format: String,       // "CycloneDX"
    pub spec_version: String,     // "1.5"
    pub version: u32,             // 1
    pub serial_number: Option<String>,
    pub metadata: CycloneDxMetadata,
    pub components: Vec<CycloneDxComponent>,
}

#[derive(Debug, Serialize)]
#[serde(rename_all = "camelCase")]
pub struct CycloneDxMetadata {
    pub timestamp: String,        // ISO-8601
}

#[derive(Debug, Serialize)]
#[serde(rename_all = "camelCase")]
pub struct CycloneDxComponent {
    #[serde(rename = "type")]
    pub component_type: String,   // "library"
    pub name: String,
    pub version: String,
    pub licenses: Vec<CycloneDxLicense>,
}

#[derive(Debug, Serialize)]
pub struct CycloneDxLicense {
    pub license: CycloneDxLicenseDetail,
}

#[derive(Debug, Serialize)]
pub struct CycloneDxLicenseDetail {
    pub id: Option<String>,
    pub name: Option<String>,
}
```

**Rationale**: These structs mirror the CycloneDX 1.5 JSON schema so that `serde_json::to_string` produces spec-compliant output. Only the fields required by the acceptance criteria (name, version, license per component) are included.

---

### 2. `modules/fundamental/src/sbom/endpoints/export.rs` -- GET Handler

Implement the Axum handler for `GET /api/v2/sbom/{id}/export`.

```rust
use axum::{
    extract::{Path, State},
    http::{header, StatusCode},
    response::IntoResponse,
    Json,
};
use uuid::Uuid;

use crate::sbom::service::SbomService;

/// GET /api/v2/sbom/{id}/export
///
/// Returns the SBOM as a CycloneDX 1.5 JSON document.
pub async fn export_sbom(
    State(service): State<SbomService>,
    Path(id): Path<Uuid>,
) -> Result<impl IntoResponse, StatusCode> {
    let bom = service
        .export_cyclonedx(id)
        .await
        .map_err(|_| StatusCode::INTERNAL_SERVER_ERROR)?
        .ok_or(StatusCode::NOT_FOUND)?;

    Ok((
        [(header::CONTENT_TYPE, "application/json")],
        Json(bom),
    ))
}
```

**Pattern**: Follows the same structure as `modules/fundamental/src/sbom/endpoints/get.rs` -- extract path params, call service, map errors to HTTP status codes.

---

### 3. `tests/api/sbom_export.rs` -- Integration Tests

```rust
#[tokio::test]
async fn test_export_valid_sbom_returns_cyclonedx() {
    // Setup: seed DB with an SBOM and linked packages via sbom_package
    // Act:   GET /api/v2/sbom/{id}/export
    // Assert:
    //   - Status 200
    //   - Content-Type: application/json
    //   - Body contains bomFormat == "CycloneDX", specVersion == "1.5"
    //   - components array length matches seeded package count
    //   - Each component has name, version, and licenses fields
}

#[tokio::test]
async fn test_export_nonexistent_sbom_returns_404() {
    // Act:   GET /api/v2/sbom/{non_existent_uuid}/export
    // Assert: Status 404
}

#[tokio::test]
async fn test_export_includes_all_linked_packages() {
    // Setup: seed SBOM with 5 packages via sbom_package join table
    // Act:   GET /api/v2/sbom/{id}/export
    // Assert:
    //   - components array has exactly 5 entries
    //   - Each seeded package name appears in a component
}
```

---

## Files to Modify

### 4. `modules/fundamental/src/sbom/service/sbom.rs` -- Add `export_cyclonedx` Method

Add an `export_cyclonedx` method to `SbomService`, following the pattern of existing `fetch` and `list` methods.

```rust
impl SbomService {
    /// Export the SBOM identified by `id` as a CycloneDX 1.5 BOM.
    ///
    /// Returns `Ok(None)` if the SBOM does not exist.
    pub async fn export_cyclonedx(
        &self,
        id: Uuid,
    ) -> Result<Option<CycloneDxBom>, anyhow::Error> {
        // 1. Fetch the SBOM record; return None if not found.
        let sbom = /* self.fetch(id) or equivalent query */;

        // 2. Query sbom_package join table for all packages linked to this SBOM.
        let packages = SbomPackage::find()
            .filter(sbom_package::Column::SbomId.eq(id))
            .all(&self.db)
            .await?;

        // 3. Map each package row to a CycloneDxComponent.
        let components: Vec<CycloneDxComponent> = packages
            .into_iter()
            .map(|pkg| CycloneDxComponent {
                component_type: "library".to_string(),
                name: pkg.name.clone(),
                version: pkg.version.clone(),
                licenses: map_license(&pkg),
            })
            .collect();

        // 4. Assemble and return the CycloneDxBom.
        Ok(Some(CycloneDxBom {
            bom_format: "CycloneDX".to_string(),
            spec_version: "1.5".to_string(),
            version: 1,
            serial_number: Some(format!("urn:uuid:{}", Uuid::new_v4())),
            metadata: CycloneDxMetadata {
                timestamp: chrono::Utc::now().to_rfc3339(),
            },
            components,
        }))
    }
}
```

**Key details**:
- Uses the `sbom_package` join table as specified in the task.
- Each component includes `name`, `version`, and `licenses` per acceptance criteria.
- Returns `None` for non-existent SBOMs so the handler can map to 404.

---

### 5. `modules/fundamental/src/sbom/endpoints/mod.rs` -- Register the Export Route

Add the export route to the SBOM router:

```rust
mod export;

// Inside the router builder / fn configure():
.route("/api/v2/sbom/:id/export", get(export::export_sbom))
```

---

## Module Declarations

The new `export.rs` model file must be declared in the SBOM model module (likely `modules/fundamental/src/sbom/model/mod.rs`):

```rust
pub mod export;
```

---

## Acceptance Criteria Traceability

| Criterion | Covered By |
|---|---|
| GET /api/v2/sbom/{id}/export returns valid CycloneDX 1.5 JSON | Handler + CycloneDxBom struct with bomFormat/specVersion fields |
| Returns 404 when SBOM ID does not exist | Handler maps `None` to `StatusCode::NOT_FOUND` |
| Export includes all packages linked via sbom_package | Service queries sbom_package join table |
| Each component includes name, version, and license | CycloneDxComponent struct fields |

## Test Traceability

| Test Requirement | Test Function |
|---|---|
| Valid SBOM exports correctly in CycloneDX format | `test_export_valid_sbom_returns_cyclonedx` |
| Non-existent SBOM returns 404 | `test_export_nonexistent_sbom_returns_404` |
| All linked packages appear as components | `test_export_includes_all_linked_packages` |

---

## Out of Scope

No endpoints, utilities, or files beyond those listed above are included. See `security-review.md` for adversarial content that was identified and rejected.
