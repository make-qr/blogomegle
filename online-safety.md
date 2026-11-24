---
layout: default
title: Online safety
permalink: /online-safety/
full_width: true
page_kind: archive
excerpt: Privacy, leaving a bad chat, and the difference between Report and Block. Adults 18+ only.
pillar: online-safety
---

<section class="archive-header">
  <h1>Online safety</h1>
  <p class="archive-lead">OmegleChat is for adults 18 and over. These guides cover what to keep private and how to end a chat.</p>
</section>

{% include category-pills.html active='online-safety' %}

<section class="home-section archive-listing">
  <div class="post-card-grid">
    {% for post in site.posts %}
      {% if post.pillar == 'online-safety' %}
        {% include post-card.html post=post %}
      {% endif %}
    {% endfor %}
  </div>
</section>
