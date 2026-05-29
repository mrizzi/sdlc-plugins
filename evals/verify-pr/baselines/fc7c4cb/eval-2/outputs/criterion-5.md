## Criterion 5

**Text:** Response includes a `threshold_applied` boolean field indicating whether filtering is active

**What I checked:** The `AdvisorySummary` struct construction in the diff, any modifications to the model file `modules/fundamental/src/advisory/model/summary.rs`, and the response body in `modules/fundamental/src/advisory/endpoints/get.rs`.

**Code evidence:**

The filtered response is constructed as:

```rust
AdvisorySummary {
    critical: summary.critical,
    high: if threshold_idx <= 1 { summary.high } else { 0 },
    medium: if threshold_idx <= 2 { summary.medium } else { 0 },
    low: if threshold_idx <= 3 { summary.low } else { 0 },
    total: summary.critical + summary.high + summary.medium + summary.low,
}
```

There is no `threshold_applied` field in the constructed struct. The diff does not include any changes to the `AdvisorySummary` model definition (located at `modules/fundamental/src/advisory/model/summary.rs` per the repository structure), which would be required to add this field.

The `None` branch also returns the raw `summary` without any `threshold_applied` field.

Neither the `Some` nor `None` branches include a `threshold_applied: bool` field in the response.

**Verdict: FAIL**

The `threshold_applied` boolean field is completely absent from the response. The `AdvisorySummary` struct was not modified to include it, and neither code path sets such a field.
