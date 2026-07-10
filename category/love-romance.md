---

## layout: page
title: Love & Romance
permalink: /category/love-romance/
full_width: true
excerpt: Late Bloom Stories and romance fiction with happy endings.
category_slug: love-romance

# Love & Romance

Serial fiction 

## Late Bloom Stories

[Series hub →]({{ '/series/late-bloom-stories/' | relative_url }})

{% for post in site.posts %} {% if post.series_slug == 'late-bloom-stories' or post.category_slug == 'love-romance' %} {% include post-card.html post=post %} {% endif %} {% endfor %}