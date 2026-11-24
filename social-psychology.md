---
layout: default
title: Connection
permalink: /social-psychology/
full_width: true
page_kind: archive
excerpt: Loneliness, stranger conversation, and friendships that begin on a screen.
pillar: social-psychology
---

<section class="archive-header">
  <h1>Connection</h1>
  <p class="archive-lead">Why people seek a stranger, and what a screen can and cannot do for loneliness.</p>
</section>

{% include category-pills.html active='social-psychology' %}

<section class="home-section archive-listing">
  <div class="post-card-grid">
    {% for post in site.posts %}
      {% if post.pillar == 'social-psychology' %}
        {% include post-card.html post=post %}
      {% endif %}
    {% endfor %}
  </div>
</section>
