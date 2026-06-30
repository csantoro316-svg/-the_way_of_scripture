#!/usr/bin/env python3

from __future__ import annotations

import html
import json
import re
from dataclasses import dataclass
from pathlib import Path
from collections import defaultdict

from passage_chapter_contexts import CHAPTER_CONTEXTS


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
ORDERED_LIST_PATTERN = re.compile(r"^\d+\.\s+")


@dataclass
class Study:
    title: str
    subtitle: str
    translation: str
    slug: str
    source_name: str
    summary: str
    intro_html: str
    body_html: str
    body_lines: list[str]
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


@dataclass(frozen=True)
class PassageVersion:
    label: str
    text: str


@dataclass(frozen=True)
class PassageContent:
    verses: list[PassageVersion]
    context_lines: list[str]
    explanation_lines: list[str]


@dataclass(frozen=True)
class MarkdownBlock:
    kind: str
    text: str


KNOWN_PASSAGE_REFERENCES: set["PassageReference"] = set()


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


def passage_href(reference: PassageReference, depth: str = "..") -> str:
    return f"{depth}/passages/{reference.slug}.html"


def passage_link_attrs() -> str:
    return ' target="_blank" rel="noopener noreferrer"'


def render_reference_links(
    text: str,
    current_reference: PassageReference | None = None,
) -> str:
    rendered = html.escape(text)

    def replace(match: re.Match[str]) -> str:
        book = match.group(1).strip()
        citation = match.group(2).strip()
        ref = PassageReference(book=book, citation=citation)
        label = html.escape(f"{book} {citation}")
        if current_reference and ref == current_reference:
            return label
        if KNOWN_PASSAGE_REFERENCES and ref not in KNOWN_PASSAGE_REFERENCES:
            return label
        return f'<a href="{passage_href(ref)}"{passage_link_attrs()}>{label}</a>'

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


def render_blocks(
    lines: list[str],
    enable_reference_links: bool = False,
    current_reference: PassageReference | None = None,
) -> str:
    output: list[str] = []
    i = 0
    inline_renderer = (
        (lambda text: render_reference_links(text, current_reference=current_reference))
        if enable_reference_links
        else render_inline
    )

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

        if stripped.startswith("#### "):
            output.append(f"<h4>{inline_renderer(stripped[5:])}</h4>")
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

        if ORDERED_LIST_PATTERN.match(stripped):
            items: list[str] = []
            while i < len(lines) and ORDERED_LIST_PATTERN.match(lines[i].strip()):
                items.append(ORDERED_LIST_PATTERN.sub("", lines[i].strip(), count=1))
                i += 1
            rendered_items = "".join(
                f"<li>{inline_renderer(item)}</li>" for item in items
            )
            output.append(f'<ol class="prose-list">{rendered_items}</ol>')
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
                or next_stripped.startswith("#### ")
                or next_stripped.startswith("> ")
                or next_stripped.startswith("- ")
                or ORDERED_LIST_PATTERN.match(next_stripped)
            ):
                break
            paragraph_lines.append(next_stripped)
            i += 1
        paragraph = " ".join(paragraph_lines)
        output.append(f"<p>{inline_renderer(paragraph)}</p>")

    return "\n              ".join(output)


