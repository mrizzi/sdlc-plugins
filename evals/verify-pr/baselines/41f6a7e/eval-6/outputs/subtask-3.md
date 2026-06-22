## Repository
sdlc-plugins

## Target Branch
main

## Description
Fix the Step 6a verdict mapping inconsistency for Documentation Coverage in SKILL.md. The current PR maps Documentation Coverage to "Style Quality *(new)*" but this report row does not exist in the Step 8 report format. Either add a Style Quality row to the Step 8 report table, or map Documentation Coverage to an existing row (e.g., include it in the "Test Quality *(combined)*" combination or create a separate report row with proper verdict source mapping).

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/SKILL.md` -- update the Step 6a verdict mapping for Documentation Coverage to reference a valid report row, and update Step 8 report format if a new row is added

## Implementation Notes
- The Step 6a mapping table in SKILL.md maps all other Style/Conventions checks to "Test Quality *(combined)*" but Documentation Coverage maps to "Style Quality *(new)*" which has no corresponding row in the Step 8 report table
- The Step 8 report table (in the "Generate Report" section) defines these rows: Review Feedback, Root-Cause Investigation, Scope Containment, Diff Size, Commit Traceability, Sensitive Patterns, CI Status, Acceptance Criteria, Test Quality, Test Change Classification, Verification Commands
- Two options: (1) Add a "Style Quality" row to Step 8 with proper verdict source mapping and overall result rules, or (2) Map Documentation Coverage into the existing Test Quality combination
- If adding a new report row, also update the verdict source mapping table in Step 8 and the overall result rules (determine if Style Quality is informational or affects PASS/WARN/FAIL)

## Acceptance Criteria
- [ ] Documentation Coverage verdict maps to a report row that exists in the Step 8 report format
- [ ] The Step 8 verdict source mapping table includes the Documentation Coverage mapping
- [ ] The report can be generated without a missing or orphaned verdict

## Target PR
https://github.com/mrizzi/sdlc-plugins/pull/747
