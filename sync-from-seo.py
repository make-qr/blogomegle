#!/usr/bin/env python3
"""Sync omegle SEO markdown → Jekyll _posts for blog.omeglechat.online."""
from __future__ import annotations

import re
import shutil
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC_LOCAL = Path.home() / "huong-dan/du-an/ca-nhan-anh/seo-offpage/content/articles"
SRC = SRC_LOCAL if SRC_LOCAL.is_dir() else ROOT / "source-articles"
POSTS = ROOT / "_posts"

# slug → publish date (newest serial last for sort order we want reverse - actually Jekyll sorts newest first)
# Assign dates so serial I is oldest in June, guides spread before
DATE_MAP: dict[str, str] = {
    "omegle-alternative-2026": "2026-03-15",
    "random-chat-safety-2026": "2026-03-22",
    "language-exchange-strangers": "2026-04-01",
    "make-friends-random-chat": "2026-04-08",
    "omegle-vs-alternatives-2026": "2026-04-15",
    "ometv-not-working-alternatives": "2026-05-01",
    "random-chat-safe-teens-checklist": "2026-05-10",
    "quiet-hours-chronicle-part-i": "2026-06-01",
    "quiet-hours-chronicle-part-ii": "2026-06-04",
    "quiet-hours-chronicle-part-iii": "2026-06-08",
    "quiet-hours-chronicle-part-iv": "2026-06-12",
    "quiet-hours-chronicle-part-v": "2026-06-16",
    "quiet-hours-chronicle-part-vi": "2026-06-20",
    "late-bloom-part-i-late-blooming-cherry": "2026-06-23",
    "late-bloom-part-ii-messages-never-sent": "2026-06-30",
}

GUIDE_CATEGORY = "Omegle & Alternatives"
GUIDE_SLUG = "omegle-alternatives"

SKIP_FILES = {"KE-HOACH", "_"}

LINK_REWRITES = [
    (r"/blog/series-the-quiet-hours-chronicle\.html", "/series/the-quiet-hours-chronicle/"),
    (r"/blog/author-morgan-rivers\.html", "/author/morgan-rivers/"),
    (r"/blog/category/human-connection\.html", "/category/human-connection/"),
    (r"https://omeglechat\.online/blog/series-the-quiet-hours-chronicle\.html", "/series/the-quiet-hours-chronicle/"),
    (r"https://omeglechat\.online/blog/author-morgan-rivers\.html", "/author/morgan-rivers/"),
    (r"https://omeglechat\.online/blog/category/human-connection\.html", "/category/human-connection/"),
    (r"https://omeglechat\.online/blog/([a-z0-9\-]+)\.html", r"/\1/"),
    (r"\(/blog/([a-z0-9\-]+)\.html\)", r"(/\1/)"),
    (r"\]\(/series-the-quiet-hours-chronicle/\)", "](/series/the-quiet-hours-chronicle/)"),
    (r"\]\(/author-morgan-rivers/\)", "](/author/morgan-rivers/)"),
    (r"\]\(/category-human-connection/\)", "](/category/human-connection/)"),
]


def parse_frontmatter(text: str) -> tuple[dict, str]:
    meta: dict = {}
    body = text
    if text.startswith("---"):
        _, front, body = text.split("---", 2)
        for line in front.strip().splitlines():
            if ":" not in line:
                continue
            k, v = line.split(":", 1)
            k, v = k.strip(), v.strip().strip('"').strip("'")
            if v == "":
                continue
            if k in ("tags",):
                if v.startswith("["):
                    meta[k] = [t.strip() for t in v.strip("[]").split(",") if t.strip()]
                else:
                    meta[k] = [t.strip() for t in v.split(",") if t.strip()]
            elif k in ("series_part", "series_parts"):
                meta[k] = int(v) if v.isdigit() else v
            else:
                meta[k] = v
    return meta, body.strip()


def rewrite_links(body: str) -> str:
    for pat, repl in LINK_REWRITES:
        body = re.sub(pat, repl, body)
    return body


def jekyll_post(meta: dict, body: str, slug: str, d: str) -> str:
    body = rewrite_links(body)
    lines = ["---"]
    lines.append(f"title: \"{meta.get('title', slug).replace(chr(34), chr(39))}\"")
    lines.append(f"date: {d}")
    lines.append(f"slug: {slug}")
    lines.append(f"permalink: /{slug}/")
    if ex := meta.get("excerpt"):
        lines.append(f"excerpt: \"{ex.replace(chr(34), chr(39))}\"")
    for key in (
        "author", "author_slug", "author_role", "category", "category_slug",
        "series_name", "series_slug", "series_part", "series_parts", "series_part_label",
        "format", "prev_part", "next_part", "tags",
    ):
        if key in meta and meta[key] not in ("", None):
            val = meta[key]
            if key == "tags" and isinstance(val, list):
                lines.append(f"tags: [{', '.join(val)}]")
            elif key in ("prev_part", "next_part") and val:
                p = val if str(val).startswith("/") else f"/{val}/"
                if not p.endswith("/"):
                    p += "/"
                lines.append(f"{key}: {p}")
            else:
                lines.append(f"{key}: {val}" if not isinstance(val, str) or " " not in val else f'{key}: "{val}"')
    if meta.get("format") != "serial" and meta.get("category") != "Human Connection":
        lines.append(f"category: {GUIDE_CATEGORY}")
        lines.append(f"category_slug: {GUIDE_SLUG}")
    lines.append("---")
    lines.append("")
    lines.append(body)
    return "\n".join(lines) + "\n"


def collect_sources() -> list[Path]:
    paths: list[Path] = []
    for p in sorted(SRC.glob("*.md")):
        if any(p.name.startswith(s) for s in SKIP_FILES):
            continue
        paths.append(p)
    serial = SRC / "serial"
    if serial.is_dir():
        for p in sorted(serial.glob("part-*.md")):
            paths.append(p)
        for p in sorted(serial.glob("late-bloom*.md")):
            paths.append(p)
    return paths


def main() -> None:
    if not SRC.is_dir():
        print(f"Skip sync: no articles at {SRC} (using committed _posts)")
        return
    if POSTS.exists():
        shutil.rmtree(POSTS)
    POSTS.mkdir()
    count = 0
    for path in collect_sources():
        meta, body = parse_frontmatter(path.read_text(encoding="utf-8"))
        slug = meta.get("slug") or path.stem
        d = DATE_MAP.get(slug, date.today().isoformat())
        out_name = f"{d}-{slug}.md"
        (POSTS / out_name).write_text(jekyll_post(meta, body, slug, d), encoding="utf-8")
        print(f"  ✓ {out_name}")
        count += 1
    print(f"\nSynced {count} posts → {POSTS}")


if __name__ == "__main__":
    main()
