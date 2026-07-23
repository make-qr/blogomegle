---
layout: default
title: The Quiet Hours Chronicle
permalink: /series/the-quiet-hours-chronicle/
full_width: true
page_kind: archive
excerpt: A six-part serial on loneliness, love, and learning to reach out again — by Morgan Rivers.
---

<section class="archive-header">
  <h1>The Quiet Hours Chronicle</h1>
  <p class="archive-lead">A serial on loneliness, love, and learning to reach out again — by <a href="{{ '/author/morgan-rivers/' | relative_url }}">Morgan Rivers</a> · <a href="{{ '/category/human-connection/' | relative_url }}">Human Connection</a></p>
</section>

{% include category-pills.html active='human-connection' %}

<section class="home-section">
  <div class="author-card">
    <p><em>The Quiet Hours Chronicle</em> is a <strong>six-part first-person essay series</strong> — not a how-to listicle, but a story you can read in order: nights that echo, evenings that slowly fill, sadness that lingers, dating without performance, and the work of <strong>keeping people close</strong> once you find them.</p>
    <p style="margin-bottom:0"><strong>~12 min read per part</strong> · Start with Part I if you're new.</p>
  </div>

  <p class="section-more" style="margin-top:0;margin-bottom:1.25rem;">
    <a class="btn" href="{{ '/quiet-hours-chronicle-part-i/' | relative_url }}">Begin Part I</a>
  </p>

  <h2 class="section-title">All parts</h2>
  <div class="post-card-grid">
    {% assign qh_posts = site.posts | where: "series_slug", "the-quiet-hours-chronicle" | sort: "series_part" %}
    {% for post in qh_posts %}
      {% include post-card.html post=post %}
    {% endfor %}
    {% if qh_posts.size == 0 %}
      {% assign qh_posts = site.posts | where_exp: "post", "post.slug contains 'quiet-hours-chronicle'" | reverse %}
      {% for post in qh_posts %}
        {% include post-card.html post=post %}
      {% endfor %}
    {% endif %}
  </div>
</section>
