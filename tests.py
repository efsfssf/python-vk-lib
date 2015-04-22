#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import auth
import feed
import profile
import sys

LOGIN = sys.argv[1]
PASS = sys.argv[2]
sys.argv = [sys.argv[0],] + sys.argv[3:]

class TestFeed(unittest.TestCase):
    def setUp(self):
        self.session = auth.login(LOGIN, PASS)

    def test_auth(self):
        self.assertTrue(len(self.session.session) > 0)

    def _test_search(self):
        self.assertTrue(len(feed.search(self.session, u"таиланд")) > 0) 

    def test_profile(self):
        self.assertFalse(profile.get(self.session, u"/agasper") is None) 

if __name__ == '__main__':
    unittest.main()