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
    "late-bloom-part-120-noodle-shop-number-3": "2026-08-26",
    "late-bloom-part-119-back-row-concert-tickets": "2026-08-26",
    "late-bloom-part-118-night-shift-77": "2026-08-25",
    "late-bloom-part-117-hello-from-random-chat": "2026-08-25",
    "late-bloom-part-116-viewer-number-27": "2026-08-24",
    "late-bloom-part-115-you-smiled-more-today": "2026-08-24",
    "late-bloom-part-114-blackout-on-the-embarcadero": "2026-08-23",
    "late-bloom-part-113-stuck-in-the-elevator-30-minutes": "2026-08-23",
    "late-bloom-part-112-an-exs-wedding": "2026-08-22",
    "late-bloom-part-111-college-rivals": "2026-08-22",
    "late-bloom-part-58-night-shift-77": "2026-07-26",
    "late-bloom-part-57-hello-from-random-chat": "2026-07-26",
    "late-bloom-part-x-coffee-number-77-every-morning": "2026-07-10",
    "late-bloom-part-ix-mochi-the-dog-and-two-strangers": "2026-07-10",
    "late-bloom-part-52-an-exs-wedding": "2026-07-23",
    "late-bloom-part-51-college-rivals": "2026-07-23",
    "late-bloom-part-50-coffee-number-7-every-morning": "2026-07-22",
    "late-bloom-part-49-mochi-the-dog-and-two-strangers": "2026-07-22",
    "late-bloom-part-48-blind-date-at-brooklyn-bridge": "2026-07-21",
    "late-bloom-part-47-8-hours-apart": "2026-07-21",
    "late-bloom-part-46-neighbors-on-floor-8": "2026-07-20",
    "late-bloom-part-45-the-friend-from-that-year-the-high-line": "2026-07-20",
    "late-bloom-part-44-a-3-year-contract": "2026-07-19",
    "late-bloom-part-43-broken-mirror-on-the-west-village": "2026-07-19",
    "late-bloom-part-42-119-messages-never-sent": "2026-07-18",
    "late-bloom-part-41-after-10-years-of-silence": "2026-07-18",
    "late-bloom-part-40-noodle-shop-number-11": "2026-07-17",
    "late-bloom-part-39-back-row-concert-tickets": "2026-07-17",
    "late-bloom-part-38-night-shift-7": "2026-07-16",
    "late-bloom-part-37-hello-from-random-chat": "2026-07-16",
    "late-bloom-part-36-viewer-number-3": "2026-07-15",
    "late-bloom-part-35-you-smiled-more-today": "2026-07-15",
    "late-bloom-part-34-blackout-on-lake-shore-drive": "2026-07-14",
    "late-bloom-part-33-stuck-in-the-elevator-30-minutes": "2026-07-14",
    "late-bloom-part-32-an-exs-wedding": "2026-07-13",
    "late-bloom-part-31-college-rivals": "2026-07-13",
    "late-bloom-part-30-coffee-number-17-every-morning": "2026-07-12",
    "late-bloom-part-29-bean-the-dog-and-two-strangers": "2026-07-12",
    "late-bloom-part-28-blind-date-at-zilker-park": "2026-07-11",
    "late-bloom-part-27-8-hours-apart": "2026-07-11",
    "late-bloom-part-26-neighbors-on-floor-8": "2026-07-10",
    "late-bloom-part-25-the-friend-from-that-year-the-congress-bridge": "2026-07-10",
    "late-bloom-part-24-a-4-year-contract": "2026-07-09",
    "late-bloom-part-23-broken-mirror-on-6th-street": "2026-07-09",
    "late-bloom-part-22-539-messages-never-sent": "2026-07-08",
    "late-bloom-part-21-after-1-years-of-silence": "2026-07-08",
    "late-bloom-part-xx-noodle-shop-number-27": "2026-07-07",
    "late-bloom-part-xix-back-row-concert-tickets": "2026-07-07",
    "late-bloom-part-xviii-night-shift-17": "2026-07-06",
    "late-bloom-part-xvii-hello-from-random-chat": "2026-07-06",
    "late-bloom-part-xvi-viewer-number-11": "2026-07-05",
    "late-bloom-part-xv-you-smiled-more-today": "2026-07-05",
    "late-bloom-part-xiv-blackout-on-the-riverfront": "2026-07-04",
    "late-bloom-part-xiii-stuck-in-the-elevator-30-minutes": "2026-07-04",
    "late-bloom-part-xii-an-exs-wedding": "2026-07-03",
    "late-bloom-part-xi-college-rivals": "2026-07-03",
    "late-bloom-part-viii-blind-date-at-pike-place": "2026-07-01",
    "late-bloom-part-vii-8-hours-apart": "2026-07-01",
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
    "late-bloom-part-ii-messages-never-sent": "2026-06-23",
    "late-bloom-part-iii-broken-mirror-rain-street": "2026-06-25",
    "late-bloom-part-iv-one-year-contract": "2026-06-26",
    "late-bloom-part-v-friend-from-that-year": "2026-06-27",
    "late-bloom-part-vi-noodle-shop-number-seven": "2026-06-28",
    "how-to-start-conversation-someone-you-like": "2026-07-10",
    "what-true-love-actually-means": "2026-07-24",
    "how-to-text-someone-you-like-without-overthinking": "2026-07-25",
    # Love Journey 8-week calendar (weeks 2–8)
    "how-to-know-if-someone-is-the-one-or-just-comfortable": "2026-07-26",
    "signs-youre-ready-to-look-for-a-life-partner": "2026-07-27",
    "how-to-choose-a-spouse-youll-still-like-in-10-years": "2026-07-28",
    "red-flags-that-look-like-passion": "2026-07-29",
    "premarital-health-body-money-emotional-readiness": "2026-07-30",
    "funny-married-life-truths-nobody-puts-in-wedding-vows": "2026-07-31",
    "after-the-wedding-first-year-map-for-real-couples": "2026-08-01",
    "how-to-fight-fair-without-threatening-the-relationship": "2026-08-02",
    "money-talks-before-marriage-scripts": "2026-08-03",
    "soft-couple-humor-when-we-becomes-a-comedy-duo": "2026-08-04",
    "lonely-nights-vs-true-loneliness-when-to-reach-out": "2026-08-05",
    "building-a-home-that-feels-safe-for-both-of-you": "2026-08-06",
    "premarital-checkup-checklist-health-habits-family": "2026-08-07",
    "10-gentle-jokes-only-long-term-couples-understand": "2026-08-08",
    # Later Years / elderly connection (Human Connection)
    "why-older-adults-talk-less-as-they-age": "2026-08-09",
    "loneliness-vs-solitude-after-60": "2026-08-10",
    "how-conversation-protects-the-aging-mind": "2026-08-11",
    "gentle-guide-seniors-online-conversation-safely": "2026-08-12",
    "how-adult-children-can-help-quiet-parents-reconnect": "2026-08-13",
    # Chat funnel discovery cluster
    "how-to-talk-to-strangers-online-without-awkwardness": "2026-08-14",
    "random-chat-vs-dating-apps": "2026-08-15",
    "lonely-at-night-low-pressure-ways-to-talk": "2026-08-16",
    "what-to-say-first-on-omegle-style-chat": "2026-08-17",
    # Stranger Scripts + funnel tools cluster
    "stranger-scripts-01-weather-opener": "2026-08-18",
    "stranger-scripts-02-why-are-you-here": "2026-08-19",
    "stranger-scripts-03-coffee-or-tea": "2026-08-20",
    "stranger-scripts-04-language-warmup": "2026-08-21",
    "stranger-scripts-05-night-desk": "2026-08-22",
    "stranger-scripts-06-hobby-hook": "2026-08-23",
    "stranger-scripts-07-honest-lonely": "2026-08-24",
    "night-desk-companion-random-chat": "2026-08-25",
    "practice-english-conversation-with-strangers-browser": "2026-08-26",
    "after-breakup-talk-without-flirting": "2026-08-27",
    # Keyword money cluster (Phase A+B)
    "best-websites-to-talk-to-strangers-2026": "2026-08-28",
    "free-random-chat-online": "2026-08-29",
    "online-random-chat-rooms-guide": "2026-08-30",
    "random-video-chat-vs-text-chat": "2026-08-31",
    "why-people-still-want-anonymous-chat-2026": "2026-09-01",
    "safe-random-chat-checklist-for-adults": "2026-09-02",
    # Lifestyle content — Table Talk / Life Habits / Love Journey (every 2 days from 2026-09-03)
    "dinner-conversation-starters-that-feel-natural": "2026-09-03",
    "why-eating-alone-feels-heavier-at-night": "2026-09-05",
    "date-night-at-home-food-and-talk": "2026-09-07",
    "how-shared-meals-strengthen-marriage": "2026-09-09",
    "evening-routines-for-people-who-live-alone": "2026-09-11",
    "walking-talking-accountability-needs-human-voice": "2026-09-13",
    "cooking-for-one-without-empty-kitchen": "2026-09-15",
    "gentle-weight-habits-not-a-diet-war": "2026-09-17",
    "sunday-cooking-reset-for-calmer-week": "2026-09-19",
    "soup-for-hard-days-comfort-without-isolation": "2026-09-21",
    "tea-and-talk-ritual-at-home": "2026-09-23",
    "grocery-run-as-social-reset": "2026-09-25",
    "sleep-before-screens-evening-boundary": "2026-09-27",
    "morning-quiet-vs-loneliness": "2026-09-29",
    "hydration-habits-without-the-hype": "2026-10-01",
    "fighting-after-dinner-how-to-reset": "2026-10-03",
    "money-talk-at-the-table-scripts": "2026-10-05",
    "in-laws-and-shared-meals-boundaries": "2026-10-07",
    "first-year-kitchen-habits-for-couples": "2026-10-09",
    "stop-scale-obsession-body-image-kindness": "2026-10-11",
    "breakfast-alone-making-mornings-less-hollow": "2026-10-13",
    "lunch-break-conversations-that-beat-scrolling": "2026-10-15",
    "weekend-brunch-friends-vs-eating-solo": "2026-10-17",
    "meal-prep-as-self-respect-not-punishment": "2026-10-19",
    "cooking-with-a-partner-without-arguing": "2026-10-21",
    "what-to-talk-about-first-home-cooked-date": "2026-10-23",
    "lonely-holidays-and-the-kitchen-table": "2026-10-25",
    "healthy-habits-after-a-breakup": "2026-10-27",
    "how-to-ask-someone-to-walk-and-talk": "2026-10-29",
    "weekly-dinner-with-friends-ritual": "2026-10-31",
    "when-appetite-changes-with-loneliness": "2026-11-02",
    "small-kitchen-wins-that-improve-mood": "2026-11-04",
}


