# Website Style Standard

Updated: 2026-10-18

## Purpose

This document defines the baseline visual and layout standard for `the_way_of_scripture`.

The site is content-first.
Design should support study, Scripture reading, and calm navigation rather than product-style promotion.

## Core Design Direction

The visual tone should be:

- reverent
- calm
- readable
- warm
- serious without feeling sterile

This site should not inherit the visual language of `memory_genie`.
It is not a SaaS landing page and should not feel like one.

## Design Priorities

In order of importance:

1. readability
2. clear study navigation
3. natural Scripture linking
4. restrained visual identity
5. decorative visuals only where they help orientation or tone

## Layout Philosophy

The site should feel closer to a well-structured reading environment than to a marketing page.

Use:

- strong content hierarchy
- generous whitespace
- limited visual noise
- consistent content widths
- predictable heading structure

Avoid:

- overly busy backgrounds
- repeated decorative gradients
- flashy motion
- heavy card clutter
- large blocks of text over images

## Homepage Standard

The homepage may carry more visual identity than interior pages, but it should still remain restrained.

### Banner Use

The homepage banner is appropriate as an early visual masthead after the opening introduction.

Usage rule:

- use the banner as a wide, shallow top visual
- do not depend on it as a text-heavy hero background
- keep overlaid text minimal and only if readability is strong
- prefer placing the main explanatory copy below the banner

The banner should create tone and orientation, not carry the main reading experience.

### Homepage Structure

Homepage order:

1. top navigation
2. opening statement of the site's purpose and the meaning of its name
3. a small text link asking what changes when we go back to the text; it opens the separate site-approach page
4. shallow banner masthead
5. one Foundations invitation linking directly to Study 1, Returning to the Word

The fuller site-focused explanation lives at `apps/web/why-we-return-to-the-text.html`, where it ends with a path into Study 1. The original teaching introduction is now Study 1 of the guided path; its former standalone URL redirects to that study. The Garden and translation-history teaching examples stay in Study 1. Keep one clear start action on the homepage rather than repeating it throughout the page.

## Interior Page Standard

Study pages and passage pages should be more restrained than the homepage.

They should feel:

- book-like
- clean
- stable
- easy to scan

Interior pages should rely on:

- typography
- spacing
- section rhythm
- link clarity

not on decorative visual effects.

### Interior Layout Rule

Interior reading pages should use a single full-width content column within the page's reading surface.

Do not use:

- right-side cards
- right-hand sidebars
- stacked utility panels beside study or passage content
- narrow main content columns created by reserving space for secondary cards

The homepage already moved away from this pattern, and the same rule applies everywhere else on the site.

If supporting navigation or relationship data is needed, integrate it into the main content flow or a lower full-width section rather than a right rail.

The Studies page presents all 14 studies as one ordered path in a single reading column. A secondary Explore by topic view groups the same studies by topic and filters those groups without changing the guided order. Individual study pages show a compact step marker in the hero and previous/continue links below the article body. On narrow screens, those links and topic cards stack vertically. Returning to the Word begins the path, The Berean Standard follows, and The Angel of the Lord follows the Gospel as Step 6.

Content panels should use the full available reading width so long-form explanations and Scripture discussion are not artificially cramped.

### Passage Reader

The canonical Passages page uses a full-width reading column on desktop and mobile. The passage/article surface stays in normal page flow: every page scroll must move its content immediately. A tall navigation menu must never determine the reader's scroll length or hold the passage in place.

Only the compact reading toolbar is sticky. It contains Book, Chapter, and Passage selectors for available library passages plus a Browse Library button. Selected headings must land below the toolbar, including after responsive resizing. Previous/next links remain at the end of the passage.

The complete navigation tree opens in a modal drawer at every screen size. While open, the drawer scrolls independently and the background page is locked; closing or selecting a destination restores normal page scrolling. Keep an accessible Close button visible, support Escape/backdrop dismissal, contain keyboard focus in the drawer, and return focus to the opener on dismissal or the selected heading on navigation. Expanding the complete menu must not increase the reading page's height.

The passage-section guide appears once above the reader as a collapsed “About these sections” disclosure. The Passages navigation link opens this reader directly.

This replaces the earlier shared-browse layout with two sticky columns, which could keep a passage stationary while a longer menu scrolled past it.

### Full-Width Card Rule

Every card-like surface on the site must let its content use the full available inner width of that card.

This applies to:

- homepage intro cards
- study and passage cards
- study and passage hero cards
- study body panels
- feedback panels
- library browse panels

Do not:

- leave inherited text-width limits inside cards
- allow paragraphs or headings inside cards to remain artificially narrow when the card itself is full width
- create card layouts that visually clip or underuse the horizontal space available for long-form copy

## Color Direction

Preferred palette direction:

- warm neutrals
- parchment or stone-adjacent backgrounds
- dark readable text
- muted accent colors

The palette should support long-form reading.

Avoid:

- bright app-style gradients across the whole site
- overly saturated modern marketing colors
- high-contrast decorative effects that compete with Scripture text

### Dark-Surface Contrast Rule

When text is placed directly on the darker site background rather than inside a light reading panel, it must switch to a light high-contrast treatment.

This applies especially to:

- section headings placed outside cards or panels
- browse links placed directly on the dark page background
- library/navigation labels that sit on the page background rather than within a light surface

Do not rely on the default dark body text color for content sitting directly on dark backgrounds.

## Typography Direction

Typography should feel intentional and readable.

General guidance:

- use a strong, readable serif or serif-forward direction for major reading content
- use a clean supporting font for navigation and utility text when needed
- preserve comfortable line length for study content
- prioritize hierarchy and reading rhythm over novelty

Study content should feel like it was designed to be read slowly and carefully.

## Icon Use

The current icon may be used strategically for brand support.

Recommended usage:

- header branding
- homepage supporting brand mark
- social/share usage if appropriate

Do not assume the current icon is automatically suitable as a favicon at very small sizes.
If favicon quality becomes important, create a simplified icon specifically for small-scale use.

## Imagery Standard

Images should be used sparingly.

Use imagery to:

- establish tone on the homepage
- support brand identity
- occasionally reinforce major content sections

Do not let imagery crowd the reading experience.

## Motion Standard

Motion should be minimal and purposeful.

Allowed uses:

- subtle load-in transitions
- small hover/focus feedback
- restrained section reveals when helpful

Avoid:

- frequent animated effects
- decorative motion for its own sake
- anything that makes study pages feel busy

## Content-First Rule

When a design choice conflicts with reading clarity or Scripture navigation, prioritize the content.

This applies especially to:

- study body text
- passage comparison blocks
- inline Scripture links
- backlink navigation between studies and passages

## Documentation Expectation

If the visual direction changes in a durable way, update:

- `documentation/architecture/WEBSITE_STYLE_STANDARD.md`
