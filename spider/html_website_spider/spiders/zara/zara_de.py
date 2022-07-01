import scrapy
from .zara import ZaraSpider


class ZaraDeSpider(ZaraSpider):
    name = 'zara_de'

    base_url = 'https://www.zara.com/de/de/'
    category_url = 'https://www.zara.com/de/de/categories?ajax=true'
