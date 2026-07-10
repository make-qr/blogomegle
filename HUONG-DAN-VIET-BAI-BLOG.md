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
hero_image: "https://images.unsplash.com/photo-...?w=1200&q=80"
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
hero_image: "https://images.unsplash.com/..."
format: serial
```

---

## Ảnh

- **Nguồn ưu tiên:** [Unsplash](https://unsplash.com) — URL trực tiếp `?w=1200&q=80` (hero) / `?w=800` (inline)
- **Caption:** Ghi `Photo: Unsplash` hoặc credit cụ thể
- **Alt text:** `hero_alt` trong frontmatter

Markdown inline:

```markdown
![Mô tả ngắn](https://images.unsplash.com/photo-...?w=800&q=80)
*Caption in nghiêng.*
```

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
