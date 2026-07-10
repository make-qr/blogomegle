---
layout: default
title: Love Journey
permalink: /category/love-journey/
full_width: true
page_kind: archive
excerpt: Practical relationship advice — meeting, dating, gifts, trust, and commitment.
category_slug: love-journey
---

<section class="archive-header">
  <h1>Love Journey</h1>
  <p class="archive-lead">Actionable advice for every stage: <strong>meeting → dating → gifts → relationship → marriage</strong>.</p>
</section>

{% include category-pills.html active='love-journey' %}

<section class="home-section archive-listing">
  <div class="post-card-grid">
    {% for post in site.posts %}
      {% if post.category_slug == 'love-journey' or post.pillar == 'love-journey' %}
        {% include post-card.html post=post %}
      {% endif %}
    {% endfor %}
  </div>
  {% assign lj_count = site.posts | where: "category_slug", "love-journey" | size %}
  {% if lj_count == 0 %}
  <p class="text-muted">New guides publishing weekly. Start with <a href="{{ '/how-to-start-conversation-someone-you-like/' | relative_url }}">how to start a conversation with someone you like</a>.</p>
  {% endif %}
</section>
