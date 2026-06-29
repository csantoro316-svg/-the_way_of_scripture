# Website Style Standard

Updated: 2026-06-29

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

The homepage banner is appropriate as a top-of-page visual masthead.

Usage rule:

- use the banner as a wide, shallow top visual
- do not depend on it as a text-heavy hero background
- keep overlaid text minimal and only if readability is strong
- prefer placing the main explanatory copy below the banner

The banner should create tone and orientation, not carry the main reading experience.

### Homepage Structure

Recommended homepage order:

1. top navigation
2. banner masthead
3. short mission/introduction block
4. featured studies
5. featured passages
6. simple explanation of how to use the site

As the site evolves, additional homepage sections may be added, but they should remain content-driven.

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

Content panels should use the full available reading width so long-form explanations and Scripture discussion are not artificially cramped.

### Full-Width Card Rule

Every card-like surface on the site must let its content use the full available inner width of that card.

This applies to:

- homepage intro cards
- featured study and featured passage cards
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
