# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ProductUrlItem(scrapy.Item):
    url = scrapy.Field()
    category_name = scrapy.Field()
    referer = scrapy.Field()
