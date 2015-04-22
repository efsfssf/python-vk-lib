#!/usr/bin/env python
# -*- coding: utf-8 -*-


import vkexceptions


def check_response(r):
    r.raise_for_status()

    if r.text.find("security_check") >= 0:
        raise exceptions.SecurityException()
