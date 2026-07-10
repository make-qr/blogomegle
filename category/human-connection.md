---
layout: page
title: Human Connection
permalink: /category/human-connection/
full_width: true
excerpt: Essays on loneliness, friendship, dating, and learning to reach out again.
category_slug: human-connection
---

# Human Connection

Essays and serial fiction on **loneliness, friendship, dating, and courage** — long reads with depth.

## Featured serial

### [The Quiet Hours Chronicle]({{ '/series/the-quiet-hours-chronicle/' | relative_url }})

By [Morgan Rivers]({{ '/author/morgan-rivers/' | relative_url }}) — six parts, personal essay.

---

## Articles in this category

<div class="post-card-grid">
{% for post in site.posts %}
  {% if post.category_slug == 'human-connection' or post.category == 'Human Connection' %}
    {% unless post.series_slug == 'late-bloom-stories' %}
      {% include post-card.html post=post %}
    {% endunless %}
  {% endif %}
{% endfor %}
</div>
