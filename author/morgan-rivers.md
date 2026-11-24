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
    <p>Morgan Rivers writes the essays on this blog: dating without a script, money and meals at home, and how to end a chat that feels wrong. The old serials are gone.</p>
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