def markdown_blocks(lines: list[str]) -> list[MarkdownBlock]:
    blocks: list[MarkdownBlock] = []
    i = 0
    while i < len(lines):
        stripped = lines[i].strip()
        if not stripped:
            i += 1
            continue
        if stripped == "---":
            i += 1
            continue
        if stripped.startswith("#### "):
            blocks.append(MarkdownBlock(kind="heading4", text=stripped[5:].strip()))
            i += 1
            continue
        if stripped.startswith("### "):
            blocks.append(MarkdownBlock(kind="heading3", text=stripped[4:].strip()))
            i += 1
            continue
        if stripped.startswith("## "):
            blocks.append(MarkdownBlock(kind="heading2", text=stripped[3:].strip()))
            i += 1
            continue
        if stripped.startswith("> "):
            quote_lines: list[str] = []
            while i < len(lines) and lines[i].strip().startswith("> "):
                quote_lines.append(lines[i].strip()[2:])
                i += 1
            blocks.append(MarkdownBlock(kind="quote", text=" ".join(quote_lines).strip()))
            continue
        if stripped.startswith("- "):
            items: list[str] = []
            while i < len(lines) and lines[i].strip().startswith("- "):
                items.append(lines[i].strip()[2:])
                i += 1
            blocks.append(MarkdownBlock(kind="list", text="\n".join(items)))
            continue
        if ORDERED_LIST_PATTERN.match(stripped):
            items: list[str] = []
            while i < len(lines) and ORDERED_LIST_PATTERN.match(lines[i].strip()):
                items.append(ORDERED_LIST_PATTERN.sub("", lines[i].strip(), count=1))
                i += 1
            blocks.append(MarkdownBlock(kind="list", text="\n".join(items)))
            continue

        paragraph_lines = [stripped]
        i += 1
        while i < len(lines):
            next_stripped = lines[i].strip()
            if (
                not next_stripped
                or next_stripped == "---"
                or next_stripped.startswith("## ")
                or next_stripped.startswith("### ")
                or next_stripped.startswith("#### ")
                or next_stripped.startswith("> ")
                or next_stripped.startswith("- ")
                or ORDERED_LIST_PATTERN.match(next_stripped)
            ):
                break
            paragraph_lines.append(next_stripped)
            i += 1
        blocks.append(MarkdownBlock(kind="paragraph", text=" ".join(paragraph_lines)))
    return blocks


def summarize_blocks(lines: list[str]) -> str:
    parts: list[str] = []
    for block in markdown_blocks(lines):
        if block.kind == "paragraph":
            text = re.sub(r"\s+", " ", block.text).strip()
            text = text.replace("**", "").replace("*", "")
            parts.append(text)
        elif block.kind == "list":
            items = [
                re.sub(r"\s+", " ", item).strip().replace("**", "").replace("*", "")
                for item in block.text.splitlines()
            ]
            parts.extend(item for item in items if item)
    return " ".join(part for part in parts if part).strip()


def hoist_leading_body_intro(body_lines: list[str]) -> tuple[list[str], list[str]]:
    if not body_lines:
        return [], body_lines

    i = 0
    while i < len(body_lines) and not body_lines[i].strip():
        i += 1

    if i >= len(body_lines):
        return [], body_lines

    first_heading_index = None
    if body_lines[i].strip().startswith("## "):
        first_heading_index = i
        i += 1
        while i < len(body_lines) and not body_lines[i].strip():
            i += 1

    intro_start = i
    saw_paragraph_content = False

    while i < len(body_lines):
        stripped = body_lines[i].strip()
        if not stripped:
            if saw_paragraph_content:
                i += 1
                continue
            break
        if (
            stripped == "---"
            or stripped.startswith("## ")
            or stripped.startswith("### ")
            or stripped.startswith("#### ")
            or stripped.startswith("> ")
            or stripped.startswith("- ")
            or ORDERED_LIST_PATTERN.match(stripped)
        ):
            break
        saw_paragraph_content = True
        i += 1

    intro_lines = body_lines[intro_start:i]
    if not summarize_blocks(intro_lines):
        return [], body_lines

    remove_start = first_heading_index if first_heading_index is not None else intro_start
    remaining_lines = body_lines[i:]
    while remaining_lines and not remaining_lines[0].strip():
        remaining_lines = remaining_lines[1:]
    if remaining_lines and remaining_lines[0].strip() == "---":
        remaining_lines = remaining_lines[1:]
        while remaining_lines and not remaining_lines[0].strip():
            remaining_lines = remaining_lines[1:]

    return intro_lines, body_lines[:remove_start] + remaining_lines


def block_mentions_reference(block: MarkdownBlock, reference: PassageReference) -> bool:
    return reference.label in block.text


