# Criterion 5: Response includes a `threshold_applied` boolean field indicating whether filtering is active

## Verdict: FAIL

## Analysis

The task requires that the API response include a `threshold_applied` boolean field that indicates whether threshold filtering is active. This field should be `true` when a valid threshold parameter is provided and `false` (or absent with a default of `false`) when no threshold is specified.

### Code Inspection

In `modules/fundamental/src/advisory/endpoints/get.rs`, the filtered response is constructed as:

```rust
AdvisorySummary {
    critical: summary.critical,
    high: if threshold_idx <= 1 { summary.high } else { 0 },
    medium: if threshold_idx <= 2 { summary.medium } else { 0 },
    low: if threshold_idx <= 3 { summary.low } else { 0 },
    total: summary.critical + summary.high + summary.medium + summary.low,
}
```

And for the no-threshold case:

```rust
None => summary,
```

### Why This Fails

The `AdvisorySummary` struct construction includes only five fields: `critical`, `high`, `medium`, `low`, and `total`. There is no `threshold_applied` field anywhere in the response.

Neither the `Some(threshold)` branch nor the `None` branch sets a `threshold_applied` field. The `AdvisorySummary` model struct (defined in `modules/fundamental/src/advisory/model/summary.rs` per the repository structure) would need to be updated to include this field, and both branches would need to set it appropriately:

- `Some(threshold)` branch: `threshold_applied: true`
- `None` branch: `threshold_applied: false`

### Impact

API consumers cannot programmatically determine whether the returned counts represent filtered or unfiltered data. This is particularly important for:
- Clients that conditionally display threshold information in the UI
- Downstream systems that need to distinguish between "no advisories at this severity" and "severity was filtered out"

### Evidence

- **File:** `modules/fundamental/src/advisory/endpoints/get.rs`, lines 47-53 (AdvisorySummary construction) and line 55 (None branch)
- **Missing field:** `threshold_applied` boolean is absent from the response struct
- **Model file:** `modules/fundamental/src/advisory/model/summary.rs` would need modification to add the field to the `AdvisorySummary` struct
- **Neither branch** in the match expression sets a `threshold_applied` value
