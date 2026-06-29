#!/usr/bin/env python3

from __future__ import annotations

import html
import re
from dataclasses import dataclass
from pathlib import Path


ROOT = Path("/home/cozwood/Documents/Dev/the_way_of_scripture")
SOURCE_DIR = ROOT / "content" / "studies"
WEB_DIR = ROOT / "apps" / "web"
OUTPUT_DIR = WEB_DIR / "studies"
SKIP_FILES = {"way_of_scripture_intro.md"}


@dataclass
class Study:
    title: str
    subtitle: str
    translation: str
    slug: str
    source_name: str
    summary: str
    body_html: str


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug or "study"


def render_inline(text: str) -> str:
    rendered = html.escape(text)
    rendered = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", rendered)
    rendered = re.sub(r"\*(.+?)\*", r"<em>\1</em>", rendered)
    return rendered


def render_blocks(lines: list[str]) -> str:
    output: list[str] = []
    i = 0

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
            output.append(f"<h3>{render_inline(stripped[4:])}</h3>")
            i += 1
            continue

        if stripped.startswith("## "):
            output.append(f"<h2>{render_inline(stripped[3:])}</h2>")
            i += 1
            continue

        if stripped.startswith("> "):
            quote_lines: list[str] = []
            while i < len(lines) and lines[i].strip().startswith("> "):
                quote_lines.append(lines[i].strip()[2:])
                i += 1
            quote_text = " ".join(part.strip() for part in quote_lines)
            output.append(f"<blockquote><p>{render_inline(quote_text)}</p></blockquote>")
            continue

        if stripped.startswith("- "):
            items: list[str] = []
            while i < len(lines) and lines[i].strip().startswith("- "):
                items.append(lines[i].strip()[2:])
                i += 1
            rendered_items = "".join(
                f"<li>{render_inline(item)}</li>" for item in items
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
        output.append(f"<p>{render_inline(paragraph)}</p>")

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
    body_html = render_blocks(body_lines)
    slug = slugify(path.stem.replace("_", "-"))

    return Study(
        title=title or path.stem.replace("_", " ").title(),
        subtitle=subtitle,
        translation=translation,
        slug=slug,
        source_name=path.name,
        summary=summary,
        body_html=body_html,
    )


def study_page_html(study: Study, all_studies: list[Study]) -> str:
    other_links = "\n".join(
        f'                <li><a href="./{item.slug}.html">{html.escape(item.title)}</a></li>'
        for item in all_studies
    )
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
        <nav class="site-nav" aria-label="Primary">
          <a href="../index.html">Home</a>
          <a href="./index.html">Studies</a>
        </nav>
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
              <h2>Study Library</h2>
              <ul class="study-link-list">
{other_links}
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


def studies_index_html(studies: list[Study]) -> str:
    cards = []
    for study in studies:
        cards.append(
            f"""          <article class="study-card">
            <p class="eyebrow">Study</p>
            <h2><a href="./{study.slug}.html">{html.escape(study.title)}</a></h2>
            <p class="study-card-subtitle">{html.escape(study.subtitle)}</p>
            <p>{html.escape(study.summary)}</p>
            <a class="study-card-link" href="./{study.slug}.html">Read study</a>
          </article>"""
        )

    return f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Studies | The Way of Scripture</title>
    <meta
      name="description"
      content="Study library for The Way of Scripture."
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
        </nav>
      </header>

      <main>
        <section class="article-hero">
          <p class="eyebrow">Study Library</p>
          <h1>Studies</h1>
          <p class="lead">
            Source-driven study pages generated from the repository study markdown files.
          </p>
        </section>

        <section class="study-card-grid">
{chr(10).join(cards)}
        </section>
      </main>
    </div>
  </body>
</html>
"""


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    studies = []
    for path in sorted(SOURCE_DIR.glob("*.md")):
        if path.name in SKIP_FILES:
            continue
        studies.append(parse_study(path))

    for study in studies:
        output_path = OUTPUT_DIR / f"{study.slug}.html"
        output_path.write_text(study_page_html(study, studies), encoding="utf-8")

    (OUTPUT_DIR / "index.html").write_text(studies_index_html(studies), encoding="utf-8")


if __name__ == "__main__":
    main()