def extract_lsb_verse_text(reference: PassageReference, studies: list[Study]) -> str | None:
    heading_marker = f"### {reference.label}"
    reference_pattern = re.compile(rf"\*\*{re.escape(reference.label)}(?:\*\*|\s*\()")
    verse_pattern = re.compile(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)")
    for study in studies:
        lines = study.body_lines
        for idx, line in enumerate(lines):
            stripped = line.strip()
            if stripped.startswith("> ") and reference_pattern.search(stripped):
                quote_lines = [stripped[2:]]
                j = idx + 1
                while j < len(lines) and lines[j].strip().startswith("> "):
                    quote_lines.append(lines[j].strip()[2:])
                    j += 1
                quote_text = " ".join(quote_lines)
                matches = verse_pattern.findall(quote_text)
                if matches:
                    return max((match.strip() for match in matches), key=len)
            if stripped == heading_marker:
                j = idx + 1
                while j < len(lines) and not lines[j].strip():
                    j += 1
                quote_lines: list[str] = []
                while j < len(lines) and lines[j].strip().startswith("> "):
                    quote_lines.append(lines[j].strip()[2:])
                    j += 1
                if quote_lines:
                    matches = verse_pattern.findall(" ".join(quote_lines))
                    if matches:
                        return max((match.strip() for match in matches), key=len)
    return None


def extract_explanation_lines(reference: PassageReference, studies: list[Study]) -> list[str]:
    seen: set[str] = set()
    for study in studies:
        blocks = markdown_blocks(study.body_lines)
        gathered: list[str] = []

        exact_heading_indexes = [
            idx for idx, block in enumerate(blocks)
            if block.kind in {"heading2", "heading3"} and block.text.strip() == reference.label
        ]
        candidate_indexes = exact_heading_indexes or [
            idx for idx, block in enumerate(blocks) if block_mentions_reference(block, reference)
        ]
        for idx in candidate_indexes:
            block = blocks[idx]

            candidate_texts: list[str] = []
            if block.kind == "paragraph":
                candidate_texts.append(block.text)

            capture_count = 0
            for next_block in blocks[idx + 1:]:
                if next_block.kind in {"heading2", "heading3"} and capture_count:
                    break
                if next_block.kind == "paragraph":
                    candidate_texts.append(next_block.text)
                    capture_count += 1
                elif next_block.kind == "list" and capture_count < 2:
                    candidate_texts.append("\n".join(f"- {item}" for item in next_block.text.splitlines()))
                    capture_count += 1
                elif next_block.kind == "quote":
                    continue
                if capture_count >= 2:
                    break

            for text in candidate_texts:
                normalized = re.sub(r"\s+", " ", text).strip()
                if not normalized or normalized in seen:
                    continue
                seen.add(normalized)
                gathered.extend(text.splitlines())
                gathered.append("")
            if len(gathered) >= 6:
                break

        while gathered and not gathered[-1].strip():
            gathered.pop()
        if gathered:
            return gathered

    return []


def build_passage_content(reference: PassageReference, linked_studies: list[Study]) -> PassageContent:
    override = PASSAGE_CONTENT.get(reference)
    if override:
        return override

    chapter = reference.citation.split(":", 1)[0]
    context_lines = CHAPTER_CONTEXTS.get(
        (reference.book, chapter),
        [f"{reference.label} should be read within the flow of its chapter and the larger argument of {reference.book}."],
    )
    explanation_lines = extract_explanation_lines(reference, linked_studies)
    verses: list[PassageVersion] = []
    lsb_text = extract_lsb_verse_text(reference, linked_studies)
    if lsb_text:
        verses.append(PassageVersion(label="LSB", text=lsb_text))

    if not explanation_lines:
        explanation_lines = [
            f"{reference.label} should be read first within its own scriptural setting rather than as an isolated slogan.",
            "",
            "Where this passage is brought into conversation with other texts, its force should still be governed by its immediate chapter flow and the larger argument of the book.",
        ]

    return PassageContent(
        verses=verses,
        context_lines=context_lines,
        explanation_lines=explanation_lines,
    )


