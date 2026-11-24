---
layout: default
title: Love Journey
permalink: /category/love-journey/
full_width: true
page_kind: archive
excerpt: True love, finding a compatible partner, marriage readiness, health before and after the wedding, and gentle couple humor.
category_slug: love-journey
---

<section class="archive-header">
  <h1>Love Journey</h1>
  <p class="archive-lead">Essays about choosing someone, staying kind, and sharing a life without turning it into a performance.</p>
</section>

{% include category-pills.html active='love-journey' %}

<section class="home-section" style="margin-bottom:1.5rem;">
  <div class="author-card">
    <p><strong>What you’ll find here</strong></p>
    <ul style="margin:0.5rem 0 0;padding-left:1.2rem;color:var(--text-muted);">
      <li>A Sunday that is a date without a restaurant script</li>
      <li>Jokes that do not embarrass the other person</li>
      <li>What waiting is, and what it is not</li>
    </ul>
  </div>
</section>

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
  <p class="text-muted">No essays in this shelf yet.</p>
  {% endif %}
</section>
