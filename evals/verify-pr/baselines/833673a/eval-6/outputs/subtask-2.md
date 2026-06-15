## Repository
sdlc-plugins

## Target Branch
main

## Description
The Step 6a verdict mapping in SKILL.md maps Documentation Coverage to a "Style Quality" report row, but the Step 8 report template and verdict source mapping do not include a "Style Quality" row. This creates an inconsistency where the orchestrator has no destination for the Documentation Coverage verdict when assembling the verification report. Add the "Style Quality" row to the Step 8 report template, the verdict source mapping, and update the overall result rules if needed.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/SKILL.md` -- add "Style Quality" row to Step 8 report template table, add entry to verdict source mapping table, and determine whether Style Quality affects the overall PASS/WARN/FAIL determination

## Implementation Notes
- The Step 6a mapping (line ~366 in the PR diff) maps `Style/Conventions | Documentation Coverage | Style Quality *(new)*`
- The Step 8 report template (lines 894-906) needs a new row: `| Style Quality | PASS/WARN/N/A | <summary> |`
- The verdict source mapping (lines 914-927) needs a new entry: `| Style Quality | Style/Conventions sub-agent (Documentation Coverage) |`
- Determine whether Style Quality should affect the overall result (PASS/WARN/FAIL) or be informational like Test Quality and Test Change Classification
- Follow the pattern of existing combined rows (e.g., Test Quality combines three checks) -- if Documentation Coverage is the only input to Style Quality, the combination logic is straightforward (pass-through)

## Acceptance Criteria
- [ ] Step 8 report template includes a "Style Quality" row with appropriate verdict values
- [ ] Verdict source mapping includes a "Style Quality" entry referencing Documentation Coverage
- [ ] Overall result rules clarify whether Style Quality affects the PASS/WARN/FAIL determination
- [ ] The Step 6a mapping and Step 8 report are consistent -- no report row referenced in Step 6a is missing from Step 8

## Review Context
This issue was identified during PR verification. The Step 6a verdict mapping references "Style Quality *(new)*" as the report row for Documentation Coverage, but this row does not exist in the Step 8 report template or verdict source mapping, creating a structural inconsistency in the verification report output.

## Target PR
https://github.com/mrizzi/sdlc-plugins/pull/747
