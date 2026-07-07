# Library Navigation Standard

Updated: 2026-07-06

## Purpose

This document defines the long-term navigation model for browsing content in `the_way_of_scripture`.

The goal is to keep one central navigation surface for the site's study library while still preserving the distinction between studies and passages.

## Core Rule

Browsing should happen through one shared library navigation system, not through two unrelated navigation experiences.

Content types remain distinct:

- studies
- passages

But navigation should feel unified.

## Library Model

The site should eventually provide a central library surface that allows the reader to browse:

- studies
- passages

Different entry points may default to different views, but they should still land inside the same library system.

Examples:

- a `Studies` link opens the featured studies landing
- a `Passages` link opens the featured passages landing
- `Browse all studies` opens the shared browse page with the studies view active
- `Browse all passages` opens the shared browse page with the passages view active

The shared library system should use a Memory Genie-style left-side navigation layout on the dedicated browse page, not on the featured landing pages.

## Study Navigation Standard

Studies should be browsable through:

- featured studies
- all studies
- later, optional alphabetical browsing if the corpus grows large enough

Current featured-studies landing rule:

- the main studies-facing library landing page should surface up to 6 featured studies at a time
- the exhaustive study list should live in a separate `Browse All Studies` view
- the featured studies section should include a right-justified `Browse all studies` link on the heading row and retain the browse link at the bottom of the section
- the featured studies landing page remains a curated landing page rather than the main browse/navigation surface

The study landing area may be curated rather than exhaustive.

This means:

- homepage does not need to list all studies
- study landing pages may emphasize selected or featured studies
- exhaustive study browsing should still be available from the library

## Passage Navigation Standard

Passages should not primarily be browsed as one flat alphabetical list.

Passages should be grouped by biblical book.

The main passages-facing landing page should be a featured-passages view, not the by-book view directly.

Current featured-passages landing rule:

- the main passages-facing library landing page should surface 12 featured passages at a time
- the exhaustive passage browse mode should live in a separate `Browse All Passages` view
- the featured passages section should include a right-justified `Browse all passages` link on the heading row and retain the browse link at the bottom of the section
- the featured passages landing page remains a curated landing page rather than the main browse/navigation surface

The expected navigation pattern is:

- book-level sections
- expand a book to reveal the passages currently available within it

This keeps passage browsing aligned with how readers naturally think about Scripture references.

## Expand / Collapse Behavior

The passage navigation surface should support:

- expand individual books
- collapse individual books
- expand all
- collapse all

This behavior should work similarly to the existing Memory Genie knowledge-base browsing pattern where grouped navigation can be opened and closed in bulk.

## Recommended Library Structure

The long-term library should support at least these browse modes:

- `Studies`
- `Passages`

Within those:

- `Studies`
  - featured
  - all studies

- `Passages`
  - featured
  - by book

Additional browse modes may be added later if useful, but this is the current baseline.

## Routing Principle

There should be one clear navigation home for the content library, even if internal views differ.

That means:

- studies and passages may still have separate generated content pages
- but library navigation should have one conceptual home
- entry links should default readers into the appropriate view rather than forcing separate systems

## Layout Rule

The content library should use two distinct page types:

- featured landing pages for `Studies` and `Passages`
- one shared browse page for exhaustive navigation

The shared browse page should follow this layout pattern:

- a consistent site-level top navigation with `Home`, `Studies`, and `Passages`
- one static page-level heading area anchored by the `Browse Library` title
- a left-side navigation panel modeled on the Memory Genie knowledge-base page
- grouped, collapsible navigation with `Expand All` and `Collapse All`
- a main content panel showing the selected study or passage

### Passage Guide Placement

The passage-structure explainer belongs to the shared browse page, not to individual passage content.

Current rule:

- when the shared browse page is in `Passages` mode, show one static page-level guide under the main `Browse Library` header
- do not repeat that explainer inside the selected passage article pane
- do not repeat that explainer on standalone generated passage pages

The guide is a browsing aid, not passage body content.

### Scroll Behavior Rule

The shared browse page must avoid stacked independent scroll regions.

Current rule:

- use one primary page scrollbar for the browse experience
- do not give both the navigation pane and the content pane their own persistent interior scrollbars on desktop
- if the navigation and content columns are visually anchored, prefer sticky positioning without nested `overflow-y: auto` regions

The goal is to keep the selected content in view while preserving a cleaner, single-scroll interaction model.

The featured landing pages should stay simpler:

- no browse-side navigation rail
- curated cards only
- heading-row browse links right-justified and high-contrast on dark backgrounds

## Documentation Expectation

If the library navigation model changes in a durable way, update:

- `documentation/architecture/LIBRARY_NAVIGATION_STANDARD.md`
