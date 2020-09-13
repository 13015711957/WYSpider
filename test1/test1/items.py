# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Test1Item(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    content = scrapy.Field()
    create_time = scrapy.Field()
    source = scrapy.Field()
    digest = scrapy.Field()
    img_url=scrapy.Field()
