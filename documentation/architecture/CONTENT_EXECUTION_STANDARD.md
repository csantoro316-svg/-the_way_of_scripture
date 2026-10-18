# Content Execution Standard

Updated: 2026-10-18

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

- the full passage text in the Berean Standard Bible (BSB), following the master doctrine and translation standard
- the passage text rendered in the main top `Passage` section of the page, directly under the passage title
- a `Context` section
- a `Common Interpretations` section describing major readings
- a `Current Position` section stating a developed position or explicitly leaving the question open
- a `Deeper Study` section linking developed treatments when available
- links back to studies that reference the passage
- a related studies area that points readers back into the study pages using that passage
- include the standard page-end feedback and revision note

Passage pages are not standalone replacements for full studies.
They are reference pages that support navigation, comparison, and context.

### Passage Section Rule

The main page-level `Passage` section is where the full BSB passage text belongs.

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

### Interpretation and Position Rule

The current renderer separates `Common Interpretations`, `Current Position`, and `Deeper Study`, as described in the [active passage-library plan](../planning/2026-07-05-passage-library-foundation-plan.md). Draw reviewed interpretation from source teaching material while speaking directly about the passage. Describe major readings without implying that each is the site's position. State a defined current position only when supported by developed study; otherwise leave the question open.

Source records use `common_interpretation_lines`, optional `current_position_lines`, and `deeper_study`. Legacy `explanation_lines` remains a compatibility fallback in validation, not a requirement to restore an `Explanation` page section.

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

The [master doctrine and standards](PROJECT_DOCTRINE_AND_STANDARDS.md) governs translation choices. BSB is the primary public English translation; original Hebrew and Greek remain the interpretive benchmark. LSB is an internal comparison reference and is not cited on the site under that standard.

### Usage Rules

- Include full BSB text on passage pages and use BSB as the public English baseline in study content.
- Define and examine significant original-language terms according to the master standard.
- Surface cross-version differences when they materially affect meaning, interpretation, emphasis, or doctrinal discussion.
- Do not add version comparisons merely for noise or volume.
- Other public translation comparisons require a specific editorial purpose and must follow the master standard; the old LSB/NKJV/NABRE three-version requirement is superseded.

### Known Implementation Debt

The current generator still contains LSB extraction, an LSB study-header default, and an audit expecting LSB/NKJV/NABRE. The current source validation instead warns on missing BSB. These legacy implementation paths have not been reconciled in this documentation session. They must be reviewed against the master standard before content regeneration; a passing structural check alone does not establish translation or editorial compliance.

The Prayer and Faith HTML also contains an authored revision absent from its Markdown source. Reconcile that source before regeneration, as recorded in [the backup change record](../changes/2026-10-18-prayer-and-faith-git-backup.md).

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

### Required Cloud Route

Follow [Keyless Cloud Operations](../runbooks/CLOUD_OPERATIONS.md) for every Firebase or Google Cloud operation. Use the executing host's certificate wrappers on either CozDev or CozPlex and explicitly target `the-way-of-scripture`. Readiness checks must pass on that host before cloud work.

After content and local verification are complete, validate Hosting without publishing:

```bash
~/.local/bin/mg-cloud-firebase deploy --only hosting --project the-way-of-scripture --dry-run
```

For a live release within the user's authorized scope, run:

```bash
~/.local/bin/mg-cloud-firebase deploy --only hosting --project the-way-of-scripture
```

Use the host-local wrapper rather than a bare Firebase CLI or interactive user login. The wrapper selects its certificate and compatible runtime. Record the executing host, project, and verification/deployment outcome in the change record. Documentation-only work does not require site generation or a Hosting deployment.

If implemented site behavior changes, add a change record under:

- `documentation/changes/`

## Current Working Assumption

Current initial workflow:

- the user provides study material first
- passage pages are created as studies reference them
- the site grows outward from study-driven content rather than from a prebuilt topical catalog