GUIDE_CATEGORY = "Safety & Guides"
GUIDE_SLUG = "safety-guides"

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
            k, v = k.strip(), v.strip()
            if (v.startswith('"') and v.endswith('"')) or (v.startswith("'") and v.endswith("'")):
                v = v[1:-1]
            v = v.replace('\\"', '"').replace("\\'", "'")
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


def yaml_str(val: str) -> str:
    """Quote a YAML string; prefer single quotes inside double-quoted values."""
    cleaned = val.replace('\\"', '"').replace("\\'", "'").replace("\\", "")
    return '"' + cleaned.replace('"', "'") + '"'


def jekyll_post(meta: dict, body: str, slug: str, d: str) -> str:
    body = rewrite_links(body)
    lines = ["---"]
    lines.append(f"title: {yaml_str(str(meta.get('title', slug)))}")
    lines.append(f"date: {d}")
    lines.append(f"slug: {slug}")
    lines.append(f"permalink: /{slug}/")
    if ex := meta.get("excerpt"):
        lines.append(f"excerpt: {yaml_str(str(ex))}")
    for key in (
        "author", "author_slug", "author_role", "category", "category_slug",
        "series_name", "series_slug", "series_part", "series_parts", "series_part_label",
        "format", "pillar", "prev_part", "next_part", "tags",
        "hero_image", "hero_alt", "hero_caption", "youtube_id", "youtube_caption",
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
            elif key in ("series_part", "series_parts") and isinstance(val, int):
                lines.append(f"{key}: {val}")
            elif key in ("hero_image", "hero_alt", "hero_caption", "youtube_caption", "excerpt", "title") or (
                isinstance(val, str) and (" " in val or val.startswith("http") or "&" in val)
            ):
                lines.append(f"{key}: {yaml_str(str(val))}")
            else:
                lines.append(f"{key}: {val}")
    if (
        meta.get("format") != "serial"
        and meta.get("category_slug")
        not in ("human-connection", "love-journey", "love-romance", "safety-guides", "table-talk", "life-habits")
        and meta.get("category") != "Human Connection"
        and meta.get("pillar") != "chat-funnel"
    ):
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
    lj = SRC / "love-journey"
    if lj.is_dir():
        for p in sorted(lj.glob("*.md")):
            paths.append(p)
    for sub in ("table-talk", "life-habits"):
        d = SRC / sub
        if d.is_dir():
            for p in sorted(d.glob("*.md")):
                paths.append(p)
    later = SRC / "later-years"
    if later.is_dir():
        for p in sorted(later.glob("*.md")):
            paths.append(p)
    funnel = SRC / "chat-funnel"
    if funnel.is_dir():
        for p in sorted(funnel.glob("*.md")):
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
