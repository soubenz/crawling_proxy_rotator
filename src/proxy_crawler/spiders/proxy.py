
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


    name = 'proxy'

    def __init__(self, *args, **kwargs):
        super(HashtagCrawler, self).__init__(*args, **kwargs)

        self.headers = {
            'authority': 'hidemyna.me',
            'cache-control': 'max-age=0',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9,fr;q=0.8,ar;q=0.7',
            'cookie': '__cfduid=d23b4b0b150eb5aeb20c0b7a5b05cf9281546696275; cf_clearance=b1f0f71d1d01c4c0ea07eb53b43e5909126ad133-1546696280-86400-150; t=91870879; PAPVisitorId=5d6f31b28b5c865876fdz0qiKJEL0b6U; _ga=GA1.2.134502053.1546696282; _gid=GA1.2.38007589.1546696282; _ym_uid=1546696282557813519; _ym_d=1546696282; _fbp=fb.1.1546696281644.1649520089; _ym_wasSynced=%7B%22time%22%3A1546696281898%2C%22params%22%3A%7B%22eu%22%3A1%7D%2C%22bkParams%22%3A%7B%7D%7D; _ym_visorc_42065329=w; _ym_isad=1; jv_enter_ts_EBSrukxUuA=1546696282909; jv_visits_count_EBSrukxUuA=1; jv_refer_EBSrukxUuA=https%3A%2F%2Fhidemyna.me%2Fen%2Fproxy-list%2F; jv_utm_EBSrukxUuA=; PHPSESSID=7nttuivncf7ckcqncgbojrqet6; _dc_gtm_UA-90263203-1=1; _gat_UA-90263203-1=1; jv_pages_count_EBSrukxUuA=13',
        }
        self.countries_max = {
            "de": 80,
            "ua": 100,
            "in": 80,            
            "al": 30,
            "bg": 100,
            "ca": 50,
            "cz": 100,
            "us": 100,
            "gb": 30,
            "hu": 80,
            "id":20,
            "nl" 100:,
            "ru": 100,
            "es": 100,
            "fr": 100,           

        }
        WINDOW_SIZE = "1920,1080"
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
        self.driver = webdriver.Chrome(executable_path ="/usr/local/bin/chromedriver", chrome_options=chrome_options)
    def start_requests(self):
        url = "https://google.dz"
        yield Request(url, callback=self.parse_proxy)
    def parse_proxy(self, response):
        # url = "https://hidemyna.me/en/proxy-list/?maxtime=1000&type=h&start=0"
        # self.driver.get(url)
        # # time.sleep(20)
        # element = WebDriverWait(self.driver, 30).until(
        # EC.presence_of_element_located((By.CSS_SELECTOR, "div.allcountries__bl")))

        # html = self.driver.page_source
        # sel = Selector(text=html)
        # all_countries = sel.css('div.allcountries__bl label span.flag-icon::attr(class)').extract()
        # self.logger.info(html)
        # print([country.split('-icon-')[-1] for country in all_countries])
        # self.logger.info(all_countries)
        countries = {}
        for i in range(50):
            skip = i * 64
            url = 'https://hidemyna.me/en/proxy-list/?country=UADEARALINBGBRBDCACZUSGBHUIDNLRUESFR&maxtime=1000&start={}#list'.format(skip)
            print(url)
            self.driver.get(url)
            element = WebDriverWait(self.driver, 30).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, "div.allcountries__bl")))

            html = self.driver.page_source
            sel = Selector(text=html)
            for r in sel.css('tbody tr'):
                p = Proxy()
                proxy = r.xpath("td[1]/text()").extract_first()
                port = r.xpath("td[2]/text()").extract_first()
                country = r.xpath("./td[3]").css('div::text').extract_first()
                country_alt_raw = r.xpath("./td[3]").css('span::attr(class)').extract_first()
                # print(country_alt_raw)
                if country_alt_raw:
                    country_alt = country_alt_raw.split('icon-')[-1]
                    if country_alt in countries:
                        countries[country_alt] += 1
                    else:
                        countries[country_alt] = 0

                else:
                    country_alt = None
                speed = r.css('div.bar p::text').extract_first()
                p_type = r.xpath("./td[5]/text()").extract_first()
                p['proxy'] = proxy
                p['port'] = port
                p['country'] = country
                p['country_alt'] = country_alt
                p['speed'] = speed
                p['protocol'] = p_type
                if p_type and country_alt in self.countries_max:
                    if countries[country_alt] <= self.countries_max[country_alt]:
                        yield p
            time.sleep(10)
        self.logger.info(countries)
