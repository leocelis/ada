# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LinksExtractorItem(scrapy.Item):
    # Object link
    link = scrapy.Field()
    # Object title
    title = scrapy.Field()
