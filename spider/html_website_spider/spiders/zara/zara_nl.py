import scrapy
from .zara import ZaraSpider


class ZaraNlSpider(ZaraSpider):
    name = 'zara_nl'

    base_url = 'https://www.zara.com/nl/nl/'

    category_url = 'https://www.zara.com/nl/nl/categories?ajax=true'
