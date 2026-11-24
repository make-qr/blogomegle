---
layout: default
title: OmegleChat Editorial
permalink: /author/omeglechat-editorial/
full_width: true
page_kind: archive
excerpt: The OmegleChat blog is written by the people who run the site. It is not affiliated with Omegle.
---

<section class="archive-header">
  <h1>OmegleChat Editorial</h1>
  <p class="archive-lead">These essays are published by OmegleChat. They describe the browser chat, conversation, culture, and safety. OmegleChat is not the old Omegle service.</p>
</section>

{% include category-pills.html active='all' %}

<section class="home-section">
  <div class="author-card">
    <p>Questions about a page, a report, or your data go to <a href="mailto:omeglechatonline@gmail.com">omeglechatonline@gmail.com</a>. The product rules are on the <a href="{{ site.main_site }}/about.html">main site</a>.</p>
  </div>
</section>

<section class="home-section">
  <h2 class="section-title">Essays</h2>
  <div class="post-card-grid">
    {% assign author_posts = site.posts | where: "author_slug", "omeglechat-editorial" %}
    {% for post in author_posts %}
      {% include post-card.html post=post %}
    {% endfor %}
  </div>
</section>
