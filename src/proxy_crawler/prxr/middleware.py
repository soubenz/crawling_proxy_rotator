
import logging
from scrapy import signals
from itertools import cycle

logger = logging.getLogger(__name__)


class PRXRMiddleware(object):
    url = None

    download_timeout = 190
    # connection_refused_delay = 90
    # preserve_delay = False
    header_prefix = '-'
    # prxr_countries = ['FR', 'DE', 'UA','IN','AL','BD',
    #                     'BG','CA','CZ','US','GB','HU','ID','NL','RU','ES']
    prxr_countries = ['RU']
    # r_header = 
    _settings = [
        # ('r_header', bool),
        # ('user', str),
        ('prxr_countries', list),
        ('url', str),
        ('download_timeout', int),
        # ('preserve_delay', bool),
    ]

    def __init__(self, crawler):
        self.crawler = crawler

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
        logger.info("Using PRXR")

        self.pool = cycle(self.prxr_countries)

    def is_enabled(self, spider):
        """Hook to enable middleware by custom rules."""
        return (
            getattr(spider, 'prxr_enabled', False) or
            self.crawler.settings.getbool("PRXR_ENABLED")
        )

    def _get_setting_value(self, spider, k, type_):
        o = getattr(self, k, None)
        s = self._settings_get(
            type_, 'PRXR_' + k.upper(), o)
        return getattr(
            spider, 'prxr_' + k,  s)

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

    def process_request(self, request, spider):
        if self._is_enabled_for_request(request):
            logger.info(self.url)
            request.meta['proxy'] = self.url
            request.meta['download_timeout'] = self.download_timeout
            self.crawler.stats.inc_value('prxr/request_count')
            self.crawler.stats.inc_value('prxr/request/method/%s' % request.method)
            # logger.info(self.countries)
            if self.prxr_countries:
                next_it = next(self.pool)
                logger.info(next_it)
                # request.headers['country'] = next_it

    def process_response(self, request, response, spider):
        return response

    def _is_enabled_for_request(self, request):
        return self.enabled

    def header_rotator(self, spider):
        """Hook to enable middleware by custom rules."""
        return (
            getattr(spider, 'prxr_countries', False) or
            self.crawler.settings.getbool("PRXR_COUNTRIES")
        )
