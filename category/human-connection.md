---
layout: default
title: Human Connection
permalink: /category/human-connection/
full_width: true
page_kind: archive
excerpt: Essays on loneliness, friendship, dating, and learning to reach out again.
category_slug: human-connection
---

<section class="archive-header">
  <h1>Human Connection</h1>
  <p class="archive-lead">Essays and serial fiction on <strong>loneliness, friendship, dating, and courage</strong>.</p>
</section>

{% include category-pills.html active='human-connection' %}

<section class="home-section archive-listing">
  <p class="section-more" style="margin-top:0;margin-bottom:1.25rem;"><a href="{{ '/series/the-quiet-hours-chronicle/' | relative_url }}">The Quiet Hours Chronicle — complete series →</a></p>
  <div class="post-card-grid">
    {% for post in site.posts %}
      {% if post.category_slug == 'human-connection' or post.category == 'Human Connection' %}
        {% unless post.series_slug == 'late-bloom-stories' %}
          {% include post-card.html post=post %}
        {% endunless %}
      {% endif %}
    {% endfor %}
  </div>
</section>
