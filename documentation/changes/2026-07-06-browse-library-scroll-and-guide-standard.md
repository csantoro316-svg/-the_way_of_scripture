# Browse Library Scroll And Guide Standard

Date: 2026-07-06

## What Changed

- Moved the passage-page structure explainer out of individual passage pages and out of per-passage article rendering inside the shared browse view.
- Placed that explainer on the shared browse page as a static page-level note shown only when the active content type is `Passages`.
- Removed nested scroll behavior from the shared browse layout by dropping independent scrolling from the left navigation pane and right content pane.
- Kept the browse columns anchored through sticky positioning while returning overall scrolling to the page itself.

## Why

- The passage-structure explainer is a browse-system aid, not passage content.
- Repeating it inside each passage wastes vertical space and weakens the actual passage reading experience.
- Three separate scrollbars on one browse screen created poor navigation ergonomics and visual clutter.
- The intended behavior is that the browse content remains visually anchored while the page uses one primary scrollbar.

## Current Rule

- The shared browse page at `apps/web/library/browse.html` owns the passage-structure explainer.
- The explainer appears once near the top of the page under the `Browse Library` header when `Passages` is active.
- Individual passage pages must not repeat that explainer.
- Per-passage article rendering inside the browse page must not repeat that explainer.
- The shared browse layout should use one page scrollbar, not nested scrolling inside both navigation and content panes.

## Files Touched

- `tools/generate_study_pages.py`
- `apps/web/styles.css`
- generated:
  - `apps/web/library/browse.html`
  - `apps/web/library/passages.html`
  - `apps/web/passages/*.html`

## Verification

- `python3 tools/generate_study_pages.py`
- `firebase deploy`
