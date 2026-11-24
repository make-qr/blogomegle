---
layout: default
title: All articles
permalink: /posts/
full_width: true
page_kind: archive
---

<section class="archive-header">
  <h1>All articles</h1>
  <p class="archive-lead">{{ site.posts.size }} original essays on meeting people, conversation, and safety.</p>
</section>

{% include category-pills.html active='all' %}

<section class="home-section">
  <div class="post-card-grid">
    {% for post in site.posts %}
      {% include post-card.html post=post %}
    {% endfor %}
  </div>
</section>
