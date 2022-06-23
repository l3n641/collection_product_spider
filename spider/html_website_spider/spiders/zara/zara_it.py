import scrapy
from .zara import ZaraSpider


class ZaraItSpider(ZaraSpider):
    name = 'zara_it'

    base_url = 'https://www.zara.com/it/it/'
    category_url = 'https://www.zara.com/it/it/categories?ajax=true'
