# External API Claim Verification

## Detected Claim

While processing **Section 4 — Requirements**, the following external API claim was detected:

> **"PR reviews cannot be updated after initial submission so always create a new review — The GitHub API does not support modifying a submitted review"**

This is a claim about the GitHub REST API asserting that PR reviews are immutable after submission and that the API does not support updating or modifying a submitted review.

## Verification Result

**Status: UNVERIFIED** — web tools unavailable; claim cannot be verified at this time.

Verification was attempted using WebSearch and WebFetch to locate the official GitHub REST API documentation for pull request review endpoints. However, both web tools are currently unavailable, so the claim could not be checked against official documentation.

## Fallback Action

Per the define-feature skill's External API Claim Verification fallback path:

> I detected a claim about an external API but cannot verify it right now
> (web tools unavailable). The claim is: **"The GitHub API does not support modifying a submitted review"**. Would you like to proceed as-is, or verify it manually before continuing?

The user was presented with this prompt to decide how to proceed. Since the claim remains unverified, the original wording has been preserved in the Feature description as-is.

## Recommendation

Before implementation, manually verify this claim by checking the GitHub REST API documentation for pull request reviews. Specifically, check whether a `PUT` or `PATCH` endpoint exists for `/repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}` that would allow updating a submitted review.
