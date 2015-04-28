#!/usr/bin/env python
# -*- coding: utf-8 -*-

from profile import Profile
import re
import urllib
import json

class Post:
    def __init__(self, root):
        self.id = ""
        self.author = None
        self.repost_data = None
        self.text = ""
        self.photos = []
        self.videos = []
        self.media = None
        self.is_comment = False
        self.parse(root)

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
                    self.photos.append(json.loads(photo_content.group()))
                if video_content is not None:
                    self.videos.append(video_content.group('id'))

    def text_with_newlines(self, elem):
        text = ''
        for e in elem.recursiveChildGenerator():
            if isinstance(e, basestring):
                text += e.strip()
            elif e.name == 'br':
                text += '\n'
        return text                    

    def __unicode__(self):
        return "%s #%s -> %s" % (self.author.name, self.author.id, self.text)

    def __str__(self):
        return self.__unicode__().encode("utf-8")