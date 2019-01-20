
#coding: utf-8
import scrapy

from scrapy.http import Request
from scrapy.shell import inspect_response
import sys
import json
import requests
from proxy_crawler.items import Proxy
import time
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from scrapy.selector import Selector
from pprint import pprint
from selenium.webdriver.chrome.options import Options

class HashtagCrawler(scrapy.Spider):
    headers = {
        'authority': 'www.instagram.com',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'referer': 'https://www.instagram.com/challenge/6759920266/A4sxzMIjpt/',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9,fr;q=0.8,ar;q=0.7',
        'cookie': 'ig_cb=1; mid=W3lceQAEAAFsRLW_4wiFJAfOVpWQ; mcd=3; csrftoken=f7UVZAzPgr5QcQaFVIfbO4DvpkMS3AV8; ds_user_id=6759920266; sessionid=IGSC727deb653735ccffb9141adfcbcfaa5d0c43245e2c55b50e817558aad53ed889%3Ab7ZxoTMMpd9ngotvXmN2ol1aVDz43z5z%3A%7B%22_auth_user_id%22%3A6759920266%2C%22_auth_user_backend%22%3A%22accounts.backends.CaseInsensitiveModelBackend%22%2C%22_auth_user_hash%22%3A%22%22%2C%22_platform%22%3A4%2C%22_token_ver%22%3A2%2C%22_token%22%3A%226759920266%3APS3yzGm1vSAzpJRSQ84TrZIaz3nXRCXl%3Adda097901b79ce681d807ca9739da870d015b0e5a5b99ff9c5a17b2c1ee0f298%22%2C%22last_refreshed%22%3A1534680489.8558909893%7D; rur=FTW; urlgen="{\\"93.11.149.64\\": 15557}:1frMV8:iIr_vPmP415HLrIHQgmx-WfKkPs"',
    }


    name = 'test'
    prxr_enabled = True
    prxr_country = "EN"
    # prxr_url = "http://127.0.0.1:80"

    def __init__(self, *args, **kwargs):
        super(HashtagCrawler, self).__init__(*args, **kwargs)

   
    def start_requests(self):
        url = "http://www.google.com"
        # headers = {"country": "FR"}
        yield Request(url, callback=self.parse_proxy)

    def parse_proxy(self, response):
        # print(response.body)
        print(response.headers)
        # print(response.request.headers)
