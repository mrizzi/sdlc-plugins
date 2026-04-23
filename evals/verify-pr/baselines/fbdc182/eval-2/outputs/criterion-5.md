# Criterion 5: Response includes a `threshold_applied` boolean field indicating whether filtering is active

## Result: FAIL

## Reasoning

The diff constructs an `AdvisorySummary` struct with only the following fields: `critical`, `high`, `medium`, `low`, and `total`. There is no `threshold_applied` boolean field anywhere in the response.

The acceptance criterion explicitly requires a `threshold_applied` boolean field that indicates whether filtering is active (true when a threshold parameter is provided, false otherwise). This field is completely absent from the implementation:

1. The `AdvisorySummary` struct (in `advisory/model/summary.rs`) was not modified to add the field.
2. The handler code in `get.rs` does not set or reference any such field.

This is a missing feature, not a bug in existing logic.
