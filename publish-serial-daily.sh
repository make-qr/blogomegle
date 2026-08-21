#!/usr/bin/env bash
# Publish today's Late Bloom episodes → blog.omeglechat.online + ping sitemaps
# Intended for NAS cron (e.g. 09:00) or local run.
set -euo pipefail

ROOT_NGON="${HOME}/huong-dan/du-an/ca-nhan-anh/ngon-tinh"
ROOT_BLOG="${HOME}/huong-dan/du-an/ca-nhan-anh/omeglechat/blog.omeglechat.online"
PUBLISH="${HOME}/huong-dan/du-an/nas/nas-apps/publish-blog-omegle.sh"
PING="${HOME}/huong-dan/du-an/ca-nhan-anh/seo-offpage/ping-sitemap.sh"
DATE="${1:-$(date -u +%F)}"

echo "=== Late Bloom daily publish · ${DATE} ==="

cd "$ROOT_NGON"
python3 remix_story_to_omegle_article.py --date "$DATE" --patch-dates

cd "$ROOT_BLOG"
python3 sync-from-seo.py
python3 download-post-images.py || true
python3 check-links.py --fix || true

if [[ -x "$PUBLISH" ]]; then
  "$PUBLISH" --sync-local "Late Bloom daily ${DATE}"
else
  echo "⚠️  Missing $PUBLISH — commit/push blog manually"
  git -C "$ROOT_BLOG" status -sb
fi

if [[ -x "$PING" ]]; then
  # Prefer IndexNow for newest URLs if INDEXNOW_URLS set in env
  bash "$PING" || true
else
  echo "⚠️  Missing ping-sitemap.sh"
fi

echo "=== Done ${DATE} · $(date '+%H:%M') ==="
echo "Live: https://blog.omeglechat.online/series/late-bloom-stories/"
