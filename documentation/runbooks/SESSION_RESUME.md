# Session Resume

Updated: 2026-06-29

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
- studies archive landing: `apps/web/library/studies-all.html`
- passages by book landing: `apps/web/library/passages-by-book.html`
- generated study pages: `apps/web/studies/*.html`
- generated passage pages: `apps/web/passages/*.html`

Current content-navigation model:
- top nav uses `Home`, `Studies`, and `Passages`
- `Studies` opens the featured studies landing
- `Passages` opens the featured passages landing
- exhaustive browsing happens through the shared browse page
- `Browse all studies` routes to `browse.html?type=studies`
- `Browse all passages` routes to `browse.html?type=passages`
- generated study and passage relationships are also materialized in `apps/web/assets/library_index.json`

Latest navigation correction:
- the Memory Genie-style left navigation belongs only on the dedicated shared browse page
- featured landing pages should remain curated and should not use the browse-page left rail

Current content execution baseline:
- source study material lives in `content/studies/`
- `tools/generate_study_pages.py` generates study pages, passage pages, and library relationship data
- study hero intros and library study-card copy should stay aligned without repeating the same intro again in the study body
- passage pages should place full default translation text in the top `Passage` section, treat `Context` as Scripture context, and link supporting passage references in new tabs

Current interior layout baseline:
- study and passage reading pages should use a single full-width content column
- right-side cards and right rails are not part of the current interior page standard

Latest verification:
- `python3 -m py_compile tools/generate_study_pages.py`
- `python3 tools/generate_study_pages.py`
- `firebase deploy --only hosting`

Latest change docs to review first:
- `documentation/changes/2026-06-29-study-content-generation-and-deployment-refresh.md`
- `documentation/changes/2026-06-29-passage-page-scripture-context-standardization.md`
- `documentation/changes/2026-06-29-interior-pages-no-right-sidebar-cards.md`

## Quick Validation Checklist

1. Check the latest relevant change docs.
2. Confirm the target scope for the session: repo, content, or website.
3. Verify any implementation or content assumptions before changing structure.
4. Capture follow-up items in a change doc if behavior or workflow changed.

## If You Want Codex To Resume Fast

In next session, say:
- "Open `documentation/runbooks/SESSION_RESUME.md` and continue."
