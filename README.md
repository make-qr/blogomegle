# blog.omeglechat.online — GitHub Pages

Jekyll blog for **OmegleChat** essays, guides, and *The Quiet Hours Chronicle* serial.

- **Live URL:** https://blog.omeglechat.online
- **Main site:** https://omeglechat.online
- **Source markdown:** `~/huong-dan/du-an/ca-nhan-anh/seo-offpage/content/articles/`

## Quick start

```bash
cd ~/huong-dan/du-an/ca-nhan-anh/omeglechat/blog.omeglechat.online

# Local preview (Docker, no Ruby cần cài)
./preview.sh
# → http://localhost:4000

# Sync articles from seo-offpage
python3 sync-from-seo.py

# Local preview (needs Ruby + Bundler)
bundle install
bundle exec jekyll serve
# → http://localhost:4000
```

## Deploy to GitHub Pages

- **Repo:** [make-qr/blogomegle](https://github.com/make-qr/blogomegle)
- **Push:** `git push origin main` (Actions build → nhánh `gh-pages`)

1. **GitHub → [Settings → Pages](https://github.com/make-qr/blogomegle/settings/pages)**
   - Source: **Deploy from branch** → `gh-pages` / `/ (root)` → Save
   - Custom domain: `blog.omeglechat.online`
   - Enforce HTTPS: ON

2. **Cloudflare DNS** (đã cấu hình):
   - CNAME `blog` → `make-qr.github.io` (DNS only)

```bash
git remote set-url origin git@github.com-personal:make-qr/blogomegle.git
git push -u origin main
```

## After writing new articles

```bash
# 1. Write in seo-offpage/content/articles/
# 2. Add slug + date to sync-from-seo.py DATE_MAP (date ≤ hôm nay — Jekyll không build bài tương lai)
python3 sync-from-seo.py
git add _posts assets/ series/ sync-from-seo.py
git commit -m "Add post: ..." && git push
```

### SEO / sitemap (mỗi lần publish — **nhớ làm**)

| Việc | Tự động? | Ghi chú |
|------|----------|---------|
| `sitemap.xml` | ✅ Jekyll build | Plugin `jekyll-sitemap` — mọi post + series + category |
| `robots.txt` | ✅ committed | `Sitemap: https://blog.omeglechat.online/sitemap.xml` |
| `feed.xml` | ✅ Jekyll build | RSS — plugin `jekyll-feed` |
| Canonical / meta | ✅ | `{% seo %}` + `permalink` trong frontmatter |
| Verify URL live | Chạy script | `./post-deploy-check.sh late-bloom-part-ii-...` |
| Ping Bing | Script | `cd seo-offpage && ./ping-sitemap.sh` (ping cả blog) |
| Google Search Console | Thủ công | Property `blog.omeglechat.online` → Submit sitemap |
| IndexNow (tuỳ) | Env | `INDEXNOW_URLS="https://blog.../slug/"` trong `omeglechat.env` |

```bash
# Sau push, đợi GH Actions ~2 phút rồi:
./post-deploy-check.sh late-bloom-part-ii-messages-never-sent

cd ~/huong-dan/du-an/ca-nhan-anh/seo-offpage
./ping-sitemap.sh
```

**Lưu ý:** `omeglechat.online/sitemap.xml` (site chính) là property khác — serial mới trên **blog subdomain** chỉ cần blog sitemap + GSC blog.

## Structure

| Path | Purpose |
|------|---------|
| `_posts/` | Generated — do not edit by hand |
| `series/` | Serial hub pages |
| `author/` | Author profiles |
| `category/` | Category indexes |
| `sync-from-seo.py` | Markdown → Jekyll |
