# blog.omeglechat.online — GitHub Pages

Jekyll blog for **OmegleChat** essays, guides, and *The Quiet Hours Chronicle* serial.

- **Live URL:** https://blog.omeglechat.online
- **Main site:** https://omeglechat.online
- **Source markdown:** `~/huong-dan/du-an/ca-nhan-anh/seo-offpage/content/articles/`

## Quick start

```bash
cd ~/huong-dan/du-an/ca-nhan-anh/omeglechat/blog.omeglechat.online

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
# 2. Add slug + date to sync-from-seo.py DATE_MAP
python3 sync-from-seo.py
git add _posts && git commit -m "Add post: ..." && git push
```

## Structure

| Path | Purpose |
|------|---------|
| `_posts/` | Generated — do not edit by hand |
| `series/` | Serial hub pages |
| `author/` | Author profiles |
| `category/` | Category indexes |
| `sync-from-seo.py` | Markdown → Jekyll |
