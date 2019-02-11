# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging
from proxy_crawler.prxr.haproxy import Haproxy
from scrapy import signals

class ProxyPipeline(object):

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.proxies = []
        self.haproxy = Haproxy()

    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_closed, signal=signals.spider_closed)
        return s

    def process_item(self, item, spider):

        country = item['country_alt']
        # self.logger.info(proxy.prxr.haproxy.get_backends())
        px = "{}://{}:{}".format(item['protocol'].lower(), item['proxy'], item['port'])
        self.proxies.append((item['proxy'], item['port'], item['country_alt']))
        # self.logger.info(country)
        # self.logger.info(proxy)
        return item

    def spider_closed(self, spider):
        backends_list = self.haproxy.get_backends()
        self.logger.info(backends_list)
        for backend in backends_list:
            backends_slots = self.haproxy.get_slots(backend)
            self.haproxy.set_servers(self.proxies, backend, backends_slots)
            # self.logger.info(backend)
            # self.logger.info(backends_slots)
        # self.logger.info(self.proxies)
        # logging.log(logging.INFO, "[ERRORS_SUMMARY]:\n" + json.dumps(self.summary, indent=4, sort_keys=True))