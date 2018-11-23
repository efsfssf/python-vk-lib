#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

def execute(session, code):
    r = session.get("https://vk.com/dev/execute")
    start = r.text.find('methodRun')+11
    l = r.text[start:].find('\'')
    hash = r.text[start:start+l]
    resp = session.post("https://vk.com/dev", {"act":"a_run_method","hash":hash,"al":1,"method":"execute","param_code":code, "param_v": 5.92}).text
    return resp[resp.find('{'):]
