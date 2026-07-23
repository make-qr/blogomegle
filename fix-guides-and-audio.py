#!/usr/bin/env python3
"""Strip audio players when the MP3 is missing; assign unique guide covers."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
POSTS = ROOT / "_posts"
AUDIO = ROOT / "assets" / "audio"
SEO = Path.home() / "huong-dan/du-an/ca-nhan-anh/seo-offpage/content/articles"

AUDIO_BLOCK_RE = re.compile(
    r"(?:<div class=\"audio-player-wrap\">[\s\S]*?</div>\s*)"
    r"|(?:<p class=\"audio-player-wrap\">[\s\S]*?</p>\s*)",
    re.I,
)
SRC_RE = re.compile(r'src="(/assets/audio/([^"]+\.mp3))"', re.I)

GUIDE_HEROES: dict[str, str] = {
    "omegle-alternative-2026": "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=1200&q=80",
    "random-chat-safety-2026": "https://images.unsplash.com/photo-1563986768609-322da13575f3?w=1200&q=80",
    "language-exchange-strangers": "https://images.unsplash.com/photo-1523240795612-9a054b0db644?w=1200&q=80",
    "make-friends-random-chat": "https://images.unsplash.com/photo-1529156069898-49953e39b3ac?w=1200&q=80",
    "omegle-vs-alternatives-2026": "https://images.unsplash.com/photo-1551434678-e076c223a692?w=1200&q=80",
    "ometv-not-working-alternatives": "https://images.unsplash.com/photo-1512941937669-90a1b58e7e9c?w=1200&q=80",
    "random-chat-safe-teens-checklist": "https://images.unsplash.com/photo-1503676260728-1c00da094a0b?w=1200&q=80",
}

HERO_RE = re.compile(
    r'^(hero_image:\s*)([\'"]?)(/assets/images/[^\s\'"]+|https?://[^\s\'"]+)\2\s*$',
    re.M,
)


def slug_from(path: Path) -> str:
    name = path.stem
    if re.match(r"^\d{4}-\d{2}-\d{2}-", name):
        return name[11:]
    # SEO numbered: 01-omegle-alternative-2026.md
    m = re.match(r"^\d+-(.+)$", name)
    return m.group(1) if m else name


def strip_missing_audio(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    if "audio-player" not in text:
        return False

    def keep_or_drop(m: re.Match[str]) -> str:
        block = m.group(0)
        src = SRC_RE.search(block)
        if not src:
            return ""
        mp3_name = src.group(2)
        mp3 = AUDIO / mp3_name
        if mp3.is_file() and mp3.stat().st_size > 1000:
            return block
        return ""

    new = AUDIO_BLOCK_RE.sub(keep_or_drop, text)
    # collapse excess blank lines after removal
    new = re.sub(r"\n{3,}", "\n\n", new)
    if new == text:
        return False
    path.write_text(new, encoding="utf-8")
    print(f"  audio stripped: {path.name}")
    return True


def ensure_guide_hero(path: Path) -> bool:
    slug = slug_from(path)
    if slug not in GUIDE_HEROES:
        return False
    hero = GUIDE_HEROES[slug]
    text = path.read_text(encoding="utf-8")
    if HERO_RE.search(text):
        new = HERO_RE.sub(lambda m: f'{m.group(1)}"{hero}"', text, count=1)
    elif text.startswith("---"):
        end = text.find("\n---", 3)
        if end == -1:
            return False
        front = text[3:end].rstrip()
        rest = text[end:]
        block = (
            f'\nhero_image: "{hero}"\n'
            f'hero_alt: "Safety guide cover — {slug}"\n'
            f'hero_caption: "Photo: Unsplash"\n'
        )
        new = f"---{front}{block}{rest}"
    else:
        return False
    if new == text:
        return False
    path.write_text(new, encoding="utf-8")
    print(f"  guide hero: {path.name}")
    return True


def remap_guide_category(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    if "omegle-alternatives" not in text and "Omegle & Alternatives" not in text:
        return False
    new = text.replace("category_slug: omegle-alternatives", "category_slug: safety-guides")
    new = new.replace('category_slug: "omegle-alternatives"', 'category_slug: safety-guides')
    new = new.replace("category: Omegle & Alternatives", "category: Safety & Guides")
    new = new.replace('category: "Omegle & Alternatives"', 'category: "Safety & Guides"')
    if new == text:
        return False
    path.write_text(new, encoding="utf-8")
    print(f"  category remap: {path.name}")
    return True


def collect() -> list[Path]:
    files: list[Path] = []
    if POSTS.is_dir():
        files.extend(POSTS.glob("*.md"))
    if SEO.is_dir():
        files.extend(SEO.glob("*.md"))
        for sub in ("serial", "love-journey"):
            d = SEO / sub
            if d.is_dir():
                files.extend(d.glob("*.md"))
    return files


def main() -> int:
    n = 0
    for path in collect():
        if any(
            [
                strip_missing_audio(path),
                ensure_guide_hero(path),
                remap_guide_category(path),
            ]
        ):
            n += 1
    print(f"Touched {n} file(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
