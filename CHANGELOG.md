# Changelog

All notable changes to the sdlc-workflow plugin are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.7.0] - 2026-04-22

### Added

- `run-evals` skill for running skill evals with deterministic output layout and CI-compatible results
- `eval-pr` GitHub Actions workflow for PR-triggered eval comparisons against baselines
- `eval-baseline` GitHub Actions workflow for push-to-main baseline generation
- Plan-feature eval fixtures with cross-skill handoff contract validation assertions
- Feedback.json tracking in eval baselines for human review

### Changed

- Added convention gap task structuring guidance to verify-pr Step 5b
- Moved eval fixtures outside plugin distribution path

### Fixed

- Replaced dangerously-skip-permissions with dontAsk mode in eval workflows
- Various eval CI fixes (Vertex AI auth, plugin installation, verbose output, prompt qualification)

### Documentation

- Added skill evaluation framework design spec
- Added eval usage guide for plan-feature
- Added eval skills CI workflow design spec
- Added eval fixture annotation conventions

## [0.6.1] - 2026-04-14

### Fixed

- Fixed script execution context for jira-client.py — all examples now `cd` to plugin root before running the script, since it lives in the plugin cache, not the working directory

## [0.6.0] - 2026-04-14

### Changed

- Added test doc comment check to verify-pr Step 12
- Added REST API v3 fallback for Jira when MCP is unavailable
- Updated Jira client description format
- Added .env file support for credential management
- Refactored Jira client to accept args directly instead of using subprocess

### Fixed

- Handle code blocks with blank lines and validate JSON input in Jira client

### Documentation

- Added CONVENTIONS.md to document project coding standards

Thanks to @mrrajan for his contributions to this release!

## [0.5.11] - 2026-04-08

### Changed

- Added CONVENTIONS.md CI check verification to implement-task Step 9
- Added test documentation guidance with given-when-then structure to implement-task
- Added test quality check for repetitive test functions to verify-pr
- Added parameterized test preference guidance to implement-task
- Added untracked file check to implement-task self-verification

## [0.5.10] - 2026-04-03

### Changed

- Added example consistency check to implement-task self-verification
- Added display text vs API value comparison guidance for Figma analysis in plan-feature
- Added data component rendering scope extraction from Figma context hierarchy in plan-feature
- Added list endpoint sort order verification to implement-task cross-repo API checks

### Fixed

- Corrected inconsistent example mapping in plan-feature display text comparison

## [0.5.9] - 2026-04-03

### Changed

- Added custom sub-component visual spec extraction guidance to plan-feature

## [0.5.8] - 2026-04-02

### Changed

- Added cross-module shared entity analysis to implement-task sibling parity
- Added cross-repo API contract verification for manual REST calls

## [0.5.7] - 2026-04-01

### Changed

- Added method-vs-fact secondary test to verify-pr root-cause universality gate
- Added code quality and test assertion guidance to implement-task

Thanks to @ruromero for his contributions to this release!

## [0.5.6] - 2026-04-01

### Changed

- Added caller-site parity check to implement-task sibling parity analysis
- Updated verify-pr workflow diagram with root-cause task

## [0.5.5] - 2026-03-27

### Changed

- Extended verify-pr CI status step with failure analysis, fix sub-task creation, and root-cause investigation integration

## [0.5.4] - 2026-03-27

### Changed

- Added universality-test classification gate to verify-pr root-cause investigation, preventing skill drift from repo-specific patterns
- Added test convention analysis to implement-task Step 4, discovering sibling test patterns for use during test writing

## [0.5.3] - 2026-03-27

### Changed

- Enforced mandatory thread enumeration on every verify-pr run to prevent missed review comments
- Used structured task description template for root-cause tasks in verify-pr, with analysis posted as Jira comment
- Added convention-aware task enrichment to plan-feature Step 5

### Fixed

- Prefixed classification markers with skill name to avoid false positives from human reviewers

## [0.5.2] - 2026-03-26

### Changed

- Added convention check before classifying review feedback in verify-pr
- Reply to all review comments and use per-run GitHub comments in verify-pr

## [0.5.1] - 2026-03-26

### Changed

