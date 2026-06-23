# Deploy blog.omeglechat.online

## Cloudflare DNS (anh làm)

| Type | Name | Content | Proxy |
|------|------|---------|-------|
| CNAME | `blog` | `vanthangtechlabglobal-pixel.github.io` | Proxied ✅ |

*(Đổi `vanthangtechlabglobal-pixel` nếu repo nằm user/org khác.)*

## GitHub Pages

1. Repo name đề xuất: **`blog.omeglechat.online`**
2. Settings → Pages → Custom domain: `blog.omeglechat.online`
3. Enforce HTTPS: ON
4. Chờ certificate (~10 phút)

## Kiểm tra sau deploy

- https://blog.omeglechat.online/
- https://blog.omeglechat.online/series/the-quiet-hours-chronicle/
- https://blog.omeglechat.online/quiet-hours-chronicle-part-i/
- https://blog.omeglechat.online/author/morgan-rivers/

## Canonical (tùy chọn)

Bài cũ trỏ `omeglechat.online/blog/...` — có thể 301 redirect trên main site hoặc cập nhật canonical trong seo-offpage sang subdomain blog.
