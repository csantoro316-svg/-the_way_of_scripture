# Interior Pages No Right Sidebar Cards

Date: 2026-06-29
Scope: website, documentation

## Summary

- Removed right-side sidebar/card panels from generated study pages.
- Removed right-side sidebar/card panels from generated passage pages.
- Collapsed interior reading layouts to a single full-width content column.
- Updated `documentation/architecture/WEBSITE_STYLE_STANDARD.md` to forbid right-side cards and narrow main-content columns on interior pages.

## Why

- The right-side cards were cluttering the reading experience and artificially narrowing the main content area.
- Interior pages should prioritize long-form readability over secondary utility panels.
- The homepage had already moved away from this pattern, and the same rule now applies repo-wide.

## Notes

- Supporting navigation or related-content material should be integrated into the main content flow or a lower full-width section if needed later.
