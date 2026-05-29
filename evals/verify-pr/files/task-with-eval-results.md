<!-- SYNTHETIC TEST DATA — names, URLs, and identifiers are fictional -->

# Jira Task: TC-9106

**Key**: TC-9106
**Summary**: Add documentation coverage check to style-conventions sub-agent
**Status**: In Review
**Labels**: ai-generated-jira
**PR URL**: https://github.com/mrizzi/sdlc-plugins/pull/747
**Web URL**: https://redhat.atlassian.net/browse/TC-9106
**Parent Feature**: TC-9100

---

## Repository
sdlc-plugins

## Target Branch
main

## Description
Add a Documentation Coverage check (Check 6) to the Style/Conventions sub-agent in verify-pr. This check verifies that new public symbols introduced in a PR have documentation comments, using the language's standard doc comment convention. The check produces a verdict (PASS/WARN/N/A) that feeds into the Style/Conventions output.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` — add Check 6 (Documentation Coverage) after Check 5, update Output Format to include sixth verdict row
- `plugins/sdlc-workflow/skills/verify-pr/SKILL.md` — update Step 6a verdict mapping to include Documentation Coverage in the combined Style/Conventions verdict

## Implementation Notes
- Follow the structure of existing Checks 1-5 in style-conventions.md for the new Check 6
- Check 6 should scan the PR diff for new function/method/struct/class definitions and verify each has a documentation comment
- Use language-specific doc comment patterns: `///` for Rust, `/** */` for Java/TypeScript, `"""` for Python, `//` for Go
- The verdict is PASS when all new symbols have doc comments, WARN when any are missing, N/A when no new symbols are introduced

## Acceptance Criteria
- [ ] Check 6 scans the PR diff for new public symbol definitions
- [ ] Check 6 verifies each new symbol has a documentation comment using the language's convention
- [ ] Check 6 produces PASS when all new symbols are documented
- [ ] Check 6 produces WARN when any new symbol lacks documentation
- [ ] Check 6 produces N/A when no new symbols are introduced in the PR
- [ ] The Output Format includes a sixth verdict row for Documentation Coverage
- [ ] Step 6a verdict mapping includes Documentation Coverage

## Test Requirements
- [ ] Verify Check 6 correctly identifies undocumented new symbols in a diff
- [ ] Verify Check 6 does not flag symbols that already have doc comments
- [ ] Verify N/A verdict when no new symbols are present
