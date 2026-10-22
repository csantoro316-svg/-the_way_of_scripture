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
- show the study's place in the guided foundation path
- provide previous/next guided-study navigation after the teaching content
- include the standard page-end feedback and revision note

### Guided Study Rule

`Foundations: A Guided Study` includes every published study. The 14-step order is defined once in `GUIDED_STUDY_STEPS` in `tools/generate_study_pages.py`: Returning to the Word; The Berean Standard; Is the Bible the Inerrant Word of God?; Is There a Source of Truth?; The Gospel According to Jesus; Who is The Angel of the Lord?; I Am a Disciple; Baptism; Prayer and Faith; What Does Prayer Look Like?; Should We Seek Signs From God?; The True Church According to Jesus; Who Shepherds the Church?; and Worship as the Early Church Knew It.

The homepage briefly explains why the site exists, offers a small link to the full site-approach page, places the banner after its opening, and leads into one Foundations invitation into Step 1. `apps/web/why-we-return-to-the-text.html` carries the full site-focused explanation and ends with its own Study 1 invitation. The original teaching introduction is now the source of Study 1, Returning to the Word; its former standalone URL redirects there. The canonical Studies page at `apps/web/library/index.html` shows the entire ordered path by default and lets readers switch to a topic-grouped view with a topic filter. There is no separate featured-studies or all-studies page. Each study shows its step number, links to the Studies page, and ends with previous/continue navigation that names the destination and explains the next topic. The last study links back to the complete path. Older guided-study and browse-all-studies URLs redirect to the canonical Studies page or its topic view. Passage browsing remains on the passage reader.

For guidance-only updates that must preserve current published study prose, run:

```bash
python3 tools/generate_study_pages.py --guided-only
```

This refreshes the 14 study-page guidance blocks, the canonical Studies page, study index order, and legacy study redirects from the existing published index without regenerating study or passage prose. The normal full generator also refreshes these surfaces after generating content.

### Study Intro Rule

The introductory material at the top of a study is hero content, not duplicate body content.

When a card presents a study synopsis, its copy should come from the study's source introduction. The guided path and topic view use short purpose statements to help readers choose a route; those navigation labels do not replace the full hero introduction on the study page.

Do:

- render the opening preface or introduction in the top study hero
- allow the hero introduction to contain multiple paragraphs when the source intro requires it
- begin the study body at the first actual content section after the intro
- use the same full introductory substance for synopsis-card copy instead of reducing it to a thin one-line teaser when the source provides a fuller preface
- keep synopsis-card intro copy and study-hero intro copy aligned so the card accurately previews what appears at the top of the study page

Do not:

- repeat the same introduction again as the first body paragraphs
- collapse a multi-paragraph introduction into a single line if the source clearly uses a fuller preface
- constrain the hero copy to a narrow column that truncates or weakens the introduction
- use a short teaser on a synopsis card when the page hero is using a fuller intro from the same source
- let the hero and a synopsis card drift into different intro lengths or mismatched framing for the same study

As the site evolves, study pages may also include:

- summaries
- related studies
- question sections
- structured application or reflection sections

## Passage Page Standard

New passage editorial work follows the owner's [Passage Editorial Standard](PASSAGE_EDITORIAL_STANDARD.md). It governs source verification, fair primary-document comparisons, the optional plan section, and authority for a site position. Legacy placeholders are not reviewed content.

Each passage page should, at minimum, include:

- the full passage text in the Berean Standard Bible (BSB), following the master doctrine and translation standard
- the passage text rendered in the main top `Passage` section of the page, directly under the passage title
- a `Context` section
- a `Common Interpretations` section describing major readings
- an optional `Where does this fit in God's plan?` section only when the editorial standard's Scripture-supported inclusion tests apply
- an `Our Position` section stating an authorized developed position or using the exact approved no-position wording
- a `Deeper Study` section linking developed treatments when available
- previous/next passage navigation immediately after `Deeper Study`
- links back to studies that reference the passage
- a related studies area that points readers back into the study pages using that passage
- include the standard page-end feedback and revision note

Passage pages are not standalone replacements for full studies.
They are reference pages that support navigation, comparison, and context.

### Passage Navigation Rule

Individual passage pages and passage articles in the Passages reader end with previous/next links showing the destination reference and its section title when available. Follow the complete library in canonical book order and numeric chapter/verse order, breaking ties by the range end. Continue across book boundaries; omit the unavailable direction at either endpoint. Noncanonical references retain their existing position after the canonical books.

These reading-navigation links open in the same tab. In the Passages reader, ordinary clicks update the article, expand and highlight its entry in the navigation drawer, clear search/filter state to reveal the destination, and move focus and scrolling to the new heading below the sticky toolbar. The selected passage is retained in the URL. Alphabetical browsing and filtering do not change the reading sequence. Links stack on narrow screens.

The canonical `library/passages.html` route uses a full-width reader with compact Book, Chapter, and Passage selectors populated from the available library. The complete navigation tree opens in a modal drawer. The article scrolls normally with the page; only the controls remain sticky. Keep the section guide in a collapsed page-level disclosure. See the [website style standard](WEBSITE_STYLE_STANDARD.md) for scrolling, responsive layout, and focus rules.

The normal generator refreshes this navigation. For a navigation-only change that must preserve existing authored HTML and translation content, run:

```bash
python3 tools/generate_study_pages.py --navigation-only
```

This refreshes passage navigation, the sorted library index, the canonical Passages reader, and legacy passage redirects without regenerating study pages, passage prose, source JSON records, or the translation audit. It does not reconcile unrelated content debt.

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

The renderer separates context, common readings, an optional plan section, a site position, and deeper-study links. Reviewed pages use conversational question headings. Common Interpretations must describe actual readings from each tradition's own directly checked documents. A baseline teacher supplies research questions, not consensus. Never name or closely reproduce the baseline teacher on public pages. Verify lexical and historical claims independently.

Do not originate a site position. Use only an existing study that addresses the passage, a supplied owner position, or an already-developed owner/assistant conclusion. Positions drawn from a site study should identify and link it. Otherwise use exactly: `We don't have a position on this passage yet. When our study reaches a conclusion the text supports, it will appear here.`

Source records use `common_interpretation_lines`, optional `god_plan_lines`, `current_position_lines`, and `deeper_study`. Reviewed records carry `editorial_review` metadata and internal evidence as specified in the editorial standard. Legacy `explanation_lines` remains a compatibility fallback in validation, not a requirement to restore an `Explanation` page section.

For a reviewed batch:

```bash
python3 tools/verify_bsb_passages.py genesis-1-1-31 genesis-2-1-3
python3 tools/check_repo.py
python3 tools/generate_study_pages.py --passages-only genesis-1-1-31 genesis-2-1-3
```

Substitute the selected reviewed source slugs. This focused refresh updates only their pages and index entries plus the shared reader, preserving unrelated published prose and bypassing the legacy translation audit. Check local/live layout, links, section omission/order, and preservation before release.

Do:

- synthesize independently checked interpretation in original prose
- connect the passage to other relevant Scriptures when that comparison is needed
- link cited passages so the reader can follow the argument

Do not:

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

The Prayer and Faith asking revision was reconciled into its Markdown source on 2026-10-18, preserving the eight authored HTML paragraphs verbatim. See [the reconciliation and navigation change record](../changes/2026-10-18-passage-navigation-and-prayer-source-reconciliation.md). The generator translation debt above remains open.

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
