#!/usr/bin/env python3
"""Download default category cover images for post cards."""
from __future__ import annotations

import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "assets" / "images" / "covers"

COVERS = {
    "late-bloom.jpg": "https://images.unsplash.com/photo-1522383225653-ed111181a951?w=1200&q=80",
    "quiet-hours.jpg": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1200&q=80",
    "love-journey.jpg": "https://images.unsplash.com/photo-1529156069898-49953e39b3ac?w=1200&q=80",
    "human-connection.jpg": "https://images.unsplash.com/photo-1516589178581-6cd7833ae3b2?w=1200&q=80",
    "guide-chat.jpg": "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=1200&q=80",
    "default-blog.jpg": "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=1200&q=80",
}

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


def fetch(url: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists() and dest.stat().st_size > 0:
        return
    req = urllib.request.Request(url, headers={"User-Agent": "OmegleChatBlog/1.0"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        dest.write_bytes(resp.read())


def main() -> None:
    for name, url in COVERS.items():
        fetch(url, OUT / name)
        print(f"cover {name}")
    print("Done.")


if __name__ == "__main__":
    main()
