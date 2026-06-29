# Content Execution Standard

Updated: 2026-06-28

## Purpose

This document defines how source content becomes website pages for `the_way_of_scripture`.

The site is content-first.
The primary workflow is:

1. source study material is provided
2. study content is turned into a study page
3. referenced Scripture passages become linked passage pages
4. passage pages support the study pages and link back to them
5. study pages and passage pages remain reciprocally connected as the content graph grows

## Core Model

There are two primary public content surfaces:

- study pages
- passage pages

Study pages are the main teaching surface.
Passage pages are supporting reference surfaces generated as studies require them.

## Source Folders

Source material lives under `content/`.

- `content/studies/`: study drafts, outlines, and source copy
- `content/passages/`: passage-specific source material when separately provided
- `content/assets/`: reference PDFs, source files, and other non-web assets

Website implementation files live under `apps/web/`.

## Execution Rules

When a study source file is provided:

1. Create or update the corresponding study page.
2. Identify every Scripture passage referenced in the study.
3. Create or update a passage page for each referenced passage.
4. Convert Scripture references in the study page into inline links to the relevant passage pages.
5. Add backlinks from each passage page to the studies that reference it.
6. Maintain reciprocal study-to-passage and passage-to-study relationships whenever either side changes.

The assistant is responsible for normalizing source content into the site structure.
The user does not need to pre-separate topics, links, or page architecture beyond placing source files in the content folders.

Layout rule:

- the assistant may adapt source material into the site's page layout and navigation structure
- but authored study content should not be compressed, paraphrased, or omitted unless explicitly requested

## Study Page Standard

Each study page should, at minimum:

- present the study title clearly
- preserve the main teaching flow of the source content
- inline-link Scripture references to passage pages
- surface related passages naturally within the study body
- include a related or referenced passages area when that relationship data exists
- include the standard page-end feedback and revision note

As the site evolves, study pages may also include:

- summaries
- related studies
- question sections
- structured application or reflection sections

## Passage Page Standard

Each passage page should, at minimum, include:

- the passage reference
- the approved Bible versions for that passage
- a short contextual summary or orientation
- links back to studies that reference the passage
- a related studies area that points readers back into the study pages using that passage
- include the standard page-end feedback and revision note

Passage pages are not standalone replacements for full studies.
They are reference pages that support navigation, comparison, and context.

## Translation Standard

Approved core versions, in default display order:

1. `LSB`
2. `NKJV`
3. `NABRE`

### Translation Roles

- `LSB`: primary teaching and doctrinal baseline
- `NKJV`: broad mainstream comparison version
- `NABRE`: Catholic-familiar comparison version

### Usage Rules

- Default to these three versions on passage pages.
- Use `LSB` as the lead reference in normal teaching flow unless a comparison note is needed.
- Surface cross-version differences when they materially affect meaning, interpretation, emphasis, or doctrinal discussion.
- Do not add version comparisons merely for noise or volume.
- Additional translations may be referenced when explicitly useful, but they are not part of the default standard.

## Linking Standard

Scripture references inside study prose should be linked as part of the sentence flow, not separated into detached citation blocks unless the design specifically calls for it.

The intent is:

- natural reading flow in the study
- direct navigation from reference to passage page
- clear relationship between teaching content and supporting Scripture pages

Reciprocal relationship rule:

- if a study references a passage, the study should link to the passage page
- the passage page should also list that study as a related study
- if a passage later appears in additional studies, that passage page should accumulate those study links rather than being overwritten

## Page-End Standard

Every public study page and passage page should end with a standard note that communicates:

- this site is a living study effort
- thoughtful feedback is welcome
- submitted comments or feedback may be reviewed before appearing publicly
- content may change over time as understanding grows and corrections are made
- the goal is faithful study, humility, and growth rather than claiming that every written conclusion is final

The exact wording may evolve, but the message should remain consistent.

This note should support the site's posture of:

- inviting respectful engagement
- acknowledging ongoing learning
- being willing to revise published interpretations when warranted

## Documentation Expectation

If the content workflow changes in a durable way, update:

- `documentation/architecture/CONTENT_EXECUTION_STANDARD.md`

If implemented site behavior changes, add a change record under:

- `documentation/changes/`

## Current Working Assumption

Current initial workflow:

- the user provides study material first
- passage pages are created as studies reference them
- the site grows outward from study-driven content rather than from a prebuilt topical catalog
