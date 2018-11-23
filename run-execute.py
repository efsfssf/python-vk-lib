#!/usr/bin/env python
# -*- coding: utf-8 -*-
import auth
import execute
import sys

session = auth.login('mail@example.com', 'passw0rd', 'session id (optional)')
print(session.get_session()) # save this session id
print(execute.execute(session, sys.argv[1]))