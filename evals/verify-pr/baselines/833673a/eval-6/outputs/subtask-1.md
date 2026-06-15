## Repository
sdlc-plugins

## Target Branch
main

## Description
Add a Markdown-specific documentation coverage rule to Check 6 in the style-conventions sub-agent. The current implementation blanket-skips Markdown files, but this repository defines skills in Markdown, making Markdown documentation coverage important. The new rule should verify that new `###` headings in Markdown files have at least one paragraph of explanatory text before any sub-sections or code blocks.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` -- add Markdown-specific documentation rule to Check 6, step 6b

## Implementation Notes
- In Check 6, step 6b, replace the current "Markdown: not applicable -- skip Markdown files" bullet with a Markdown-specific rule
- The new rule should check that new `###` (or deeper) headings introduced in the PR diff have at least one paragraph of explanatory text before any sub-sections or code blocks
- This is consistent with how the repository's skills are structured: each `###` section in skill files contains introductory text explaining its purpose
- Follow the structure of the existing language-specific doc comment patterns (Rust, TypeScript/Java, Python, Go) when adding the Markdown rule

## Acceptance Criteria
- [ ] Check 6 step 6b includes a Markdown-specific rule that checks new `###` headings for introductory explanatory text
- [ ] The Markdown rule replaces the blanket "not applicable -- skip Markdown files" exclusion
- [ ] The rule only applies to new headings introduced in the PR diff (consistent with 6a's "new symbol" detection)

## Review Context
Reviewer reviewer-b (comment #50001, file: plugins/sdlc-workflow/skills/verify-pr/style-conventions.md, line 310):
> "The Check 6 description says 'Markdown: not applicable -- skip Markdown files' but this is a documentation-heavy repository where skills are defined in Markdown. The check should still verify that new Markdown sections have introductory text explaining their purpose, even if traditional doc comments don't apply. Consider adding a Markdown-specific rule that checks whether new `###` headings have at least one paragraph of explanatory text before any sub-sections or code blocks."

## Target PR
https://github.com/mrizzi/sdlc-plugins/pull/747
