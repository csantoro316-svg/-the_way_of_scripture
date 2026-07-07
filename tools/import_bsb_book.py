#!/usr/bin/env python3

from __future__ import annotations

import argparse
import html
import json
import re
import sys
import urllib.request
from pathlib import Path

from passage_chapter_contexts import CHAPTER_CONTEXTS


ROOT = Path("/home/cozwood/Documents/Dev/the_way_of_scripture")
PASSAGE_SOURCE_DIR = ROOT / "content" / "passages"
BASE_URL = "https://www.tblz.org/bible"

BOOK_CHAPTERS = {
    "Genesis": 50,
    "Exodus": 40,
    "Deuteronomy": 34,
    "1 Samuel": 31,
    "Judges": 21,
    "Proverbs": 31,
    "Isaiah": 66,
    "Jeremiah": 52,
    "Malachi": 4,
}

HEADING_RE = re.compile(r"<h4>(.*?)</h4>", re.DOTALL | re.IGNORECASE)
TAG_RE = re.compile(r"<[^>]+>")
VERSE_RE = re.compile(r'<sup class="ref"><a name="(\d+)">', re.IGNORECASE)


def slugify(text: str) -> str:
    value = text.strip().lower()
    value = value.replace("&", "and")
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")


def clean_heading(raw: str) -> str:
    raw = re.sub(r"<br\s*/?>.*", "", raw, flags=re.DOTALL | re.IGNORECASE)
    text = TAG_RE.sub("", raw)
    text = html.unescape(text)
    return " ".join(text.split()).strip()


def clean_text_block(raw: str) -> str:
    raw = re.sub(r"<a href=\"#fn\".*?</a>", "", raw, flags=re.DOTALL | re.IGNORECASE)
    raw = re.sub(r"<span class=\"fn1\">.*?</span>", "", raw, flags=re.DOTALL | re.IGNORECASE)
    raw = re.sub(r"<a name=.*?>", "", raw, flags=re.DOTALL | re.IGNORECASE)
    raw = raw.replace("&nbsp;", " ")
    text = TAG_RE.sub("", raw)
    text = html.unescape(text)
    text = re.sub(r"\s+", " ", text)
    for marker in (
        "300 Pollock RdState College",
        "About Bible Beliefs Teaching Values",
        "© 2020-2026 Trailblazers Church",
    ):
        if marker in text:
            text = text.split(marker, 1)[0].strip()
    return text.strip()


def fetch(url: str) -> str:
    with urllib.request.urlopen(url) as response:
        return response.read().decode("utf-8")


def chapter_url(book: str, chapter: int) -> str:
    return f"{BASE_URL}/{slugify(book)}-{chapter}.php"


def parse_sections(book: str, chapter: int, page_html: str) -> list[dict[str, object]]:
    matches = list(HEADING_RE.finditer(page_html))
    sections: list[dict[str, object]] = []

    for index, match in enumerate(matches):
        title = clean_heading(match.group(1))
        if not title:
            continue
        if title.startswith("<") or "Previous Chapter" in title or "Next Chapter" in title:
            continue

        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(page_html)
        block = page_html[start:end]
        if "<b>Footnotes:</b>" in block:
            block = block.split("<b>Footnotes:</b>", 1)[0]

        verses = [int(value) for value in VERSE_RE.findall(block)]
        if not verses:
            continue

        paragraphs = re.findall(r"<p[^>]*>(.*?)</p>", block, re.DOTALL | re.IGNORECASE)
        text_parts: list[str] = []
        for paragraph in paragraphs:
            cleaned = clean_text_block(paragraph)
            if not cleaned:
                continue
            if cleaned == "\u00a0":
                continue
            text_parts.append(cleaned)

        if not text_parts:
            continue

        text = " ".join(text_parts).strip()
        start_verse = min(verses)
        end_verse = max(verses)
        citation = f"{chapter}:{start_verse}-{end_verse}" if start_verse != end_verse else f"{chapter}:{start_verse}"

        sections.append(
            {
                "book": book,
                "chapter": chapter,
                "citation": citation,
                "title": title,
                "text": text,
                "paragraphs": text_parts,
            }
        )

    return sections


def build_context_lines(book: str, chapter: int) -> list[str]:
    context = CHAPTER_CONTEXTS.get((book, str(chapter)))
    if context:
        return context
    return [
        f"In **{book} {chapter}**, this section should be read within the flow of the chapter and the larger movement of {book}.",
    ]


def build_common_interpretations(book: str, chapter: int, section_title: str) -> list[str]:
    return [
        f"A common reading of **{section_title}** is that it should be interpreted in light of the chapter's full narrative movement rather than as an isolated proof text.",
        "",
        f"Where interpreters differ on details, the immediate setting in **{book} {chapter}** remains the first control on meaning.",
    ]


def load_existing(path: Path) -> dict[str, object] | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def build_payload(section: dict[str, object], existing: dict[str, object] | None) -> dict[str, object]:
    book = str(section["book"])
    citation = str(section["citation"])
    label = f"{book} {citation}"
    slug = slugify(f"{book}-{citation}")
    chapter = int(str(section["chapter"]))
    section_title = str(section["title"])
    text = str(section["text"])
    paragraphs = [
        str(paragraph).strip()
        for paragraph in section.get("paragraphs", [])
        if str(paragraph).strip()
    ]

    existing_context = existing.get("context_lines") if existing else None
    existing_common = None
    if existing:
        existing_common = existing.get("common_interpretation_lines", existing.get("explanation_lines"))
    existing_deeper = existing.get("deeper_study") if existing else None
    existing_current_position = existing.get("current_position_lines") if existing else None
    existing_title = str(existing.get("section_title", "")).strip() if existing else ""

    payload = {
        "reference": {
            "book": book,
            "citation": citation,
            "label": label,
            "slug": slug,
        },
        "section_title": existing_title or section_title,
        "versions": [
            {
                "label": "BSB",
                **({"paragraphs": paragraphs} if paragraphs else {"text": text}),
            }
        ],
        "context_lines": existing_context or build_context_lines(book, chapter),
        "common_interpretation_lines": existing_common or build_common_interpretations(book, chapter, section_title),
        "deeper_study": existing_deeper or [],
    }
    if existing_current_position is not None:
        payload["current_position_lines"] = existing_current_position
    return payload


def import_book(book: str) -> tuple[int, int]:
    total = 0
    written = 0
    chapter_count = BOOK_CHAPTERS[book]
    PASSAGE_SOURCE_DIR.mkdir(parents=True, exist_ok=True)

    for chapter in range(1, chapter_count + 1):
        html_text = fetch(chapter_url(book, chapter))
        sections = parse_sections(book, chapter, html_text)
        total += len(sections)
        for section in sections:
            slug = slugify(f"{section['book']}-{section['citation']}")
            path = PASSAGE_SOURCE_DIR / f"{slug}.json"
            payload = build_payload(section, load_existing(path))
            path.write_text(json.dumps(payload, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
            written += 1

    return total, written


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("book", choices=sorted(BOOK_CHAPTERS))
    args = parser.parse_args()

    total, written = import_book(args.book)
    print(f"Imported {args.book}: {total} section(s), wrote {written} file(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
