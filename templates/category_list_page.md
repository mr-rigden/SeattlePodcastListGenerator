---
title: "Seattle Podcast Categories"
date: {{ date }}
---


<ul>
{% for category in categories %}<li><a href="https://seattlepodcasters.com/{{category.stub}}">{{category.title}}</a></li>
<br>
{% endfor %}
</ul>