PASSAGE_CONTENT: dict[PassageReference, PassageContent] = {
    passage_reference("1 John", "5:14-15"): PassageContent(
        verses=[
            PassageVersion(
                label="LSB",
                text=(
                    "Now this is the confidence which we have before Him, that if we ask "
                    "anything according to His will, He hears us. And if we know that He "
                    "hears us in whatever we ask, we know that we have the requests which "
                    "we have asked from Him."
                ),
            ),
            PassageVersion(
                label="NKJV",
                text=(
                    "Now this is the confidence that we have in Him, that if we ask "
                    "anything according to His will, He hears us. And if we know that He "
                    "hears us, whatever we ask, we know that we have the petitions that we "
                    "have asked of Him."
                ),
            ),
            PassageVersion(
                label="NABRE",
                text=(
                    "And we have this confidence in him, that if we ask anything according "
                    "to his will, he hears us. And if we know that he hears us in regard to "
                    "whatever we ask, we know that what we have asked him for is ours."
                ),
            ),
        ],
        context_lines=[
            "**1 John 5:14-15** comes near the close of the letter, where John is drawing "
            "together his pastoral purpose: that believers may know the life they have in the "
            "Son and live with confidence before God.",
            "",
            "The immediate context matters. In **1 John 5:13**, John says he is writing so "
            "that believers may know they have eternal life. Then in verses 14-15 he moves "
            "straight into confidence in prayer, and in verses 16-17 he applies that confidence "
            "to a concrete case involving prayer for a brother in sin. The passage is therefore "
            "not an isolated slogan about getting what one wants from God. It sits inside a "
            "larger argument about abiding in the Son, walking in truth, and praying in a way "
            "consistent with God's own life and character.",
            "",
            "That wider setting also guards against cherry-picking. Throughout **1 John**, John "
            "contrasts truth and falsehood, obedience and disobedience, love and hatred, life "
            "and death. By the time chapter 5 arrives, confidence before God is already tied to "
            "remaining in Him, believing rightly about Christ, and keeping His commandments. "
            "Verses 14-15 belong inside that whole framework.",
        ],
        explanation_lines=[
            "The promise is conditional at every step. The text does not say, 'ask and you will "
            "receive' without qualification. It says that **if** we ask according to His will, "
            "**then** He hears us; and if He hears us, **then** we know we have what we asked.",
            "",
            "That means the controlling issue is not sincerity, repetition, or emotional force. "
            "The controlling issue is alignment with God's will. John places confidence in "
            "prayer under God's rule, not under human desire.",
            "",
            "Read that way, the verse becomes a boundary for other prayer passages. "
            "**Acts 4:29-31** shows believers asking for boldness so the word of God may go "
            "forward, and the request is granted. By contrast, **2 Corinthians 12:7-9** and "
            "**Romans 15:30-32** show that even earnest, specific requests are not granted "
            "simply because they are heartfelt. The issue remains whether the request serves "
            "God's purpose rather than personal relief or preference.",
            "",
            "The same principle fits naturally with **John 15:7**, where abiding in Christ shapes "
            "what is desired and asked, and with **Romans 8:26-27**, where the Spirit intercedes "
            "according to the will of God when believers do not know how to pray as they should. "
            "Taken together, **1 John 5:14-15** presents prayer as confidence under God's will, "
            "not leverage for securing personal outcomes.",
        ],
    ),
}


