#!/usr/bin/env python
# -*- coding: utf-8 -*-


from bs4 import BeautifulSoup
from profile import Profile
from post import Post
from util import check_response
import requests
import urllib
import vkexceptions
import re
import json


def search(session, text):
    r = session.get("https://vk.com/feed?q=%s&section=search" % urllib.quote(text.encode('utf-8')))
    check_response(r)
    posts = []

    soup = BeautifulSoup(r.text, "lxml")
    soup.prettify()

    for post_html in soup.find_all("div", {"class":"post_table"}):
        post = Post(post_html)
        posts.append(post)

    return posts
