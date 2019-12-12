---
title: "{{ title }}"
date: {{ date }}
---
This is a list of all the podcasts about {{ category }} being made in the Seattle area. There are {{ active | count }} active podcasts in this category. We also have a list of [all active podcasts in Seattle](https://seattlepodcasters.com/seattle-podcast-list).
<ul>
{% for podcast in active %}<li><a href="{{podcast.homepage}}">{{ podcast.title }}</a></li>
<br>
{% endfor %}
</ul>


{% if inactive  %}
## Inactive Podcasts
These podcasts about {{ category }} haven't released an episode in the last 90 days. Just because they haven't released an episode recently, doesn't mean they aren't awesome.
<ul>
{% for podcast in inactive %}<li><a href="{{podcast.homepage}}">{{ podcast.title }}</a></li>
<br>
{% endfor %}
{% endif %}
</ul>

### Add Your Podcast!

If you would like to add your Podcast, please email Jason Rigden at jasonrigden@gmail.com. You can also email Jason with any questions or comments about the list.
