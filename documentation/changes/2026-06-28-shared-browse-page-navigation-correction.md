# Shared Browse Page Navigation Correction

Date: 2026-06-28
Scope: website

## Summary

- Corrected the library navigation model after an initial misread of the intended layout.
- Restored the featured studies and featured passages pages as curated landing pages without a left-side browse rail.
- Added a dedicated shared browse page at `apps/web/library/browse.html`.
- Routed:
  - `Browse all studies` to `apps/web/library/browse.html?type=studies`
  - `Browse all passages` to `apps/web/library/browse.html?type=passages`
- Updated `apps/web/library/studies-all.html` and `apps/web/library/passages-by-book.html` to redirect into the shared browse page.
- Added generated browse data at `apps/web/assets/library_index.json`.
- Updated the generator and navigation documentation to reflect the corrected model.

## Why

- The intended behavior was to keep featured landing pages simple and curated.
- The Memory Genie-style navigation pattern was supposed to apply to a separate browse page, not to the featured landing pages themselves.
- A dedicated browse page keeps the curated entry surfaces intact while still giving the site one scalable navigation system for larger content sets.

## Verification

- `python3 -m py_compile tools/generate_study_pages.py`
- `python3 tools/generate_study_pages.py`

## Notes

- The shared browse page currently supports:
  - study browsing grouped A-Z
  - passage browsing grouped by biblical book
  - expand all / collapse all
  - search within the active content type
- Further visual or interaction tuning can now be done against one dedicated browse surface instead of reworking the featured landing pages.
