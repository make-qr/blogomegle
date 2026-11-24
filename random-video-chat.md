---
layout: default
title: Random video chat
permalink: /random-video-chat/
full_width: true
page_kind: archive
excerpt: How one-to-one random video chat works, what to expect, and how OmegleChat fits.
pillar: random-video-chat
---

<section class="archive-header">
  <h1>Random video chat</h1>
  <p class="archive-lead">For adults who want to understand a one-to-one browser chat before they start. OmegleChat is not affiliated with Omegle.</p>
</section>

{% include category-pills.html active='random-video-chat' %}

<section class="home-section archive-listing">
  <div class="post-card-grid">
    {% for post in site.posts %}
      {% if post.pillar == 'random-video-chat' %}
        {% include post-card.html post=post %}
      {% endif %}
    {% endfor %}
  </div>
</section>
