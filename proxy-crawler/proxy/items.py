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
class HashtagItem(scrapy.Item):
    # define the fields for your item here like:
    
    name = scrapy.Field()
    mediaCount = scrapy.Field()
     
class InstagramItem(scrapy.Item):
    # define the fields for your item here like:
    id = scrapy.Field()
    hashtag = scrapy.Field()
    followers = scrapy.Field()
    influencer  = scrapy.Field()
    username  = scrapy.Field()
    picture  = scrapy.Field()
    biography = scrapy.Field()
    address = scrapy.Field()
    email = scrapy.Field()
    businessCategory = scrapy.Field()
    phoneNumber = scrapy.Field()
    country = scrapy.Field()
    followers = scrapy.Field()
    externalUrl = scrapy.Field()
    fullName = scrapy.Field()
    isBusiness = scrapy.Field()
    isVerified= scrapy.Field()
    isPrivate= scrapy.Field()
    profilePic= scrapy.Field()
    followNum = scrapy.Field()
    fbPage = scrapy.Field()
    position = scrapy.Field()
    averageEngagement = scrapy.Field()
    hasEngagers = scrapy.Field()
    
