## Repository
sdlc-plugins

## Target Branch
main

## Description
Add a Markdown-specific documentation rule to Check 6 (Documentation Coverage) in the style-conventions sub-agent. The current implementation skips Markdown files entirely ("Markdown: not applicable -- skip Markdown files"), but since this is a documentation-heavy repository where skills are defined in Markdown, the check should verify that new Markdown sections have introductory explanatory text. Specifically, when new `###` headings are introduced in a PR diff, Check 6 should verify that at least one paragraph of explanatory text exists between the heading and any sub-sections or code blocks.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` -- update Check 6 section 6b to replace the Markdown "not applicable" exclusion with a Markdown-specific rule that checks new `###` headings for explanatory text

## Implementation Notes
- In section "6b -- Check Documentation Comments", replace the line `- **Markdown:** not applicable -- skip Markdown files` with a Markdown-specific rule
- The Markdown rule should check whether new `###` (or deeper) headings have at least one paragraph of explanatory text before any sub-sections or code blocks
- Follow the pattern of other language-specific checks in 6b: each language has a specific convention for what constitutes documentation
- For Markdown, the "documentation" equivalent is introductory prose that explains the purpose of the section
- Do not change the verdict logic in 6c -- the existing PASS/WARN/N/A verdicts apply to Markdown sections the same way they apply to code symbols

## Acceptance Criteria
- [ ] Check 6 section 6b includes a Markdown-specific documentation rule
- [ ] The rule checks whether new `###` headings have at least one paragraph of explanatory text before sub-sections or code blocks
- [ ] The Markdown exclusion ("not applicable -- skip Markdown files") is removed
- [ ] Existing language-specific doc comment checks are not affected

## Test Requirements
- [ ] Verify the Markdown rule flags new headings that go directly to sub-sections or code blocks without explanatory text
- [ ] Verify the Markdown rule does not flag headings that have explanatory text

## Review Context
**Comment ID:** 50001
**Reviewer:** reviewer-b
**File:** `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md`, line 310
**Comment:** "The Check 6 description says 'Markdown: not applicable -- skip Markdown files' but this is a documentation-heavy repository where skills are defined in Markdown. The check should still verify that new Markdown sections have introductory text explaining their purpose, even if traditional doc comments don't apply. Consider adding a Markdown-specific rule that checks whether new `###` headings have at least one paragraph of explanatory text before any sub-sections or code blocks."

## Target PR
https://github.com/mrizzi/sdlc-plugins/pull/747
