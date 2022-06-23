import scrapy
from .zara import ZaraSpider


class ZaraDkSpider(ZaraSpider):
    name = 'zara_dk'

    base_url = 'https://www.zara.com/dk/da/'
    category_url = 'https://www.zara.com/dk/da/categories?ajax=true'
