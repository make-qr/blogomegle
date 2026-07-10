#!/usr/bin/env python3
"""Download external post images to assets/images/posts/ and rewrite markdown to local paths."""
from __future__ import annotations

import hashlib
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
IMG_ROOT = ROOT / "assets" / "images" / "posts"
POSTS = ROOT / "_posts"
SEO = Path.home() / "huong-dan/du-an/ca-nhan-anh/seo-offpage/content/articles"

# Known broken Unsplash IDs → working replacements (same theme)
BROKEN_REPLACEMENTS: dict[str, str] = {
    "photo-1522673607210-e57a6d6de36c": "https://images.unsplash.com/photo-1522383225653-ed111181a951",
    "photo-1477959857187-3cebc4723ba0": "https://images.unsplash.com/photo-1516589178581-6cd7833ae3b2",
    "photo-1518199266791-5375a83190cc": "https://images.unsplash.com/photo-1529156069898-49953e39b3ac",
}

HTTP_URL_RE = re.compile(r"https?://[^\s\"')>\]]+")
HERO_RE = re.compile(r"^(hero_image:\s*)([\"']?)(https?://[^\s\"']+)\2", re.MULTILINE)
MD_IMG_RE = re.compile(r"(!\[[^\]]*\]\()(https?://[^)]+)(\))")


def post_slug_from_path(path: Path) -> str:
    name = path.stem
    if re.match(r"^\d{4}-\d{2}-\d{2}-", name):
        return name[11:]
    return name


def fix_broken_url(url: str) -> str:
    for broken, replacement in BROKEN_REPLACEMENTS.items():
        if broken in url:
            w = "1200" if "w=1200" in url or "hero" in url else "800"
            q = "80"
            return f"{replacement}?w={w}&q={q}"
    return url


def ext_from_content_type(ct: str, url: str) -> str:
    if "jpeg" in ct or "jpg" in ct:
        return ".jpg"
    if "png" in ct:
        return ".png"
    if "webp" in ct:
        return ".webp"
    if ".png" in url.lower():
        return ".png"
    if ".webp" in url.lower():
        return ".webp"
    return ".jpg"


def download_image(url: str, dest: Path) -> Path | None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists() and dest.stat().st_size > 0:
        return dest
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "OmegleChatBlog/1.0 (image-localizer)"},
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = resp.read()
            if not data:
                print(f"  EMPTY {url}", file=sys.stderr)
                return None
            ext = ext_from_content_type(resp.headers.get("Content-Type", ""), url)
            out = dest if dest.suffix == ext else dest.with_suffix(ext)
            out.write_bytes(data)
            return out
    except urllib.error.HTTPError as e:
        print(f"  HTTP {e.code} {url}", file=sys.stderr)
        return None
    except OSError as e:
        print(f"  ERR {url}: {e}", file=sys.stderr)
        return None


def local_path_for(post_slug: str, role: str, url: str) -> Path:
    key = hashlib.sha1(url.encode()).hexdigest()[:8]
    return IMG_ROOT / post_slug / f"{role}-{key}.jpg"


def relative_url(path: Path) -> str:
    return "/" + path.relative_to(ROOT).as_posix()


def process_markdown(path: Path) -> int:
    text = path.read_text(encoding="utf-8")
    post_slug = post_slug_from_path(path)
    changed = 0

    def localize_url(url: str, role: str) -> str | None:
        if url.startswith("/assets/"):
            return None
        fixed = fix_broken_url(url)
        dest = local_path_for(post_slug, role, fixed)
        saved = download_image(fixed, dest)
        if not saved:
            return None
        return relative_url(saved)

    # hero_image in frontmatter
    def hero_sub(m: re.Match[str]) -> str:
        nonlocal changed
        prefix, quote, url = m.group(1), m.group(2), m.group(3)
        local = localize_url(url, "hero")
        if local:
            changed += 1
            q = quote or ""
            return f"{prefix}{q}{local}{q}"
        return m.group(0)

    text = HERO_RE.sub(hero_sub, text)

    # markdown images
    inline_n = 0

    def md_sub(m: re.Match[str]) -> str:
        nonlocal changed, inline_n
        prefix, url, suffix = m.group(1), m.group(2), m.group(3)
        inline_n += 1
        local = localize_url(url, f"inline-{inline_n:02d}")
        if local:
            changed += 1
            return f"{prefix}{local}{suffix}"
        return m.group(0)

    text = MD_IMG_RE.sub(md_sub, text)

    if changed:
        path.write_text(text, encoding="utf-8")
        print(f"  updated {path.name} ({changed} image(s))")
    return changed


def collect_sources() -> list[Path]:
    files: list[Path] = []
    if POSTS.is_dir():
        files.extend(sorted(POSTS.glob("*.md")))
    if SEO.is_dir():
        for md in sorted(SEO.rglob("*.md")):
            if any(skip in md.name for skip in ("KE-HOACH", "_")):
                continue
            files.append(md)
    return files


def main() -> int:
    files = collect_sources()
    if not files:
        print("No markdown files found.")
        return 1
    total = 0
    print(f"Scanning {len(files)} file(s)...")
    for path in files:
        if HTTP_URL_RE.search(path.read_text(encoding="utf-8")):
            print(path.relative_to(ROOT) if path.is_relative_to(ROOT) else path)
            total += process_markdown(path)
    print(f"Done — {total} image reference(s) localized.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
