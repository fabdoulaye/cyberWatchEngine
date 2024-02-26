# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
# Extracted data - > Temporary containers (items) -> Storing in database
from typing import Any

import scrapy
from scrapy import Field


class TheHackerNewsWatchEngineItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    date = scrapy.Field()
    tags = scrapy.Field()
    # tag2 = scrapy.Field()
    label = scrapy.Field()
    description = scrapy.Field()
    link = scrapy.Field()
    imagepath = scrapy.Field()
    alterimagetext = scrapy.Field()
    domainname = scrapy.Field()