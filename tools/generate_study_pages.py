#!/usr/bin/env python3

from __future__ import annotations

import html
import json
import re
from dataclasses import dataclass
from pathlib import Path
from collections import defaultdict


ROOT = Path("/home/cozwood/Documents/Dev/the_way_of_scripture")
SOURCE_DIR = ROOT / "content" / "studies"
WEB_DIR = ROOT / "apps" / "web"
OUTPUT_DIR = WEB_DIR / "studies"
LIBRARY_DIR = WEB_DIR / "library"
PASSAGES_DIR = WEB_DIR / "passages"
SKIP_FILES = {"way_of_scripture_intro.md"}
PASSAGE_SOURCE_FILES = {"way_of_scripture_intro.md"}
FEATURED_STUDY_LIMIT = 6
FEATURED_STUDY_ORDER = [
    "prayer_and_faith.md",
    "what_does_prayer_look_like.md",
    "seek_signs.md",
    "true_church.md",
    "baptism.md",
]
FEATURED_PASSAGE_ORDER = [
    ("1 John", "5:14-15"),
    ("Matthew", "26:39"),
    ("Proverbs", "3:5-6"),
    ("Acts", "17:11"),
    ("Hebrews", "4:12"),
    ("1 Corinthians", "3:16"),
    ("1 Peter", "2:9"),
    ("Romans", "8:26-27"),
    ("Romans", "6:3-4"),
    ("John", "13:34-35"),
    ("Deuteronomy", "4:2"),
    ("1 Corinthians", "14:26"),
]
FEATURED_PASSAGE_NOTES = {
    ("1 John", "5:14-15"): "The governing principle of prayer: we approach God on His terms, not ours.",
    ("Matthew", "26:39"): "Gethsemane and surrendered faith: not as I will, but as You will.",
    ("Proverbs", "3:5-6"): "Trust that runs through prayer, baptism, faith, and the site’s entire posture.",
    ("Acts", "17:11"): "The Berean standard: examine everything against the Word yourself.",
    ("Hebrews", "4:12"): "What the site believes about Scripture itself: living, active, and discerning.",
    ("1 Corinthians", "3:16"): "A core church passage: the people of God are His temple.",
    ("1 Peter", "2:9"): "Every believer as priest: a royal priesthood, not a clerical class.",
    ("Romans", "8:26-27"): "When words fail, the Spirit intercedes according to the will of God.",
    ("Romans", "6:3-4"): "The theological heart of baptism: buried and raised with Christ.",
    ("John", "13:34-35"): "Love as the identifying mark of the true Church.",
    ("Deuteronomy", "4:2"): "Do not add to the Word: stated plainly in the Law and echoed across the site.",
    ("1 Corinthians", "14:26"): "Let all things be done for edification: a closing standard for the whole project.",
}

BOOK_ORDER = [
    "Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy", "Joshua", "Judges",
    "Ruth", "1 Samuel", "2 Samuel", "1 Kings", "2 Kings", "1 Chronicles",
    "2 Chronicles", "Ezra", "Nehemiah", "Esther", "Job", "Psalm", "Psalms",
    "Proverbs", "Ecclesiastes", "Song of Solomon", "Isaiah", "Jeremiah",
    "Lamentations", "Ezekiel", "Daniel", "Hosea", "Joel", "Amos", "Obadiah",
    "Jonah", "Micah", "Nahum", "Habakkuk", "Zephaniah", "Haggai", "Zechariah",
    "Malachi", "Matthew", "Mark", "Luke", "John", "Acts", "Romans",
    "1 Corinthians", "2 Corinthians", "Galatians", "Ephesians", "Philippians",
    "Colossians", "1 Thessalonians", "2 Thessalonians", "1 Timothy", "2 Timothy",
    "Titus", "Philemon", "Hebrews", "James", "1 Peter", "2 Peter", "1 John",
    "2 John", "3 John", "Jude", "Revelation",
]

REFERENCE_PATTERN = re.compile(
    r"(?<![A-Za-z0-9])((?:[1-3]\s)?[A-Z][A-Za-z]+(?:\s[A-Z][A-Za-z]+)*)\s(\d+:\d+(?:-\d+)?)"
)


@dataclass
class Study:
    title: str
    subtitle: str
    translation: str
    slug: str
    source_name: str
    summary: str
    body_html: str
    references: list["PassageReference"]


@dataclass(frozen=True)
class PassageReference:
    book: str
    citation: str

    @property
    def slug(self) -> str:
        return slugify(f"{self.book}-{self.citation}")

    @property
    def label(self) -> str:
        return f"{self.book} {self.citation}"


@dataclass(frozen=True)
class PassageSource:
    title: str
    href: str


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug or "study"


