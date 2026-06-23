# Deploy blog.omeglechat.online

## Repo & hosting

| Mục | Giá trị |
|-----|---------|
| GitHub | [make-qr/blogomegle](https://github.com/make-qr/blogomegle) |
| Custom domain | `blog.omeglechat.online` |
| Pages branch | `gh-pages` (tự deploy qua Actions) |

## Cloudflare DNS (đã cấu hình)

| Type | Name | Content | Proxy |
|------|------|---------|-------|
| CNAME | `blog` | `make-qr.github.io` | DNS only (grey) |

## GitHub Pages (anh bật 1 lần)

1. Mở [Settings → Pages](https://github.com/make-qr/blogomegle/settings/pages)
2. **Build and deployment → Source:** Deploy from a branch
3. **Branch:** `gh-pages` / `/ (root)` → Save
4. **Custom domain:** `blog.omeglechat.online` (nếu chưa có)
5. **Enforce HTTPS:** ON (sau khi certificate sẵn sàng, ~10 phút)

## Sync bài từ seo-offpage (máy local)

```bash
python3 sync-from-seo.py   # đọc ~/huong-dan/.../seo-offpage/content/articles
git add _posts && git commit -m "Sync posts" && git push
```

## Kiểm tra sau deploy

- https://blog.omeglechat.online/
- https://blog.omeglechat.online/series/the-quiet-hours-chronicle/
- https://blog.omeglechat.online/quiet-hours-chronicle-part-i/
- https://blog.omeglechat.online/author/morgan-rivers/
