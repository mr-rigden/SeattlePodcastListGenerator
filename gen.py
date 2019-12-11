import datetime
import json
import os 
import time

import pprint

from bs4 import BeautifulSoup
import feedparser
from jinja2 import Environment, FileSystemLoader
import requests
import requests_cache
from slugify import slugify

data_dir = '/home/jason/Computron/data/Seattle-Podcast-RSS-URL-Lists'
target_dir = '/home/jason/Computron/hugo/seattlepodcasters.com/content'


requests_cache.install_cache()
pp = pprint.PrettyPrinter(indent=4)
deadline = datetime.datetime.now() - datetime.timedelta(days=90)
file_loader = FileSystemLoader('templates')
env = Environment(loader=file_loader)


date_now = f"{datetime.datetime.now():%Y-%m-%d}"


def get_indie_urls():
    indie_file_path = os.path.join(data_dir, 'indie.txt')
    with open(indie_file_path) as f:
        urls = f.read().splitlines()
    return urls

def get_radio_urls():
    radio_file_path = os.path.join(data_dir, 'radio.txt')
    with open(radio_file_path) as f:
        urls = f.read().splitlines()
    return urls

def better_sortable_text(text):
    text = text.lower().strip()
    text = remove_article(text)
    return text

def remove_article(text):
    articles = ["the ", "a ", "an "]
    for article in articles:
        if text.startswith(article):
            text = text[len(article):]
    return text

def get_feed_itunes_categories(soup):
    itunes_categories = []
    temp_categories = soup.findAll('itunes:category')
    for category in temp_categories:
        category_text = category.get('text')
        if category_text is not None:
            itunes_categories.append(category_text.lower().strip())
    itunes_categories = list(set(itunes_categories))
    return itunes_categories


def is_podcast_active(podcast):
    active = False
    for each in podcast.entries:
        published = datetime.datetime.fromtimestamp(time.mktime(each.published_parsed))
        if published > deadline:
            active = True
            break
    return active

        


def process_feed(url):
    feed = {}
    r = requests.get(url)
    if r.status_code != 200:
        log_bad_url(url + "Bad Status Code")
        return None
    d = feedparser.parse(r.content)
    soup = BeautifulSoup(r.content, 'html.parser')
    try:
        feed['title'] = d['feed']['title']
    except KeyError:
        log_bad_url(url + "Bad Feed")
        return None
    feed['sortable_title'] = better_sortable_text(feed['title'])
    try:
        feed['homepage'] = d['feed']['link']
    except KeyError:
        log_bad_url(url + "No Homepage")
        return None
    feed['description'] = d['feed']['subtitle']
    feed['description'] = feed['description'].replace("\r"," ")
    feed['description'] = feed['description'].replace("\n"," ")
    feed['description'] = feed['description'].replace("\n"," ")
    feed['description'] = feed['description'].replace("<p>"," ")
    feed['description'] = feed['description'].replace("</p>"," ")
    feed['categories'] = get_feed_itunes_categories(soup)
    feed['active'] = is_podcast_active(d)
    return feed


def get_categories(feeds):
    bad_cats = ('', '-- none --')
    categories = []
    for feed in feeds:
        categories.extend(feed['categories'])
    categories = set(categories)
    categories = categories.difference(bad_cats)
    categories = list(categories)
    return categories

def alphabetize_podcasts(podcasts):
    alphabetizes_podcasts = sorted(podcasts, key=lambda x: x['sortable_title'])
    return alphabetizes_podcasts


def render_all_page(indie, radio):
    indie_podcasts = {}
    indie_podcasts['active'], indie_podcasts['inactive'] = separate_active_and_inactive(indie)
    
    radio_podcasts = {}
    radio_podcasts['active'], radio_podcasts['inactive'] = separate_active_and_inactive(radio)

    number_of_podcasts = len(indie) + len(radio)

    file_path = os.path.join(target_dir, "seattle-podcast-list.md")
    template = env.get_template('all_page.md')
    output = template.render(date=date_now, indie_podcasts=indie_podcasts, radio_podcasts=radio_podcasts, number_of_podcasts=number_of_podcasts)
    f = open(file_path, "w")
    f.write(output)
    f.close()




def separate_active_and_inactive(podcasts):
    active = []
    inactive = []
    for podcast in podcasts:
        if podcast['active']:
            active.append(podcast)
        else:
            inactive.append(podcast)
    return active, inactive


def read_podcasts_from_json(filename):
    with open(filename) as f:
        podcasts = json.load(f)
    return podcasts


def get_podcasts(urls):
    podcasts = []
    for url in urls:
        podcast = process_feed(url)
        if podcast:
            podcasts.append(podcast)
    podcasts = alphabetize_podcasts(podcasts)
    return podcasts

def save_podcasts_as_json(podcasts, filename):
    with open(filename, 'w') as f:
        json.dump(podcasts, f)


def save_data():
    indie_urls = get_indie_urls()
    indie_podcasts = get_podcasts(indie_urls)
    save_podcasts_as_json(indie_podcasts, 'indie.json')

    radio_urls = get_radio_urls()
    radio_podcasts = get_podcasts(radio_urls)
    save_podcasts_as_json(radio_podcasts, 'radio.json')

def load_data():
    indie_podcasts = read_podcasts_from_json('indie.json')
    radio_podcasts = read_podcasts_from_json('radio.json')
    return indie_podcasts, radio_podcasts


def render_category_pages(indie, radio):
    podcasts = indie + radio
    podcasts = alphabetize_podcasts(podcasts)
    categories = get_categories(podcasts)
    render_categories_list_page(categories)
    for category in categories:
        render_category_page(category, podcasts)

def render_category_page(category, podcasts):
    filtered_podcasts = []
    for podcast in podcasts:
        if category in podcast['categories']:
            filtered_podcasts.append(podcast)
    active, inactive = separate_active_and_inactive(filtered_podcasts)
    title = "Seattle Podcasts about " + category.title()
    filename = slugify(title) + ".md"

    file_path = os.path.join(target_dir, filename)
    template = env.get_template('category_page.md')
    category_name = category.title()
    output = template.render(date=date_now, title=title, active=active, inactive=inactive, category=category_name)
    f = open(file_path, "w")
    f.write(output)
    f.close()

def render_categories_list_page(categories):
    categories.sort()
    cats = []
    for category in categories:
        cat = {}
        cat['name'] = category.title()
        cat['title'] = category.title()
        title = "Seattle Podcasts about " + category.title()
        cat['stub'] = slugify(title)
        cats.append(cat)
    file_path = os.path.join(target_dir, "seattle_podcast_categories.md")
    template = env.get_template('category_list_page.md')
    output = template.render(date=date_now, categories=cats)
    f = open(file_path, "w")
    f.write(output)
    f.close()


def log_bad_url(url, message):
    f = open("bad_url.log", "a+")
    f.write(url + " - " + message + '\n')
    f.close()


def full_run():
    save_data()
    indie, radio = load_data()
    render_all_page(indie, radio)
    render_category_pages(indie, radio)




full_run()