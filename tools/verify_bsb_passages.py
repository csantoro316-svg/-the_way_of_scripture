#!/usr/bin/env python3
"""Compare selected source quotations directly with BibleHub's BSB text."""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
from pathlib import Path
from urllib.request import urlopen

SOURCE_DIR = Path(__file__).resolve().parents[1] / "content" / "passages"


def biblehub_verses(raw: str) -> dict[int, str]:
    # Stop before footnotes and study summaries; neither is Scripture text.
    raw = re.split(r'<a\s+name="fn"|<div\s+id="botbox"', raw, maxsplit=1, flags=re.I)[0]
    marker = re.compile(r'<span class="reftext">\s*<a\b[^>]*>\s*<b>(\d+)</b>\s*</a>\s*</span>', re.I)
    matches = list(marker.finditer(raw))
    verses = {}
    for index, match in enumerate(matches):
        chunk = raw[match.end():matches[index + 1].start() if index + 1 < len(matches) else len(raw)]
        chunk = re.sub(r'<p class="(?:subhdg|hdg)">.*?(?=<p\b|$)', '', chunk, flags=re.S | re.I)
        chunk = re.sub(r'<span class="(?:fn|cross)">.*?</span>', '', chunk, flags=re.S | re.I)
        verses[int(match.group(1))] = normalize(html.unescape(re.sub(r'<[^>]+>', ' ', chunk)))
    if not verses:
        raise ValueError("BibleHub verse markup was not recognized; no quotation was verified")
    return verses


def normalize(text: str) -> str:
    return re.sub(r'\s+', ' ', text).strip()


def quotation_matches(local: str, verses: dict[int, str], start: int, end: int) -> bool:
    """Accept printed verse labels without removing numbers in Scripture itself."""
    plain = normalize(' '.join(verses[number] for number in range(start, end + 1)))
    numbered = normalize(' '.join(f'{number} {verses[number]}' for number in range(start, end + 1)))
    return normalize(local) in (plain, numbered)


def verify(slug: str) -> None:
    source = json.loads((SOURCE_DIR / f"{slug}.json").read_text())
    reference = source["reference"]
    match = re.fullmatch(r'(\d+):(\d+)(?:-(\d+))?', reference["citation"])
    if not match:
        raise ValueError("Verify cross-chapter quotations separately")
    chapter, start, end = (int(match.group(1)), int(match.group(2)), int(match.group(3) or match.group(2)))
    book = {'Psalm': 'psalms', 'Song of Solomon': 'songs'}.get(reference["book"], reference["book"].lower().replace(' ', '_'))
    url = f"https://biblehub.com/bsb/{book}/{chapter}.htm"
    with urlopen(url, timeout=30) as response:
        verses = biblehub_verses(response.read().decode('utf-8'))
    remote = normalize(' '.join(verses[number] for number in range(start, end + 1)))
    versions = [version for version in source["versions"] if version["label"] == "BSB"]
    if len(versions) != 1:
        raise ValueError("Expected exactly one BSB source block")
    version = versions[0]
    local = ' '.join(version.get("paragraphs", [])) or version.get("text", "")
    if not quotation_matches(local, verses, start, end):
        raise ValueError(f"{slug}: BSB wording differs from {url}")
    print(f"{slug}: verified against {url}; normalized SHA-256 {hashlib.sha256(remote.encode()).hexdigest()}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("slugs", nargs="+")
    for slug in parser.parse_args().slugs:
        verify(slug)
