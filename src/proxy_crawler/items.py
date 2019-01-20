# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Proxy(scrapy.Item):
    # define the fields for your item here like:
    
    proxy = scrapy.Field()
    port = scrapy.Field()
    speed = scrapy.Field()
    country = scrapy.Field()
    country_alt = scrapy.Field()
    protocol = scrapy.Field()