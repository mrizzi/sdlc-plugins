## Repository
sdlc-plugins

## Target Branch
main

## Description
Add a Markdown-specific documentation rule to Check 6 (Documentation Coverage) in the style-conventions sub-agent. Currently, Check 6 skips Markdown files entirely with the note "Markdown: not applicable -- skip Markdown files." However, this repository defines skills primarily in Markdown files, so a Markdown-specific rule is needed to verify that new sections have introductory explanatory text.

The rule should check whether new `###` headings introduced in the PR diff have at least one paragraph of explanatory text before any sub-sections or code blocks. This ensures that new skill sections, check definitions, and other Markdown-based documentation are self-explanatory.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` -- update Check 6 step 6b to replace the Markdown "not applicable" rule with a Markdown-specific documentation check for new headings

## Implementation Notes
- In step 6b of Check 6, replace the line "Markdown: not applicable -- skip Markdown files" with a Markdown-specific rule
- The new rule should check whether new `###` (or deeper) headings have at least one paragraph of explanatory text before any sub-sections or code blocks
- Follow the existing pattern of language-specific conventions in step 6b (Rust, TypeScript/Java, Python, Go)
- A "paragraph of explanatory text" means at least one non-empty line of prose text (not a heading, code block fence, or list item) between the heading and any subsequent sub-heading or code block

## Acceptance Criteria
- [ ] Check 6 step 6b includes a Markdown-specific documentation rule
- [ ] The Markdown rule checks that new `###` headings have at least one paragraph of explanatory text before sub-sections or code blocks
- [ ] The Markdown "not applicable" exclusion is removed or replaced with the new rule

## Test Requirements
- [ ] Verify the Markdown rule flags new headings without explanatory text
- [ ] Verify the Markdown rule passes for headings that have introductory paragraphs

## Review Context
**Reviewer:** reviewer-b
**Comment:** "The Check 6 description says 'Markdown: not applicable -- skip Markdown files' but this is a documentation-heavy repository where skills are defined in Markdown. The check should still verify that new Markdown sections have introductory text explaining their purpose, even if traditional doc comments don't apply. Consider adding a Markdown-specific rule that checks whether new `###` headings have at least one paragraph of explanatory text before any sub-sections or code blocks."
**File:** `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md`, line 310

## Target PR
https://github.com/mrizzi/sdlc-plugins/pull/747
