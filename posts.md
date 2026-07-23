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

{% include category-pills.html active='all' %}

{% include ad-leaderboard.html %}

{% assign lb_posts = site.posts | where: "series_slug", "late-bloom-stories" | sort: "series_part" | reverse %}
{% assign qh_posts = site.posts | where: "series_slug", "the-quiet-hours-chronicle" | sort: "series_part" %}
{% assign guide_posts = site.posts | where_exp: "p", "p.category_slug == 'safety-guides' or p.category_slug == 'omegle-alternatives'" %}
{% assign advice_posts = site.posts | where: "category_slug", "love-journey" %}
{% assign other_posts = site.posts | where_exp: "p", "p.series_slug == nil and p.category_slug != 'safety-guides' and p.category_slug != 'omegle-alternatives' and p.category_slug != 'love-journey'" %}

<section class="home-section">
  <h2 class="section-title">Late Bloom Stories</h2>
  <p class="archive-lead" style="margin-top:-0.5rem;margin-bottom:1.25rem;">Latest romance episodes — <a href="{{ '/series/late-bloom-stories/' | relative_url }}">full series index ({{ lb_posts.size }} parts) →</a></p>
  <div class="post-card-grid">
    {% for post in lb_posts limit: 6 %}
      {% include post-card.html post=post %}
    {% endfor %}
  </div>
  <p class="section-more"><a href="{{ '/series/late-bloom-stories/' | relative_url }}">Browse all Late Bloom parts →</a></p>
</section>

{% if advice_posts.size > 0 %}
<section class="home-section">
  <h2 class="section-title">Love Journey</h2>
  <p class="archive-lead" style="margin-top:-0.5rem;margin-bottom:1.25rem;">Dating and relationship advice — <a href="{{ '/category/love-journey/' | relative_url }}">view category →</a></p>
  <div class="post-card-grid">
    {% for post in advice_posts %}
      {% include post-card.html post=post %}
    {% endfor %}
  </div>
</section>
{% endif %}

{% if guide_posts.size > 0 %}
<section class="home-section">
  <h2 class="section-title">Safety &amp; Guides</h2>
  <p class="archive-lead" style="margin-top:-0.5rem;margin-bottom:1.25rem;">Omegle alternatives and safer random chat — <a href="{{ '/category/safety-guides/' | relative_url }}">view category →</a></p>
  <div class="post-card-grid">
    {% for post in guide_posts %}
      {% include post-card.html post=post %}
    {% endfor %}
  </div>
</section>
{% endif %}

{% if qh_posts.size > 0 %}
<section class="home-section">
  <h2 class="section-title">The Quiet Hours Chronicle</h2>
  <p class="archive-lead" style="margin-top:-0.5rem;margin-bottom:1.25rem;">Six essays on loneliness and connection — <a href="{{ '/series/the-quiet-hours-chronicle/' | relative_url }}">series index →</a></p>
  <div class="post-card-grid">
    {% for post in qh_posts %}
      {% include post-card.html post=post %}
    {% endfor %}
  </div>
</section>
{% endif %}

{% if other_posts.size > 0 %}
<section class="home-section">
  <h2 class="section-title">More articles</h2>
  <div class="post-card-grid">
    {% for post in other_posts %}
      {% include post-card.html post=post %}
    {% endfor %}
  </div>
</section>
{% endif %}
