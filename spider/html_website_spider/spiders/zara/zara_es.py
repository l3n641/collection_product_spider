import scrapy
from .zara import ZaraSpider


class ZaraEsSpider(ZaraSpider):
    name = 'zara_es'

    base_url = 'https://www.zara.com/es/es/'
    category_url = 'https://www.zara.com/es/es/categories?ajax=true'
