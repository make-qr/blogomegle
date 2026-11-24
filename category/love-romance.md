---
layout: default
title: Love & Romance
permalink: /category/love-romance/
full_width: true
page_kind: archive
excerpt: Closed-door notes on liking someone and spending time together.
category_slug: love-romance
---

<section class="archive-header">
  <h1>Love &amp; Romance</h1>
  <p class="archive-lead">Short essays about liking someone. Not a serial, and not a list of other websites.</p>
</section>

{% include category-pills.html active='love-romance' %}

<section class="home-section archive-listing">
  <div class="post-card-grid">
    {% for post in site.posts %}
      {% if post.series_slug == 'late-bloom-stories' or post.category_slug == 'love-romance' %}
        {% include post-card.html post=post %}
      {% endif %}
    {% endfor %}
  </div>
</section>
