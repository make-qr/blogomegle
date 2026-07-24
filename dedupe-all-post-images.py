#!/usr/bin/env python3
"""Assign a globally unique image URL to every hero + inline slot across all posts.

Uses verified Unsplash IDs first, then picsum seeds so no two slots share content.
Updates blog `_posts` and matching SEO markdown. Then run:
  python3 download-post-images.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
POSTS = ROOT / "_posts"
SEO = Path.home() / "huong-dan/du-an/ca-nhan-anh/seo-offpage/content/articles"
OK_IDS = Path("/tmp/unsplash-ok-ids.txt")

HERO_RE = re.compile(
    r'^(hero_image:\s*)([\'"]?)(/assets/images/[^\s\'"]+|https?://[^\s\'"]+)\2\s*$',
    re.M,
)
MD_IMG_RE = re.compile(r"(!\[[^\]]*\]\()(/assets/images/[^)]+|https?://[^)]+)(\))")
SLUG_RE = re.compile(r'^slug:\s*["\']?([^"\'\n]+)', re.M)


def photo_url(pid: str, w: int = 1200) -> str:
    return f"https://images.unsplash.com/{pid}?auto=format&fit=crop&w={w}&q=80"


def picsum_url(seed: str, w: int = 1600, h: int = 900) -> str:
    return f"https://picsum.photos/seed/{seed}/{w}/{h}"


def load_pool(need: int) -> list[str]:
    ids = [ln.strip() for ln in OK_IDS.read_text().splitlines() if ln.strip()]
    urls = [photo_url(i) for i in ids]
    # Guaranteed unique fillers (different seed → different image)
    n = 0
    while len(urls) < need:
        n += 1
        urls.append(picsum_url(f"omeglechat-unique-{n:04d}"))
    return urls


def post_slug(path: Path, text: str) -> str:
    m = SLUG_RE.search(text)
    if m:
        return m.group(1).strip()
    name = path.stem
    if re.match(r"^\d{4}-\d{2}-\d{2}-", name):
        return name[11:]
    return re.sub(r"^\d{2}-", "", name)


def assign_for_text(text: str, urls: list[str], cursor: list[int]) -> tuple[str, int]:
    """Replace hero + markdown images with next unique URLs. Returns (text, count)."""
    changed = 0

    def next_url() -> str:
        i = cursor[0]
        if i >= len(urls):
            raise RuntimeError("image pool exhausted")
        cursor[0] = i + 1
        return urls[i]

    if HERO_RE.search(text):
        def hero_sub(m: re.Match[str]) -> str:
            nonlocal changed
            changed += 1
            return f'{m.group(1)}"{next_url()}"'

        text = HERO_RE.sub(hero_sub, text, count=1)

    def md_sub(m: re.Match[str]) -> str:
        nonlocal changed
        changed += 1
        return f"{m.group(1)}{next_url()}{m.group(3)}"

    text = MD_IMG_RE.sub(md_sub, text)
    return text, changed


def find_seo_for_slug(slug: str) -> Path | None:
    if not SEO.is_dir():
        return None
    # Prefer exact filename match under known folders
    for sub in ("serial", "love-journey", "later-years", "chat-funnel", ""):
        base = SEO / sub if sub else SEO
        if not base.is_dir():
            continue
        for p in base.rglob("*.md"):
            stem = re.sub(r"^\d{2}-", "", p.stem)
            if stem == slug or p.stem.endswith(slug) or slug in p.stem:
                body = p.read_text(encoding="utf-8", errors="ignore")
                sm = SLUG_RE.search(body)
                if sm and sm.group(1).strip() == slug:
                    return p
                if stem == slug:
                    return p
    return None


def mirror_to_seo(seo_path: Path, blog_text: str) -> None:
    """Copy image URLs from blog text into SEO file; absolutize for offpage."""
    seo_text = seo_path.read_text(encoding="utf-8")
    # If SEO body was corrupted by a bad rewrite, replace body from blog
    corrupt = bool(
        re.search(r"assets/images/posts/[^)\s]*https://", seo_text)
        or re.search(r"blog\.omeglechat\.online/assets/images/posts/[^)\s]*https://", seo_text)
    )

    blog_hero = HERO_RE.search(blog_text)
    blog_inlines = [m.group(2) for m in MD_IMG_RE.finditer(blog_text)]

    def abs_url(u: str) -> str:
        if u.startswith("/assets/"):
            return "https://blog.omeglechat.online" + u
        return u

    if corrupt:
        # Rebuild SEO from blog: keep SEO front-matter keys when possible, else use blog
        # Safest: take blog content and absolutize asset URLs
        out = blog_text
        out = re.sub(
            r"(/assets/images/[^)\s\"']+)",
            r"https://blog.omeglechat.online\1",
            out,
        )
        seo_path.write_text(out, encoding="utf-8")
        return

    if blog_hero and HERO_RE.search(seo_text):
        hero_u = abs_url(blog_hero.group(3))
        seo_text = HERO_RE.sub(lambda m: f'{m.group(1)}"{hero_u}"', seo_text, count=1)

    idx = 0

    def md_sub(m: re.Match[str]) -> str:
        nonlocal idx
        if idx >= len(blog_inlines):
            return m.group(0)
        u = abs_url(blog_inlines[idx])
        idx += 1
        return f"{m.group(1)}{u}{m.group(3)}"

    if blog_inlines and MD_IMG_RE.search(seo_text):
        seo_text = MD_IMG_RE.sub(md_sub, seo_text)

    seo_path.write_text(seo_text, encoding="utf-8")


def main() -> int:
    posts = sorted(POSTS.glob("*.md"))
    if not posts:
        print("No posts found", file=sys.stderr)
        return 1

    # Count slots
    slots = 0
    for p in posts:
        t = p.read_text(encoding="utf-8")
        if HERO_RE.search(t):
            slots += 1
        slots += len(MD_IMG_RE.findall(t))

    pool = load_pool(slots + 10)
    cursor = [0]
    print(f"Posts: {len(posts)} | image slots: {slots} | pool: {len(pool)}")

    used_photo_keys: set[str] = set()
    total = 0
    for p in posts:
        text = p.read_text(encoding="utf-8")
        slug = post_slug(p, text)
        new_text, n = assign_for_text(text, pool, cursor)
        if n:
            p.write_text(new_text, encoding="utf-8")
            total += n
            print(f"  {slug}: {n} image(s)")
            seo = find_seo_for_slug(slug)
            if seo:
                mirror_to_seo(seo, new_text)
                print(f"    → SEO {seo.relative_to(SEO)}")

    # Verify uniqueness of assigned Unsplash/picsum seeds in posts
    keys: dict[str, list[str]] = {}
    for p in posts:
        t = p.read_text(encoding="utf-8")
        urls = []
        m = HERO_RE.search(t)
        if m:
            urls.append(m.group(3))
        urls.extend(x.group(2) for x in MD_IMG_RE.finditer(t))
        for u in urls:
            if "photo-" in u:
                key = re.search(r"photo-[a-z0-9-]+", u).group(0)  # type: ignore
            elif "picsum.photos/seed/" in u:
                key = re.search(r"seed/([^/]+)", u).group(1)  # type: ignore
            else:
                key = u
            keys.setdefault(key, []).append(p.name)

    dups = {k: v for k, v in keys.items() if len(v) > 1}
    print(f"Done — reassigned {total} refs. Unique keys: {len(keys)}. Dup keys: {len(dups)}")
    if dups:
        for k, v in list(dups.items())[:10]:
            print(f"  DUP {k}: {v}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
