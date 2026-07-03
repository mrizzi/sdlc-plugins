# Criterion 2: `GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all severity counts (backward compatible)

## Verdict: PASS

## Analysis

The task requires that when no `threshold` query parameter is provided, the endpoint returns all severity counts unchanged, maintaining backward compatibility with existing clients.

The implementation handles this case in the `None` branch of the match:

```rust
None => summary,
```

When `params.threshold` is `None` (no threshold parameter provided), the original `summary` object from `AdvisoryService::aggregate_severities()` is returned unmodified. This preserves all four severity counts (critical, high, medium, low) and the total exactly as they were computed by the existing aggregation logic.

The `SummaryParams` struct defines `threshold` as `Option<String>`, which means the parameter is truly optional -- requests without the `threshold` query parameter will deserialize into `SummaryParams { threshold: None }`.

**Caveat:** While the counts are backward compatible, the response is missing the new `threshold_applied` boolean field specified in Criterion 5. If existing clients perform strict schema validation, the absence of this field maintains compatibility. However, the intent of Criterion 5 is to ADD this field to ALL responses (set to `false` when no threshold is applied), which would technically modify the response shape. Since Criterion 2 specifically asks about "severity counts" being preserved, this is evaluated as PASS -- the missing `threshold_applied` field is tracked separately under Criterion 5.

## Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs`
- The `None => summary` branch returns the unmodified summary object
- `threshold` is defined as `Option<String>` ensuring optional behavior
- The existing `SbomService::fetch()` and `AdvisoryService::aggregate_severities()` calls are unchanged
