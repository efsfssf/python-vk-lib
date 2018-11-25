#!/usr/bin/env python
# -*- coding: utf-8 -*-


import requests
import vkexceptions
import re

USER_AGENT = "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.152 Safari/537.360"

class VkSession:
    def __init__(self, login, password):
        self.login = login
        self.password = password
        self.session = ""
        self.dev_hash = ""

    def get(self, url, headers = {}):
        headers_original = {
            "Origin": "https://vk.com",
            "Cookie" : "remixsslsid=1; remixsid=%s" % self.session,
            "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
            "Accept-Charset": "utf-8",
            "User-Agent": USER_AGENT }
        headers_original.update(headers)
        r = requests.get(url, headers=headers_original)
        r.raise_for_status()
        return r

    def post(self, url, payload, headers = {}):
        headers_original = {
            "Origin": "https://vk.com",
            "Cookie" : "remixsslsid=1; remixsid=%s" % self.session,
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4",
            "Pragma":"no-cache",
            "Cache-Control":"no-cache",
            "Accept-Charset": "utf-8",
            "User-Agent": USER_AGENT }
        headers_original.update(headers)
        r = requests.post(url, data=payload, headers=headers_original)
        r.raise_for_status()
        return r

    def get_session(self):
        return self.session

    def update_dev_hash(self):
        r = self.get("https://vk.com/dev/execute")
        start = r.text.find('methodRun')+11
        if start > 0:
            l = r.text[start:].find('\'')
            self.dev_hash = r.text[start:start+l]
            return True
        return False


def login(login, password, remixsid = None):
    result = VkSession(login, password)
    # try reuse remixsid
    if remixsid:
        result.session = remixsid
        r = result.get("https://vk.com/dev/execute")
        if result.update_dev_hash():
            return result

    ip_h, lg_h, cookie = __get_h()
    remixlhk = re.findall('remixlhk=(?P<h>[A-Za-z0-9]+);', cookie)[1]
    remixstid = re.search('remixstid=(?P<h>[A-Za-z0-9_]+);', cookie).group('h')

    payload = {
        "act": "login",
        "role": "al_frame",
        "expire": "",
        "recapthca":"",
        "captcha_key": "",
        "captcha_sid": "",
        "_origin": "https://vk.com",
        "ip_h": ip_h,
        "lg_h": lg_h,
        "email": login,
        "pass": password,
        "utf-8": "1"
    }
    headers = {
        "Referer": "https://vk.com",
        "Origin": "https://vk.com",
        "Accept-Charset": "utf-8",
        "Cookie": "remixlang=0; remixlhk=%s; remixstid=%s; remixdt=0; remixflash=18.0.0; remixscreen_depth=24" % (remixlhk, remixstid),
        "User-Agent":USER_AGENT
    }
    
    r = requests.post("https://login.vk.com/?act=login", data=payload, headers=headers)
    r.raise_for_status()

    if "Set-Cookie" not in r.headers:
        raise vkexceptions.InvalidAuthException("No Cookie")
    if r.status_code == 200:
        result.session = re.search('remixsid=([A-Za-z0-9]+)', r.headers["Set-Cookie"]).group().split("=")[1]
        if result.session == "DELETED":
            raise vkexceptions.InvalidAuthException("200: DELETED Session")
    else:
        raise vkexceptions.InvalidAuthException("NON 200 CODE")
    result.update_dev_hash()
    return result


def __get_h():
    r = requests.get("https://vk.com/login")
    r.raise_for_status()

    ip_h = re.search('"ip_h" value="(?P<h>[A-Za-z0-9]+)"', r.text)
    lg_h = re.search('"lg_h" value="(?P<h>[A-Za-z0-9]+)"', r.text)

    return ip_h.group("h"), lg_h.group("h"), r.headers["Set-Cookie"]
