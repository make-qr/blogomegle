---
layout: page
title: All articles
permalink: /posts/
---

# All articles

<ul class="post-list">
{% for post in site.posts %}
  <li>
    <a class="title" href="{{ post.url | relative_url }}">{{ post.title }}</a>
    <div class="meta">
      {% if post.series_name %}<em>{{ post.series_name }}</em> · {% endif %}
      {{ post.date | date: "%Y-%m-%d" }}
      {% if post.author %} · {{ post.author }}{% endif %}
    </div>
  </li>
{% endfor %}
</ul>
