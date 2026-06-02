## Repository
sdlc-plugins

## Target Branch
main

## Description
Add the "Style Quality" row to the Step 8 report template in SKILL.md and update the verdict source mapping. The PR adds a Documentation Coverage check mapped to "Style Quality *(new)*" in Step 6a's verdict mapping table, but the Step 8 report template and verdict source mapping table do not include a corresponding "Style Quality" row. Without this row, the Documentation Coverage verdict has no place in the final verification report.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/SKILL.md` -- add a "Style Quality" row to the Step 8 report template table and the verdict source mapping table

## Implementation Notes
- In the Step 8 report template (the markdown table under "Compile all findings"), add a row for Style Quality after the existing rows, following the same format: `| Style Quality | PASS/WARN/N/A | <summary> |`
- In the Step 8 verdict source mapping table, add: `| Style Quality | Style/Conventions sub-agent (Documentation Coverage) |`
- Consider whether Style Quality should be informational (like Test Quality and Test Change Classification, excluded from Overall result) or should affect the Overall result. Given that documentation coverage is advisory (WARN, not FAIL), making it informational is consistent with the existing pattern
- Update the "Overall result rules" note to list Style Quality as informational if that design is chosen

## Review Context
This gap was identified during verification: the Step 6a verdict mapping adds `| Style/Conventions | Documentation Coverage | Style Quality *(new)* |` but the Step 8 report template does not include a Style Quality row. This means the Documentation Coverage verdict would not appear in the final report output.

## Target PR
https://github.com/mrizzi/sdlc-plugins/pull/747

## Acceptance Criteria
- [ ] Step 8 report template includes a "Style Quality" row
- [ ] Step 8 verdict source mapping includes Style Quality mapped to the Style/Conventions sub-agent's Documentation Coverage check
- [ ] The Overall result rules document whether Style Quality is informational or affects the verdict
