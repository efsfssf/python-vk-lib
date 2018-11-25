#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import vk
import json

def do_execute(session, hash, code):
    resp = session.post("https://vk.com/dev", {"act":"a_run_method","hash":hash,"al":1,"method":"execute","param_code":code, "param_v": 5.92}).text
    return resp

def execute(session, code):
#    print session.dev_hash
    s = vk.parse(do_execute(session, session.dev_hash, code))
    if s:return json.loads(s)
    session.update_dev_hash()
    return json.loads(vk.parse(do_execute(session, session.dev_hash, code)))

def call(session, method, params):
    return execute(session,'return API.'+method+'('+json.dumps(params, ensure_ascii=False).replace('u\'','"').replace('\'','"')+');')
