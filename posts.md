---
layout: default
title: All articles
permalink: /posts/
full_width: true
page_kind: archive
---

<section class="archive-header">
  <h1>All articles</h1>
  <p class="archive-lead">Romance serials, relationship advice, and safer chat guides — {{ site.posts.size }} articles and counting.</p>
</section>

{% include ad-leaderboard.html %}

{% include category-pills.html active='all' %}

<section class="home-section archive-listing">
  <div class="post-card-grid">
    {% for post in site.posts %}
      {% include post-card.html post=post %}
    {% endfor %}
  </div>
</section>
