#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import vk
# mailru chat flags
MAIL_CHAT_FLAG_ADMINS_CAN_INVITE_LINK = 32
MAIL_CHAT_FLAG_ADMINS_CAN_ADD_ADMINS = 16
MAIL_CHAT_FLAG_ONLY_ADMINS_CAN_CHANGE_TITLE = 8
MAIL_CHAT_FLAG_ONLY_ADMINS_CAN_INVITE = 1
MAIL_CHAT_FLAG_ONLY_ADMINS_CAN_PIN = 4

def im_request(session, chat_id, params):
    add = {"al":1,"hash":get_chat_hash(session,chat_id),"im_v":2,"gid":0}
    params.update(add)
    print add
    return vk.parse(session.post("https://vk.com/al_im.php",params).text)

def add_chat_bot(session, chat_id, bot_id):
    r = session.post("https://vk.com/al_groups.php",{"act":"a_search_chats_box","al":1,"group_id":-bot_id})
    start = r.text.find('add_hash')+11
    l = r.text[start:].find('"')
    hash = r.text[start:start+l]
    r = session.post("https://vk.com/al_im.php",{"act":"a_add_bots_to_chat","al":1, "add_hash":hash,"bot_id":bot_id,"peer_ids":chat_id})
    return vk.parse(r.text)
#    print r.text.encode('utf-8')

def get_chat_hash(session, chat_id):
    r = session.post("https://vk.com/al_im.php",{"act":"a_renew_hash","al":1,"peers":chat_id,"gid":0})
    start = r.text.find('":"')+3
    l = r.text[start:].find('"')
    hash = r.text[start:start+l]
    return hash

def get_chat_details(session, chat_id):
    return im_request(session,chat_id,{"act":"a_get_chat_details","chat":chat_id})

def toggle_admin(session,chat_id,member_id,is_admin):
    return im_request(session,chat_id,{"act":"a_toggle_admin","al":1,"hash":get_chat_hash(session,chat_id),"chat":chat_id, "mid":member_id,"is_admin":is_admin})

def toggle_community(session,chat_id,peer_id,state):
    return im_request(session,chat_id,{"act":"a_toggle_community", "peer_id":peer_id,"state":state})

def load_chat_info(session,chat_id):
    return im_request(session,chat_id,{"act":"a_load_chat_info","peer":chat_id})

def return_to_chat(session,chat_id):
    return im_request(session,chat_id,{"act":"a_return_to_chat","chat":chat_id-2000000000})

def change_caccess(session,chat_id,member_id,access):
    return im_request(session,chat_id,{"act":"a_change_caccess", "peer_id":chat_id,"member_id":member_id,"access":access})

def update_flags(session,chat_id,flags):
    return im_request(session,chat_id,{"act":"a_update_flags","chat":chat_id, "flags":flags})

def kick_user(session,chat_id,member_id):
    return im_request(session,chat_id,{"act":"a_kick_user","chat":chat_id, "mid":member_id})
