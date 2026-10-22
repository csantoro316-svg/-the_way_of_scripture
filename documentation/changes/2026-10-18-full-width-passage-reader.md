# Full-Width Passage Reader

Date: 2026-10-18
Host: CozPlex
Project: `the-way-of-scripture`
Scope: shared Browse Library layout and navigation

## Problem

The earlier layout made both browse columns sticky. On the live Genesis 10 page, the 3,936 px navigation tree kept the shorter passage pinned at 16 px from the viewport top through the first 1,000 px of scrolling. Removing independent scrollbars had not fixed that reading behavior.

The owner approved a full-width reader with compact passage selectors and an on-demand navigation drawer. This supersedes the two-sticky-column guidance recorded on 2026-07-06.

## Changes

- Removed the persistent sidebar and sticky passage. The article now occupies the full reading width and scrolls normally with the page.
- Added a sticky toolbar with Book, Chapter, and Passage selectors populated from existing library records. It stays synchronized with drawer selections, search results, URL restoration, and previous/next navigation, including cross-chapter ranges.
- Moved the complete navigation tree into a native modal dialog at every screen size. It scrolls independently while open, locks background scrolling, contains focus, and supports Close, Escape, backdrop dismissal, and selection. Dismissal returns focus to Browse Library; selection focuses the heading below the toolbar.
- Collapsed the section explainer into an About these sections disclosure above the reader.
- Preserved study browsing in the shared drawer, including alphabetical/topic views. Made search results keyboard-activatable buttons.
- Updated the generator template, generated browse page, shared styles, content/style standards, and resume instructions. Used the navigation-only refresh to preserve existing content.

## Verification

- Both active-host certificate checks passed on CozPlex: the project read returned exactly `the-way-of-scripture`, and Firebase app-list succeeded with an empty list.
- Repository checks passed with 0 errors and the existing 401 passage warnings.
- Browser checks confirmed immediate article movement at widths 320, 390, 640, 768, 900, 920, 960, and 1440 px, with no horizontal overflow. Expanding the complete menu left the reading page height unchanged at every width.
- Actual mouse-wheel input over the desktop passage moved its content with every scroll through the lower portion of the passage. Wheel input over the open, fully expanded drawer scrolled only the drawer.
- An actual mobile touch swipe moved the article immediately, and mobile selection positioned and focused the heading below the sticky controls.
- Actual Escape, Shift+Tab, backdrop click, and keyboard Enter checks covered dismissal, focus containment/return, background scroll restoration, and search result activation. The focus-return issue found during testing was corrected before release.
- All 970 passages were reachable with synchronized Book/Chapter/Passage controls. Direct selector changes, cross-chapter John 7:53–8:11 → John 8:58 navigation, drawer filtering/selection, URL restoration, guide disclosure, and study alphabetical/topic browsing were checked.
- SHA-256 comparison confirmed all 2,030 protected website and content files remained identical to their state after the preceding navigation/Prayer and Faith release. Only browse HTML and shared CSS changed in the served files for this layout update.
- Desktop/mobile screenshots were inspected; `git diff --check` passed.

## Deployment

Both the Hosting dry run and live deployment succeeded through CozPlex's certificate wrapper with the explicit `the-way-of-scripture` project. Firebase released the version successfully, uploading only the two changed served files out of 1,045 total files:

```bash
~/.local/bin/mg-cloud-firebase deploy --only hosting --project the-way-of-scripture --dry-run
~/.local/bin/mg-cloud-firebase deploy --only hosting --project the-way-of-scripture
```

Live browse HTML, CSS, the library index, Prayer and Faith, and a representative standalone passage matched local files byte for byte. The actual wheel, drawer, Escape/focus, Shift+Tab, backdrop, Enter/search, and mobile touch checks also passed on the live reader after a cache-bypassing reload. An existing browser session initially retained the previous HTML/CSS from cache; returning readers may need a hard refresh to load the new layout.

## Remaining Work

Existing generator translation debt and passage source warnings remain separate follow-up work. The Prayer and Faith revision and all existing passage content were preserved.
