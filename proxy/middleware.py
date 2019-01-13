import os
import logging
import warnings
from collections import defaultdict

from six.moves.urllib.parse import urlparse
from w3lib.http import basic_auth_header
from scrapy import signals
from scrapy.resolver import dnscache
from scrapy.exceptions import ScrapyDeprecationWarning
from twisted.internet.error import ConnectionRefusedError, ConnectionDone


class PXRMiddleware(object):
    url = 'http://127.0.0.1:80'

    download_timeout = 190
    # Handle crawlera server failures
    connection_refused_delay = 90
    preserve_delay = False
    header_prefix = '-'

    _settings = [
        ('apikey', str),
        ('user', str),
        ('pass', str),
        ('url', str),
        ('maxbans', int),
        ('download_timeout', int),
        ('preserve_delay', bool),
    ]


    def __init__(self, crawler):
        self.crawler = crawler
        # self.job_id = os.environ.get('SCRAPY_JOB')
        self._bans = defaultdict(int)
        self._saved_delays = defaultdict(lambda: None)


    @classmethod
    def from_crawler(cls, crawler):
        o = cls(crawler)
        crawler.signals.connect(o.open_spider, signals.spider_opened)
        return o



    def open_spider(self, spider):
        self.enabled = self.is_enabled(spider)
        if not self.enabled:
            return

        for k, type_ in self._settings:
            setattr(self, k, self._get_setting_value(spider, k, type_))


    def is_enabled(self, spider):
        """Hook to enable middleware by custom rules."""
        
        return (
            getattr(spider, 'prxr_enabled', False) or
            self.crawler.settings.getbool("PRXR_ENABLED")
        )



    def _settings_get(self, type_, *a, **kw):
        if type_ is int:
            return self.crawler.settings.getint(*a, **kw)
        elif type_ is bool:
            return self.crawler.settings.getbool(*a, **kw)
        elif type_ is list:
            return self.crawler.settings.getlist(*a, **kw)
        elif type_ is dict:
            return self.crawler.settings.getdict(*a, **kw)
        else:
            return self.crawler.settings.get(*a, **kw)


    def _get_setting_value(self, spider, k, type_):
        o = getattr(self, k, None)
        s = self._settings_get(
            type_, 'PRXR_' + k.upper(), o)
        return getattr(
            spider, 'prxr_' + k,  s)

    def process_request(self, request, spider):
        if self._is_enabled_for_request(request):
            self._set_crawlera_default_headers(request)
            request.meta['proxy'] = self.url
            # request.meta['download_timeout'] = self.download_timeout
            # request.headers['Proxy-Authorization'] = self._proxyauth


    def process_response(self, request, response, spider):
        if not self._is_enabled_for_request(request):
            return response


    