# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ProductUrlItem(scrapy.Item):
    url = scrapy.Field()
    category_name = scrapy.Field()
    referer = scrapy.Field()


class ProductDetailItem(scrapy.Item):
    PageUrl = scrapy.Field()
    category_name = scrapy.Field()
    sku = scrapy.Field()
    color = scrapy.Field()
    size = scrapy.Field()
    price = scrapy.Field()
    title = scrapy.Field()
    dade = scrapy.Field()
    basc = scrapy.Field()
    brand = scrapy.Field()
    img = scrapy.Field()


class ImagesItem(scrapy.Item):
    image_urls = scrapy.Field()
    images = scrapy.Field()
    image_paths = scrapy.Field()
