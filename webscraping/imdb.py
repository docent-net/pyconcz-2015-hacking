#!/usr/bin/python

# remember to check for mobile versions - it's easier to scrap those (and its more lightweight)

import requests
from bs4 import BeautifulSoup
from urlparse import urljoin
from collections import defaultdict

base_url = "http://m.imdb.com/chart/top"


#soup.find_all(class_="media")[0].find("h4")

#soup.find_all(class_="media")[0].find("h4").text.split("\n")[2]

def get_top_movies():
    res = requests.get(base_url)
    soup = BeautifulSoup(res.text, "html.parser")

    for movie_tag in soup.find_all(class_="media"):
        name = movie_tag.find("h4").text.split("\n")[2]
        href = movie_tag.find("a")["href"]

        yield name, urljoin(base_url, href)
        #print name
        #get_actors(urljoin(base_url, href))

def get_actors(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")

    for actor_tag in soup.find(id="cast-and-crew").find_all("li"):
        name = actor_tag.find("strong").text
        #print("\t"+name)
        yield name

#for name, actors in get_top_movies():
#    print name

# to na dole to juz POC pisany na szybko
res = defaultdict(lambda: 0)

for i, (name, url) in enumerate(get_top_movies()):
    print ("Downloading", name)
    for actor in get_actors(url):
        res[actor] += 1

    if (i>10):
        break

# ktorzy aktorzy wystepuja wiecej niz raz we wszystkich filmach?
for name, appearances in res.items():
    if appearances >= 2:
        print ("Good actor:", name)