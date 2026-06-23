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

1. Create repo **`blog.omeglechat.online`** on GitHub (account `vanthangtechlabglobal-pixel` or org)
2. Push this folder:

```bash
git init
git add .
git commit -m "Initial OmegleChat blog — Jekyll + Quiet Hours Chronicle"
git branch -M main
git remote add origin git@github.com:YOUR_USER/blog.omeglechat.online.git
git push -u origin main
```

3. **GitHub → Settings → Pages**
   - Source: **Deploy from branch** `main` / `/ (root)`
   - Or enable **GitHub Actions** (Jekyll build runs on push)

4. **Cloudflare DNS** (anh tự cấu hình):
   - Type: `CNAME`
   - Name: `blog`
   - Target: `YOUR_USER.github.io` (or custom Pages URL)
   - **SSL:** Full

5. **GitHub → Settings → Pages → Custom domain:** `blog.omeglechat.online`

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