- Added review feedback resolution and full-chain root-cause investigation to verify-pr
- Added contract and sibling parity self-verification check to implement-task

### Documentation

- Added missing define-feature skill to README

## [0.5.0] - 2026-03-25

### Added

- `define-feature` skill for interactive Feature creation with guided template walkthrough

## [0.4.5] - 2026-03-25

### Changed

- Added data-flow trace self-verification check to implement-task

## [0.4.4] - 2026-03-25

### Changed

- Added convention conformance analysis guardrail to implement-task

### Fixed

- Used gh pr comment --edit-last for idempotent report posting in verify-pr
- Added --jq to commit traceability and CI refresh for revised reports in verify-pr

## [0.4.3] - 2026-03-24

### Changed

- Added conditional PR branch checkout to verify-pr skill
- Added systematic duplication-risk scan and Reuse Candidates section to plan-feature

### Fixed

- Replaced invalid --stat flag with gh api for diff size check in verify-pr

### Documentation

- Updated README with all four skills, complete doc index, and setup step
- Added Mermaid diagram, expanded Verify Phase, and restructured Setup in workflow docs

## [0.4.2] - 2026-03-23

### Changed

- Added documentation-impact evaluation to planning and implementation skills
- Enforced DRY principle across planning and implementation skills
- Added GitHub Issue custom field to setup skill and project configuration
- Added GitHub issue Closes reference to PR description
- Added Markdown link for Jira issue in PR description

## [0.4.1] - 2026-03-23

### Fixed

- Use inlineCard ADF node for Git Pull Request custom field

## [0.4.0] - 2026-03-20

### Added

- `verify-pr` skill for PR verification against Jira tasks

### Changed

- Added CONVENTIONS.md fill-in prompt to setup skill

### Fixed

- Added markdown footnote to verify-pr GitHub PR comment

### Documentation

- Added version bump decision guide with y-stream vs z-stream criteria

## [0.3.2] - 2026-03-20

### Changed

- Enhanced comment footer with plugin link, skill name, and version
- Added loop detection guidance to implement-task skill
- Added CONVENTIONS.md lookup to plan-feature, implement-task, and setup skills

### Documentation

- Added GitHub release creation step to releasing guide

## [0.3.1] - 2026-03-20

### Changed

- Enhanced `/setup` skill to ship a `constraints.md` template
- Enhanced `/plan-feature` with constraint-aware task generation
- Clarified PR link fallback in `/implement-task` when custom field is not configured

### Documentation

- Added workflow, tools, and conventions documentation
- Added documentation table of contents to CLAUDE.md
- Added PR description format to conventions-spec
- Added release process and changelog entries for v0.2.0 and v0.2.2

## [0.3.0] - 2025-03-20

### Added

- `/setup` skill for project configuration validation
- Project config template and reference documentation

### Changed

- Bumped version to 0.3.0

## [0.2.4] - 2025-03-19

### Added

- Self-verification step in implement-task before commit
- Verification Commands section in plan-feature task template
- Metrics definitions for AI-assisted SDLC workflow
- Architectural constraints document

## [0.2.3] - 2025-03-18

### Added

- Assign-to-me on task start in implement-task

### Fixed

- Removed hardcoded Git Pull Request custom field ID from implement-task

## [0.2.2] - 2025-03-17

### Added

- GitHub Actions workflow for plugin validation
- CLAUDE.md with version sync instructions

### Fixed

- Added version and author fields to plugin manifest
- Updated Git Pull Request custom field ID to customfield_10875
- Removed smoke-test job that requires authentication
- Fixed version reference and marketplace add command in README
- Removed invalid skills array from plugin manifest

## [0.2.1] - 2025-03-17

### Fixed

- Added missing description field to skill entries

## [0.2.0] - 2025-03-16

### Changed

- Genericized skill files to use project configuration contract references

## [0.1.0] - 2025-03-16

### Added

- Initial release of the sdlc-workflow plugin
- `plan-feature` skill — generate implementation plans and Jira tasks from a feature
- `implement-task` skill — implement Jira tasks with structured descriptions
- Plugin marketplace repository structure
- Project configuration contract documentation
- SDLC methodology documentation
- README with installation guide
