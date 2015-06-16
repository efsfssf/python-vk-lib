#!/usr/bin/env python
# -*- coding: utf-8 -*-


class SecurityException(Exception):
    pass

class InvalidAuthException(Exception):
    def __init__(self, message=""):
        super(Exception, self).__init__(message)