def extract_references(text: str) -> list[PassageReference]:
    seen: set[PassageReference] = set()
    references: list[PassageReference] = []
    for match in REFERENCE_PATTERN.finditer(text):
        book = match.group(1).strip()
        citation = match.group(2).strip()
        ref = PassageReference(book=book, citation=citation)
        if ref not in seen:
            seen.add(ref)
            references.append(ref)
    return references


def passage_reference(book: str, citation: str) -> PassageReference:
    return PassageReference(book=book, citation=citation)


def render_reference_links(text: str) -> str:
    rendered = html.escape(text)

    def replace(match: re.Match[str]) -> str:
        book = match.group(1).strip()
        citation = match.group(2).strip()
        ref = PassageReference(book=book, citation=citation)
        label = html.escape(f"{book} {citation}")
        return f'<a href="../passages/{ref.slug}.html">{label}</a>'

    rendered = re.sub(
        r"((?:[1-3]\s)?[A-Z][A-Za-z]+(?:\s[A-Z][A-Za-z]+)*)\s(\d+:\d+(?:-\d+)?)",
        replace,
        rendered,
    )
    rendered = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", rendered)
    rendered = re.sub(r"\*(.+?)\*", r"<em>\1</em>", rendered)
    return rendered


def render_inline(text: str) -> str:
    rendered = html.escape(text)
    rendered = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", rendered)
    rendered = re.sub(r"\*(.+?)\*", r"<em>\1</em>", rendered)
    return rendered


def render_blocks(lines: list[str], enable_reference_links: bool = False) -> str:
    output: list[str] = []
    i = 0
    inline_renderer = render_reference_links if enable_reference_links else render_inline

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if not stripped:
            i += 1
            continue

        if stripped == "---":
            if output:
                output.append('<hr class="prose-divider" />')
            i += 1
            continue

        if stripped.startswith("### "):
            output.append(f"<h3>{inline_renderer(stripped[4:])}</h3>")
            i += 1
            continue

        if stripped.startswith("## "):
            output.append(f"<h2>{inline_renderer(stripped[3:])}</h2>")
            i += 1
            continue

        if stripped.startswith("> "):
            quote_lines: list[str] = []
            while i < len(lines) and lines[i].strip().startswith("> "):
                quote_lines.append(lines[i].strip()[2:])
                i += 1
            quote_text = " ".join(part.strip() for part in quote_lines)
            output.append(f"<blockquote><p>{inline_renderer(quote_text)}</p></blockquote>")
            continue

        if stripped.startswith("- "):
            items: list[str] = []
            while i < len(lines) and lines[i].strip().startswith("- "):
                items.append(lines[i].strip()[2:])
                i += 1
            rendered_items = "".join(
                f"<li>{inline_renderer(item)}</li>" for item in items
            )
            output.append(f'<ul class="prose-list">{rendered_items}</ul>')
            continue

        paragraph_lines = [stripped]
        i += 1
        while i < len(lines):
            next_stripped = lines[i].strip()
            if not next_stripped:
                break
            if (
                next_stripped == "---"
                or next_stripped.startswith("## ")
                or next_stripped.startswith("### ")
                or next_stripped.startswith("> ")
                or next_stripped.startswith("- ")
            ):
                break
            paragraph_lines.append(next_stripped)
            i += 1
        paragraph = " ".join(paragraph_lines)
        output.append(f"<p>{inline_renderer(paragraph)}</p>")

    return "\n              ".join(output)


def parse_study(path: Path) -> Study:
    lines = path.read_text(encoding="utf-8").splitlines()
    title = ""
    subtitle = ""
    translation = "Legacy Standard Bible (LSB)"
    summary = ""
    body_start = 0

    for idx, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("# ") and not title:
            title = stripped[2:].strip()
            body_start = idx + 1
            continue
        if stripped.startswith("## ") and not subtitle:
            subtitle = stripped[3:].strip()
            continue
        if stripped.startswith("*Primary Translation:"):
            translation = stripped.strip("*").replace("Primary Translation:", "").strip()
            continue
        if stripped and not stripped.startswith("#") and stripped != "---" and not summary:
            if not stripped.startswith("*Primary Translation:"):
                summary = stripped.strip("*")
        if title and summary:
            break

    if not subtitle:
        preface_lines: list[str] = []
        in_intro_block = False
        for line in lines[body_start:]:
            stripped = line.strip()
            if not stripped:
                continue
            if stripped == "---":
                if in_intro_block:
                    break
                in_intro_block = True
                continue
            if stripped.startswith("## "):
                break
            if stripped.startswith("*Primary Translation:"):
                continue
            if in_intro_block:
                preface_lines.append(stripped.strip("*").strip())

        if preface_lines:
            subtitle = preface_lines[0]
            if len(preface_lines) > 1:
                summary = " ".join(preface_lines[1:])
            else:
                summary = preface_lines[0]

    filtered_body: list[str] = []
    consumed_subtitle = False
    consumed_translation = False

    for idx, line in enumerate(lines[body_start:], start=body_start):
        stripped = line.strip()
        if idx == body_start - 1:
            continue
        if stripped.startswith("## ") and not consumed_subtitle and stripped[3:].strip() == subtitle:
            consumed_subtitle = True
            continue
        if (
            stripped.startswith("*Primary Translation:")
            and not consumed_translation
        ):
            consumed_translation = True
            continue
        filtered_body.append(line)

    body_lines = filtered_body
    body_text = "\n".join(body_lines)
    references = extract_references(body_text)
    body_html = render_blocks(body_lines, enable_reference_links=True)
    slug = slugify(path.stem.replace("_", "-"))

    return Study(
        title=title or path.stem.replace("_", " ").title(),
        subtitle=subtitle,
        translation=translation,
        slug=slug,
        source_name=path.name,
        summary=summary,
        body_html=body_html,
        references=references,
    )


