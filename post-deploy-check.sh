#!/usr/bin/env bash
# Sau mỗi lần push blog — verify sitemap, robots, feed, URL bài mới
set -euo pipefail
BASE="${BLOG_URL:-https://blog.omeglechat.online}"
SLUG="${1:-}"

echo "=== Blog post-deploy check: $BASE ==="

curl -sf "$BASE/robots.txt" | grep -q "sitemap.xml" && echo "✓ robots.txt → sitemap"
curl -sf "$BASE/sitemap.xml" | grep -q "<loc>" && echo "✓ sitemap.xml reachable"
curl -sf "$BASE/feed.xml" | grep -q "<rss" && echo "✓ feed.xml (RSS)"

if [[ -n "$SLUG" ]]; then
  URL="$BASE/$SLUG/"
  curl -sfI "$URL" | head -1 | grep -q "200" && echo "✓ $URL" || echo "✗ $URL (404?)"
  curl -sf "$BASE/sitemap.xml" | grep -q "$SLUG" && echo "✓ slug in sitemap" || echo "✗ slug NOT in sitemap"
fi

echo ""
echo "GSC (thủ công): Search Console → blog.omeglechat.online → Sitemaps → $BASE/sitemap.xml"
echo "Ping Bing: cd seo-offpage && ./ping-sitemap.sh"
