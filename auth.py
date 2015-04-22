#!/usr/bin/env python
# -*- coding: utf-8 -*-


import requests
import vkexceptions
import re

USER_AGENT = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.57 Safari/537.17"

class VkSession:
    def __init__(self, login, password):
        self.login = login
        self.password = password
        self.session = ""

    def get(self, url):
        r = requests.get(url, headers = { 
            "Cookie" : "remixsid=%s" % self.session,
            "Accept-Charset": "utf-8",
            "User-Agent": USER_AGENT })
        r.raise_for_status()
        return r

    def post(self, url, payload):
        r = requests.post(url, data=payload, headers = { 
            "Cookie" : "remixsid=%s" % self.session,
            "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
            "Accept-Charset": "utf-8",
            "User-Agent": USER_AGENT })
        r.raise_for_status()
        return r


def login(login, password):
    result = VkSession(login, password)
    ip_h = __get_ip_h()
    payload = {
        "act": "login",
        "role": "al_frame",
        "expire": "",
        "captcha_key": "",
        "captcha_sid": "",
        "_origin": "https://vk.com",
        "ip_h": ip_h,
        "email": login,
        "pass": password
    }
    headers = {
        "Referer": "https://vk.com",
        "Origin": "https://vk.com",
        "Accept-Charset": "utf-8",
        "User-Agent":USER_AGENT
    }
    r = requests.post("https://login.vk.com/?act=login", data=payload, headers=headers)
    r.raise_for_status()
    if "Set-Cookie" not in r.headers:
        raise vkexceptions.InvalidCredentialsException()
    result.session = re.search('remixsid=([A-Za-z0-9]+)', r.headers["Set-Cookie"]).group().split("=")[1]
    if result.session == "DELETED":
        raise vkexceptions.InvalidCredentialsException()
    return result


def __get_ip_h():
    r = requests.get("https://vk.com")
    r.raise_for_status()
    ip_h = re.search('ip_h=([A-Za-z0-9]+)', r.text)
    return ip_h.group().split('=')[1]