def primary_nav(current: str, depth: str = "..") -> str:
    studies_href = f"{depth}/library/index.html"
    passages_href = f"{depth}/library/passages.html"
    return f"""        <nav class="site-nav" aria-label="Primary">
          <a href="{depth}/index.html">Home</a>
          <a href="{studies_href}"{" aria-current=\"page\"" if current == "studies" else ""}>Studies</a>
          <a href="{passages_href}"{" aria-current=\"page\"" if current == "passages" else ""}>Passages</a>
        </nav>"""


def library_rail(current: str) -> str:
    return f"""        <aside class="library-rail" aria-label="Library navigation">
          <p class="eyebrow">Library</p>
          <nav class="library-rail-nav">
            <a href="./index.html"{" aria-current=\"page\"" if current == "studies-featured" else ""}>Featured Studies</a>
            <a href="./studies-all.html"{" aria-current=\"page\"" if current == "studies-all" else ""}>Browse All Studies</a>
            <a href="./passages.html"{" aria-current=\"page\"" if current == "passages-featured" else ""}>Featured Passages</a>
            <a href="./passages-by-book.html"{" aria-current=\"page\"" if current == "passages-by-book" else ""}>Browse All Passages</a>
          </nav>
        </aside>"""


def library_heading(title: str, browse_label: str, browse_href: str) -> str:
    return f"""          <div class="library-heading">
            <h2>{html.escape(title)}</h2>
            <a class="library-heading-link" href="{browse_href}">{html.escape(browse_label)}</a>
          </div>"""


