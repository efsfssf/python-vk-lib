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

def get_chat_hash(session, chat_id):
    r = session.post("https://vk.com/al_im.php",{"act":"a_renew_hash","al":1,"peers":chat_id,"gid":0})
    start = r.text.find('":"')+3
    l = r.text[start:].find('"')
    hash = r.text[start:start+l]
    return hash

def get_chat_details(session, chat_id):
    return session.post("https://vk.com/al_im.php",{"act":"a_get_chat_details","al":1,"hash":get_chat_hash(session,chat_id),"chat":chat_id, "im_v":2,"gid":0}).text

def toggle_admin(session,chat_id,member_id,is_admin):
    return session.post("https://vk.com/al_im.php",{"act":"a_toggle_admin","al":1,"hash":get_chat_hash(session,chat_id),"chat":chat_id, "mid":member_id,"is_admin":is_admin,"im_v":2,"gid":0}).text

def toggle_community(session,chat_id,peer_id,state):
    return session.post("https://vk.com/al_im.php",{"act":"a_toggle_community","al":1,"hash":get_chat_hash(session,chat_id), "peer_id":peer_id,"state":state,"im_v":2,"gid":0}).text

def load_chat_info(session,chat_id):
    return session.post("https://vk.com/al_im.php",{"act":"a_load_chat_info","al":1,"hash":get_chat_hash(session,chat_id),"peer":chat_id, "im_v":2,"gid":0}).text

def return_to_chat(session,chat_id):
    return session.post("https://vk.com/al_im.php",{"act":"a_return_to_chat","al":1,"hash":get_chat_hash(session,chat_id),"chat":chat_id-2000000000, "im_v":2,"gid":0}).text

def change_caccess(session,chat_id,memberid,access):
    return session.post("https://vk.com/al_im.php",{"act":"a_change_caccess","al":1,"hash":get_chat_hash(session,chat_id), "peer_id":peer_id,"member_id":member_id,"access":state,"im_v":2,"gid":0}).text

def update_flags(session,chat_id,flags):
    return session.post("https://vk.com/al_im.php",{"act":"a_update_flags","al":1,"hash":get_chat_hash(session,chat_id),"chat":chat_id, "flags":flags, "im_v":2,"gid":0}).text
