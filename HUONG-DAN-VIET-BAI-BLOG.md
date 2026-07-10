# Hướng dẫn viết bài blog — OmegleChat Blog

> **Cập nhật:** 10/07/2026  
> **Blog:** https://blog.omeglechat.online  
> **Thư mục:** `du-an/ca-nhan-anh/omeglechat/blog.omeglechat.online/`

---

## Chuẩn bắt buộc mỗi bài

| Tiêu chí | Yêu cầu |
|----------|---------|
| **Độ dài** | **≥ 1.000 từ** (fiction serial + advice + guides) |
| **Ảnh** | **Hero** (`hero_image`) + **≥ 1 ảnh inline** trong thân bài |
| **Video / audio** | Có khi phù hợp: `youtube_id` hoặc file `/assets/audio/*.mp3` |
| **Cấu trúc** | ≥ 3 heading `##` (để TOC tự sinh) |
| **CTA** | 1 link OmegleChat cuối bài — không spam mỗi đoạn |

---

## Frontmatter mẫu — Love Journey (advice)

```yaml
---
title: "..."
date: 2026-07-10
slug: your-slug
permalink: /your-slug/
excerpt: "..."
author: Morgan Rivers
author_slug: morgan-rivers
category: Love Journey
category_slug: love-journey
pillar: love-journey
format: article
hero_image: "/assets/images/posts/your-slug/hero-xxxxxxxx.jpg"
hero_alt: "Mô tả ảnh"
hero_caption: "Photo: Unsplash"
youtube_id: "VIDEO_ID"          # tuỳ chọn
youtube_caption: "Video: ..."
---
```

## Frontmatter mẫu — Late Bloom (serial)

```yaml
category: Love & Romance
category_slug: love-romance
series_slug: late-bloom-stories
hero_image: "/assets/images/posts/your-slug/hero-xxxxxxxx.jpg"
format: serial
```

---

## Ảnh

**Sau khi viết/sync bài — bắt buộc chạy:**

```bash
cd ~/huong-dan/du-an/ca-nhan-anh/omeglechat/blog.omeglechat.online
python3 download-post-images.py
```

Script tải ảnh Unsplash (hoặc URL ngoài) về `assets/images/posts/{slug}/` và đổi link trong markdown sang đường dẫn local `/assets/images/...`. **Không hotlink** — tránh ảnh 404 trên live site.

- **Nguồn ưu tiên:** [Unsplash](https://unsplash.com) — chọn ảnh còn hoạt động (test URL trước)
- **Hero:** `hero_image: "/assets/images/posts/your-slug/hero-xxxxxxxx.jpg"`
- **Inline:** `![Mô tả](/assets/images/posts/your-slug/inline-01-xxxxxxxx.jpg)`
- **Caption:** Ghi `Photo: Unsplash` hoặc credit cụ thể
- **Alt text:** `hero_alt` trong frontmatter

Markdown inline (sau khi localize):

```markdown
![Mô tả ngắn](/assets/images/posts/your-slug/inline-01-xxxxxxxx.jpg)
*Caption in nghiêng.*
```

---

## Link — trỏ đúng website đích

Mọi link phải tới đúng đích, tránh 404. Sau khi viết/sync chạy:

```bash
cd ~/huong-dan/du-an/ca-nhan-anh/omeglechat/blog.omeglechat.online
python3 check-links.py         # kiểm tra (nội bộ + omeglechat.online)
python3 check-links.py --fix   # tự sửa dạng sai đã biết (thiếu .html)
```

Quy tắc:

- **Trang chính (site chính):** luôn có đuôi `.html` — `https://omeglechat.online/chat.html`, `/making-friends.html`, `/safety-tips.html`, `/language-learning.html`. **Không** dùng `/chat` (404).
- **Nút chat / main site:** dùng biến `{{ site.chat_url }}` và `{{ site.main_site }}` (khai báo trong `_config.yml`), không hardcode.
- **Link nội bộ blog:** dùng permalink có `/` đầu–cuối — `/late-bloom-part-i-.../`, `/series/late-bloom-stories/`, `/category/love-journey/`, `/author/morgan-rivers/`. **Không** dùng `/blog/....html` (đường dẫn cũ).
- **Ảnh:** `/assets/images/...` phải tồn tại trên đĩa (script tự kiểm tra).

CI và script NAS tự chạy `check-links.py --fix` trước khi build.

---

## Video YouTube

Frontmatter:

```yaml
youtube_id: "Fnt6f3Zp0FE"
youtube_caption: "Video: The Gottman Institute — ..."
```

Layout `post.html` tự embed iframe.

---

## Audio (serial)

```html
<div class="audio-player-wrap">
  <strong>🎧 Listen (narrated)</strong><br>
  <audio controls preload="metadata">
    <source src="/assets/audio/late-bloom-part-i-late-blooming-cherry.mp3" type="audio/mpeg">
  </audio>
  <em>Soft narration — Late Bloom Stories</em>
</div>
```

File MP3 đặt tại `assets/audio/`.

---

## Pipeline serial NAS

```bash
# Remix story → offpage (≥1000 từ, ảnh, audio block)
cd ~/huong-dan/du-an/ca-nhan-anh/ngon-tinh
python3 remix_story_to_omegle_article.py --episode ep-007-8-hours-apart --patch-dates

# Sync sang blog Jekyll
cd ~/huong-dan/du-an/ca-nhan-anh/omeglechat/blog.omeglechat.online
python3 sync-from-seo.py
```

Script `remix_story_to_omegle_article.py` tự thêm: hero, insights, FAQ, inline images.

---

## Category

| slug | Loại |
|------|------|
| `love-journey` | Advice — hẹn hò, quà, quan hệ |
| `love-romance` | Late Bloom fiction |
| `human-connection` | Quiet Hours essay |
| `safety-guides` | Omegle alternative, safety |

---

## Kiểm tra trước khi publish

```bash
# Đếm từ
python3 -c "
import re, sys
t=open(sys.argv[1]).read().split('---',2)[-1]
print(len(re.findall(r'\w+', t)), 'words')
" _posts/YOUR-POST.md
```

- [ ] ≥ 1.000 từ  
- [ ] `hero_image` có  
- [ ] ≥ 1 ảnh trong body  
- [ ] ≥ 3 `##` headings  
- [ ] `category_slug` đúng  

---

*Giao diện blog: card grid, TOC, sidebar — xem `assets/css/blog.css`.*
