---
layout: page
title: Human Connection
permalink: /category/human-connection/
excerpt: Essays on loneliness, friendship, dating, and learning to reach out again.
---

# Human Connection

*Essays on loneliness, friendship, dating, and the courage to say hello again.*

---

## Featured serial

### [The Quiet Hours Chronicle]({{ '/series/the-quiet-hours-chronicle/' | relative_url }})

By [Morgan Rivers]({{ '/author/morgan-rivers/' | relative_url }}) — six parts, personal essay.

---

## Articles in this category

<ul class="post-list">
{% for post in site.posts %}
  {% if post.category_slug == 'human-connection' or post.category == 'Human Connection' %}
  <li>
    <a class="title" href="{{ post.url | relative_url }}">{{ post.title }}</a>
    <div class="meta">{{ post.date | date: "%Y-%m-%d" }}{% if post.author %} · {{ post.author }}{% endif %}</div>
  </li>
  {% endif %}
{% endfor %}
</ul>

{% assign guides = site.posts | where_exp: "item", "item.category_slug != 'human-connection'" %}
{% if guides.size > 0 %}
## Guides &amp; alternatives

<ul class="post-list">
{% for post in guides %}
  {% unless post.category == 'Human Connection' %}
  <li>
    <a class="title" href="{{ post.url | relative_url }}">{{ post.title }}</a>
    <div class="meta">{{ post.date | date: "%Y-%m-%d" }}</div>
  </li>
  {% endunless %}
{% endfor %}
</ul>
{% endif %}
