#!/usr/bin/env python
# -*- coding: utf-8 -*-

from profile import Profile
from bs4 import BeautifulSoup
from util import check_response
import urllib
import re
import urllib
import json


def public(session, text, to_type, to_id, official=True, signed=False, status_export = False):
    if to_type != "id" and to_type != "public" and to_type != "club":
        raise ValueError("to_type must be `id`, `public` or `club`")
    to_id = 70564753
    r = session.get("https://vk.com/%s%s" % (to_type, str(to_id)))
    check_response(r)
    profile_hash = re.search('"post_hash":"(?P<hash>[0-9abcdef]+)"', r.text).group("hash")
    payload = {
        "Message": text,
        "act": "post",
        "al": "1",
        "status_export": "1" if status_export else "",
        "hash": profile_hash,
        "facebook_export": "fixed",
        "fixed": "",
        "from": "",
        "signed": "1" if signed else "",
        "friends_only": "",
        "official": "1" if official and to_type in ('public', 'club') else "",
        "to_id": str(-int(to_id) if to_type in ('public', 'club') else int(to_id)),
        "type": "own"
    }
    r = session.post("https://vk.com/al_wall.php", payload, {
            "Referer":"https://vk.com/public" + str(to_id),
            "X-Requested-With" : "XMLHttpRequest"})
    if len(r.text) < 64:
        raise Exception("Wrong response. Probably captha: " + r.text)


class Post:
    def __init__(self, root):
        self.id = ""
        self.author = None
        self.repost_data = None
        self.text = ""
        self.photos_raw = []
        self.photos = []
        self.videos = []
        self.media = None
        self.is_comment = False
        try:
            self.parse(root)
        except Exception, ex:
            raise Exception("Post invalid markup `%s`. %s" % (root, str(ex)))

    def parse(self, root):
        wall_text = root.find("div", {"class":"wall_text_name"})
        self.author = Profile(url=wall_text.a["href"], id=int(wall_text.a["data-from-id"]), name=unicode(wall_text.a.string))
        self.id = root.find("div", { "class": "replies" }).find("div", { "class" : "reply_link_wrap"})["id"][10:]
        self.is_comment = root.find("a", { "class" : "reply_parent_link"}) is not None
        repost_table = root.find("table", { "class" : "published_by_wrap" })
        if repost_table is not None:
            repost_a = repost_table.find("a", { "class" : "published_by"})
            self.repost_data = {
                "author_url": repost_a["href"],
                "post_id": repost_a["data-post-id"]
            }

        #print root.find("div", { "class" : "wall_post_text"}).stripped_strings
        text_div = root.find("div", { "class" : "wall_post_text"})
        if text_div is not None:
            self.text = unicode(self.text_with_newlines(root.find("div", { "class" : "wall_post_text"})))

        media_link = root.find("div", { "class" : "page_media_thumbed_link"})
        if media_link is not None:
            self.media = urllib.unquote(media_link.find("a")["href"][13:])

        media_content = root.find("div", {"class" : "page_post_sized_thumbs"})
        if media_content is not None:
            for content_a in media_content:
                photo_content = re.search('\{"base".+?\}', content_a["onclick"])
                video_content = re.search("showInlineVideo\('(?P<id>[\d_]+)'", content_a["onclick"])
                if photo_content is not None:
                    self.photos_raw.append(json.loads(photo_content.group()))
                if video_content is not None:
                    self.videos.append(video_content.group('id'))

        for photo in self.photos_raw:
            base = photo["base"]
            if "z_" in photo:
                link = base + photo["z_"][0]
            elif "y_" in photo:
                link = base + photo["y_"][0]
            else:
                link = base + photo["x_"][0]
            link += ".jpg"
            self.photos.append(link)

    def text_with_newlines(self, elem):
        text = ''
        for e in elem.recursiveChildGenerator():
            if isinstance(e, basestring):
                text += e
            elif e.name == 'br':
                text += '\n'
        return text

    def __unicode__(self):
        return "%s #%s -> %s" % (self.author.name, self.author.id, self.text)

    def __str__(self):
        return self.__unicode__().encode("utf-8")
