---
layout: default
title: Table Talk
permalink: /category/table-talk/
full_width: true
page_kind: archive
excerpt: Food, dinner-table conversation, and the small rituals of eating together — dinner starters, cooking for one, date nights at home, and holidays around a quiet table.
category_slug: table-talk
---

<section class="archive-header">
  <h1>Table Talk</h1>
  <p class="archive-lead">Food and conversation, together: <strong>dinner starters, cooking for one, home date nights, and the rituals</strong> that make a table feel like company instead of just a meal.</p>
</section>

{% include category-pills.html active='table-talk' %}

<section class="home-section" style="margin-bottom:1.5rem;">
  <div class="author-card">
    <p><strong>What you’ll find here</strong></p>
    <ul style="margin:0.5rem 0 0;padding-left:1.2rem;color:var(--text-muted);">
      <li>Dinner conversation starters that actually feel natural</li>
      <li>Cooking and eating alone without the evening feeling hollow</li>
      <li>Home date nights, first home-cooked dates, and weekly dinner rituals</li>
      <li>Soup, tea, Sunday resets, and other small food rituals worth keeping</li>
    </ul>
  </div>
</section>

<section class="home-section archive-listing">
  <div class="post-card-grid">
    {% for post in site.posts %}
      {% if post.category_slug == 'table-talk' or post.pillar == 'table-talk' %}
        {% include post-card.html post=post %}
      {% endif %}
    {% endfor %}
  </div>
  {% assign tt_count = site.posts | where: "category_slug", "table-talk" | size %}
  {% if tt_count == 0 %}
  <p class="text-muted">New guides publishing soon. Start with <a href="{{ '/lonely-nights-vs-true-loneliness-when-to-reach-out/' | relative_url }}">lonely nights vs true loneliness</a>.</p>
  {% endif %}
</section>
