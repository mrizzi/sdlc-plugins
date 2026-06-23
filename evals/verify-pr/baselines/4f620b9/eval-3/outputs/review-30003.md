## Review Comment 30003 — Classification

**Comment ID:** 30003
**Author:** reviewer-a
**File:** modules/fundamental/src/sbom/endpoints/mod.rs
**Line:** 18
**Content:** Nit: `context("SBOM not found")` is misleading here because `.context()` wraps the error message for the anyhow chain — it doesn't mean the SBOM wasn't found. The actual 404 is handled by `ok_or(AppError::NotFound(...))` on the next line. Consider changing the context message to something like `"Failed to fetch SBOM"` to avoid confusion in error logs.

### Classification: nit

### Reasoning

The reviewer explicitly labels this as a "Nit" and uses the word "Consider," indicating this is minor style or clarity feedback. The issue is about the wording of an error context message in logging, not about functional correctness. The `.context()` call works correctly regardless of its message text — it wraps the anyhow error chain for debugging purposes. Changing the message from "SBOM not found" to "Failed to fetch SBOM" would improve log clarity but has no impact on application behavior or API responses. This is a minor readability improvement, not a required code change.

### Action

No sub-task created.
