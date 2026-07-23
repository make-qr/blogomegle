---
layout: default
title: Morgan Rivers
permalink: /author/morgan-rivers/
full_width: true
page_kind: archive
excerpt: Staff Essayist at OmegleChat — on loneliness, conversation, romance, and the courage to say hello again.
---

<section class="archive-header">
  <h1>Morgan Rivers</h1>
  <p class="archive-lead">Staff Essayist · OmegleChat — loneliness, conversation, romance, and the courage to say hello again.</p>
</section>

{% include category-pills.html active='all' %}

<section class="home-section">
  <div class="author-card">
    <p>Morgan Rivers writes <strong>long-form</strong> pieces about modern connection — essays, romance serials, and relationship advice (1,000+ words, with images and audio when it serves the story).</p>
    <p style="margin-bottom:0">Series include <a href="{{ '/series/the-quiet-hours-chronicle/' | relative_url }}">The Quiet Hours Chronicle</a> (six essays) and <a href="{{ '/series/late-bloom-stories/' | relative_url }}">Late Bloom Stories</a> (300-part romance). New <a href="{{ '/category/love-journey/' | relative_url }}">Love Journey</a> guides cover dating, gifts, trust, and commitment.</p>
  </div>

  <div class="featured-grid">
    <article class="featured-card featured-primary">
      <p class="label">Ongoing · 300 parts planned</p>
      <h2><a href="{{ '/series/late-bloom-stories/' | relative_url }}">Late Bloom Stories</a></h2>
      <p>Romance with happy endings — US settings, loneliness, and safe random chat as a night-time bridge.</p>
      <a class="btn" href="{{ '/late-bloom-part-i-late-blooming-cherry/' | relative_url }}">Read Late Bloom Part I</a>
    </article>
    <article class="featured-card">
      <p class="label">Complete · 6 parts</p>
      <h2><a href="{{ '/series/the-quiet-hours-chronicle/' | relative_url }}">The Quiet Hours Chronicle</a></h2>
      <p>First-person essays on loneliness, dating without performance, and keeping people close.</p>
      <a class="btn btn-outline" href="{{ '/quiet-hours-chronicle-part-i/' | relative_url }}">Read Quiet Hours Part I</a>
    </article>
  </div>
</section>

<section class="home-section">
  <h2 class="section-title">Latest by Morgan Rivers</h2>
  <div class="post-card-grid">
    {% assign author_posts = site.posts | where: "author_slug", "morgan-rivers" | slice: 0, 12 %}
    {% for post in author_posts %}
      {% include post-card.html post=post %}
    {% endfor %}
  </div>
  <p class="section-more"><a href="{{ '/posts/' | relative_url }}">View all articles →</a></p>
</section>
