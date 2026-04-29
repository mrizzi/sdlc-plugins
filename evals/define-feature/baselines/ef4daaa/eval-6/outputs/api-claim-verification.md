# External API Claim Verification

## Claim Detected

**Section:** Requirements (Section 4)

**Claim:** "PR reviews cannot be updated after initial submission so always create a new review" / "The GitHub API does not support modifying a submitted review"

**Classification:** Assertion that an external API (GitHub REST API) lacks a specific capability (updating/modifying submitted PR reviews).

## Verification Result

**Status:** UNVERIFIED -- web tools unavailable

Verification could not be performed because WebSearch and WebFetch are unavailable in the current environment. The claim was detected but could NOT be verified against official GitHub API documentation.

### Fallback Action

The following message was presented to the user:

> I detected a claim about an external API but cannot verify it right now
> (web tools unavailable). The claim is: **"PR reviews cannot be updated after initial submission / The GitHub API does not support modifying a submitted review."** Would you like to proceed as-is, or verify it manually before continuing?

Since verification was not possible, the original claim wording has been retained in the Feature description as provided by the user. The user should independently verify this claim against the [GitHub REST API documentation for pull request reviews](https://docs.github.com/en/rest/pulls/reviews) before implementation begins.

### Note

This claim may be incorrect. The GitHub REST API does provide a `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}` endpoint that can update a review. The user is advised to verify manually.
