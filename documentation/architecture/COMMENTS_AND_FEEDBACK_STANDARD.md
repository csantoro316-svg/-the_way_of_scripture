# Comments And Feedback Standard

Updated: 2026-06-28

## Purpose

This document defines the baseline policy and system expectations for reader feedback, public comments, and moderation on `the_way_of_scripture`.

The goal is to welcome thoughtful engagement without turning the site into an unmoderated discussion surface.

## Core Posture

The site should communicate that:

- this is a living study and teaching effort
- respectful feedback is welcome
- readers may disagree and still be heard respectfully
- published content may be revised when better understanding or correction warrants it
- all engagement is subject to review for tone, relevance, and appropriateness

## Page-End Note Requirement

Every public study page and passage page should include a standard closing note that communicates:

- the work is ongoing
- feedback is welcome
- submissions may be reviewed before public display
- content may change in response to correction, clarification, or further study

This is a required recurring content component, not an optional extra.

## Public Comment Policy

Comments should not publish automatically.

Initial moderation rule:

- all public comments are submitted for approval
- approval happens before a comment appears on the site

The site should say this clearly so readers understand:

- comments are moderated
- inappropriate submissions will not be published
- respectful disagreement is allowed
- publication is not guaranteed

## Feedback Intake Channels

The long-term structure should support two distinct feedback paths:

1. public comments attached to a study or passage page
2. direct private feedback through a site email/contact path

These serve different purposes:

- comments are public-facing and page-specific
- direct feedback may be private, longer-form, or administrative

## Moderation Standard

Moderation should evaluate at least:

- appropriateness
- relevance to the page
- clarity
- respectful tone
- spam or abusive content risk

Respectful disagreement should not be rejected merely because it differs from the site's position.

## Revision Standard

The site should remain open to revising published content when feedback or further study reveals a better understanding.

When a material interpretation changes:

- update the published page
- preserve the improved position in the current content
- document meaningful site-behavior or workflow changes in `documentation/changes/` when appropriate

The site is not required to preserve every historical draft publicly, but it should maintain an honest posture about growth and correction.

## Initial System Shape

The implementation should eventually support:

- page-level comment submission
- pending moderation state
- human approval before publication
- an email notification path for new submissions

Initial human workflow:

1. reader submits comment or feedback
2. submission is held in pending state
3. notification is sent to the site owner
4. owner reviews and approves, rejects, or ignores
5. approved comments become public

## Future AI Review Path

AI-assisted review may be added later, but it should be treated as a support layer rather than the initial source of authority.

Planned direction:

- AI may help triage or summarize incoming feedback
- human approval remains the publishing gate unless the policy is explicitly changed later

## Email Integration Expectation

The future implementation should be designed so new feedback can notify the site owner through email.

This is especially important before any richer admin tooling exists.

The email path should support:

- awareness of new submissions
- page identification
- submission content review
- approval workflow support

## Documentation Expectation

If the feedback policy or moderation workflow changes in a durable way, update:

- `documentation/architecture/COMMENTS_AND_FEEDBACK_STANDARD.md`
