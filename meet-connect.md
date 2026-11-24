---
layout: default
title: Meet and connect
permalink: /meet-connect/
full_width: true
page_kind: archive
excerpt: First messages, questions, and making friends with people you have not met.
pillar: meet-connect
---

<section class="archive-header">
  <h1>Meet and connect</h1>
  <p class="archive-lead">Practical notes on talking to someone new without turning the first minute into a performance.</p>
</section>

{% include category-pills.html active='meet-connect' %}

<section class="home-section archive-listing">
  <div class="post-card-grid">
    {% for post in site.posts %}
      {% if post.pillar == 'meet-connect' %}
        {% include post-card.html post=post %}
      {% endif %}
    {% endfor %}
  </div>
</section>
