<!-- SYNTHETIC TEST DATA — mock PR diff for eval testing; simulates `gh pr diff` output for an implementation that misses acceptance criteria -->

```diff
diff --git a/modules/fundamental/src/advisory/endpoints/get.rs b/modules/fundamental/src/advisory/endpoints/get.rs
index 2c3d4e5..f6a7b8c 100644
--- a/modules/fundamental/src/advisory/endpoints/get.rs
+++ b/modules/fundamental/src/advisory/endpoints/get.rs
@@ -1,5 +1,6 @@
 use axum::extract::{Path, Query};
 use axum::Json;
+use serde::Deserialize;

 use crate::advisory::service::AdvisoryService;
 use common::error::AppError;
@@ -8,10 +9,17 @@ use common::error::AppError;
 pub struct SbomId {
     pub id: i64,
 }

+#[derive(Debug, Deserialize)]
+pub struct SummaryParams {
+    pub threshold: Option<String>,
+}
+
 /// Handles GET /api/v2/sbom/{id}/advisory-summary with optional threshold.
 pub async fn advisory_summary(
     db: DatabaseConnection,
     Path(sbom_id): Path<SbomId>,
+    Query(params): Query<SummaryParams>,
 ) -> Result<Json<AdvisorySummary>, AppError> {
     let sbom = SbomService::new(&db)
         .fetch(sbom_id.id)
@@ -20,7 +28,22 @@ pub async fn advisory_summary(

     let summary = AdvisoryService::new(&db)
         .aggregate_severities(sbom.id)
         .await
         .context("Failed to aggregate advisory severities")?;

-    Ok(Json(summary))
+    let filtered = match &params.threshold {
+        Some(threshold) => {
+            let severity_order = ["critical", "high", "medium", "low"];
+            let threshold_idx = severity_order.iter()
+                .position(|&s| s == threshold.to_lowercase())
+                .unwrap_or(0);
+            AdvisorySummary {
+                critical: summary.critical,
+                high: if threshold_idx <= 1 { summary.high } else { 0 },
+                medium: if threshold_idx <= 2 { summary.medium } else { 0 },
+                low: if threshold_idx <= 3 { summary.low } else { 0 },
+                total: summary.critical + summary.high + summary.medium + summary.low,
+            }
+        }
+        None => summary,
+    };
+
+    Ok(Json(filtered))
 }
diff --git a/modules/fundamental/src/advisory/service/advisory.rs b/modules/fundamental/src/advisory/service/advisory.rs
index 3d4e5f6..a7b8c9d 100644
--- a/modules/fundamental/src/advisory/service/advisory.rs
+++ b/modules/fundamental/src/advisory/service/advisory.rs
@@ -45,6 +45,7 @@ impl AdvisoryService {
             low: counts.get("low").copied().unwrap_or(0),
             total: counts.values().sum(),
         })
     }
 }
```

**Notes on what this diff is missing (for eval grading context):**
<!-- These notes are NOT part of the mock diff — they document what acceptance criteria are NOT satisfied:
  1. No validation of invalid threshold values — `unwrap_or(0)` silently accepts invalid input instead of returning 400
  2. No `threshold_applied` boolean field in the response
  3. Total is recomputed from unfiltered counts instead of filtered counts
  4. No 404 test for non-existent SBOM (though 404 behavior exists, no test was added)
  5. No test file was created at all — tests/api/advisory_summary.rs is absent from the diff
-->
