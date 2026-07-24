---
layout: default
title: Life Habits
permalink: /category/life-habits/
full_width: true
page_kind: archive
excerpt: Gentle, sustainable daily habits — evening routines, sleep, hydration, movement, and a kinder relationship with food and body image, without diet-war extremes.
category_slug: life-habits
---

<section class="archive-header">
  <h1>Life Habits</h1>
  <p class="archive-lead">Small, sustainable habits for ordinary days: <strong>evening routines, sleep, gentle movement, and a kinder relationship with food and body image</strong> — no diet wars, no extremes.</p>
</section>

{% include category-pills.html active='life-habits' %}

<section class="home-section" style="margin-bottom:1.5rem;">
  <div class="author-card">
    <p><strong>What you’ll find here</strong></p>
    <ul style="margin:0.5rem 0 0;padding-left:1.2rem;color:var(--text-muted);">
      <li>Evening and morning routines for people living alone</li>
      <li>Walking, talking, and accountability that actually sticks</li>
      <li>Gentle, sustainable habits around food, weight, and body image</li>
      <li>Sleep, screens, and hydration without the hype</li>
    </ul>
  </div>
</section>

<section class="home-section archive-listing">
  <div class="post-card-grid">
    {% for post in site.posts %}
      {% if post.category_slug == 'life-habits' or post.pillar == 'life-habits' %}
        {% include post-card.html post=post %}
      {% endif %}
    {% endfor %}
  </div>
  {% assign lh_count = site.posts | where: "category_slug", "life-habits" | size %}
  {% if lh_count == 0 %}
  <p class="text-muted">New guides publishing soon. Start with <a href="{{ '/lonely-nights-vs-true-loneliness-when-to-reach-out/' | relative_url }}">lonely nights vs true loneliness</a>.</p>
  {% endif %}
</section>
