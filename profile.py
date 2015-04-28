#!/usr/bin/env python
# -*- coding: utf-8 -*-

from util import check_response
from bs4 import BeautifulSoup
import re
import json


class Profile:
    def __init__(self, id=0, name="", url =""):
        self.id = id
        self.name = name
        self.url = url
        self.friends_count = 0
        self.total_posts_count = 0
        self.wall_posts = []
        self.status = ""
        self.hometown = ""
        self.town = ""

    def __unicode__(self):
        return self.name + " #" + str(self.id)

    def __str__(self):
        return self.__unicode__().encode("utf-8")

def get(session, url):
    url = url if url[0] != "/" else url[1:]
    r = session.get("https://vk.com/" + url)
    check_response(r)

    soup = BeautifulSoup(r.text, "lxml")
    soup.prettify()

    id = int(soup.find("a", id="profile_gift_send_btn")["href"][6:].split("?")[0])
    name = unicode(soup.find("div", { "class" : "page_name fl_l ta_l" }).string)
    result = Profile(id, name, url)

    if soup.find("div", id="profile_friends") is not None:
        result.friends_count = int("".join(soup.find("div", id="profile_friends")
            .find("div", { "class" : "p_header_bottom"}).stripped_strings).split()[0])

    status_span = soup.find("span", { "class" : "current_text"})
    if status_span is not None:
        result.status = unicode(status_span.string)

    posts_data = soup.find("div", id="page_wall_posts")
    result.total_posts_count = int(posts_data.find("input", id="page_wall_count_own")["value"])

    from post import Post
    for post_html in posts_data.find_all("div", {"class":"post_table"}):
        post = Post(post_html)
        result.wall_posts.append(post)

    hometown = soup.find("div", text="Родной город:")
    if hometown is not None:
        result.hometown = unicode(hometown.next_sibling.next_sibling.a.string)

    town = soup.find("div", text="Город:")
    if town is not None:
        result.town = unicode(town.next_sibling.next_sibling.a.string)

    return result
