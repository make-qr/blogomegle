#!/usr/bin/env python3
"""Reassign Late Bloom hero + inline images so card thumbs are not duplicates.

Updates seo-offpage serial markdown and blog _posts. Then run:
  python3 sync-from-seo.py   # optional if SEO is source
  python3 download-post-images.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
POSTS = ROOT / "_posts"
SEO_SERIAL = Path.home() / "huong-dan/du-an/ca-nhan-anh/seo-offpage/content/articles/serial"
sys.path.insert(0, str(Path.home() / "huong-dan/du-an/ca-nhan-anh/ngon-tinh"))
from remix_story_to_omegle_article import HERO_POOL, INLINE_POOL  # noqa: E402

HERO_RE = re.compile(
    r'^(hero_image:\s*)([\'"]?)(/assets/images/[^\s\'"]+|https?://[^\s\'"]+)\2\s*$',
    re.M,
)
MD_IMG_RE = re.compile(r"(!\[[^\]]*\]\()(/assets/images/[^)]+|https?://[^)]+)(\))")
PART_RE = re.compile(r"late-bloom-part-(?:([ivxlcdm]+)|(\d+))-", re.I)

ROMAN = {
    "i": 1, "ii": 2, "iii": 3, "iv": 4, "v": 5, "vi": 6, "vii": 7, "viii": 8,
    "ix": 9, "x": 10, "xi": 11, "xii": 12, "xiii": 13, "xiv": 14, "xv": 15,
    "xvi": 16, "xvii": 17, "xviii": 18, "xix": 19, "xx": 20,
}


def episode_from_name(name: str) -> int:
    m = PART_RE.search(name)
    if not m:
        return 0
    if m.group(2):
        return int(m.group(2))
    return ROMAN.get(m.group(1).lower(), 0)


def hero_for(ep: int) -> str:
    return HERO_POOL[(ep - 1) % len(HERO_POOL)]


def inlines_for(ep: int) -> tuple[str, str]:
    n = len(INLINE_POOL)
    a = INLINE_POOL[(ep + 2) % n]
    b = INLINE_POOL[(ep + 7) % n]
    if a == b:
        b = INLINE_POOL[(ep + 8) % n]
    return a, b


def ensure_hero_frontmatter(text: str, hero: str, alt: str) -> str:
    if HERO_RE.search(text):
        return HERO_RE.sub(lambda m: f'{m.group(1)}"{hero}"', text, count=1)
    if not text.startswith("---"):
        return text
    end = text.find("\n---", 3)
    if end == -1:
        return text
    front = text[3:end].rstrip()
    rest = text[end:]
    block = (
        f'\nhero_image: "{hero}"\n'
        f'hero_alt: "{alt}"\n'
        f'hero_caption: "Photo: Unsplash — editorial illustration for Late Bloom Stories"\n'
    )
    return f"---{front}{block}{rest}"


def process(path: Path) -> bool:
    name = path.stem
    # _posts are dated: 2026-07-03-late-bloom-...
    slug = name[11:] if re.match(r"^\d{4}-\d{2}-\d{2}-", name) else name
    if not slug.startswith("late-bloom"):
        return False
    ep = episode_from_name(slug)
    if ep < 1:
        print(f"  skip (no episode): {slug}", file=sys.stderr)
        return False

    text = path.read_text(encoding="utf-8")
    hero = hero_for(ep)
    img_a, img_b = inlines_for(ep)
    alt = f"Late Bloom Stories Part {ep} cover"

    text2 = ensure_hero_frontmatter(text, hero, alt)

    inline_urls = [img_a, img_b]
    idx = 0

    def md_sub(m: re.Match[str]) -> str:
        nonlocal idx
        url = inline_urls[idx % 2]
        idx += 1
        return f"{m.group(1)}{url}{m.group(3)}"

    text2 = MD_IMG_RE.sub(md_sub, text2)
    if text2 == text:
        return False
    path.write_text(text2, encoding="utf-8")
    print(f"  ✓ ep {ep:03d} → {path.name}")
    return True


def main() -> int:
    paths: list[Path] = []
    if SEO_SERIAL.is_dir():
        paths.extend(sorted(SEO_SERIAL.glob("late-bloom*.md")))
    if POSTS.is_dir():
        paths.extend(sorted(POSTS.glob("*-late-bloom*.md")))
    n = 0
    for path in paths:
        if process(path):
            n += 1
    print(f"Updated {n} file(s)")

    heroes: list[str] = []
    for path in sorted(POSTS.glob("*-late-bloom*.md")) if POSTS.is_dir() else []:
        m = HERO_RE.search(path.read_text(encoding="utf-8"))
        if m:
            heroes.append(m.group(3).strip("\"'"))
    if heroes:
        print(f"_posts unique heroes: {len(set(heroes))} / {len(heroes)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