def browse_redirect_html(target: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta http-equiv="refresh" content="0; url={target}" />
    <title>Redirecting...</title>
  </head>
  <body>
    <p><a href="{target}">Continue to browse.</a></p>
  </body>
</html>
"""


def study_page_html(study: Study) -> str:
    subtitle_html = (
        f'            <p class="article-subtitle">{html.escape(study.subtitle)}</p>\n'
        if study.subtitle
        else ""
    )
    return f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{html.escape(study.title)} | The Way of Scripture</title>
    <meta
      name="description"
      content="{html.escape(study.summary)}"
    />
    <link rel="stylesheet" href="../styles.css" />
  </head>
  <body>
    <div class="page-shell">
      <header class="site-header">
        <a class="brand" href="../index.html" aria-label="The Way of Scripture home">
          <img
            class="brand-mark"
            src="../assets/icons/icon.jpg"
            alt="The Way of Scripture icon"
          />
          <div class="brand-copy">
            <span class="brand-title">The Way of Scripture</span>
            <span class="brand-subtitle">Returning to the text itself</span>
          </div>
        </a>
{primary_nav("studies")}
      </header>

      <main>
        <section class="article-hero">
          <p class="eyebrow">Study</p>
          <h1>{html.escape(study.title)}</h1>
{subtitle_html}          <p class="article-meta">Primary Translation: {html.escape(study.translation)}</p>
          <p class="lead">{html.escape(study.summary)}</p>
        </section>

        <div class="article-layout">
          <article class="article-body">
            <div class="prose">
              {study.body_html}
            </div>
          </article>

          <aside class="sidebar">
            <section class="sidebar-card">
              <h2>Library</h2>
              <ul class="study-link-list">
                <li><a href="../library/index.html">Featured studies</a></li>
                <li><a href="../library/studies-all.html">Browse all studies</a></li>
              </ul>
            </section>

            <section class="sidebar-card">
              <h2>Source File</h2>
              <p>{html.escape(study.source_name)}</p>
            </section>
          </aside>
        </div>

        <section class="feedback-note" aria-label="Feedback note">
          <h2>A Living Study And Exchange</h2>
          <p>
            This site is a living study effort. Thoughtful feedback is welcome, and future study may lead to clarification, correction, or revision.
          </p>
          <p>
            Public comments, when enabled, will be reviewed before appearing on the site so discussion remains respectful and relevant. The goal is to grow in understanding, test everything by Scripture, and remain willing to change where the text requires it.
          </p>
        </section>
      </main>
    </div>
  </body>
</html>
"""


def passage_page_html(reference: PassageReference, linked_studies: list[Study]) -> str:
    related_studies = "\n".join(
        f'                <li><a href="../studies/{study.slug}.html">{html.escape(study.title)}</a></li>'
        for study in linked_studies
    ) or "                <li>No linked study page yet.</li>"
    return f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{html.escape(reference.label)} | The Way of Scripture</title>
    <meta
      name="description"
      content="Passage reference page for {html.escape(reference.label)}."
    />
    <link rel="stylesheet" href="../styles.css" />
  </head>
  <body>
    <div class="page-shell">
      <header class="site-header">
        <a class="brand" href="../index.html" aria-label="The Way of Scripture home">
          <img
            class="brand-mark"
            src="../assets/icons/icon.jpg"
            alt="The Way of Scripture icon"
          />
          <div class="brand-copy">
            <span class="brand-title">The Way of Scripture</span>
            <span class="brand-subtitle">Returning to the text itself</span>
          </div>
        </a>
{primary_nav("passages")}
      </header>

      <main>
        <section class="article-hero">
          <p class="eyebrow">Passage</p>
          <h1>{html.escape(reference.label)}</h1>
          <p class="article-meta">Default Display Order: LSB, NKJV, NABRE</p>
          <p class="lead">
            This passage page exists to support study navigation and reciprocal linking. Source translation text and fuller comparison content can be expanded here later.
          </p>
        </section>

        <div class="article-layout">
          <article class="article-body">
            <div class="prose">
              <h2>Passage Reference</h2>
              <p>{html.escape(reference.label)}</p>

              <h2>Context Note</h2>
              <p>
                This is a generated reference page created from study usage. It currently serves as the navigation target for study references and a shared place to accumulate related study links.
              </p>

              <h2>Translation Standard</h2>
              <ul class="prose-list">
                <li><strong>LSB</strong> as the primary study text</li>
                <li><strong>NKJV</strong> as a broad comparison version</li>
                <li><strong>NABRE</strong> as a Catholic-familiar comparison version</li>
              </ul>
            </div>
          </article>

          <aside class="sidebar">
            <section class="sidebar-card">
              <h2>Related Studies</h2>
              <ul class="study-link-list">
{related_studies}
              </ul>
            </section>

            <section class="sidebar-card">
              <h2>Library</h2>
              <ul class="study-link-list">
                <li><a href="../library/passages.html">Featured passages</a></li>
                <li><a href="../library/passages-by-book.html">Browse all passages</a></li>
                <li><a href="../library/index.html">Featured studies</a></li>
              </ul>
            </section>
          </aside>
        </div>

        <section class="feedback-note" aria-label="Feedback note">
          <h2>A Living Study And Exchange</h2>
          <p>
            This site is a living study effort. Thoughtful feedback is welcome, and future study may lead to clarification, correction, or revision.
          </p>
          <p>
            Public comments, when enabled, will be reviewed before appearing on the site so discussion remains respectful and relevant. The goal is to grow in understanding, test everything by Scripture, and remain willing to change where the text requires it.
          </p>
        </section>
      </main>
    </div>
  </body>
</html>
"""


def studies_all_html(studies: list[Study]) -> str:
    return browse_redirect_html("./browse.html?type=studies")


def library_index_html(studies: list[Study]) -> str:
    featured = studies[:FEATURED_STUDY_LIMIT]
    cards = []
    for study in featured:
        subtitle = (
            f'\n            <p class="study-card-subtitle">{html.escape(study.subtitle)}</p>'
            if study.subtitle
            else ""
        )
        cards.append(
            f"""          <article class="study-card">
            <p class="eyebrow">Featured Study</p>
            <h2><a href="../studies/{study.slug}.html">{html.escape(study.title)}</a></h2>
{subtitle}
            <p>{html.escape(study.summary)}</p>
            <a class="study-card-link" href="../studies/{study.slug}.html">Read study</a>
          </article>"""
        )

    return f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Library | The Way of Scripture</title>
    <meta
      name="description"
      content="Featured studies and central library navigation for The Way of Scripture."
    />
    <link rel="stylesheet" href="../styles.css" />
  </head>
  <body>
    <div class="page-shell">
      <header class="site-header">
        <a class="brand" href="../index.html" aria-label="The Way of Scripture home">
          <img
            class="brand-mark"
            src="../assets/icons/icon.jpg"
            alt="The Way of Scripture icon"
          />
          <div class="brand-copy">
            <span class="brand-title">The Way of Scripture</span>
            <span class="brand-subtitle">Returning to the text itself</span>
          </div>
        </a>
{primary_nav("studies")}
      </header>

      <main>
        <section class="article-hero">
          <p class="eyebrow">Studies</p>
          <h1>Featured Studies</h1>
          <p class="lead">
            A curated front door to the study library, with the full corpus available when you want to browse further.
          </p>
        </section>

        <section class="library-panel">
{library_heading("Featured Studies", "Browse all studies", "./browse.html?type=studies")}
          <div class="study-card-grid">
{chr(10).join(cards)}
          </div>
          <p class="library-browse-link">
            <a href="./browse.html?type=studies">Browse all studies</a>
          </p>
        </section>
      </main>
    </div>
  </body>
</html>
"""


def featured_passages_html(featured_references: list[PassageReference]) -> str:
    cards = []
    for reference in featured_references:
        note = FEATURED_PASSAGE_NOTES.get((reference.book, reference.citation), "Featured passage.")
        cards.append(
            f"""          <article class="study-card passage-card">
            <p class="eyebrow">Featured Passage</p>
            <h2><a href="../passages/{reference.slug}.html">{html.escape(reference.label)}</a></h2>
            <p>{html.escape(note)}</p>
            <a class="study-card-link" href="../passages/{reference.slug}.html">Read passage</a>
          </article>"""
        )

    return f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Featured Passages | The Way of Scripture</title>
    <meta
      name="description"
      content="Featured passage pages for The Way of Scripture."
    />
    <link rel="stylesheet" href="../styles.css" />
  </head>
  <body>
    <div class="page-shell">
      <header class="site-header">
        <a class="brand" href="../index.html" aria-label="The Way of Scripture home">
          <img
            class="brand-mark"
            src="../assets/icons/icon.jpg"
            alt="The Way of Scripture icon"
          />
          <div class="brand-copy">
            <span class="brand-title">The Way of Scripture</span>
            <span class="brand-subtitle">Returning to the text itself</span>
          </div>
        </a>
{primary_nav("passages")}
      </header>

      <main>
        <section class="article-hero">
          <p class="eyebrow">Passages</p>
          <h1>Featured Passages</h1>
          <p class="lead">
            Foundational references that shape the site’s teaching posture, study standards, and core doctrinal arguments.
          </p>
        </section>

        <section class="library-panel">
{library_heading("Featured Passages", "Browse all passages", "./browse.html?type=passages")}
          <div class="study-card-grid">
{chr(10).join(cards)}
          </div>
          <p class="library-browse-link">
            <a href="./browse.html?type=passages">Browse all passages</a>
          </p>
        </section>
      </main>
    </div>
  </body>
</html>
"""


def passages_by_book_html(grouped_references: dict[str, list[PassageReference]]) -> str:
    return browse_redirect_html("./browse.html?type=passages")


def browse_page_html() -> str:
    return """<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Browse Library | The Way of Scripture</title>
    <meta
      name="description"
      content="Browse studies and passages for The Way of Scripture."
    />
    <link rel="stylesheet" href="../styles.css" />
  </head>
  <body>
    <div class="page-shell">
      <header class="site-header">
        <a class="brand" href="../index.html" aria-label="The Way of Scripture home">
          <img
            class="brand-mark"
            src="../assets/icons/icon.jpg"
            alt="The Way of Scripture icon"
          />
          <div class="brand-copy">
            <span class="brand-title">The Way of Scripture</span>
            <span class="brand-subtitle">Returning to the text itself</span>
          </div>
        </a>
        <nav class="site-nav" aria-label="Primary">
          <a href="../index.html">Home</a>
          <a href="./index.html">Studies</a>
          <a href="./passages.html">Passages</a>
        </nav>
      </header>

      <main class="kb-shell">
        <section class="kb-topbar scripture-kb-topbar">
          <div class="kb-topbar-inner scripture-kb-topbar-inner">
            <h1 class="kb-title">Browse Library</h1>
            <input id="librarySearch" class="kb-search" type="search" placeholder="Search studies, passages, books..." />
            <button id="libraryBrowseBtn" class="kb-browse-btn" aria-expanded="false">Browse</button>
          </div>
        </section>

        <section class="kb-layout scripture-kb-layout">
          <aside class="kb-nav" id="libraryNavDrawer">
            <div class="kb-nav-controls">
              <label class="kb-control-label" for="libraryTypeSelect">Content Type</label>
              <select id="libraryTypeSelect" class="kb-select">
                <option value="studies">Studies</option>
                <option value="passages">Passages</option>
              </select>

              <label class="kb-control-label" for="libraryViewSelect">Browse By</label>
              <select id="libraryViewSelect" class="kb-select">
                <option value="az">A-Z</option>
                <option value="book">By Book</option>
              </select>

              <div class="kb-nav-actions">
                <button id="libraryExpandAll" class="kb-nav-action-btn">Expand All</button>
                <button id="libraryCollapseAll" class="kb-nav-action-btn">Collapse All</button>
              </div>
            </div>
            <div id="libraryNav"></div>
          </aside>
          <div id="libraryNavBackdrop" class="kb-nav-backdrop"></div>
          <article class="kb-content">
            <div id="libraryResults" class="kb-results"></div>
            <div id="libraryArticle"></div>
          </article>
        </section>
      </main>
    </div>

    <script>
      let LIBRARY_DATA = { studies: [], passages: [] };
      let activeType = "studies";
      let activeId = "";
      let navView = "az";
      const collapsedGroups = new Set();

      const typeSelectEl = document.getElementById("libraryTypeSelect");
      const viewSelectEl = document.getElementById("libraryViewSelect");
      const expandAllEl = document.getElementById("libraryExpandAll");
      const collapseAllEl = document.getElementById("libraryCollapseAll");
      const navEl = document.getElementById("libraryNav");
      const navDrawerEl = document.getElementById("libraryNavDrawer");
      const navBackdropEl = document.getElementById("libraryNavBackdrop");
      const browseBtnEl = document.getElementById("libraryBrowseBtn");
      const articleEl = document.getElementById("libraryArticle");
      const resultsEl = document.getElementById("libraryResults");
      const searchEl = document.getElementById("librarySearch");
      const mobileMq = window.matchMedia("(max-width: 960px)");

      function getCurrentItems() {
        return LIBRARY_DATA[activeType] || [];
      }

      function syncQuery() {
        const url = new URL(window.location.href);
        url.searchParams.set("type", activeType);
        window.history.replaceState({}, "", url);
      }

      function syncViewOptions() {
        if (activeType === "studies") {
          viewSelectEl.innerHTML = '<option value="az">A-Z</option>';
          navView = "az";
        } else {
          viewSelectEl.innerHTML = '<option value="book">By Book</option>';
          navView = "book";
        }
      }

      function openDrawer() {
        if (!mobileMq.matches) return;
        document.body.classList.add("kb-nav-open");
        browseBtnEl.setAttribute("aria-expanded", "true");
      }

      function closeDrawer() {
        document.body.classList.remove("kb-nav-open");
        browseBtnEl.setAttribute("aria-expanded", "false");
      }

      function getGroups() {
        const items = getCurrentItems();
        const groups = {};
        if (activeType === "studies") {
          items.forEach((item) => {
            const first = (item.title.trim()[0] || "#").toUpperCase();
            const letter = /[A-Z]/.test(first) ? first : "#";
            if (!groups[letter]) groups[letter] = [];
            groups[letter].push(item);
          });
          return Object.keys(groups).sort().map((key) => ({ key, label: key, items: groups[key] }));
        }

        items.forEach((item) => {
          const key = item.book || "Other";
          if (!groups[key]) groups[key] = [];
          groups[key].push(item);
        });
        const order = LIBRARY_DATA.book_order || [];
        return Object.keys(groups)
          .sort((a, b) => {
            const ai = order.indexOf(a);
            const bi = order.indexOf(b);
            const ar = ai === -1 ? Number.MAX_SAFE_INTEGER : ai;
            const br = bi === -1 ? Number.MAX_SAFE_INTEGER : bi;
            return ar - br || a.localeCompare(b);
          })
          .map((key) => ({ key, label: key, items: groups[key] }));
      }

      function renderNav() {
        navEl.innerHTML = "";
        const groups = getGroups();
        if (!groups.length) {
          navEl.innerHTML = '<p class="kb-paragraph">No content is available yet.</p>';
          return;
        }

        if (!activeId) {
          activeId = groups[0].items[0] ? groups[0].items[0].id : "";
        }

        groups.forEach((group, index) => {
          const key = `${activeType}:${group.key}`;
          const wrap = document.createElement("section");
          wrap.className = "kb-nav-group";

          const headerBtn = document.createElement("button");
          headerBtn.className = "kb-nav-group-toggle";
          const containsActive = group.items.some((item) => item.id === activeId);
          const shouldCollapse = collapsedGroups.has(key) && !containsActive;
          headerBtn.setAttribute("aria-expanded", shouldCollapse ? "false" : "true");
          headerBtn.innerHTML = `<span>${group.label} (${group.items.length})</span><span class="kb-chevron">${shouldCollapse ? "▸" : "▾"}</span>`;
          headerBtn.addEventListener("click", () => {
            if (collapsedGroups.has(key)) {
              collapsedGroups.delete(key);
            } else {
              collapsedGroups.add(key);
            }
            renderNav();
          });
          wrap.appendChild(headerBtn);

          const list = document.createElement("ul");
          list.className = "kb-nav-list";
          if (shouldCollapse) list.style.display = "none";
          group.items
            .slice()
            .sort((a, b) => a.title.localeCompare(b.title))
            .forEach((item) => {
              const li = document.createElement("li");
              li.className = "kb-nav-item";
              const btn = document.createElement("button");
              btn.className = item.id === activeId ? "is-active" : "";
              btn.textContent = item.title;
              btn.addEventListener("click", () => {
                activeId = item.id;
                renderArticle(activeId);
                renderNav();
                hideResults();
                closeDrawer();
              });
              li.appendChild(btn);
              list.appendChild(li);
            });
          wrap.appendChild(list);
          navEl.appendChild(wrap);

          if (index === 0 && !containsActive && !activeId) {
            activeId = group.items[0] ? group.items[0].id : "";
          }
        });
      }

      function renderStudy(item) {
        return `
          <p class="kb-breadcrumb">Library / Studies / ${item.title}</p>
          <h2 class="kb-article-title">${item.title}</h2>
          ${item.subtitle ? `<p class="article-subtitle">${item.subtitle}</p>` : ""}
          <p class="kb-meta">Primary Translation: ${item.translation}</p>
          <p class="kb-paragraph">${item.summary}</p>
          <p class="kb-paragraph"><a href="${item.href}">Open study page</a></p>
        `;
      }

      function renderPassage(item) {
        const related = item.related_studies.length
          ? `<ul class="study-link-list">${item.related_studies.map((study) => `<li><a href="${study.href}">${study.title}</a></li>`).join("")}</ul>`
          : `<p class="kb-paragraph">No related study page yet.</p>`;
        return `
          <p class="kb-breadcrumb">Library / Passages / ${item.book} / ${item.title}</p>
          <h2 class="kb-article-title">${item.title}</h2>
          <p class="kb-meta">Default Display Order: LSB, NKJV, NABRE</p>
          <p class="kb-paragraph">${item.note}</p>
          <p class="kb-paragraph"><a href="${item.href}">Open passage page</a></p>
          <h3 class="kb-section-title">Related Studies</h3>
          ${related}
        `;
      }

      function renderArticle(id) {
        const item = getCurrentItems().find((entry) => entry.id === id) || getCurrentItems()[0];
        if (!item) {
          articleEl.innerHTML = '<p class="kb-paragraph">No content is available yet.</p>';
          return;
        }
        activeId = item.id;
        articleEl.innerHTML = activeType === "studies" ? renderStudy(item) : renderPassage(item);
      }

      function hideResults() {
        resultsEl.classList.remove("is-visible");
        resultsEl.innerHTML = "";
      }

      function renderResults(query) {
        const q = query.trim().toLowerCase();
        if (!q) {
          hideResults();
          return;
        }
        const hits = getCurrentItems().filter((item) => {
          const parts = [item.title, item.summary || "", item.subtitle || "", item.book || "", item.note || ""];
          return parts.join(" ").toLowerCase().includes(q);
        });
        resultsEl.classList.add("is-visible");
        if (!hits.length) {
          resultsEl.innerHTML = '<div class="kb-result-item"><h4>No results</h4><p>Try searching by study title, passage, or biblical book.</p></div>';
          return;
        }
        resultsEl.innerHTML = hits.map((item) => `
          <div class="kb-result-item" data-id="${item.id}">
            <h4>${item.title}</h4>
            <p>${activeType === "studies" ? "Study" : item.book}</p>
          </div>
        `).join("");
        resultsEl.querySelectorAll(".kb-result-item[data-id]").forEach((el) => {
          el.addEventListener("click", () => {
            activeId = el.dataset.id;
            renderArticle(activeId);
            renderNav();
            hideResults();
            searchEl.value = "";
            closeDrawer();
          });
        });
      }

      async function initLibrary() {
        try {
          const res = await fetch("../assets/library_index.json", { cache: "no-store" });
          LIBRARY_DATA = await res.json();
        } catch (e) {
          LIBRARY_DATA = { studies: [], passages: [], book_order: [] };
        }

        const params = new URLSearchParams(window.location.search);
        activeType = params.get("type") === "passages" ? "passages" : "studies";
        typeSelectEl.value = activeType;
        syncViewOptions();
        activeId = getCurrentItems()[0] ? getCurrentItems()[0].id : "";
        syncQuery();
        renderNav();
        renderArticle(activeId);

        typeSelectEl.addEventListener("change", () => {
          activeType = typeSelectEl.value;
          collapsedGroups.clear();
          syncViewOptions();
          activeId = getCurrentItems()[0] ? getCurrentItems()[0].id : "";
          searchEl.value = "";
          hideResults();
          syncQuery();
          renderNav();
          renderArticle(activeId);
        });

        viewSelectEl.addEventListener("change", () => {
          navView = viewSelectEl.value;
          renderNav();
        });

        browseBtnEl.addEventListener("click", () => {
          if (document.body.classList.contains("kb-nav-open")) closeDrawer();
          else openDrawer();
        });

        navBackdropEl.addEventListener("click", closeDrawer);

        expandAllEl.addEventListener("click", () => {
          collapsedGroups.clear();
          renderNav();
        });

        collapseAllEl.addEventListener("click", () => {
          collapsedGroups.clear();
          getGroups().forEach((group) => {
            collapsedGroups.add(`${activeType}:${group.key}`);
          });
          renderNav();
        });

        searchEl.addEventListener("input", (e) => renderResults(e.target.value));
      }

      initLibrary();
    </script>
  </body>
</html>
"""


def library_index_data(
    studies: list[Study],
    reference_map: dict[PassageReference, list[Study]],
    grouped_references: dict[str, list[PassageReference]],
) -> str:
    studies_payload = [
        {
            "id": study.slug,
            "title": study.title,
            "subtitle": study.subtitle,
            "summary": study.summary,
            "translation": study.translation,
            "href": f"../studies/{study.slug}.html",
        }
        for study in studies
    ]

    ordered_books = sorted(
        grouped_references.keys(),
        key=lambda book: (BOOK_ORDER.index(book) if book in BOOK_ORDER else 10_000, book),
    )

    passages_payload = []
    for book in ordered_books:
        refs = sorted(grouped_references[book], key=lambda ref: ref.label)
        for ref in refs:
            passages_payload.append(
                {
                    "id": ref.slug,
                    "title": ref.label,
                    "book": ref.book,
                    "citation": ref.citation,
                    "note": FEATURED_PASSAGE_NOTES.get(
                        (ref.book, ref.citation),
                        "Generated reference page linked from site studies.",
                    ),
                    "href": f"../passages/{ref.slug}.html",
                    "related_studies": [
                        {
                            "title": study.title,
                            "href": f"../studies/{study.slug}.html",
                        }
                        for study in reference_map.get(ref, [])
                    ],
                }
            )

    payload = {
        "studies": studies_payload,
        "passages": passages_payload,
        "book_order": ordered_books,
    }
    return json.dumps(payload, ensure_ascii=True, indent=2)


def studies_redirect_html() -> str:
    return """<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta http-equiv="refresh" content="0; url=../library/index.html" />
    <title>Redirecting...</title>
  </head>
  <body>
    <p><a href="../library/index.html">Go to the library.</a></p>
  </body>
</html>
"""


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    LIBRARY_DIR.mkdir(parents=True, exist_ok=True)
    PASSAGES_DIR.mkdir(parents=True, exist_ok=True)
    studies = []
    for path in sorted(SOURCE_DIR.glob("*.md")):
        if path.name in SKIP_FILES:
            continue
        studies.append(parse_study(path))

    featured_rank = {name: index for index, name in enumerate(FEATURED_STUDY_ORDER)}
    studies.sort(
        key=lambda study: (
            featured_rank.get(study.source_name, 10_000),
            study.title.lower(),
        )
    )

    reference_map: dict[PassageReference, list[Study]] = defaultdict(list)
    grouped_references: dict[str, list[PassageReference]] = defaultdict(list)
    for study in studies:
        for reference in study.references:
            reference_map[reference].append(study)
            if reference not in grouped_references[reference.book]:
                grouped_references[reference.book].append(reference)

    for source_name in PASSAGE_SOURCE_FILES:
        source_path = SOURCE_DIR / source_name
        if not source_path.exists():
            continue
        for reference in extract_references(source_path.read_text(encoding="utf-8")):
            if reference not in grouped_references[reference.book]:
                grouped_references[reference.book].append(reference)
            reference_map.setdefault(reference, [])

    featured_references = []
    for book, citation in FEATURED_PASSAGE_ORDER:
        reference = passage_reference(book, citation)
        if reference in reference_map:
            featured_references.append(reference)

    for study in studies:
        output_path = OUTPUT_DIR / f"{study.slug}.html"
        output_path.write_text(study_page_html(study), encoding="utf-8")

    for reference, linked_studies in reference_map.items():
        output_path = PASSAGES_DIR / f"{reference.slug}.html"
        output_path.write_text(
            passage_page_html(reference, linked_studies),
            encoding="utf-8",
        )

    (LIBRARY_DIR / "index.html").write_text(library_index_html(studies), encoding="utf-8")
    (LIBRARY_DIR / "browse.html").write_text(browse_page_html(), encoding="utf-8")
    (LIBRARY_DIR / "studies-all.html").write_text(studies_all_html(studies), encoding="utf-8")
    (LIBRARY_DIR / "passages.html").write_text(
        featured_passages_html(featured_references),
        encoding="utf-8",
    )
    (LIBRARY_DIR / "passages-by-book.html").write_text(
        passages_by_book_html(grouped_references),
        encoding="utf-8",
    )
    (WEB_DIR / "assets" / "library_index.json").write_text(
        library_index_data(studies, reference_map, grouped_references),
        encoding="utf-8",
    )
    (OUTPUT_DIR / "index.html").write_text(studies_redirect_html(), encoding="utf-8")


if __name__ == "__main__":
    main()
