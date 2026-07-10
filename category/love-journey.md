---
layout: page
title: Love Journey
permalink: /category/love-journey/
full_width: true
excerpt: Practical relationship advice — meeting, dating, gifts, trust, and commitment.
category_slug: love-journey
---

# Love Journey

Actionable advice for every stage: **meeting → dating → gifts → relationship → marriage**. Articles are **1,000+ words** with photos and video when helpful.

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
