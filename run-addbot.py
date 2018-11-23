#!/usr/bin/env python
# -*- coding: utf-8 -*-
import auth
import addbot
import sys

session = auth.login('mail@example.com', 'passw0rd', 'session id (optional)')
print(session.get_session()) # save this session id
print(addbot.add_chat_bot(session, sys.argv[1], int(sys.argv[2])).text)