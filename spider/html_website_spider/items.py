# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ProductUrlItem(scrapy.Item):
    url = scrapy.Field()  # 产品详情的url
    category_name = scrapy.Field()  # 产品类别名称
    referer = scrapy.Field()  # 产品类别对应的url


class ProductDetailItem(scrapy.Item):
    project_name = scrapy.Field()
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
