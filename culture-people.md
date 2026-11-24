---
layout: default
title: Culture and people
permalink: /culture-people/
full_width: true
page_kind: archive
excerpt: What changes when the person on the other side grew up somewhere else.
pillar: culture-people
---

<section class="archive-header">
  <h1>Culture and people</h1>
  <p class="archive-lead">Culture is not a costume. These notes are about listening before you explain someone else's country to them.</p>
</section>

{% include category-pills.html active='culture-people' %}

<section class="home-section archive-listing">
  <div class="post-card-grid">
    {% for post in site.posts %}
      {% if post.pillar == 'culture-people' %}
        {% include post-card.html post=post %}
      {% endif %}
    {% endfor %}
  </div>
</section>