def parse_study(path: Path) -> Study:
    lines = path.read_text(encoding="utf-8").splitlines()
    title = ""
    subtitle = ""
    translation = "Legacy Standard Bible (LSB)"
    body_start = 0
    seen_header_divider = False

    for idx, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("# ") and not title:
            title = stripped[2:].strip()
            body_start = idx + 1
            continue
        if stripped == "---":
            seen_header_divider = True
            continue
        if stripped.startswith("## ") and not subtitle and not seen_header_divider:
            subtitle = stripped[3:].strip()
            continue
        if stripped.startswith("*Primary Translation:"):
            translation = stripped.strip("*").replace("Primary Translation:", "").strip()
            continue
    if not subtitle:
        preface_lines: list[str] = []
        preface_raw_lines: list[str] = []
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
                preface_raw_lines.append(stripped)
                preface_lines.append(stripped.strip("*").strip())

        stylized_preface = bool(preface_raw_lines) and all(
            raw.startswith("*") and raw.endswith("*") for raw in preface_raw_lines
        )

        if preface_lines and stylized_preface:
            subtitle = preface_lines[0]

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

    intro_started = False
    intro_complete = False
    intro_lines: list[str] = []
    body_lines: list[str] = []

    for line in filtered_body:
        stripped = line.strip()
        if not intro_complete:
            if not stripped:
                if intro_started and intro_lines:
                    intro_lines.append(line)
                continue
            if stripped == "---":
                if not intro_started:
                    intro_started = True
                    continue
                intro_complete = True
                continue
            if not intro_started:
                continue
            if stripped.startswith("## "):
                intro_complete = True
                body_lines.append(line)
                continue
            intro_lines.append(line)
            continue
        body_lines.append(line)

    if not intro_complete and intro_lines:
        body_lines = []

    if not intro_lines:
        hoisted_intro_lines, body_lines = hoist_leading_body_intro(body_lines)
        if hoisted_intro_lines:
            intro_lines = hoisted_intro_lines

    study_text = "\n".join(intro_lines + body_lines)
    references = extract_references(study_text)
    intro_html = render_blocks(intro_lines, enable_reference_links=True)
    body_html = render_blocks(body_lines, enable_reference_links=True)
    summary = summarize_blocks(intro_lines)
    if not summary:
        summary = title or path.stem.replace("_", " ").title()
    slug = slugify(path.stem.replace("_", "-"))

    return Study(
        title=title or path.stem.replace("_", " ").title(),
        subtitle=subtitle,
        translation=translation,
        slug=slug,
        source_name=path.name,
        summary=summary,
        intro_html=intro_html,
        body_html=body_html,
        body_lines=body_lines,
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
    intro_html = study.intro_html or f'<p class="lead">{html.escape(study.summary)}</p>'
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
          <div class="article-hero-copy prose">
            {intro_html}
          </div>
        </section>

        <div class="article-layout">
          <article class="article-body">
            <div class="prose">
              {study.body_html}
            </div>
          </article>
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


def render_passage_versions(versions: list[PassageVersion]) -> str:
    return "\n".join(
        f"""          <div class="passage-version">
            <h2>{html.escape(version.label)}</h2>
            <blockquote><p>{html.escape(version.text)}</p></blockquote>
          </div>"""
        for version in versions
    )


def render_passage_hero(reference: PassageReference) -> str:
    content = build_passage_content(reference, [])
    if not content.verses:
        return """          <p class="lead">Full passage content has not been curated from the study material yet.</p>"""

    return render_passage_versions(content.verses)


def render_passage_body_sections(reference: PassageReference, linked_studies: list[Study]) -> str:
    content = build_passage_content(reference, linked_studies)
    if not content:
        return """              <h2>Context</h2>
              <p>
                This passage page exists as a navigation target, but its study-derived context
                and explanation still need to be written.
              </p>

              <h2>Explanation</h2>
              <p>
                This passage still needs its full treatment from the source material.
              </p>"""

    context_html = render_blocks(
        content.context_lines,
        enable_reference_links=True,
        current_reference=reference,
    )
    explanation_html = render_blocks(
        content.explanation_lines,
        enable_reference_links=True,
        current_reference=reference,
    )
    return f"""              <h2>Context</h2>
              {context_html}

              <h2>Explanation</h2>
              {explanation_html}"""


def passage_page_html(reference: PassageReference, linked_studies: list[Study]) -> str:
    content = build_passage_content(reference, linked_studies)
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
{render_passage_versions(content.verses) if content.verses else '          <p class="lead">Full passage text for this reference is not yet quoted in the current local source material.</p>'}
        </section>

        <div class="article-layout">
          <article class="article-body">
            <div class="prose">
{render_passage_body_sections(reference, linked_studies)}
            </div>
          </article>
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
            <h2><a href="{passage_href(reference)}"{passage_link_attrs()}>{html.escape(reference.label)}</a></h2>
            <p>{html.escape(note)}</p>
            <a class="study-card-link" href="{passage_href(reference)}"{passage_link_attrs()}>Read passage</a>
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
          <p class="kb-paragraph">${item.note}</p>
          <p class="kb-paragraph"><a href="${item.href}" target="_blank" rel="noopener noreferrer">Open passage page</a></p>
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

    KNOWN_PASSAGE_REFERENCES.clear()
    KNOWN_PASSAGE_REFERENCES.update(reference_map.keys())

    for study in studies:
        study.body_html = render_blocks(study.body_lines, enable_reference_links=True)

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
