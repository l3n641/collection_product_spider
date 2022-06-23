import scrapy
from .zara import ZaraSpider


class ZaraPlSpider(ZaraSpider):
    name = 'zara_pl'

    base_url = 'https://www.zara.com/pl/pl'
    category_url = 'https://www.zara.com/pl/pl/categories?ajax=true'
