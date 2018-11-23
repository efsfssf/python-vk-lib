#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

def add_chat_bot(session, chat_id, bot_id):
    r = session.post("https://vk.com/al_groups.php",{"act":"a_search_chats_box","al":1,"group_id":bot_id})
    start = r.text.find('add_hash')+11
    l = r.text[start:].find('"')
    hash = r.text[start:start+l]
    r = session.post("https://vk.com/al_im.php",{"act":"a_add_bots_to_chat","al":1, "add_hash":hash,"bot_id":-bot_id,"peer_ids":chat_id})
    return r
#    print r.text.encode('utf-8')
