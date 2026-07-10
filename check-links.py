#!/usr/bin/env python3
"""Verify every link in blog posts/pages points to a valid destination.

- Internal links (/slug/, /series/..., /assets/...) must resolve to a real
  post permalink, static page, or file on disk.
- External links to the main site (omeglechat.online) must return HTTP 200.
- Known bad forms (missing .html on omeglechat.online pages) are auto-fixed
  with --fix so links always hit the correct destination.

Exit code is non-zero when unresolved links remain (fails CI).
"""
from __future__ import annotations

import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
POSTS = ROOT / "_posts"
PAGE_GLOBS = ("category/*.md", "series/*.md", "author/*.md", "*.md", "index.html")

MAIN_HOST = "omeglechat.online"

# Bare omeglechat.online paths that must carry a .html suffix.
MAIN_SITE_PAGES = ("chat", "making-friends", "safety-tips", "language-learning")

LINK_RE = re.compile(r"\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
HREF_RE = re.compile(r'href="([^"]+)"')

# Static/liquid pages that always exist (not emitted as markdown permalinks).
STATIC_PATHS = {"/", "/posts/", "/series/", "/feed.xml", "/sitemap.xml"}

_http_cache: dict[str, int] = {}


def source_files() -> list[Path]:
    files: list[Path] = []
    if POSTS.is_dir():
        files.extend(sorted(POSTS.glob("*.md")))
    for pattern in ("category/*.md", "series/*.md", "author/*.md"):
        files.extend(sorted(ROOT.glob(pattern)))
    return files


def valid_internal_targets() -> set[str]:
    targets = set(STATIC_PATHS)
    for post in POSTS.glob("*.md"):
        text = post.read_text(encoding="utf-8")
        m = re.search(r"^permalink:\s*(\S+)", text, re.MULTILINE)
        if m:
            targets.add(m.group(1).strip().strip('"').strip("'"))
        else:
            slug_m = re.search(r"^slug:\s*(\S+)", text, re.MULTILINE)
            if slug_m:
                targets.add(f"/{slug_m.group(1).strip()}/")
    for pattern in ("category/*.md", "series/*.md", "author/*.md"):
        for page in ROOT.glob(pattern):
            text = page.read_text(encoding="utf-8")
            m = re.search(r"^permalink:\s*(\S+)", text, re.MULTILINE)
            if m:
                targets.add(m.group(1).strip().strip('"').strip("'"))
    return targets


def extract_links(text: str) -> list[str]:
    links = [m.group(1) for m in LINK_RE.finditer(text)]
    links += [m.group(1) for m in HREF_RE.finditer(text)]
    return links


def http_status(url: str) -> int:
    if url in _http_cache:
        return _http_cache[url]
    status = 0
    for method in ("HEAD", "GET"):
        try:
            req = urllib.request.Request(
                url, method=method, headers={"User-Agent": "OmegleChatLinkCheck/1.0"}
            )
            with urllib.request.urlopen(req, timeout=20) as resp:
                status = resp.status
                break
        except urllib.error.HTTPError as e:
            status = e.code
            if method == "GET":
                break
        except OSError:
            status = 0
    _http_cache[url] = status
    return status


def fix_main_site(url: str) -> str | None:
    """Return corrected URL for known bare omeglechat.online pages, else None."""
    m = re.match(rf"https?://{re.escape(MAIN_HOST)}/([a-z0-9\-]+)/?$", url)
    if m and m.group(1) in MAIN_SITE_PAGES:
        return f"https://{MAIN_HOST}/{m.group(1)}.html"
    return None


def check_asset(path: str) -> bool:
    rel = path.lstrip("/").split("#")[0].split("?")[0]
    return (ROOT / rel).exists()


def main() -> int:
    do_fix = "--fix" in sys.argv
    check_external = "--no-external" not in sys.argv
    targets = valid_internal_targets()

    broken: list[tuple[str, str, str]] = []
    fixed = 0

    for path in source_files():
        text = path.read_text(encoding="utf-8")
        original = text
        for raw in extract_links(text):
            url = raw.strip()
            if url.startswith("#") or url.startswith("mailto:") or url.startswith("tel:"):
                continue

            if url.startswith("http"):
                corrected = fix_main_site(url)
                if corrected:
                    if do_fix:
                        text = text.replace(url, corrected)
                        fixed += 1
                    else:
                        broken.append((path.name, url, f"should be {corrected}"))
                    continue
                if check_external and MAIN_HOST in url:
                    status = http_status(url)
                    if status != 200:
                        broken.append((path.name, url, f"HTTP {status}"))
                continue

            if url.startswith("/assets/"):
                if not check_asset(url):
                    broken.append((path.name, url, "asset not found on disk"))
                continue

            if url.startswith("/"):
                clean = "/" + url.strip("/").split("#")[0].split("?")[0]
                clean = clean if clean.endswith("/") or "." in clean.rsplit("/", 1)[-1] else clean + "/"
                if clean == "//":
                    clean = "/"
                if clean not in targets:
                    broken.append((path.name, url, "internal target missing"))
                continue

        if do_fix and text != original:
            path.write_text(text, encoding="utf-8")

    if do_fix and fixed:
        print(f"Fixed {fixed} link(s) to correct destination.")

    if broken:
        print(f"\n{len(broken)} broken/incorrect link(s):", file=sys.stderr)
        for fname, url, why in broken:
            print(f"  [{fname}] {url}  →  {why}", file=sys.stderr)
        return 1

    print("All links point to valid destinations.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
