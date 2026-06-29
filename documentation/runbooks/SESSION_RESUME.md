# Session Resume

Updated: 2026-06-28

## Canonical Resume Document

Use this file as a stable operational baseline for repository work.
Session continuity should come from change docs.

## Current State

Repository:
- `the_way_of_scripture`

Primary scopes:
- repo docs: `documentation/`
- website app: `apps/web/`
- content source: `content/`

Current repo connections:
- GitHub remote for this repo uses the dedicated `csantoro316-svg` SSH identity
- Firebase project for this repo is `the-way-of-scripture`
- Firebase default hosting URL is `https://the-way-of-scripture.web.app`
- custom apex domain setup for `thewayofscripture.com` is in progress

Current implemented website surfaces:
- homepage: `apps/web/index.html`
- featured studies landing: `apps/web/library/index.html`
- featured passages landing: `apps/web/library/passages.html`
- shared browse page: `apps/web/library/browse.html`

Current content-navigation model:
- top nav uses `Home`, `Studies`, and `Passages`
- `Studies` opens the featured studies landing
- `Passages` opens the featured passages landing
- exhaustive browsing happens through the shared browse page
- `Browse all studies` routes to `browse.html?type=studies`
- `Browse all passages` routes to `browse.html?type=passages`

Latest navigation correction:
- the Memory Genie-style left navigation belongs only on the dedicated shared browse page
- featured landing pages should remain curated and should not use the browse-page left rail

Latest verification:
- `python3 -m py_compile tools/generate_study_pages.py`
- `python3 tools/generate_study_pages.py`
- `firebase deploy --only hosting`

## Quick Validation Checklist

1. Check the latest relevant change docs.
2. Confirm the target scope for the session: repo, content, or website.
3. Verify any implementation or content assumptions before changing structure.
4. Capture follow-up items in a change doc if behavior or workflow changed.

## If You Want Codex To Resume Fast

In next session, say:
- "Open `documentation/runbooks/SESSION_RESUME.md` and continue."
