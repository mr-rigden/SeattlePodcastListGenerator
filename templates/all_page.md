---
title: "The Seattle Podcasts List"
date: {{ date }}
---
This is a list of all the podcasts made in the Seattle area. We have {{ number_of_podcasts }} podcasts in this list! This list is separated by active podcasts, inactive podcasts, and radio podcasts. We also have the list broken up by [category](https://seattlepodcasters.com/seattle_podcast_categories). If you would like to add your podcast, please email Jason Rigden at jasonrigden@gmail.com. You can also email Jason with any questions or comments about the list.


## Active Podcasts

<ul>
{% for podcast in indie_podcasts.active %}<li><a href="{{podcast.homepage}}">{{ podcast.title }}</a></li>
<br>
{% endfor %}
</ul>


{% if indie_podcasts.inactive  %}
## Inactive Podcasts
This is our list of Seattle area podcasts that haven't released an episode in the last 90 days. Just because they haven't released an episode recently, doesn't mean they aren't awesome.
<ul>
{% for podcast in indie_podcasts.inactive %}<li><a href="{{podcast.homepage}}">{{ podcast.title }}</a></li>
<br>
{% endfor %}
{% endif %}
</ul>

## Radio Podcasts
This is our list of active podcasts produced by radio stations in the Seattle area. 
<ul>
{% for podcast in radio_podcasts.active %}<li><a href="{{podcast.homepage}}">{{ podcast.title }}</a></li>
<br>
{% endfor %}
</ul>

