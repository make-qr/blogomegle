---
layout: default
title: Love & Romance
permalink: /category/love-romance/
full_width: true
page_kind: archive
excerpt: Late Bloom Stories and romance fiction with happy endings.
category_slug: love-romance
---

<section class="archive-header">
  <h1>Love &amp; Romance</h1>
  <p class="archive-lead">Serial fiction with happy endings — <strong>Late Bloom Stories</strong> and more.</p>
</section>

{% include category-pills.html active='love-romance' %}

<section class="home-section archive-listing">
  <p class="section-more" style="margin-top:0;margin-bottom:1.25rem;"><a href="{{ '/series/late-bloom-stories/' | relative_url }}">Late Bloom Stories — series index →</a></p>
  <div class="post-card-grid">
    {% for post in site.posts %}
      {% if post.series_slug == 'late-bloom-stories' or post.category_slug == 'love-romance' %}
        {% include post-card.html post=post %}
      {% endif %}
    {% endfor %}
  </div>
</section>
