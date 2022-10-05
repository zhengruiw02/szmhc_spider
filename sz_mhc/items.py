# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SzMhcItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    date = scrapy.Field()
    # month = scrapy.Field()
    # day = scrapy.Field()
    confirmed = scrapy.Field()
    asymptomatic = scrapy.Field()
    pass
