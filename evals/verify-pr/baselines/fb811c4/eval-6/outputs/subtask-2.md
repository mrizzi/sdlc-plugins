# Sub-Task: Add Markdown-specific documentation rule to Check 6

## Repository
sdlc-plugins

## Target Branch
tc-9106-doc-coverage

## Description
Add a Markdown-specific documentation rule to Check 6 (Documentation Coverage) in the style-conventions sub-agent. Currently Check 6 skips Markdown files entirely, but since this is a documentation-heavy repository where skills are defined in Markdown, the check should verify that new Markdown sections have introductory text explaining their purpose.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` -- update Check 6 section 6b to add a Markdown-specific rule that checks whether new `###` headings have at least one paragraph of explanatory text before any sub-sections or code blocks

## Implementation Notes
- Replace the "Markdown: not applicable -- skip Markdown files" bullet with a Markdown-specific rule
- The rule should check that new `###` headings (identified by `+` prefix in the diff) are followed by at least one paragraph of explanatory text before any sub-sections or code blocks
- Follow the structure of the existing language-specific conventions in section 6b

## Acceptance Criteria
- [ ] Check 6 includes a Markdown-specific rule for verifying new section headings have introductory text
- [ ] The Markdown rule checks for at least one paragraph of explanatory text after new `###` headings
- [ ] The previous "not applicable" handling for Markdown files is replaced with the new rule

## Review Context

**Source:** Review comment 50001 from reviewer-b on `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md`, line 310

**Comment text:**
> The Check 6 description says 'Markdown: not applicable -- skip Markdown files' but this is a documentation-heavy repository where skills are defined in Markdown. The check should still verify that new Markdown sections have introductory text explaining their purpose, even if traditional doc comments don't apply. Consider adding a Markdown-specific rule that checks whether new `###` headings have at least one paragraph of explanatory text before any sub-sections or code blocks.

## Target PR
https://github.com/mrizzi/sdlc-plugins/pull/747
