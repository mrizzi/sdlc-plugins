# Sub-task: Add Markdown-specific documentation coverage rule to Check 6

## Repository
sdlc-plugins

## Target Branch
main

## Description
Add a Markdown-specific documentation coverage rule to Check 6 in the style-conventions sub-agent. Currently, Check 6 skips Markdown files entirely ("Markdown: not applicable -- skip Markdown files"), but this repository is documentation-heavy with skills defined in Markdown. The check should verify that new Markdown sections (headings) have introductory explanatory text.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` -- update Check 6's language-specific conventions to add a Markdown rule that checks whether new `###` headings have at least one paragraph of explanatory text before any sub-sections or code blocks

## Implementation Notes
- Replace the current "Markdown: not applicable -- skip Markdown files" entry in Check 6b with a Markdown-specific rule
- The Markdown rule should check whether new `###` (or deeper) headings introduced in the PR diff have at least one paragraph of explanatory text before any sub-sections or code blocks
- Follow the structure of the existing language-specific convention entries in Check 6b
- The rule should work on the PR diff context, identifying new headings by `+` prefix lines

## Acceptance Criteria
- [ ] Check 6b includes a Markdown-specific documentation rule instead of "not applicable"
- [ ] The Markdown rule checks that new headings have at least one paragraph of explanatory text before sub-sections or code blocks
- [ ] The rule applies to `###` and deeper headings in Markdown files
- [ ] Existing non-Markdown language conventions remain unchanged

## Review Context
Reviewer reviewer-b (CHANGES_REQUESTED) commented on `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` line 310:

> The Check 6 description says 'Markdown: not applicable -- skip Markdown files' but this is a documentation-heavy repository where skills are defined in Markdown. The check should still verify that new Markdown sections have introductory text explaining their purpose, even if traditional doc comments don't apply. Consider adding a Markdown-specific rule that checks whether new `###` headings have at least one paragraph of explanatory text before any sub-sections or code blocks.

## Target PR
https://github.com/mrizzi/sdlc-plugins/pull/747
