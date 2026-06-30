# Content Execution Standard

Updated: 2026-06-29

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
- place the source intro or preface content in the top hero card as the main introduction
- preserve the main teaching flow of the source content
- inline-link Scripture references to passage pages
- surface related passages naturally within the study body
- include a related or referenced passages area when that relationship data exists
- include the standard page-end feedback and revision note

### Study Intro Rule

The introductory material at the top of a study is hero content, not duplicate body content.

The same substantive introductory content should also drive study-card copy on library surfaces.

Do:

- render the opening preface or introduction in the top study hero
- allow the hero introduction to contain multiple paragraphs when the source intro requires it
- begin the study body at the first actual content section after the intro
- use the same full introductory substance for study-card summary copy instead of reducing it to a thin one-line teaser when the source provides a fuller preface
- keep study-card intro copy and study-hero intro copy aligned so the card accurately previews what appears at the top of the study page

Do not:

- repeat the same introduction again as the first body paragraphs
- collapse a multi-paragraph introduction into a single line if the source clearly uses a fuller preface
- constrain the hero copy to a narrow column that truncates or weakens the introduction
- use a short teaser on the study card when the page hero is using a fuller intro from the same source
- let the hero and the study card drift into different intro lengths or mismatched framing for the same study

As the site evolves, study pages may also include:

- summaries
- related studies
- question sections
- structured application or reflection sections

## Passage Page Standard

Each passage page should, at minimum, include:

- the full passage text in the approved Bible versions for that passage
- the passage text rendered in the main top `Passage` section of the page, directly under the passage title
- a `Context` section
- an `Explanation` section
- links back to studies that reference the passage
- a related studies area that points readers back into the study pages using that passage
- include the standard page-end feedback and revision note

Passage pages are not standalone replacements for full studies.
They are reference pages that support navigation, comparison, and context.

### Passage Section Rule

The main page-level `Passage` section is where the default translations belong.

Do not:

- create a second internal `Passage` block lower on the page
- leave placeholder copy about future expansion
- show administrative labels such as default display-order notes
- include a `Passage Reference` section that merely repeats the citation already shown in the page title
- include a `Translation Standard` section that explains version policy to the reader

The reader should encounter the Scripture text itself immediately.

### Context Rule

`Context` means Scripture context, not process context.

The `Context` section should explain:

- where the passage sits in its immediate chapter flow
- how the surrounding verses shape its meaning
- what the broader movement of the book or argument is doing
- why the verse should not be read in isolation

Do not use `Context` to describe:

- that the page was generated
- that the passage is being used by a study
- that the page exists for navigation
- implementation notes about the site

The purpose of `Context` is to guard against cherry-picking and help the reader interpret the passage within Scripture itself.

### Explanation Rule

The `Explanation` section should draw its substance from the repository's source teaching material while speaking directly about the passage.

Do:

- carry forward the actual interpretive reasoning already established in the source content
- connect the passage to other relevant Scriptures when that comparison is needed
- link cited passages so the reader can follow the argument

Do not:

- refer to "the study" as an object in the public prose
- narrate the content-production process
- write meta commentary about where the explanation came from

Public copy should read as direct teaching and interpretation, not as commentary about internal source documents.

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
- On passage pages, render the full text of all three default versions unless the user explicitly directs otherwise.

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
- passage links should open in a new tab so readers can follow supporting references without losing their place

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

## Completion Rule

For website content-integration work, completion means more than local generation.

When study pages, passage pages, library surfaces, styling, or other public website behavior has been updated and verified, deploy the finished website state to Firebase hosting before considering the task complete, unless the user explicitly says not to deploy.

If implemented site behavior changes, add a change record under:

- `documentation/changes/`

## Current Working Assumption

Current initial workflow:

- the user provides study material first
- passage pages are created as studies reference them
- the site grows outward from study-driven content rather than from a prebuilt topical catalog
