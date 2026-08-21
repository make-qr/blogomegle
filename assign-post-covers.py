#!/usr/bin/env python3
"""Add hero_image frontmatter to posts missing cover art."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
POSTS = ROOT / "_posts"

POST_HERO_URLS = {
    "late-bloom-part-ii-messages-never-sent": "https://images.unsplash.com/photo-1516589178581-6cd7833ae3b2?w=1200&q=80",
    "late-bloom-part-iii-broken-mirror-rain-street": "https://images.unsplash.com/photo-1428908728789-d2de25dbd4e2?w=1200&q=80",
    "late-bloom-part-iv-one-year-contract": "https://images.unsplash.com/photo-1529333166437-7750a6dd5a70?w=1200&q=80",
    "late-bloom-part-v-friend-from-that-year": "https://images.unsplash.com/photo-1529156069898-49953e39b3ac?w=1200&q=80",
    "late-bloom-part-vi-noodle-shop-number-seven": "https://images.unsplash.com/photo-1555126634-323283e090fa?w=1200&q=80",
    "late-bloom-part-vii-8-hours-apart": "https://images.unsplash.com/photo-1470229722913-7c0e2dbbafd3?w=1200&q=80",
    "late-bloom-part-viii-blind-date-at-pike-place": "https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=1200&q=80",
    "late-bloom-part-ix-mochi-the-dog-and-two-strangers": "https://images.unsplash.com/photo-1587300003388-59208cc962cb?w=1200&q=80",
    "late-bloom-part-x-coffee-number-77-every-morning": "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=1200&q=80",
    "quiet-hours-chronicle-part-i": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1200&q=80",
    "quiet-hours-chronicle-part-ii": "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=1200&q=80",
    "quiet-hours-chronicle-part-iii": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1200&q=80",
    "quiet-hours-chronicle-part-iv": "https://images.unsplash.com/photo-1516589178581-6cd7833ae3b2?w=1200&q=80",
    "quiet-hours-chronicle-part-v": "https://images.unsplash.com/photo-1529156069898-49953e39b3ac?w=1200&q=80",
    "quiet-hours-chronicle-part-vi": "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=1200&q=80",
    "omegle-alternative-2026": "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=1200&q=80",
    "random-chat-safety-2026": "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=1200&q=80",
    "language-exchange-strangers": "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=1200&q=80",
    "make-friends-random-chat": "https://images.unsplash.com/photo-1529156069898-49953e39b3ac?w=1200&q=80",
    "omegle-vs-alternatives-2026": "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=1200&q=80",
    "ometv-not-working-alternatives": "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=1200&q=80",
    "random-chat-safe-teens-checklist": "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=1200&q=80",
}

HERO_ALT = {
    "late-bloom": "Late Bloom Stories — romance serial cover",
    "quiet-hours": "The Quiet Hours Chronicle — essay cover",
    "guide": "Random chat safety guide",
}


def post_slug(path: Path) -> str:
    name = path.stem
    if re.match(r"^\d{4}-\d{2}-\d{2}-", name):
        return name[11:]
    return name


def hero_alt_for(slug: str) -> str:
    if slug.startswith("late-bloom"):
        return HERO_ALT["late-bloom"]
    if slug.startswith("quiet-hours"):
        return HERO_ALT["quiet-hours"]
    return HERO_ALT["guide"]


def has_hero(text: str) -> bool:
    return bool(re.search(r"^hero_image:\s*\S", text, re.MULTILINE))


def add_hero(text: str, url: str, alt: str) -> str:
    block = f'hero_image: {url}\nhero_alt: "{alt}"\nhero_caption: "Photo: Unsplash"\n'
    if not text.startswith("---"):
        return text
    end = text.find("\n---", 3)
    if end == -1:
        return text
    front = text[3:end]
    rest = text[end:]
    return f"---\n{front.rstrip()}\n{block}{rest}"


def main() -> None:
    updated = 0
    for path in sorted(POSTS.glob("*.md")):
        slug = post_slug(path)
        if slug not in POST_HERO_URLS:
            continue
        text = path.read_text(encoding="utf-8")
        if has_hero(text):
            continue
        path.write_text(add_hero(text, POST_HERO_URLS[slug], hero_alt_for(slug)), encoding="utf-8")
        print(f"hero added: {path.name}")
        updated += 1
    print(f"Done — {updated} post(s) updated.")


if __name__ == "__main__":
    main()
