# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NewhouseItem(scrapy.Item):
    province = scrapy.Field()
    city = scrapy.Field()
    name = scrapy.Field()
    address = scrapy.Field()
    rooms = scrapy.Field()
    square = scrapy.Field()
    price = scrapy.Field()
    sale = scrapy.Field()
    loupan_url = scrapy.Field()
    number = scrapy.Field()



class EsfItem(scrapy.Item):
    province = scrapy.Field()
    city = scrapy.Field()
    name = scrapy.Field()
    address = scrapy.Field()
    rooms = scrapy.Field()
    area = scrapy.Field()
    floor = scrapy.Field()
    toward = scrapy.Field()
    build = scrapy.Field()
    price = scrapy.Field()
    union = scrapy.Field()


