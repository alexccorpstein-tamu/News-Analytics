# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    headline = scrapy.Field()
    date = scrapy.Field()
    article = scrapy.Field()
    publisher = scrapy.Field()
    website = scrapy.Field()
    #neg = scrapy.Field()
    #neu = scrapy.Field()
    #pos = scrapy.Field()
    #compound = scrapy.Field()
    #sentiment = scrapy.Field()
    #subjectivity = scrapy.Field()
    pass
