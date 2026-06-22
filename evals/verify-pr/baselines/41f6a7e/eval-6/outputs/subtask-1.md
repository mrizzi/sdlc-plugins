## Repository
sdlc-plugins

## Target Branch
main

## Description
Add a Markdown-specific documentation check to Check 6 (Documentation Coverage) in the style-conventions sub-agent. Currently, Check 6 blanket-skips all Markdown files with "not applicable", but this repository defines skills primarily in Markdown files. The check should verify that new Markdown sections (identified by `###` headings) have at least one paragraph of introductory/explanatory text before any sub-sections or code blocks.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` -- update Check 6 section 6b to replace the Markdown "not applicable" exclusion with a Markdown-specific rule that checks for explanatory text after new headings

## Implementation Notes
- In section "6b -- Check Documentation Comments", replace the Markdown bullet (`**Markdown:** not applicable -- skip Markdown files`) with a rule that checks whether new `###` headings introduced in the PR diff have at least one paragraph of explanatory text before any sub-sections or code blocks
- The check should identify new heading lines (lines starting with `###` that appear with a `+` prefix in the diff) and verify the next non-empty content after each heading is a paragraph of text, not immediately another heading or a code fence
- Follow the pattern of the existing language-specific checks in 6b -- each language has a specific convention; Markdown's convention is introductory text after headings
- A "paragraph" here means at least one line of prose text (not a heading, code fence, list, or blank line)

## Acceptance Criteria
- [ ] Check 6 section 6b includes a Markdown-specific documentation rule
- [ ] The Markdown rule checks that new `###` headings have introductory text before sub-sections or code blocks
- [ ] The blanket "not applicable -- skip Markdown files" exclusion is removed
- [ ] Markdown files with new headings that lack introductory text produce WARN verdict
- [ ] Markdown files with new headings that have introductory text produce PASS verdict

## Review Context
**Comment ID:** 50001
**Reviewer:** reviewer-b
**File:** plugins/sdlc-workflow/skills/verify-pr/style-conventions.md, line 310
**Comment:** "The Check 6 description says 'Markdown: not applicable -- skip Markdown files' but this is a documentation-heavy repository where skills are defined in Markdown. The check should still verify that new Markdown sections have introductory text explaining their purpose, even if traditional doc comments don't apply. Consider adding a Markdown-specific rule that checks whether new `###` headings have at least one paragraph of explanatory text before any sub-sections or code blocks."

## Target PR
https://github.com/mrizzi/sdlc-plugins/pull/747
